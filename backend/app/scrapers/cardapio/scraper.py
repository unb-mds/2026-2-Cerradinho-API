"""Captura HTTP para o scraper de Cardápio (RF06/RF07): HTML da página de
listagem e download do PDF selecionado por parser.py.

O RU publica o PDF do Darcy Ribeiro em duas páginas, `cardapio/` e
`cardapio-refeitorio/`, e alterna qual delas atualiza (ver risco A2 em
docs/fontes/ru-cardapio.md). A que fica para trás continua respondendo 200
com HTML válido, só que com a semana antiga. Por isso o scraper consulta as
duas, na ordem de URLS_CARDAPIO, e usa a primeira que tiver o PDF da semana.
"""

import logging
import time

import requests

from app.core.exceptions import ErroFonteIndisponivel

logger = logging.getLogger(__name__)

URLS_CARDAPIO = ("https://ru.unb.br/cardapio/", "https://ru.unb.br/cardapio-refeitorio/")
HEADERS = {"User-Agent": "CerradinhoBot/1.0 (+https://github.com/unb-mds/2026-2-Cerradinho-API)"}
TENTATIVAS_DOWNLOAD = 3
ESPERA_ENTRE_TENTATIVAS = 2  # segundos; dobra a cada nova tentativa


def baixar_html(url: str, timeout: int = 10) -> str:
    """Faz o request da página de listagem e retorna o HTML como texto."""
    response = requests.get(url, headers=HEADERS, timeout=timeout)
    response.raise_for_status()
    return response.text


def baixar_pdf(url_pdf: str, timeout: int = 15) -> bytes:
    """Baixa o PDF da URL informada e valida que a resposta é mesmo um PDF
    (não uma página de erro disfarçada de 200 OK)."""
    ultimo_erro: Exception | None = None

    for tentativa in range(1, TENTATIVAS_DOWNLOAD + 1):
        try:
            response = requests.get(url_pdf, headers=HEADERS, timeout=timeout)
            response.raise_for_status()

            content_type = response.headers.get("Content-Type", "")
            if "application/pdf" not in content_type.lower():
                raise ValueError(
                    f"Resposta de {url_pdf} não é um PDF (Content-Type: {content_type!r}). "
                    "Provavelmente o link mudou ou o servidor retornou uma página de erro."
                )
            return response.content

        except (requests.RequestException, ValueError) as erro:
            ultimo_erro = erro
            logger.warning(
                "Tentativa %d/%d de baixar %s falhou: %s", tentativa, TENTATIVAS_DOWNLOAD, url_pdf, erro,
            )
            if tentativa < TENTATIVAS_DOWNLOAD:
                time.sleep(ESPERA_ENTRE_TENTATIVAS * tentativa)

    raise ErroFonteIndisponivel(
        f"Não foi possível baixar o PDF após {TENTATIVAS_DOWNLOAD} tentativas."
        ) from ultimo_erro
