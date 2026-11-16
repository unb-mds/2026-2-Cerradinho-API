"""Sabotagem do RU (RNF09): site fora do ar, PDF indisponível e layout
mudado (da página de listagem e do PDF), do `requests.get` até o log de
execução.

O RU não tem sessão; o equivalente à sessão expirada do SIGAA é o link do
PDF que deixa de valer e passa a devolver uma página de erro com status 200.

Módulos críticos exercitados: app/scrapers/cardapio/parser.py,
app/domain/cardapio.py, app/tasks/cardapio.py,
app/tasks/logging_signals.py e app/domain/execucoes.py.
"""

from __future__ import annotations

import logging
from contextlib import contextmanager
from datetime import date, timedelta
from pathlib import Path
from types import SimpleNamespace

import pytest
import requests

import app.scrapers.cardapio.parser as parser_mod
import app.scrapers.cardapio.scraper as scraper_mod
import app.tasks.cardapio as cardapio_task
from app.core import cache
from app.core.exceptions import ErroFonteIndisponivel
from app.domain.cardapio import listar_cardapio_semana, persistir_cardapio
from app.models import Cardapio
from app.schemas.cardapio import ItemCardapio
from app.scrapers.cardapio import raspar_cardapio
from app.scrapers.cardapio.parser import extrair_itens_cardapio, extrair_links_cardapio
from app.scrapers.cardapio.scraper import HEADERS, URLS_CARDAPIO, baixar_html, baixar_pdf

SEGUNDA_DA_FIXTURE = date(2026, 10, 12)
FIXTURES = Path(__file__).parents[1] / "scrapers" / "fixtures"
PDF_REAL = (FIXTURES / f"cardapio_darcy_{SEGUNDA_DA_FIXTURE}.pdf").read_bytes()
URL_PDF = "https://ru.unb.br/wp-content/uploads/Darcy-Ribeiro-Semana.pdf"
CATEGORIAS_QUE_IDENTIFICAM_A_REFEICAO = ("PANIFICAÇÃO", "FRUTA", "GUARNIÇÃO", "SOPA", "TORRADA")


def _listagem_da_semana_atual() -> str:
    # a task usa a data de hoje, então o link precisa ser o da semana de hoje
    segunda = date.today() - timedelta(days=date.today().weekday())
    domingo = segunda + timedelta(days=6)
    intervalo = f"{segunda.day}/{segunda.month}/{segunda.year} A {domingo.day}/{domingo.month}/{domingo.year}"
    return f'<a href="/wp-content/uploads/Darcy-Ribeiro-Semana.pdf">ISM &#8211; {intervalo}</a>'


def _resposta(url: str, status: int = 200, corpo: bytes = b"", content_type: str = "text/html") -> requests.Response:
    resposta = requests.Response()
    resposta.url = url
    resposta.status_code = status
    resposta._content = corpo
    resposta.encoding = "utf-8"
    resposta.headers["Content-Type"] = content_type
    return resposta


class RuFalso:
    """Dublê do site do RU no lugar de `requests.get`.

    - `paginas[url]`: HTML da listagem, um status HTTP (int) ou uma exceção;
    - `pdf`: bytes do PDF, uma exceção ou uma `requests.Response` pronta;
    - `pdf_falhas`: quantos downloads do PDF dão timeout antes de dar certo.
    """

    def __init__(self):
        listagem = _listagem_da_semana_atual()
        self.paginas: dict[str, str | int | Exception] = dict.fromkeys(URLS_CARDAPIO, listagem)
        self.pdf: bytes | Exception | requests.Response = PDF_REAL
        self.pdf_falhas = 0
        self.chamadas: list[tuple[str, dict, int]] = []

    def get(self, url, headers=None, timeout=None):
        self.chamadas.append((url, headers, timeout))
        resposta = self.paginas.get(url, self.pdf)
        if url not in self.paginas and self.pdf_falhas:
            self.pdf_falhas -= 1
            raise requests.Timeout(f"Read timed out. (read timeout={timeout})")
        if isinstance(resposta, Exception):
            raise resposta
        if isinstance(resposta, requests.Response):
            return resposta
        if isinstance(resposta, int):
            return _resposta(url, status=resposta)
        if isinstance(resposta, bytes):
            return _resposta(url, corpo=resposta, content_type="application/pdf")
        return _resposta(url, corpo=resposta.encode())


@pytest.fixture
def ru(monkeypatch):
    falso = RuFalso()
    monkeypatch.setattr(scraper_mod.requests, "get", falso.get)
    return falso


@pytest.fixture
def esperas(monkeypatch):
    """Tira o backoff entre tentativas e devolve as esperas pedidas."""
    pedidas: list[float] = []
    monkeypatch.setattr(scraper_mod.time, "sleep", pedidas.append)
    return pedidas


class _PaginaSabotada:
    """Página real do PDF com as palavras e o texto das células trocados,
    simulando o RU mudando o modelo da tabela."""

    def __init__(self, pagina, trocar_texto, sem_tabelas):
        self._pagina = pagina
        self._trocar = trocar_texto
        self._sem_tabelas = sem_tabelas

    def extract_words(self):
        return [{**p, "text": self._trocar(p["text"])} for p in self._pagina.extract_words()]

    def find_tables(self):
        return [] if self._sem_tabelas else self._pagina.find_tables()

    def filter(self, funcao):
        recorte = self._pagina.filter(funcao)
        return SimpleNamespace(extract_text=lambda: self._trocar(recorte.extract_text() or ""))


@pytest.fixture
def pdf_sabotado(monkeypatch):
    """Faz o pdfplumber devolver páginas sabotadas: `trocar_texto` reescreve
    todo texto lido da página e `sem_tabelas` some com as bordas da tabela."""
    abrir_real = parser_mod.pdfplumber.open

    def sabotar(trocar_texto=lambda texto: texto, sem_tabelas=False):
        @contextmanager
        def abrir(arquivo):
            with abrir_real(arquivo) as pdf:
                yield SimpleNamespace(pages=[_PaginaSabotada(p, trocar_texto, sem_tabelas) for p in pdf.pages])

        monkeypatch.setattr(parser_mod.pdfplumber, "open", abrir)

    return sabotar


def _renomear(*antigos: str, novo: str = "OUTRA"):
    def trocar(texto: str) -> str:
        for antigo in antigos:
            texto = texto.replace(antigo, novo)
        return texto

    return trocar


def _datas_por_extenso(texto: str) -> str:
    return parser_mod.RE_DATA.sub("dia", texto)


# ---------------------------------------------------------------- scraper


def test_baixar_html_identifica_o_bot_e_usa_timeout(ru):
    assert "Darcy-Ribeiro" in baixar_html(URLS_CARDAPIO[0])
    assert ru.chamadas == [(URLS_CARDAPIO[0], HEADERS, 10)]


def test_baixar_html_com_erro_500_levanta_erro_http(ru):
    ru.paginas[URLS_CARDAPIO[0]] = 500

    with pytest.raises(requests.HTTPError):
        baixar_html(URLS_CARDAPIO[0])


def test_baixar_pdf_instavel_se_recupera_e_espera_antes_de_tentar_de_novo(ru, esperas):
    ru.pdf_falhas = 1

    assert baixar_pdf(URL_PDF) == PDF_REAL
    assert esperas == [2]
    assert ru.chamadas[-1] == (URL_PDF, HEADERS, 15)


def test_baixar_pdf_fora_do_ar_vira_erro_da_fonte_com_espera_crescente(ru, esperas):
    ru.pdf = requests.ConnectionError("fora do ar")

    with pytest.raises(ErroFonteIndisponivel, match="após 3 tentativas") as erro:
        baixar_pdf(URL_PDF)

    assert isinstance(erro.value.__cause__, requests.ConnectionError)
    assert esperas == [2, 4]
    assert len(ru.chamadas) == 3


def test_baixar_pdf_rejeita_pagina_de_erro_com_status_200(ru, esperas):
    ru.pdf = _resposta(URL_PDF, corpo=b"<html>Arquivo removido</html>", content_type="text/html; charset=UTF-8")

    with pytest.raises(ErroFonteIndisponivel) as erro:
        baixar_pdf(URL_PDF)

    assert "não é um PDF" in str(erro.value.__cause__)


def test_baixar_pdf_aceita_content_type_em_maiusculas(ru, esperas):
    ru.pdf = _resposta(URL_PDF, corpo=PDF_REAL, content_type="Application/PDF")

    assert baixar_pdf(URL_PDF) == PDF_REAL
    assert esperas == []


def test_primeira_pagina_com_erro_500_nao_impede_a_segunda(ru, esperas):
    ru.paginas[URLS_CARDAPIO[0]] = 500

    itens = raspar_cardapio()

    assert {i.data for i in itens} >= {SEGUNDA_DA_FIXTURE}
    assert [url for url, _, _ in ru.chamadas] == [*URLS_CARDAPIO, URL_PDF]


# ----------------------------------------------------------------- parser


def test_listagem_sem_link_de_pdf_avisa_que_o_layout_pode_ter_mudado(caplog):
    with caplog.at_level(logging.WARNING, logger=parser_mod.__name__):
        assert extrair_links_cardapio("<div>Cardápio em manutenção</div>") == []

    assert "layout do site pode ter mudado" in caplog.text


def test_controle_pdf_real_sem_sabotagem_extrai_as_tres_refeicoes(pdf_sabotado):
    pdf_sabotado()

    itens = extrair_itens_cardapio(PDF_REAL)

    assert {i.refeicao for i in itens} == {"cafe_da_manha", "almoco", "jantar"}


@pytest.mark.parametrize(
    "sabotagem, erro",
    [
        (dict(trocar_texto=_renomear("COMPOSIÇÃO", novo="ITENS")), "Coluna 'COMPOSIÇÃO' não encontrada"),
        (dict(trocar_texto=_datas_por_extenso), "datas dos dias no cabeçalho"),
        (dict(sem_tabelas=True), "Nenhuma tabela encontrada"),
        (dict(trocar_texto=_renomear(*CATEGORIAS_QUE_IDENTIFICAM_A_REFEICAO)), "Não reconheci a refeição"),
    ],
    ids=["coluna_de_categoria_renomeada", "datas_por_extenso", "tabela_sem_bordas", "categorias_novas"],
)
def test_pdf_com_layout_novo_falha_com_erro_explicito(pdf_sabotado, sabotagem, erro):
    pdf_sabotado(**sabotagem)

    with pytest.raises(ValueError, match=erro):
        extrair_itens_cardapio(PDF_REAL)


# ------------------------------------------- task de ponta a ponta, com o log

ALMOCO_JA_GRAVADO = ItemCardapio(
    data=SEGUNDA_DA_FIXTURE, refeicao="almoco", categoria="PRATO PRINCIPAL", item="Gravado antes da sabotagem"
)
CHAVE_DE_CACHE = f"cache:v1:cardapio:semana:{SEGUNDA_DA_FIXTURE}"


def _retrato(banco) -> list[tuple]:
    banco.expire_all()
    return sorted((c.data, c.cafe, c.almoco, c.jantar) for c in banco.query(Cardapio))


@pytest.fixture
def banco_com_cardapio(banco):
    persistir_cardapio(banco, [ALMOCO_JA_GRAVADO])
    banco.commit()
    cache._cliente.dados = {CHAVE_DE_CACHE: "{}"}
    return banco


def _sabotar_site(ru, pdf_sabotado, cenario):
    if cenario == "fora_do_ar":
        ru.paginas = dict.fromkeys(URLS_CARDAPIO, requests.ConnectionError("fora do ar"))
    elif cenario == "listagem_com_erro_500":
        ru.paginas = dict.fromkeys(URLS_CARDAPIO, 503)
    elif cenario == "listagem_sem_o_pdf_da_semana":
        ru.paginas = dict.fromkeys(URLS_CARDAPIO, "<div>Cardápio em manutenção</div>")
    elif cenario == "pdf_fora_do_ar":
        ru.pdf = requests.Timeout("Read timed out.")
    elif cenario == "link_do_pdf_expirado":
        ru.pdf = _resposta(URL_PDF, status=404)
    elif cenario == "pdf_virou_pagina_de_erro":
        ru.pdf = _resposta(URL_PDF, corpo=b"<html>Arquivo removido</html>")
    elif cenario == "pdf_corrompido":
        ru.pdf = PDF_REAL[: len(PDF_REAL) // 3]
    elif cenario == "layout_do_pdf_mudou":
        pdf_sabotado(trocar_texto=_renomear("COMPOSIÇÃO", novo="ITENS"))


SABOTAGENS = {
    "fora_do_ar": "fonte",
    "listagem_com_erro_500": "fonte",
    "listagem_sem_o_pdf_da_semana": "fonte",
    "pdf_fora_do_ar": "fonte",
    "link_do_pdf_expirado": "fonte",
    "pdf_virou_pagina_de_erro": "fonte",
    "pdf_corrompido": "interna",
    "layout_do_pdf_mudou": "interna",
}


def test_controle_sem_sabotagem_grava_o_cardapio_e_registra_sucesso(
    ru, esperas, banco_com_cardapio, execucao_registrada
):
    cardapio_task.scrape_cardapio_task.apply()

    execucao = execucao_registrada()
    assert (execucao.task_name, execucao.status, execucao.tipo_falha) == (
        cardapio_task.scrape_cardapio_task.name,
        "sucesso",
        None,
    )
    segunda = listar_cardapio_semana(banco_com_cardapio, SEGUNDA_DA_FIXTURE).dias[0]
    assert segunda.publicado
    assert ALMOCO_JA_GRAVADO.item not in [i.item for i in segunda.almoco]
    assert cache._cliente.dados == {}


@pytest.mark.parametrize("sabotagem", SABOTAGENS)
def test_sabotagem_registra_falha_e_preserva_o_cardapio_e_o_cache(
    ru, esperas, pdf_sabotado, banco_com_cardapio, execucao_registrada, sabotagem
):
    _sabotar_site(ru, pdf_sabotado, sabotagem)
    antes = _retrato(banco_com_cardapio)

    cardapio_task.scrape_cardapio_task.apply()

    execucao = execucao_registrada()
    assert (execucao.status, execucao.tipo_falha) == ("falha", SABOTAGENS[sabotagem])
    assert execucao.mensagem
    assert _retrato(banco_com_cardapio) == antes
    segunda = listar_cardapio_semana(banco_com_cardapio, SEGUNDA_DA_FIXTURE).dias[0]
    assert [i.item for i in segunda.almoco] == [ALMOCO_JA_GRAVADO.item]
    assert set(cache._cliente.dados) == {CHAVE_DE_CACHE}
