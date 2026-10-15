from datetime import date, timedelta
from pathlib import Path

import pytest

from app.scrapers.cardapio.parser import encontrar_pdf_da_semana, extrair_itens_cardapio, extrair_links_cardapio

FIXTURES = Path(__file__).parent / "fixtures"

# Um PDF real por semana, cada um com a tabela montada de um jeito
# (ver a docstring de app/scrapers/cardapio/parser.py). A data é a
# segunda-feira da semana.
SEMANAS = [date(2026, 9, 14), date(2026, 9, 21), date(2026, 9, 28), date(2026, 10, 5), date(2026, 10, 12)]


def _itens_da_semana(segunda: date):
    return extrair_itens_cardapio((FIXTURES / f"cardapio_darcy_{segunda.isoformat()}.pdf").read_bytes())


def _item(itens, data_dia: date, refeicao: str, categoria: str) -> str | None:
    return next((i.item for i in itens if (i.data, i.refeicao, i.categoria) == (data_dia, refeicao, categoria)), None)

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


@pytest.mark.parametrize("segunda", SEMANAS, ids=str)
def test_extrair_itens_cardapio_le_as_tres_refeicoes_nos_sete_dias(segunda):
    itens = _itens_da_semana(segunda)

    assert {i.data for i in itens} == {segunda + timedelta(days=n) for n in range(7)}
    for refeicao in ("cafe_da_manha", "almoco", "jantar"):
        dias_com_prato = {i.data for i in itens if i.refeicao == refeicao and i.categoria == "PRATO PRINCIPAL PADRÃO"}
        dias_com_fruta = {i.data for i in itens if i.refeicao == refeicao and i.categoria == "FRUTA"}
        assert len(dias_com_prato | dias_com_fruta) == 7, refeicao


@pytest.mark.parametrize(
    ("segunda", "refeicao", "categoria", "esperado"),
    [
        # dia e data na mesma célula; célula quebrada em duas linhas visuais
        (date(2026, 9, 14), "almoco", "PRATO PRINCIPAL PADRÃO", "Carne de sol trinchada com cebola roxa"),
        # letra que passa da borda da célula
        (date(2026, 9, 14), "jantar", "MOLHO PARA SALADA", "Rosé / Limão"),
        # data numa linha separada e prato uma coluna à esquerda da data
        (date(2026, 9, 21), "almoco", "SALADA 1", "Repolho roxo"),
        (date(2026, 9, 21), "jantar", "PRATO PRINCIPAL PADRÃO", "Bife de panela"),
        # datas espalhadas em linhas diferentes da mesma página
        (date(2026, 9, 28), "almoco", "PRATO PRINCIPAL PADRÃO", "Carne ao molho"),
        (date(2026, 10, 5), "almoco", "PRATO PRINCIPAL PADRÃO", "Frango assado com manjericão"),
        (date(2026, 10, 12), "jantar", "PRATO PRINCIPAL PADRÃO", "Suíno ao molho barbecue de figo"),
    ],
)
def test_extrair_itens_cardapio_atribui_o_prato_ao_dia_e_categoria_certos(segunda, refeicao, categoria, esperado):
    itens = _itens_da_semana(segunda)

    assert _item(itens, segunda, refeicao, categoria) == esperado


def test_extrair_itens_cardapio_atribui_cada_dia_na_coluna_certa():
    itens = _itens_da_semana(date(2026, 9, 28))

    assert _item(itens, date(2026, 9, 29), "almoco", "PRATO PRINCIPAL PADRÃO") == "Frango assado"
    assert _item(itens, date(2026, 9, 29), "almoco", "SALADA 1") == "Mix de folhas"


@pytest.mark.parametrize("segunda", SEMANAS, ids=str)
def test_extrair_itens_cardapio_aplica_celula_da_semana_inteira_a_todos_os_dias(segunda):
    itens = _itens_da_semana(segunda)

    bebidas = {i.data: i.item for i in itens if i.refeicao == "cafe_da_manha" and i.categoria == "BEBIDAS"}
    assert len(bebidas) == 7
    assert all("leite integral" in texto.lower() and "café" in texto.lower() for texto in bebidas.values())


def test_extrair_itens_cardapio_almoco_tem_categoria_guarnicao():
    itens = _itens_da_semana(date(2026, 9, 14))

    almoco_segunda = [i for i in itens if i.refeicao == "almoco" and i.data == date(2026, 9, 14)]
    assert any(i.categoria == "GUARNIÇÃO" for i in almoco_segunda)


def test_extrair_itens_cardapio_falha_com_pdf_sem_tabela():
    with pytest.raises(Exception):
        extrair_itens_cardapio(b"%PDF-1.4 nao e um cardapio de verdade")
