from datetime import date
from pathlib import Path

import pytest

from app.scrapers.cardapio.parser import encontrar_pdf_da_semana, extrair_itens_cardapio, extrair_links_cardapio

FIXTURE_PDF = Path(__file__).parent / "fixtures" / "cardapio_darcy_semana.pdf"

HTML_LISTAGEM = """
<html><body>
<h3>Cardápio Darcy Ribeiro</h3>
<a href="/wp-content/uploads/2026/09/Darcy-Ribeiro-Semana-03-7-9-a-13-9.pdf">ISM &ndash; 7/9/2026 A 13/9/2026</a>
<a href="/wp-content/uploads/2026/09/Darcy-Ribeiro-Semana-04-14-9-a-20-9.pdf">ISM &ndash; 14/9/2026 A 20/9/2026</a>
<h3>Cardápio Ceilândia</h3>
<a href="/wp-content/uploads/2026/09/Ceilandia-Semana-04-14-9-a-20-9.pdf">ISM &ndash; 14/9/2026 A 20/9/2026</a>
</body></html>
"""


def test_extrair_links_cardapio_filtra_por_campus_e_resolve_url_absoluta():
    links = extrair_links_cardapio(HTML_LISTAGEM, url_base="https://ru.unb.br/cardapio-refeitorio/")

    assert len(links) == 2
    assert all("Darcy-Ribeiro" in link["url"] for link in links)
    assert links[0]["url"].startswith("https://ru.unb.br/")


def test_encontrar_pdf_da_semana_escolhe_o_intervalo_que_contem_a_referencia():
    links = extrair_links_cardapio(HTML_LISTAGEM, url_base="https://ru.unb.br/cardapio-refeitorio/")

    pdf = encontrar_pdf_da_semana(links, referencia=date(2026, 9, 16))

    assert pdf is not None
    assert "Semana-04" in pdf


def test_encontrar_pdf_da_semana_retorna_none_sem_correspondencia():
    links = extrair_links_cardapio(HTML_LISTAGEM, url_base="https://ru.unb.br/cardapio-refeitorio/")

    assert encontrar_pdf_da_semana(links, referencia=date(2026, 1, 1)) is None


def test_extrair_itens_cardapio_le_as_tres_refeicoes_da_semana():
    conteudo_pdf = FIXTURE_PDF.read_bytes()

    itens = extrair_itens_cardapio(conteudo_pdf)

    assert len(itens) > 0
    assert {i.refeicao for i in itens} == {"cafe_da_manha", "almoco", "jantar"}
    assert {i.data for i in itens} == {date(2026, 9, d) for d in range(14, 21)}


def test_extrair_itens_cardapio_almoco_tem_categoria_guarnicao():
    conteudo_pdf = FIXTURE_PDF.read_bytes()

    itens = extrair_itens_cardapio(conteudo_pdf)

    almoco_segunda = [i for i in itens if i.refeicao == "almoco" and i.data == date(2026, 9, 14)]
    assert any(i.categoria == "GUARNIÇÃO" for i in almoco_segunda)


def test_extrair_itens_cardapio_falha_com_pdf_sem_tabela():
    with pytest.raises(Exception):
        extrair_itens_cardapio(b"%PDF-1.4 nao e um cardapio de verdade")
