"""Seleção do PDF da semana e extração do cardápio (RF06/RF07).

Descobertas da análise do PDF real (Darcy Ribeiro, semana de 14 a
20/9/2026), testadas com pdfplumber:

- extract_tables() com a estratégia PADRÃO (por linhas) funciona bem pra
  esse layout. strategy="text" embaralha colunas e cabeçalhos — não usar.
- Cada página tem várias tabelas "fantasma" (fragmentos do cabeçalho, tipo
  uma tabela só com "3ª FEIRA" e a data); a tabela de verdade é sempre a
  maior (mais linhas) — extrair_tabela_pagina cuida disso.
- Às vezes uma célula quebra em mais linhas visuais que as vizinhas (ex:
  "Carne de sol trinchada" / "com cebola roxa" em duas linhas), e o
  pdfplumber devolve isso como linhas extras com a coluna de categoria
  vazia. Sem tratar isso, o dado se perde silenciosamente (confirmado
  removendo o prato principal de segunda-feira do almoço) — normalizar_tabela
  agrupa essas linhas de volta ao bloco da categoria anterior.
- O número de colunas varia entre páginas (às vezes tem uma coluna fantasma
  vazia entre um dia e outro); por isso as colunas são mapeadas pelas datas
  do cabeçalho (regex), não por índice fixo.
- A refeição de cada página é identificada pelo conjunto de categorias que
  aparecem nela (só café da manhã tem "PANIFICAÇÃO"/"FRUTA"; só almoço tem
  "GUARNIÇÃO"; só jantar tem "SOPA"/"TORRADA"), em vez de assumir uma ordem
  fixa de páginas — evita erro silencioso se uma semana vier com menos
  páginas (feriado sem jantar) ou em ordem diferente.
- Os ícones de alérgeno (leite, soja, glúten etc.) são imagens embutidas no
  PDF, não texto, e não são capturados por extract_tables() (ver
  docs/estudos/fonte-ru-cardapio.md).
"""

from __future__ import annotations

import io
import logging
import re
from datetime import date
from urllib.parse import urljoin

import pdfplumber
from bs4 import BeautifulSoup

from app.schemas.cardapio import ItemCardapio, Refeicao

from .scraper import URL_CARDAPIO

logger = logging.getLogger(__name__)

# Categorias que só aparecem numa refeição específica, usadas para
# identificar a qual refeição uma página pertence (em vez de confiar na
# ordem das páginas no PDF).
ASSINATURAS_REFEICAO: dict[Refeicao, set[str]] = {
    "cafe_da_manha": {"PANIFICAÇÃO", "FRUTA"},
    "almoco": {"GUARNIÇÃO"},
    "jantar": {"SOPA", "TORRADA"},
}


def extrair_links_cardapio(html: str, url_base: str = URL_CARDAPIO, campus: str = "darcy") -> list[dict]:
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
    risco A2 em docs/estudos/fonte-ru-cardapio.md)."""
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


def _extrair_tabela_pagina(pagina) -> list[list]:
    """Extrai a tabela principal de uma página (descarta as tabelas fantasmas)."""
    tabelas = pagina.extract_tables()
    if not tabelas:
        raise ValueError("Nenhuma tabela encontrada na página.")
    return max(tabelas, key=len)


def _mapear_colunas_dos_dias(cabecalho: list) -> dict[int, date]:
    """Mapeia índice da coluna -> data, lendo a linha de cabeçalho."""
    mapa = {}
    for i, celula in enumerate(cabecalho):
        if celula:
            m = re.search(r"\d{1,2}/\d{1,2}/\d{4}", celula)
            if m:
                mapa[i] = _string_para_data(m.group())
    if not mapa:
        raise ValueError("Não foi possível identificar as colunas de dias no cabeçalho.")
    return mapa


def _categorias_da_tabela(tabela: list, primeira_col_dia: int) -> set[str]:
    """Coleta o conjunto de categorias (coluna antes dos dias) presentes na tabela."""
    categorias = set()
    for linha in tabela[1:]:
        celula_categoria = next((c for c in linha[:primeira_col_dia] if c), None)
        if celula_categoria:
            categorias.add(celula_categoria.replace("\n", " ").strip())
    return categorias


def _identificar_refeicao(categorias: set[str]) -> Refeicao:
    """Identifica a refeição pelas categorias encontradas na página."""
    for refeicao, chaves in ASSINATURAS_REFEICAO.items():
        if chaves & categorias:
            return refeicao
    raise ValueError(f"Não reconheci a refeição pelas categorias encontradas: {categorias}")


def _normalizar_tabela(tabela: list, refeicao: Refeicao, colunas_dias: dict[int, date]) -> list[ItemCardapio]:
    """Agrupa linhas em blocos por categoria (uma linha de categoria + suas
    linhas de continuação, quando uma célula quebrou em mais linhas que as
    vizinhas) e junta o texto de cada coluna dentro do bloco."""
    primeira_col_dia = min(colunas_dias)

    blocos: list[tuple[str, dict[int, list[str]]]] = []
    for linha in tabela[1:]:
        celula_categoria = next((c for c in linha[:primeira_col_dia] if c), None)
        if celula_categoria:
            categoria = celula_categoria.replace("\n", " ").strip()
            blocos.append((categoria, {idx: [] for idx in colunas_dias}))
        if not blocos:
            continue  # linha antes de qualquer categoria (não deveria acontecer)
        for idx in colunas_dias:
            texto = linha[idx]
            if texto:
                blocos[-1][1][idx].append(texto.replace("\n", " ").strip())

    itens = []
    for categoria, colunas in blocos:
        for idx, data_coluna in colunas_dias.items():
            texto_completo = " ".join(colunas[idx]).strip()
            if texto_completo:
                itens.append(
                    ItemCardapio(data=data_coluna, refeicao=refeicao, categoria=categoria, item=texto_completo)
                )
    return itens


def extrair_itens_cardapio(conteudo_pdf: bytes) -> list[ItemCardapio]:
    """Percorre as páginas do PDF (uma por refeição) e retorna todos os
    itens de cardápio já validados."""
    itens: list[ItemCardapio] = []
    refeicoes_encontradas: set[Refeicao] = set()

    with pdfplumber.open(io.BytesIO(conteudo_pdf)) as pdf:
        for num_pagina, pagina in enumerate(pdf.pages):
            tabela = _extrair_tabela_pagina(pagina)
            colunas_dias = _mapear_colunas_dos_dias(tabela[0])
            categorias = _categorias_da_tabela(tabela, min(colunas_dias))
            refeicao = _identificar_refeicao(categorias)

            if refeicao in refeicoes_encontradas:
                logger.warning(
                    "Refeição '%s' identificada em mais de uma página (página %d) — "
                    "pode haver duplicidade nos dados.", refeicao, num_pagina,
                )
            refeicoes_encontradas.add(refeicao)

            itens.extend(_normalizar_tabela(tabela, refeicao, colunas_dias))

    faltando = set(ASSINATURAS_REFEICAO) - refeicoes_encontradas
    if faltando:
        logger.warning(
            "Refeições não encontradas neste PDF: %s (pode ser feriado ou mudança de layout).",
            faltando,
        )

    if not itens:
        raise ValueError("Nenhum item extraído do PDF — verifique se o layout mudou.")

    return itens
