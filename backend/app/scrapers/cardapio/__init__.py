"""Ponto de entrada público do scraper de Cardápio (RF06/RF07).

Orquestra scraper.py (captura HTTP) + parser.py (seleção do PDF da semana e
extração via pdfplumber, validação via Pydantic), expondo só o resultado
já validado. Quem chama isso daqui (uma task do Celery, por exemplo) não
precisa saber que por baixo tem requests/pdfplumber — só recebe
list[ItemCardapio].
"""

from datetime import date

from app.schemas.cardapio import ItemCardapio

from .parser import encontrar_pdf_da_semana, extrair_itens_cardapio, extrair_links_cardapio
from .scraper import baixar_html, baixar_pdf

__all__ = ["raspar_cardapio"]


def raspar_cardapio(referencia: date | None = None) -> list[ItemCardapio]:
    """Captura e valida o cardápio da semana que contém `referencia` (por
    padrão, hoje). Este é o contrato público do módulo: entrada = data de
    referência opcional, saída = list[ItemCardapio].

    Levanta RuntimeError se nenhum PDF for encontrado para a semana — nunca
    deve devolver silenciosamente o cardápio de uma semana antiga (risco A2
    em docs/estudos/fonte-ru-cardapio.md).
    """
    html = baixar_html()
    links = extrair_links_cardapio(html)
    if not links:
        raise RuntimeError("Nenhum link de cardápio encontrado na página do RU.")

    pdf_da_semana = encontrar_pdf_da_semana(links, referencia)
    if not pdf_da_semana:
        raise RuntimeError("Nenhum PDF de cardápio encontrado para a semana atual.")

    conteudo_pdf = baixar_pdf(pdf_da_semana)
    return extrair_itens_cardapio(conteudo_pdf)
