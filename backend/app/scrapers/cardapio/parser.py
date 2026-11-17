"""selecao do pdf da semana e extracao do cardapio rf06 rf07

leitura pela posicao das datas na pagina ver specs/RF06
"""

from __future__ import annotations

import io
import logging
import re
from collections import defaultdict
from datetime import date
from typing import NamedTuple
from urllib.parse import urljoin

import pdfplumber
from bs4 import BeautifulSoup

from app.schemas.cardapio import ItemCardapio, Refeicao

from .scraper import URLS_CARDAPIO

logger = logging.getLogger(__name__)

# Categorias que só aparecem numa refeição específica, usadas para
# identificar a qual refeição uma página pertence (em vez de confiar na
# ordem das páginas no PDF).
ASSINATURAS_REFEICAO: dict[Refeicao, set[str]] = {
    "cafe_da_manha": {"PANIFICAÇÃO", "FRUTA"},
    "almoco": {"GUARNIÇÃO"},
    "jantar": {"SOPA", "TORRADA"},
}

RE_DATA = re.compile(r"\d{1,2}/\d{1,2}/\d{4}")
TITULO_COLUNA_CATEGORIA = "COMPOSIÇÃO"
TOLERANCIA_Y = 1  # folga entre bordas de celulas vizinhas


class Celula(NamedTuple):
    x0: float
    top: float
    x1: float
    bottom: float
    texto: str


def extrair_links_cardapio(html: str, url_base: str = URLS_CARDAPIO[0], campus: str = "darcy") -> list[dict]:
    """Percorre o HTML da página de listagem e retorna uma lista de dicts
    com o texto do link (ex: "ISM – 7/9/2026 A 13/9/2026") e a URL absoluta
    do PDF correspondente ao `campus` informado.

    O filtro de campus é aplicado tanto na URL quanto no texto do link,
    porque o nome do arquivo pode mudar de convenção sem aviso, mas o texto
    do link tende a ser mais estável. Por padrão filtra só Darcy Ribeiro —
    os outros campi publicados (Ceilândia, Gama, Planaltina, Fazenda Água
    Limpa) ficam para um trabalho futuro de multi-campus.
    """
    soup = BeautifulSoup(html, "html.parser")
    links_cardapio = []

    for link in soup.find_all("a", href=True):
        texto = link.get_text(strip=True)
        href_absoluto = urljoin(url_base, link["href"])

        eh_pdf = href_absoluto.lower().endswith(".pdf")
        eh_do_campus = campus in href_absoluto.lower() or campus in texto.lower()

        if eh_pdf and eh_do_campus:
            links_cardapio.append({"texto": texto, "url": href_absoluto})

    if not links_cardapio:
        logger.warning(
            "Nenhum link de cardápio encontrado em %s para o campus '%s' — "
            "o layout do site pode ter mudado.", url_base, campus,
        )

    return links_cardapio


def _extrai_intervalo(texto: str) -> tuple[date | None, date | None]:
    """Extrai as duas datas (início, fim) do texto do link, ex:
    "ISM – 7/9/2026 A 13/9/2026"."""
    datas_encontradas = re.findall(r"(\d{1,2}/\d{1,2}/\d{4})", texto)
    if len(datas_encontradas) != 2:
        return None, None

    inicio, fim = (_string_para_data(d) for d in datas_encontradas)
    return inicio, fim


def _string_para_data(data_str: str) -> date:
    dia, mes, ano = (int(parte) for parte in data_str.split("/"))
    return date(ano, mes, dia)


def encontrar_pdf_da_semana(links_cardapio: list[dict], referencia: date | None = None) -> str | None:
    """Retorna a URL do PDF cujo intervalo de datas contém `referencia`
    (por padrão, hoje). Retorna None se nenhum PDF corresponder — quem
    chama isso não deve persistir um cardápio de uma semana antiga (ver
    risco A2 em docs/fontes/ru-cardapio.md)."""
    referencia = referencia or date.today()

    for item in links_cardapio:
        inicio, fim = _extrai_intervalo(item["texto"])
        if inicio and fim and inicio <= referencia <= fim:
            return item["url"]

    logger.warning(
        "Nenhum PDF encontrado para a semana de %s entre %d link(s) disponíveis.",
        referencia, len(links_cardapio),
    )
    return None


def _texto_da_celula(pagina, bbox: tuple[float, float, float, float]) -> str:
    # caracteres com o centro dentro da celula
    x0, top, x1, bottom = bbox

    def dentro(obj) -> bool:
        if obj.get("object_type") != "char":
            return False
        cx = (obj["x0"] + obj["x1"]) / 2
        cy = (obj["top"] + obj["bottom"]) / 2
        return x0 <= cx <= x1 and top <= cy <= bottom

    return " ".join((pagina.filter(dentro).extract_text() or "").split())


def _posicoes_das_datas(palavras: list[dict]) -> tuple[list[tuple[float, date]], float]:
    # datas ordenadas por x e o fim do cabecalho
    datas: dict[date, tuple[float, float]] = {}
    for palavra in palavras:
        # desde 16/11 a data vem entre parenteses
        texto = palavra["text"].strip("()")
        if RE_DATA.fullmatch(texto):
            centro_x = (palavra["x0"] + palavra["x1"]) / 2
            datas.setdefault(_string_para_data(texto), (centro_x, palavra["bottom"]))

    if not datas:
        raise ValueError("Não foi possível identificar as datas dos dias no cabeçalho.")

    colunas = sorted((x, data_dia) for data_dia, (x, _) in datas.items())
    fim_cabecalho = max(bottom for _, bottom in datas.values())
    return colunas, fim_cabecalho


def _x_da_coluna_de_categoria(palavras: list[dict]) -> float:
    # x da coluna de categorias
    for palavra in palavras:
        if palavra["text"] == TITULO_COLUNA_CATEGORIA:
            return (palavra["x0"] + palavra["x1"]) / 2
    raise ValueError(f"Coluna '{TITULO_COLUNA_CATEGORIA}' não encontrada na página.")


def _celulas_do_corpo(pagina, fim_cabecalho: float) -> list[Celula]:
    # celulas abaixo do cabecalho de todas as tabelas
    bboxes = {bbox for tabela in pagina.find_tables() for bbox in tabela.cells}
    if not bboxes:
        raise ValueError("Nenhuma tabela encontrada na página.")

    celulas = []
    for bbox in bboxes:
        if (bbox[1] + bbox[3]) / 2 < fim_cabecalho:
            continue
        texto = _texto_da_celula(pagina, bbox)
        if texto and texto != TITULO_COLUNA_CATEGORIA and not RE_DATA.search(texto):
            celulas.append(Celula(*bbox, texto))
    return celulas


def _identificar_refeicao(categorias: set[str]) -> Refeicao:
    """Identifica a refeição pelas categorias encontradas na página."""
    for refeicao, chaves in ASSINATURAS_REFEICAO.items():
        if chaves & categorias:
            return refeicao
    raise ValueError(f"Não reconheci a refeição pelas categorias encontradas: {categorias}")


def _categoria_na_altura(categorias: list[Celula], top: float) -> str | None:
    for categoria in categorias:
        if categoria.top - TOLERANCIA_Y <= top + TOLERANCIA_Y <= categoria.bottom:
            return categoria.texto
    return None


def _extrair_itens_pagina(pagina) -> tuple[Refeicao, list[ItemCardapio]]:
    # uma pagina por refeicao na ordem do pdf
    palavras = pagina.extract_words()
    colunas_dias, fim_cabecalho = _posicoes_das_datas(palavras)
    x_categoria = _x_da_coluna_de_categoria(palavras)
    celulas = _celulas_do_corpo(pagina, fim_cabecalho)

    categorias = sorted((c for c in celulas if c.x0 <= x_categoria <= c.x1), key=lambda c: c.top)
    refeicao = _identificar_refeicao({c.texto for c in categorias})

    textos: dict[tuple[str, date], list[str]] = defaultdict(list)
    for celula in sorted((c for c in celulas if c.x0 > x_categoria), key=lambda c: (c.top, c.x0)):
        categoria = _categoria_na_altura(categorias, celula.top)
        dias = [data_dia for x, data_dia in colunas_dias if celula.x0 <= x <= celula.x1]
        if categoria is None or not dias:
            logger.warning("Texto sem categoria ou dia na página de %s, ignorado: %r", refeicao, celula.texto)
            continue
        for data_dia in dias:
            textos[(categoria, data_dia)].append(celula.texto)

    itens = [
        ItemCardapio(data=data_dia, refeicao=refeicao, categoria=categoria.texto, item=" ".join(partes))
        for categoria in categorias
        for _, data_dia in colunas_dias
        if (partes := textos.get((categoria.texto, data_dia)))
    ]
    return refeicao, itens


def extrair_itens_cardapio(conteudo_pdf: bytes) -> list[ItemCardapio]:
    """Percorre as páginas do PDF (uma por refeição) e retorna todos os
    itens de cardápio já validados."""
    itens: list[ItemCardapio] = []
    refeicoes_encontradas: set[Refeicao] = set()

    with pdfplumber.open(io.BytesIO(conteudo_pdf)) as pdf:
        for num_pagina, pagina in enumerate(pdf.pages):
            refeicao, itens_pagina = _extrair_itens_pagina(pagina)

            if refeicao in refeicoes_encontradas:
                logger.warning(
                    "Refeição '%s' identificada em mais de uma página (página %d) — "
                    "pode haver duplicidade nos dados.", refeicao, num_pagina,
                )
            refeicoes_encontradas.add(refeicao)
            itens.extend(itens_pagina)

    faltando = set(ASSINATURAS_REFEICAO) - refeicoes_encontradas
    if faltando:
        logger.warning(
            "Refeições não encontradas neste PDF: %s (pode ser feriado ou mudança de layout).",
            faltando,
        )

    if not itens:
        raise ValueError("Nenhum item extraído do PDF — verifique se o layout mudou.")

    return itens
