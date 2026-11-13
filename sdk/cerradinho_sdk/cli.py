"""CLI da Cerradinho API (RF13), em cima do `CerradinhoClient`.

Cada comando chama um método do SDK e só formata a resposta: nenhuma chamada
HTTP é montada aqui, e nada que a API já calcula (salas vazias, agenda) é
recalculado.

    cerradinho --base-url https://api.<ip>.sslip.io resumo
    export CERRADINHO_API_URL=https://api.<ip>.sslip.io
    cerradinho salas-vazias segunda 14:00
    cerradinho --json disciplinas --busca "métodos de desenvolvimento"
"""

from __future__ import annotations

import datetime
import json
from collections.abc import Callable, Iterator
from contextlib import contextmanager
from dataclasses import dataclass
from typing import Annotated, Any

import httpx
import typer
from rich.console import Console
from rich.table import Table

from . import __version__
from ._gerado.models import Agenda, CardapioSemana, DiaSemana, Resumo
from ._gerado.types import Unset
from .client import CerradinhoClient, ProfessorNaoEncontrado, RespostaInesperada

app = typer.Typer(
    name="cerradinho",
    help="Consulta a API pública da Cerradinho: disciplinas, professores, salas e cardápio do RU da UnB.",
    no_args_is_help=True,
    add_completion=False,
)
@dataclass
class Opcoes:
    base_url: str
    json: bool
    timeout: float


def _versao(mostrar: bool) -> None:
    if mostrar:
        typer.echo(f"cerradinho {__version__}")
        raise typer.Exit()


@app.callback()
def principal(
    ctx: typer.Context,
    base_url: Annotated[
        str,
        typer.Option(
            "--base-url",
            envvar="CERRADINHO_API_URL",
            help="Endereço da API, ex. https://api.<ip>.sslip.io (ver docs/DEPLOY.md).",
            show_envvar=True,
        ),
    ],
    saida_json: Annotated[bool, typer.Option("--json", help="Imprime a resposta da API em JSON.")] = False,
    timeout: Annotated[float, typer.Option(help="Tempo máximo de cada requisição, em segundos.")] = 30.0,
    versao: Annotated[
        bool, typer.Option("--version", callback=_versao, is_eager=True, help="Mostra a versão e sai.")
    ] = False,
) -> None:
    ctx.obj = Opcoes(base_url=base_url, json=saida_json, timeout=timeout)


@contextmanager
def _cliente(opcoes: Opcoes) -> Iterator[CerradinhoClient]:
    """Abre o SDK e traduz os erros dele numa mensagem e código de saída 1."""
    try:
        with CerradinhoClient(opcoes.base_url, timeout=opcoes.timeout) as cliente:
            yield cliente
    except ProfessorNaoEncontrado as e:
        _falhar(str(e))
    except RespostaInesperada as e:
        _falhar(_explicar(e))
    except httpx.TimeoutException:
        _falhar(f"A API em {opcoes.base_url} não respondeu em {opcoes.timeout:g} s.")
    except httpx.TransportError as e:
        _falhar(f"Não foi possível acessar a API em {opcoes.base_url}: {e}")


def _explicar(e: RespostaInesperada) -> str:
    if e.status_code == httpx.codes.NOT_FOUND:
        # rota que o SDK conhece e a API não: a API no ar é de uma versão anterior
        return f"A API não tem essa consulta (status 404). Ela pode estar numa versão anterior à do SDK {__version__}."
    if e.status_code == httpx.codes.TOO_MANY_REQUESTS:
        return "Limite de requisições da API atingido (status 429). Tente de novo daqui a pouco."
    detalhe = e.corpo.to_dict() if hasattr(e.corpo, "to_dict") else e.corpo
    return f"A API respondeu fora do esperado (status {e.status_code})" + (f": {detalhe}" if detalhe else ".")


def _falhar(mensagem: str) -> None:
    Console(stderr=True).print(f"[bold red]Erro:[/] {mensagem}", highlight=False)
    raise typer.Exit(code=1)


def _imprimir(opcoes: Opcoes, resposta: Any, tabela: Callable[[], Table]) -> None:
    if opcoes.json:
        dados = [item.to_dict() for item in resposta] if isinstance(resposta, list) else resposta.to_dict()
        typer.echo(json.dumps(dados, ensure_ascii=False, indent=2))
    elif isinstance(resposta, list) and not resposta:
        Console().print("Nenhum resultado.")
    else:
        Console().print(tabela())


def _tabela(titulo: str | None, *colunas: str) -> Table:
    tabela = Table(title=titulo, title_justify="left")
    for coluna in colunas:
        tabela.add_column(coluna)
    return tabela


@app.command()
def disciplinas(
    ctx: typer.Context,
    busca: Annotated[str | None, typer.Option(help="Código ou nome da disciplina, ou nome de professor.")] = None,
    departamento: Annotated[str | None, typer.Option(help="Prefixo do código, ex. FGA.")] = None,
    limite: Annotated[int | None, typer.Option(min=1, help="Máximo de turmas devolvidas.")] = None,
    offset: Annotated[int, typer.Option(min=0, help="Quantas turmas pular, para paginar.")] = 0,
) -> None:
    """Turmas ofertadas no período (RF01-RF05)."""
    opcoes: Opcoes = ctx.obj
    with _cliente(opcoes) as cliente:
        turmas = cliente.listar_disciplinas(busca=busca, departamento=departamento, limite=limite, offset=offset)

    def tabela() -> Table:
        t = _tabela(None, "Código", "Disciplina", "Turma", "Professores", "Horários", "Sala", "Vagas")
        for turma in turmas:
            t.add_row(
                turma.disciplina_codigo,
                turma.disciplina_nome,
                turma.numero,
                ", ".join(p.nome for p in turma.professores),
                " ".join(h.codigo for h in turma.horarios),
                turma.sala.descricao,
                f"{turma.vagas_ocupadas}/{turma.vagas_ofertadas}",
            )
        return t

    _imprimir(opcoes, turmas, tabela)


@app.command()
def professores(
    ctx: typer.Context,
    nome: Annotated[str | None, typer.Argument(help="Parte do nome, sem diferenciar acento ou caixa.")] = None,
    limite: Annotated[int | None, typer.Option(min=1, help="Máximo de professores devolvidos.")] = None,
    offset: Annotated[int, typer.Option(min=0, help="Quantos professores pular, para paginar.")] = 0,
) -> None:
    """Docentes do período, com o id usado no comando `agenda` (RF04)."""
    opcoes: Opcoes = ctx.obj
    with _cliente(opcoes) as cliente:
        docentes = cliente.listar_professores(nome, limite=limite, offset=offset)

    def tabela() -> Table:
        t = _tabela(None, "Id", "Nome", "Disciplinas")
        for docente in docentes:
            t.add_row(str(docente.id), docente.nome, ", ".join(docente.disciplinas))
        return t

    _imprimir(opcoes, docentes, tabela)


@app.command()
def agenda(
    ctx: typer.Context,
    professor_id: Annotated[int, typer.Argument(help="Id do professor (veja no comando `professores`).")],
) -> None:
    """Agenda semanal de um professor, com a sala de cada aula (RF18)."""
    opcoes: Opcoes = ctx.obj
    with _cliente(opcoes) as cliente:
        resposta: Agenda = cliente.obter_agenda(professor_id)

    def tabela() -> Table:
        t = _tabela(resposta.nome, "Dia", "Início", "Fim", "Código", "Disciplina", "Turma", "Sala")
        for turma in resposta.turmas:
            for bloco in turma.horarios:
                sala = f"{bloco.sala.predio} - {bloco.sala.nome}" if bloco.sala else "sem sala"
                t.add_row(
                    bloco.dia,
                    bloco.inicio,
                    bloco.fim,
                    turma.disciplina_codigo,
                    turma.disciplina_nome,
                    turma.numero,
                    sala,
                )
        return t

    _imprimir(opcoes, resposta, tabela)


@app.command()
def salas(ctx: typer.Context) -> None:
    """Salas com aula no período (RF05)."""
    opcoes: Opcoes = ctx.obj
    with _cliente(opcoes) as cliente:
        espacos = cliente.listar_salas()
    _imprimir(opcoes, espacos, lambda: _tabela_de_salas(espacos))


@app.command("salas-vazias")
def salas_vazias(
    ctx: typer.Context,
    dia: Annotated[DiaSemana, typer.Argument(help="Dia da semana.")],
    horario: Annotated[str, typer.Argument(help="Início da aula, no formato HH:MM, ex. 14:00.")],
) -> None:
    """Salas sem turma no dia e horário dados (RF17)."""
    opcoes: Opcoes = ctx.obj
    with _cliente(opcoes) as cliente:
        espacos = cliente.listar_salas_vazias(dia, horario)
    _imprimir(opcoes, espacos, lambda: _tabela_de_salas(espacos))


def _tabela_de_salas(espacos: list) -> Table:
    t = _tabela(None, "Id", "Prédio", "Sala")
    for espaco in espacos:
        t.add_row(str(espaco.id), espaco.predio, espaco.nome)
    return t


@app.command()
def cardapio(
    ctx: typer.Context,
    data_inicio: Annotated[
        datetime.datetime | None,
        typer.Option(formats=["%Y-%m-%d"], help="Primeiro dia da semana (AAAA-MM-DD). Padrão: hoje."),
    ] = None,
) -> None:
    """Cardápio do RU (Darcy) dos 7 dias a partir da data (RF19)."""
    opcoes: Opcoes = ctx.obj
    with _cliente(opcoes) as cliente:
        semana: CardapioSemana = cliente.obter_cardapio_semana(data_inicio.date() if data_inicio else None)

    def tabela() -> Table:
        titulo = f"Cardápio de {semana.data_inicio:%d/%m} a {semana.data_fim:%d/%m}"
        t = _tabela(titulo, "Dia", "Café", "Almoço", "Jantar")
        for dia in semana.dias:
            data = f"{dia.data:%d/%m}"
            if not dia.publicado:
                t.add_row(data, "não publicado", "", "")
                continue
            refeicoes = (dia.cafe_da_manha, dia.almoco, dia.jantar)
            t.add_row(data, *("\n".join(i.item for i in refeicao) for refeicao in refeicoes))
        return t

    _imprimir(opcoes, semana, tabela)


@app.command()
def execucoes(
    ctx: typer.Context,
    limite: Annotated[int, typer.Option(min=1, help="Máximo de execuções devolvidas.")] = 20,
) -> None:
    """Últimas execuções dos scrapers, com sucesso ou falha (RF16)."""
    opcoes: Opcoes = ctx.obj
    with _cliente(opcoes) as cliente:
        lista = cliente.listar_execucoes(limite)

    def tabela() -> Table:
        t = _tabela(None, "Id", "Quando (UTC)", "Task", "Status", "Falha", "Mensagem")
        for execucao in lista:
            t.add_row(
                str(execucao.id),
                f"{execucao.criado_em:%d/%m/%Y %H:%M}",
                execucao.task_name.rsplit(".", 1)[-1],  # app.tasks.cardapio.x -> x
                execucao.status,
                _texto(execucao.tipo_falha),
                _texto(execucao.mensagem),
            )
        return t

    _imprimir(opcoes, lista, tabela)


def _texto(valor: str | None | Unset) -> str:
    return valor if isinstance(valor, str) else ""


@app.command()
def resumo(ctx: typer.Context) -> None:
    """Quantas turmas, disciplinas, professores e salas a API tem."""
    opcoes: Opcoes = ctx.obj
    with _cliente(opcoes) as cliente:
        contagens: Resumo = cliente.obter_resumo()

    def tabela() -> Table:
        t = _tabela(None, "Domínio", "Total")
        for nome in ("turmas", "disciplinas", "professores", "salas"):
            t.add_row(nome.capitalize(), str(getattr(contagens, nome)))
        return t

    _imprimir(opcoes, contagens, tabela)


if __name__ == "__main__":
    app()
