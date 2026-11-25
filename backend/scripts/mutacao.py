"""Teste de mutação nos módulos críticos do RNF09, com o cosmic-ray.

Uso, de dentro de backend/:

    python -m scripts.mutacao                      # todos os módulos críticos
    python -m scripts.mutacao app/tasks/cardapio.py  # só os módulos informados
    python -m scripts.mutacao --paralelo 4         # módulos em paralelo

Para cada módulo crítico, o script copia o backend para uma pasta
temporária, roda `cosmic-ray init`, `baseline` e `exec` lá dentro e lê o
resultado do banco da sessão. O cosmic-ray altera o arquivo no disco para
criar cada mutante; rodando numa cópia, uma execução interrompida não deixa
mutante no código de verdade.

O comando de teste usa o caminho completo do Python que está rodando o
script, e não `python`: no Windows o `python` pode cair no Python do
sistema, sem o pytest, e todo mutante aparece como morto (ver
docs/estudos/estudo-teste-de-mutacao.md).

Sai com código 1 se algum módulo ficar abaixo da meta (50%, RNF09) ou se o
baseline falhar. Os mutantes sobreviventes são listados para análise: cada
um é uma lacuna de teste ou um mutante equivalente.
"""

from __future__ import annotations

import argparse
import ast
import shutil
import subprocess
import sys
import tempfile
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass, field
from pathlib import Path

BACKEND = Path(__file__).resolve().parents[1]
META = 50.0
TIMEOUT_POR_MUTANTE = 120.0

# Módulo crítico -> testes que exercitam ele. O score depende de quais
# testes rodam, não só do módulo: um teste que não está aqui não mata
# mutante nenhum.
MODULOS_CRITICOS: dict[str, list[str]] = {
    "app/scrapers/disciplinas/parser.py": [
        "tests/scrapers/test_disciplinas_parser.py",
        "tests/sabotagem/test_sabotagem_sigaa.py",
    ],
    "app/scrapers/cardapio/parser.py": [
        "tests/scrapers/test_cardapio_parser.py",
        "tests/scrapers/test_cardapio_parser_posicional.py",
        "tests/scrapers/test_cardapio_scraper.py",
        "tests/sabotagem/test_sabotagem_ru.py",
    ],
    "app/domain/disciplinas.py": [
        "tests/domain/test_disciplinas.py",
        "tests/routers/test_disciplinas_router.py",  # busca e paginação (RF20) passam pelo domínio
        "tests/sabotagem/test_sabotagem_sigaa.py",
    ],
    "app/domain/cardapio.py": [
        "tests/domain/test_cardapio.py",
        "tests/routers/test_cardapio_router.py",
        "tests/sabotagem/test_sabotagem_ru.py",
    ],
    "app/tasks/scraping.py": [
        "tests/tasks/test_scraping.py",
        "tests/tasks/test_log_das_tasks.py",
        "tests/sabotagem/test_sabotagem_sigaa.py",
    ],
    "app/tasks/cardapio.py": [
        "tests/tasks/test_log_das_tasks.py",
        "tests/sabotagem/test_sabotagem_ru.py",
    ],
    "app/tasks/logging_signals.py": [
        "tests/tasks/test_loggin_signals.py",
        "tests/tasks/test_log_das_tasks.py",
        "tests/sabotagem/test_sabotagem_sigaa.py",
        "tests/sabotagem/test_sabotagem_ru.py",
    ],
    "app/domain/execucoes.py": [
        "tests/domain/test_execucoes.py",
        "tests/routers/test_execucoes_router.py",
        "tests/sabotagem/test_sabotagem_sigaa.py",
        "tests/sabotagem/test_sabotagem_ru.py",
    ],
}

_IGNORAR_NA_COPIA = shutil.ignore_patterns(
    ".venv", "venv", "__pycache__", ".pytest_cache", ".ruff_cache", ".coverage", "*.sqlite"
)


@dataclass
class Resultado:
    modulo: str
    mortos: int = 0
    anotacoes_puladas: int = 0
    sobreviventes: list[str] = field(default_factory=list)
    erro: str | None = None

    @property
    def total(self) -> int:
        return self.mortos + len(self.sobreviventes)

    @property
    def score(self) -> float:
        return 100 * self.mortos / self.total if self.total else 0.0


def _config(modulo: str, testes: list[str]) -> str:
    python = Path(sys.executable).as_posix()
    comando = f"{python} -m pytest -x -q -p no:cacheprovider {' '.join(testes)}"
    return (
        "[cosmic-ray]\n"
        f'module-path = "{modulo}"\n'
        f"timeout = {TIMEOUT_POR_MUTANTE}\n"
        "excluded-modules = []\n"
        f'test-command = "{comando}"\n'
        "\n[cosmic-ray.distributor]\n"
        'name = "local"\n'
    )


def _cosmic_ray(pasta: Path, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run(  # nosec B603 - comando fixo, sem entrada de usuário
        [sys.executable, "-m", "cosmic_ray.cli", *args], cwd=pasta, capture_output=True, text=True
    )


def _trechos_de_anotacao(codigo: str) -> list[tuple[tuple[int, int], tuple[int, int]]]:
    """Início e fim (linha, coluna em caracteres) de cada anotação de tipo
    do módulo. O ast conta a coluna em bytes UTF-8; o cosmic-ray, em
    caracteres."""
    linhas = codigo.splitlines()

    def posicao(linha: int, coluna_em_bytes: int) -> tuple[int, int]:
        return linha, len(linhas[linha - 1].encode("utf-8")[:coluna_em_bytes].decode("utf-8"))

    anotacoes = []
    for no in ast.walk(ast.parse(codigo)):
        if isinstance(no, ast.arg | ast.AnnAssign):
            anotacoes.append(no.annotation)
        elif isinstance(no, ast.FunctionDef | ast.AsyncFunctionDef):
            anotacoes.append(no.returns)
    return [
        (posicao(a.lineno, a.col_offset), posicao(a.end_lineno, a.end_col_offset)) for a in anotacoes if a is not None
    ]


def _pular_anotacoes(pasta: Path, modulo: str) -> int:
    """Marca como pulados os mutantes dentro de anotações de tipo, como
    `str | None` virando `str + None`. Com `from __future__ import
    annotations` a anotação nunca é avaliada, então esses mutantes são
    equivalentes: nenhum teste consegue matá-los. Devolve quantos pulou."""
    from cosmic_ray.work_db import WorkDB, use_db
    from cosmic_ray.work_item import WorkerOutcome, WorkResult

    trechos = _trechos_de_anotacao((pasta / modulo).read_text(encoding="utf-8"))
    pulados = 0
    with use_db(str(pasta / "cr.sqlite"), WorkDB.Mode.open) as db:
        for item in list(db.pending_work_items):
            mutacao = item.mutations[0]
            if any(inicio <= tuple(mutacao.start_pos) and tuple(mutacao.end_pos) <= fim for inicio, fim in trechos):
                db.set_result(item.job_id, WorkResult(worker_outcome=WorkerOutcome.SKIPPED))
                pulados += 1
    return pulados


def _ler_sessao(sessao: Path, resultado: Resultado) -> None:
    from cosmic_ray.work_db import WorkDB, use_db
    from cosmic_ray.work_item import TestOutcome

    with use_db(str(sessao), WorkDB.Mode.open) as db:
        for item, res in db.completed_work_items:
            if res.test_outcome is None:
                continue  # pulado
            if res.test_outcome == TestOutcome.SURVIVED:
                mutacao = item.mutations[0]
                linha = mutacao.start_pos[0]
                resultado.sobreviventes.append(
                    f"linha {linha}: {mutacao.operator_name} (ocorrência {mutacao.occurrence})"
                )
            else:
                resultado.mortos += 1
    resultado.sobreviventes.sort(key=lambda s: int(s.split()[1].rstrip(":")))


def rodar_modulo(modulo: str) -> Resultado:
    resultado = Resultado(modulo)
    testes = [t for t in MODULOS_CRITICOS.get(modulo, []) if (BACKEND / t).exists()]
    if not testes:
        resultado.erro = "nenhum teste mapeado para o módulo"
        return resultado

    with tempfile.TemporaryDirectory(prefix="mutacao-") as tmp:
        pasta = Path(tmp) / "backend"
        shutil.copytree(BACKEND, pasta, ignore=_IGNORAR_NA_COPIA)
        (pasta / "cr.toml").write_text(_config(modulo, testes), encoding="utf-8")

        for passo in (("init", "cr.toml", "cr.sqlite"), ("baseline", "cr.toml"), ("exec", "cr.toml", "cr.sqlite")):
            if passo[0] == "exec":
                resultado.anotacoes_puladas = _pular_anotacoes(pasta, modulo)
            processo = _cosmic_ray(pasta, *passo)
            if processo.returncode != 0:
                resultado.erro = f"`cosmic-ray {passo[0]}` falhou:\n{processo.stdout}{processo.stderr}"
                return resultado

        _ler_sessao(pasta / "cr.sqlite", resultado)
    return resultado


def _imprimir(resultados: list[Resultado]) -> None:
    print("\n| Módulo | Mutantes | Mortos | Sobreviventes | Score | Pulados (anotação) |")
    print("|---|---|---|---|---|---|")
    for r in resultados:
        if r.erro:
            print(f"| `{r.modulo}` | - | - | - | erro | - |")
        else:
            print(
                f"| `{r.modulo}` | {r.total} | {r.mortos} | {len(r.sobreviventes)} | {r.score:.1f}% "
                f"| {r.anotacoes_puladas} |"
            )

    for r in resultados:
        if r.erro:
            print(f"\n## {r.modulo}: erro\n{r.erro}")
        elif r.sobreviventes:
            print(f"\n## Sobreviventes em {r.modulo}")
            for s in r.sobreviventes:
                print(f"- {s}")


def main(argv: list[str] | None = None) -> int:
    sys.stdout.reconfigure(encoding="utf-8")  # o console do Windows não é UTF-8 por padrão
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("modulos", nargs="*", help="módulos a mutar (padrão: todos os críticos)")
    parser.add_argument("--paralelo", type=int, default=1, help="quantos módulos rodar ao mesmo tempo")
    args = parser.parse_args(argv)

    modulos = args.modulos or list(MODULOS_CRITICOS)
    desconhecidos = [m for m in modulos if m not in MODULOS_CRITICOS]
    if desconhecidos:
        parser.error(f"módulo fora da lista de críticos: {', '.join(desconhecidos)}")

    with ThreadPoolExecutor(max_workers=args.paralelo) as executor:
        resultados = list(executor.map(rodar_modulo, modulos))

    _imprimir(resultados)
    reprovados = [r for r in resultados if r.erro or r.score < META]
    return 1 if reprovados else 0


if __name__ == "__main__":
    sys.exit(main())
