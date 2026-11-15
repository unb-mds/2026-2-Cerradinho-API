"""Regras posicionais do parser do cardápio (ver a docstring de
app/scrapers/cardapio/parser.py) numa página montada à mão, com as
coordenadas sob controle do teste.

Os PDFs reais (test_cardapio_parser.py) mostram que o parser funciona
nas semanas que já vimos, mas não isolam cada regra. Estes testes foram
escritos a partir dos mutantes que sobreviveram ao teste de mutação
(RNF09, `python -m scripts.mutacao app/scrapers/cardapio/parser.py`).
"""

from __future__ import annotations

import logging
from contextlib import contextmanager
from datetime import date
from types import SimpleNamespace

import pytest

import app.scrapers.cardapio.parser as parser_mod
from app.scrapers.cardapio.parser import (
    _texto_da_celula,
    encontrar_pdf_da_semana,
    extrair_itens_cardapio,
    extrair_links_cardapio,
)

SEGUNDA, TERCA = date(2026, 9, 14), date(2026, 9, 15)


def _palavra(texto, x0, x1, top=0, bottom=10):
    return {"text": texto, "x0": x0, "x1": x1, "top": top, "bottom": bottom}


def _caractere(texto, x0, x1, top, bottom):
    return {"object_type": "char", "text": texto, "x0": x0, "x1": x1, "top": top, "bottom": bottom}


class PaginaFalsa:
    """Imita o pedaço do pdfplumber que o parser usa: `extract_words`,
    `find_tables().cells` e `filter(...).extract_text()`. O texto de cada
    célula vira um caractere no centro dela."""

    def __init__(self, celulas: list[tuple[tuple[float, float, float, float], str]], objetos=None):
        self._celulas = celulas
        self.objetos = objetos if objetos is not None else [
            _caractere(texto, (x0 + x1) / 2 - 1, (x0 + x1) / 2 + 1, (top + bottom) / 2 - 1, (top + bottom) / 2 + 1)
            for (x0, top, x1, bottom), texto in celulas
        ]

    def extract_words(self):
        # cabeçalho: coluna de categoria em x 0-100, segunda em x 100-200 e
        # terça em x 200-300; o cabeçalho termina em y = 10
        return [
            _palavra("COMPOSIÇÃO", 20, 80),
            _palavra(f"{SEGUNDA.day}/{SEGUNDA.month}/{SEGUNDA.year}", 110, 190),
            _palavra(f"{TERCA.day}/{TERCA.month}/{TERCA.year}", 210, 290),
        ]

    def find_tables(self):
        return [SimpleNamespace(cells=[bbox for bbox, _ in self._celulas])]

    def filter(self, funcao):
        selecionados = [o for o in self.objetos if funcao(o)]
        return SimpleNamespace(extract_text=lambda: " ".join(o["text"] for o in selecionados))


ALMOCO = [
    ((0, 20, 100, 40), "GUARNIÇÃO"),
    # um pouco acima da categoria, por arredondamento entre bordas vizinhas
    ((100, 19.6, 200, 40), "Arroz"),
    ((200, 20, 300, 40), "Feijão"),
    # texto à direita do último dia: sem dia, ignorado
    ((300, 20, 400, 40), "Observação"),
    ((0, 40, 100, 60), "PRATO PRINCIPAL"),
    # célula mesclada que cobre os dois dias
    ((100, 40, 300, 60), "Frango"),
]
JANTAR = [((0, 20, 100, 40), "SOPA"), ((100, 20, 300, 40), "Sopa de legumes")]


@pytest.fixture
def pdf_com_paginas(monkeypatch):
    def montar(*paginas: list):
        @contextmanager
        def abrir(_arquivo):
            yield SimpleNamespace(pages=[PaginaFalsa(celulas) for celulas in paginas])

        monkeypatch.setattr(parser_mod.pdfplumber, "open", abrir)

    return montar


def _tuplas(itens):
    return [(i.refeicao, i.categoria, i.data, i.item) for i in itens]


def test_le_categoria_por_altura_e_dia_por_posicao_ignorando_texto_sem_dia(pdf_com_paginas, caplog):
    pdf_com_paginas(ALMOCO)

    with caplog.at_level(logging.WARNING, logger=parser_mod.__name__):
        itens = extrair_itens_cardapio(b"pdf")

    assert _tuplas(itens) == [
        ("almoco", "GUARNIÇÃO", SEGUNDA, "Arroz"),
        ("almoco", "GUARNIÇÃO", TERCA, "Feijão"),
        ("almoco", "PRATO PRINCIPAL", SEGUNDA, "Frango"),
        ("almoco", "PRATO PRINCIPAL", TERCA, "Frango"),
    ]
    assert "'Observação'" in caplog.text


def test_avisa_quais_refeicoes_faltam_no_pdf(pdf_com_paginas, caplog):
    pdf_com_paginas(ALMOCO, JANTAR)

    with caplog.at_level(logging.WARNING, logger=parser_mod.__name__):
        itens = extrair_itens_cardapio(b"pdf")

    assert {i.refeicao for i in itens} == {"almoco", "jantar"}
    assert "Refeições não encontradas neste PDF: {'cafe_da_manha'}" in caplog.text
    assert "mais de uma página" not in caplog.text


def test_avisa_refeicao_repetida_em_duas_paginas(pdf_com_paginas, caplog):
    pdf_com_paginas(ALMOCO, ALMOCO)

    with caplog.at_level(logging.WARNING, logger=parser_mod.__name__):
        extrair_itens_cardapio(b"pdf")

    assert "Refeição 'almoco' identificada em mais de uma página (página 1)" in caplog.text


def test_pagina_so_com_categorias_falha_por_nao_ter_item(pdf_com_paginas):
    pdf_com_paginas([((0, 20, 100, 40), "GUARNIÇÃO")])

    with pytest.raises(ValueError, match="Nenhum item extraído"):
        extrair_itens_cardapio(b"pdf")


def test_letra_que_passa_da_borda_entra_pela_posicao_do_centro():
    # centro em (10.5, 5.5): dentro da célula que começa em x = 10.3,
    # mesmo com o caractere começando antes da borda (o caso do "Rosé")
    pagina = PaginaFalsa([], objetos=[_caractere("R", 10.2, 10.8, 5.2, 5.8)])

    assert _texto_da_celula(pagina, (10.3, 5.3, 20, 10)) == "R"
    assert _texto_da_celula(pagina, (10.6, 0, 20, 10)) == ""


# ------------------------------------------------- links da página do RU

LISTAGEM = """
<a href="/a.pdf">ISM &#8211; 7/9/2026 A 13/9/2026 (atualizado em 8/9/2026) Darcy</a>
<a href="/b.pdf">ISM &#8211; 14/9/2026 Darcy</a>
<a href="/c.pdf">ISM &#8211; 21/9/2026 A 27/9/2026 Darcy</a>
"""


def test_link_que_nao_tem_exatamente_duas_datas_e_ignorado():
    links = extrair_links_cardapio(LISTAGEM, url_base="https://ru.unb.br/cardapio/")

    assert len(links) == 3
    assert encontrar_pdf_da_semana(links, date(2026, 9, 8)) is None
    assert encontrar_pdf_da_semana(links, date(2026, 9, 14)) is None


@pytest.mark.parametrize("dia", [date(2026, 9, 21), date(2026, 9, 27)], ids=["primeiro_dia", "ultimo_dia"])
def test_primeiro_e_ultimo_dia_do_intervalo_contam_como_da_semana(dia):
    links = extrair_links_cardapio(LISTAGEM, url_base="https://ru.unb.br/cardapio/")

    assert encontrar_pdf_da_semana(links, dia) == "https://ru.unb.br/c.pdf"
