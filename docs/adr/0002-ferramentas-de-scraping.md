# ADR 0002 — Ferramentas de scraping por fonte

## Status
Aceito

## Contexto
As fontes têm naturezas diferentes. A consulta pública de turmas do SIGAA é uma aplicação JSF: a busca depende de postback e de um `ViewState` mantido na sessão, então o HTML só aparece depois de preencher e enviar o formulário. O site do RU publica o cardápio como PDF semanal, com link numa página HTML simples. A agenda de notícias e os editais são páginas HTML comuns.

## Decisão
- **SIGAA:** Playwright para navegar (preencher o formulário por unidade e reaproveitar a sessão), com espera entre unidades para não sobrecarregar o servidor. O HTML resultante é lido com BeautifulSoup.
- **RU:** `requests` para baixar a página e o PDF, BeautifulSoup para achar o link do PDF da semana e `pdfplumber` para ler as tabelas.
- **Eventos e editais (Release 2):** `requests` + BeautifulSoup, sem navegador.
- Em todas as fontes, o scraper só baixa o conteúdo e o parser só transforma em contrato Pydantic ([ARQUITETURA.md](../ARQUITETURA.md), camadas do backend).

## Alternativas descartadas
- **Requisição HTTP simples para o SIGAA:** não sustenta o postback e o `ViewState` do JSF.
- **Playwright para todas as fontes:** funcionaria, mas é mais pesado (navegador real) sem necessidade nas fontes HTML e PDF.

## Consequências
- A imagem Docker do backend precisa do Chromium do Playwright (`playwright install --with-deps chromium`), o que a deixa maior.
- O scraper do SIGAA é o mais lento e o mais frágil: mudanças no formulário quebram a navegação. O risco está no [relatório de risco](../fontes/relatorio-de-risco.md).
