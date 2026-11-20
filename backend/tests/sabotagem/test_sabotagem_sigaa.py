"""Sabotagem do SIGAA (RNF09): fonte fora do ar, sessão expirada e layout
mudado, do Playwright até o log de execução.

Módulos críticos exercitados: app/scrapers/disciplinas/parser.py,
app/domain/disciplinas.py, app/tasks/scraping.py,
app/tasks/logging_signals.py e app/domain/execucoes.py.
"""

from __future__ import annotations

import asyncio
import math
from pathlib import Path
from types import SimpleNamespace

import pytest
from playwright.async_api import Error as ErroPlaywright
from playwright.async_api import TimeoutError as TimeoutPlaywright
from pydantic import ValidationError

import app.scrapers.disciplinas.scraper as scraper_mod
import app.tasks.scraping as scraping_task
from app.core import cache
from app.core.exceptions import ErroFonteIndisponivel
from app.domain.disciplinas import persistir_turmas
from app.models import Turma
from app.schemas.disciplina import Horario, Professor, Sala
from app.schemas.disciplina import Turma as TurmaCapturada
from app.scrapers.disciplinas import raspar_disciplinas, raspar_disciplinas_varias_unidades
from app.scrapers.disciplinas.parser import listar_unidades, parse_turmas
from app.scrapers.disciplinas.scraper import DisciplinaScraper, _sessao_expirada

FIXTURE_TURMAS = Path(__file__).parents[1] / "scrapers" / "fixtures" / "turmas_fcte_gama_2026_2.html"
RESULTADO_REAL = FIXTURE_TURMAS.read_text(encoding="utf-8")
TURMAS_NA_FIXTURE = len(parse_turmas(RESULTADO_REAL))

FORMULARIO = """
<form id="formTurma">
  <select name="formTurma:inputDepto">
    <option value="0">-- SELECIONE --</option>
    <option value="673">CAMPUS UNB GAMA: FCTE</option>
    <option value="650">FACULDADE UNB PLANALTINA</option>
  </select>
</form>
"""
# O SIGAA escreve a mensagem com escape unicode dentro de um script
SESSAO_EXPIRADA = '<script>alert("A sess\\u00e3o n\\u00e3o est\\u00e1 mais ativa.")</script>'
SEMPRE = math.inf


class SigaaFalso:
    """Dublê do Playwright apontado para um SIGAA que se comporta como o
    teste mandar.

    - `rede_falha(n)`: decide se a n-ésima navegação (`goto`, a partir de 1)
      dá erro de rede;
    - `expiracoes[unidade]`: quantas buscas daquela unidade devolvem
      "sessão não está mais ativa" antes de dar certo (SEMPRE = nunca);
    - `formulario` e `resultado`: HTML da página de busca e do resultado.
    """

    def __init__(self, formulario=FORMULARIO, resultado=RESULTADO_REAL, rede_falha=lambda n: False, expiracoes=None):
        self.formulario = formulario
        self.resultado = resultado
        self.rede_falha = rede_falha
        self.expiracoes = dict(expiracoes or {})
        self.navegacoes = 0
        self.lancamentos = 0
        self.buscas: list[str] = []

    # async_playwright() -> contexto -> chromium.launch() -> browser
    def __call__(self):
        return self

    async def __aenter__(self):
        return self

    async def __aexit__(self, *_):
        return False

    @property
    def chromium(self):
        return self

    async def launch(self, headless=True):
        self.lancamentos += 1
        return self

    async def new_page(self):
        return _PaginaFalsa(self)

    async def close(self):
        pass


class _PaginaFalsa:
    def __init__(self, sigaa: SigaaFalso):
        self.sigaa = sigaa
        self.unidade: str | None = None
        self.buscou = False

    async def goto(self, url, wait_until=None):
        self.sigaa.navegacoes += 1
        self.buscou = False
        if self.sigaa.rede_falha(self.sigaa.navegacoes):
            raise TimeoutPlaywright(f"Timeout 30000ms exceeded navigating to {url}")

    def locator(self, seletor):
        return _CampoFalso(self, seletor)

    async def wait_for_load_state(self, estado):
        pass

    async def content(self):
        if not self.buscou:
            return self.sigaa.formulario
        self.sigaa.buscas.append(self.unidade)
        restantes = self.sigaa.expiracoes.get(self.unidade, 0)
        if restantes:
            self.sigaa.expiracoes[self.unidade] = restantes - 1
            return SESSAO_EXPIRADA
        return self.sigaa.resultado


class _CampoFalso:
    def __init__(self, pagina: _PaginaFalsa, seletor: str):
        self.pagina = pagina
        self.seletor = seletor

    async def select_option(self, valor):
        if self.seletor == scraper_mod._SELETOR_UNIDADE:
            self.pagina.unidade = valor

    async def fill(self, valor):
        pass

    async def click(self):
        self.pagina.buscou = True


def sempre_fora(n):
    return True


def cai_depois_de(navegacoes_ok):
    return lambda n: n > navegacoes_ok


def instavel_nas_primeiras(navegacoes_com_erro):
    return lambda n: n <= navegacoes_com_erro


@pytest.fixture
def sigaa(monkeypatch):
    """Instala um SigaaFalso no lugar do Playwright e tira a espera de
    etiqueta entre unidades. Configure os atributos dele no teste."""
    falso = SigaaFalso()
    monkeypatch.setattr(scraper_mod, "async_playwright", falso)

    async def sem_espera(_segundos):
        return None

    monkeypatch.setattr(scraper_mod, "asyncio", SimpleNamespace(sleep=sem_espera))
    return falso


# ---------------------------------------------------------------- scraper


def test_sessao_expirada_reconhece_a_mensagem_com_escape_unicode():
    assert _sessao_expirada(SESSAO_EXPIRADA)
    assert _sessao_expirada("<html>javax.faces.application.ViewExpiredException</html>")
    assert not _sessao_expirada(RESULTADO_REAL)


def test_sessao_expirada_uma_vez_tenta_de_novo_e_devolve_o_resultado(sigaa):
    sigaa.expiracoes = {"673": 1}

    html = asyncio.run(DisciplinaScraper().buscar_html("G", "673", "2026", "2"))

    assert html == RESULTADO_REAL
    assert sigaa.lancamentos == 2


def test_sessao_sempre_expirada_vira_erro_da_fonte_depois_das_tentativas(sigaa):
    sigaa.expiracoes = {"673": SEMPRE}

    with pytest.raises(ErroFonteIndisponivel, match="unidade 673 após 3 tentativas"):
        asyncio.run(DisciplinaScraper().buscar_html("G", "673", "2026", "2"))

    assert sigaa.lancamentos == 3


def test_sigaa_fora_do_ar_vira_erro_da_fonte_depois_das_tentativas(sigaa):
    sigaa.rede_falha = sempre_fora

    with pytest.raises(ErroFonteIndisponivel, match="não respondeu para a unidade 673") as erro:
        asyncio.run(DisciplinaScraper().buscar_html("G", "673", "2026", "2", tentativas=2))

    assert isinstance(erro.value.__cause__, ErroPlaywright)
    assert sigaa.lancamentos == 2


def test_sigaa_instavel_na_primeira_tentativa_se_recupera_na_segunda(sigaa):
    sigaa.rede_falha = instavel_nas_primeiras(1)

    html = asyncio.run(DisciplinaScraper().buscar_html("G", "673", "2026", "2"))

    assert html == RESULTADO_REAL
    assert sigaa.lancamentos == 2


def test_sigaa_fora_do_ar_ao_abrir_o_formulario_vira_erro_da_fonte(sigaa):
    sigaa.rede_falha = sempre_fora

    with pytest.raises(ErroFonteIndisponivel, match="formulário de busca"):
        asyncio.run(DisciplinaScraper().obter_html_formulario())


def test_varias_unidades_pula_so_a_unidade_com_sessao_sempre_expirada(sigaa):
    sigaa.expiracoes = {"650": SEMPRE, "673": 2}

    resultado = asyncio.run(DisciplinaScraper().buscar_html_varias_unidades("G", "2026", "2", ["650", "673"]))

    assert list(resultado) == ["673"]
    assert sigaa.buscas == ["650"] * 3 + ["673"] * 3


def test_varias_unidades_pula_a_unidade_em_que_a_rede_cai(sigaa):
    # 1 navegação para a home + 1 por tentativa; a primeira unidade passa de
    # primeira e a rede cai antes da segunda
    sigaa.rede_falha = cai_depois_de(2)

    resultado = asyncio.run(DisciplinaScraper().buscar_html_varias_unidades("G", "2026", "2", ["673", "650"]))

    assert list(resultado) == ["673"]


def test_varias_unidades_com_a_home_fora_do_ar_vira_erro_da_fonte(sigaa):
    sigaa.rede_falha = sempre_fora

    with pytest.raises(ErroFonteIndisponivel, match="página inicial"):
        asyncio.run(DisciplinaScraper().buscar_html_varias_unidades("G", "2026", "2", ["673"]))


def test_raspar_disciplinas_de_uma_unidade_devolve_as_turmas_validadas(sigaa):
    turmas = asyncio.run(raspar_disciplinas("G", "673", "2026", "2"))

    assert len(turmas) == TURMAS_NA_FIXTURE
    assert sigaa.buscas == ["673"]


def test_raspar_varias_unidades_sem_lista_usa_as_unidades_do_formulario(sigaa):
    turmas_por_unidade, _ = asyncio.run(raspar_disciplinas_varias_unidades("G", "2026", "2", ["673", "650"]))

    assert list(turmas_por_unidade) == ["673", "650"]
    assert all(len(turmas) == TURMAS_NA_FIXTURE for turmas in turmas_por_unidade.values())


def test_raspar_varias_unidades_aceita_unidade_sem_turma_se_outra_tem(monkeypatch):
    # uma unidade sem oferta no semestre é normal; só todas vazias indica layout novo
    resultados = {"673": RESULTADO_REAL, "650": "<html><body>Nenhuma turma encontrada</body></html>"}

    async def buscar(self, nivel, ano, periodo, unidades):
        return {u: resultados[u] for u in unidades}

    monkeypatch.setattr(DisciplinaScraper, "buscar_html_varias_unidades", buscar)

    turmas_por_unidade, _ = asyncio.run(raspar_disciplinas_varias_unidades("G", "2026", "2", ["673", "650"]))

    assert len(turmas_por_unidade["673"]) == TURMAS_NA_FIXTURE
    assert turmas_por_unidade["650"] == []

def test_raspar_varias_unidades_unidade_que_nunca_responde_entra_em_unidades_com_falha(sigaa):
    sigaa.expiracoes = {"650": SEMPRE}

    turmas_por_unidade, unidades_com_falha = asyncio.run(
        raspar_disciplinas_varias_unidades("G", "2026", "2", ["673", "650"]))

    assert list(turmas_por_unidade) == ["673"]
    assert unidades_com_falha == ["650"]

# ----------------------------------------------------------------- parser

AGRUPADOR = '<tr class="agrupador"><td colspan="8"><span class="tituloDisciplina">FGA0242 - MDS</span></td></tr>'


def _linha(*celulas: str) -> str:
    return "<tr>" + "".join(f"<td>{c}</td>" for c in celulas) + "</tr>"


TURMA_OK = _linha("01", "2026.2", "ANA SOUZA", "6T2345", "", "40", "38", "FCTE - I9")


def _resultado(*linhas: str, id_div: str = "turmasAbertas") -> str:
    return f'<div id="{id_div}"><table class="listagem"><tbody>{"".join(linhas)}</tbody></table></div>'


def test_parser_le_a_tabela_minima_de_controle():
    [turma] = parse_turmas(_resultado(AGRUPADOR, TURMA_OK))

    assert (turma.disciplina_codigo, turma.disciplina_nome, turma.numero) == ("FGA0242", "MDS", "01")
    assert (turma.vagas_ofertadas, turma.vagas_ocupadas) == (40, 38)
    assert turma.sala.descricao == "FCTE - I9"


def test_parser_sem_a_div_de_turmas_devolve_vazio():
    assert parse_turmas(_resultado(AGRUPADOR, TURMA_OK, id_div="turmasOfertadas")) == []


def test_parser_ignora_linha_com_coluna_a_menos():
    linha_sem_sala = _linha("01", "2026.2", "ANA SOUZA", "6T2345", "", "40", "38")

    assert parse_turmas(_resultado(AGRUPADOR, linha_sem_sala, TURMA_OK)) == parse_turmas(
        _resultado(AGRUPADOR, TURMA_OK)
    )


def test_parser_ignora_turma_antes_de_qualquer_disciplina():
    assert parse_turmas(_resultado(TURMA_OK)) == []


def test_parser_com_colunas_trocadas_falha_na_validacao():
    # sala no lugar das vagas: melhor falhar do que gravar vaga errada
    trocada = _linha("01", "2026.2", "ANA SOUZA", "6T2345", "", "FCTE - I9", "38", "40")

    with pytest.raises(ValidationError, match="vagas_ofertadas"):
        parse_turmas(_resultado(AGRUPADOR, trocada))


def test_listar_unidades_sem_o_select_devolve_vazio_e_ignora_o_placeholder():
    assert listar_unidades("<form></form>") == []
    assert listar_unidades(FORMULARIO) == [
        ("673", "CAMPUS UNB GAMA: FCTE"),
        ("650", "FACULDADE UNB PLANALTINA"),
    ]


# ------------------------------------------- task de ponta a ponta, com o log

TURMA_JA_GRAVADA = TurmaCapturada(
    disciplina_codigo="SAB0001",
    disciplina_nome="Turma gravada antes da sabotagem",
    numero="01",
    ano_periodo="2026.2",
    professores=[Professor(nome="Ana Souza")],
    horarios=[Horario(codigo="6T2345", descricao="Sexta-feira 14:00 às 17:50")],
    sala=Sala(descricao="FCTE - I9/I10"),
    vagas_ofertadas=40,
    vagas_ocupadas=38,
)
CHAVES_DE_CACHE = ("cache:v1:disciplinas", "cache:v1:professores", "cache:v1:salas:vazias:sexta:14:00")


def _retrato(banco) -> list[tuple]:
    banco.expire_all()
    return sorted(
        (
            t.disciplina.codigo,
            t.numero,
            t.unidade,
            t.vagas_ofertadas,
            t.vagas_ocupadas,
            tuple(sorted(p.nome for p in t.professores)),
            tuple(sorted(h.codigo for h in t.horarios)),
        )
        for t in banco.query(Turma)
    )


@pytest.fixture
def banco_com_turma(banco):
    persistir_turmas(banco, [TURMA_JA_GRAVADA], "673")
    banco.commit()
    cache._cliente.dados = {chave: "[]" for chave in CHAVES_DE_CACHE}
    return banco


SABOTAGENS = {
    "fora_do_ar": (dict(rede_falha=sempre_fora), "fonte"),
    "cai_durante_a_busca": (dict(rede_falha=cai_depois_de(3)), "fonte"),
    "sessao_expirada": (dict(expiracoes={"673": SEMPRE, "650": SEMPRE}), "fonte"),
    "formulario_mudou": (dict(formulario="<form id='formBusca'></form>"), "interna"),
    "resultado_mudou": (
        dict(resultado=RESULTADO_REAL.replace('id="turmasAbertas"', 'id="turmasOfertadas"')),
        "interna",
    ),
}


def _rodar_task():
    scraping_task.scrape_disciplinas_task.apply(kwargs={"nivel": "G", "ano": "2026", "periodo": "2"})


def test_controle_sem_sabotagem_grava_as_turmas_e_registra_sucesso(sigaa, banco_com_turma, execucao_registrada):
    _rodar_task()

    execucao = execucao_registrada()
    assert (execucao.task_name, execucao.status, execucao.tipo_falha) == (
        scraping_task.scrape_disciplinas_task.name,
        "sucesso",
        None,
    )
    assert banco_com_turma.query(Turma).count() > TURMAS_NA_FIXTURE
    assert cache._cliente.dados == {}


@pytest.mark.parametrize("sabotagem", SABOTAGENS)
def test_sabotagem_registra_falha_e_preserva_o_banco_e_o_cache(sigaa, banco_com_turma, execucao_registrada, sabotagem):
    configuracao, tipo_falha = SABOTAGENS[sabotagem]
    for atributo, valor in configuracao.items():
        setattr(sigaa, atributo, valor)
    antes = _retrato(banco_com_turma)

    _rodar_task()

    execucao = execucao_registrada()
    assert (execucao.status, execucao.tipo_falha) == ("falha", tipo_falha)
    assert execucao.mensagem
    assert _retrato(banco_com_turma) == antes
    assert set(cache._cliente.dados) == set(CHAVES_DE_CACHE)
