"""Ponto de entrada público do scraper de Cardápio (RF06/RF07).

Orquestra scraper.py (captura HTTP) + parser.py (seleção do PDF da semana e
extração via pdfplumber, validação via Pydantic), expondo só o resultado
já validado. Quem chama isso daqui (uma task do Celery, por exemplo) não
precisa saber que por baixo tem requests/pdfplumber — só recebe
list[ItemCardapio].
"""

import logging
from datetime import date

import requests

from app.core.exceptions import ErroFonteIndisponivel
from app.schemas.cardapio import ItemCardapio

from .parser import encontrar_pdf_da_semana, extrair_itens_cardapio, extrair_links_cardapio
from .scraper import URLS_CARDAPIO, baixar_html, baixar_pdf

__all__ = ["raspar_cardapio"]

logger = logging.getLogger(__name__)


def _url_do_pdf_da_semana(referencia: date | None) -> str:
    """Procura o PDF da semana em cada página de URLS_CARDAPIO, na ordem, e
    devolve o primeiro encontrado. Uma página fora do ar não impede a
    consulta à outra."""
    for url in URLS_CARDAPIO:
        try:
            html = baixar_html(url)
        except requests.RequestException as erro:
            logger.warning("Página de cardápio %s indisponível: %s", url, erro)
            continue

        pdf_da_semana = encontrar_pdf_da_semana(extrair_links_cardapio(html, url_base=url), referencia)
        if pdf_da_semana:
            return pdf_da_semana

    raise ErroFonteIndisponivel(
        f"Nenhum PDF de cardápio da semana atual em {', '.join(URLS_CARDAPIO)}."
    )


def raspar_cardapio(referencia: date | None = None) -> list[ItemCardapio]:
    """Captura e valida o cardápio da semana que contém `referencia` (por
    padrão, hoje). Este é o contrato público do módulo: entrada = data de
    referência opcional, saída = list[ItemCardapio].

    Levanta ErroFonteIndisponivel se nenhuma página tiver o PDF da semana.
    Nunca devolve o cardápio de uma semana antiga (risco A2 em
    docs/fontes/ru-cardapio.md).
    """
    conteudo_pdf = baixar_pdf(_url_do_pdf_da_semana(referencia))
    return extrair_itens_cardapio(conteudo_pdf)
