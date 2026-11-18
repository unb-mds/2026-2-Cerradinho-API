from datetime import date

import pytest
import requests

import app.scrapers.cardapio as cardapio
from app.core.exceptions import ErroFonteIndisponivel
from app.scrapers.cardapio.scraper import URLS_CARDAPIO

# As duas páginas onde o RU publica o PDF do Darcy Ribeiro. Em outubro de
# 2026 uma delas ficou uma semana parada enquanto a outra já tinha a semana
# nova, e depois as duas voltaram a ser atualizadas (risco A2).
PAGINA_ATUALIZADA = """
<a href="/wp-content/uploads/Darcy-Ribeiro-Semana-01-19-10-a-25-10.pdf">ISM &#8211; 19/10/2026 À 25/10/2026</a>
"""
PAGINA_PARADA = """
<a href="/wp-content/uploads/Darcy-Ribeiro-Semana-06-12-10-a-18-10.pdf">ISM &#8211; 12/10/2026 A 18/10/2026</a>
"""
SEMANA_NOVA = date(2026, 10, 21)


@pytest.fixture
def paginas(monkeypatch):
    """Substitui o download das páginas pelo HTML de cada URL e devolve o
    PDF escolhido, sem baixar nem ler PDF de verdade."""
    conteudo: dict[str, str | Exception] = {}

    def baixar_html_falso(url):
        resposta = conteudo[url]
        if isinstance(resposta, Exception):
            raise resposta
        return resposta

    monkeypatch.setattr(cardapio, "baixar_html", baixar_html_falso)
    monkeypatch.setattr(cardapio, "baixar_pdf", lambda url: url)
    monkeypatch.setattr(cardapio, "extrair_itens_cardapio", lambda url: url)
    return conteudo


@pytest.mark.parametrize("parada", URLS_CARDAPIO)
def test_usa_a_pagina_que_tem_a_semana_atual(paginas, parada):
    for url in URLS_CARDAPIO:
        paginas[url] = PAGINA_PARADA if url == parada else PAGINA_ATUALIZADA

    assert "19-10-a-25-10" in cardapio.raspar_cardapio(SEMANA_NOVA)


def test_pagina_fora_do_ar_nao_impede_a_outra(paginas):
    paginas[URLS_CARDAPIO[0]] = requests.ConnectionError("fora do ar")
    paginas[URLS_CARDAPIO[1]] = PAGINA_ATUALIZADA

    assert "19-10-a-25-10" in cardapio.raspar_cardapio(SEMANA_NOVA)


def test_falha_quando_nenhuma_pagina_tem_a_semana_atual(paginas):
    for url in URLS_CARDAPIO:
        paginas[url] = PAGINA_PARADA

    with pytest.raises(ErroFonteIndisponivel):
        cardapio.raspar_cardapio(SEMANA_NOVA)
