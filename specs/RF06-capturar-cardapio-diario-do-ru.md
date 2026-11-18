# RF06 · Capturar cardápio diário do RU

| Release | Responsável | Issue |
|---|---|---|
| R1 | Gabriel | [#40](https://github.com/unb-mds/2026-2-Cerradinho-API/issues/40) |

**Critérios de aceitação**
- O scraper baixa o PDF da semana corrente do campus configurado e extrai os itens por dia e por refeição (café, almoço, jantar).
- Célula do PDF que vale pra semana inteira (ex: "Leite integral OU Bebida de soja") é aplicada a todos os dias daquela semana, não só ao primeiro.

**Regra de negócio**
- A extração é posicional (coordenadas das células do PDF), não por leitura linear de texto — uma extração sequencial embaralha qual prato pertence a qual dia, porque o layout usa células mescladas.
- O layout da tabela muda de uma semana para outra. Já apareceram o dia e a data na mesma célula ou em linhas separadas, cada data numa linha diferente da mesma página, colunas fantasma entre os dias com o prato à esquerda da coluna da data e a data entre parênteses (desde 16/11). Por isso a leitura não depende de qual linha ou coluna da tabela tem cada coisa.
- O dia de cada célula vem da posição horizontal das datas no cabeçalho. A data é procurada dentro de cada palavra, então ela é reconhecida mesmo colada em outro texto, como "(16/11/2026)" ou "FEIRA(16/11/2026)". A célula pertence a todos os dias cuja data cai dentro da sua largura, e é assim que uma célula mesclada vale para todos os dias que ela cobre.
- A categoria de um prato é a célula da coluna "COMPOSIÇÃO" que cobre a altura dele. Uma categoria que ocupa várias linhas visuais (BEBIDAS com leite e café, por exemplo) junta todo o texto dela.
- Um caractere pertence à célula quando o seu centro está dentro dela, porque uma letra pode passar um pouco da borda ("Rosé" virava "osé" quando se exigia o caractere inteiro dentro da célula).
- As células vêm de todas as tabelas da página, porque o pdfplumber às vezes quebra o cabeçalho em tabelas menores.
- Cada página do PDF é uma refeição, identificada pelas categorias que só ela tem (PANIFICAÇÃO e FRUTA no café da manhã, GUARNIÇÃO no almoço, SOPA e TORRADA no jantar), e não pela ordem das páginas. Assim uma semana com menos páginas, como um feriado sem jantar, ou com outra ordem não gera erro silencioso.
- Os ícones de alérgeno são imagens dentro do PDF, não texto, e não são capturados (ver [`docs/fontes/ru-cardapio.md`](https://github.com/unb-mds/2026-2-Cerradinho-API/blob/dev/docs/fontes/ru-cardapio.md)).
- O PDF do Darcy Ribeiro sai em duas páginas (`ru.unb.br/cardapio` e `ru.unb.br/cardapio-refeitorio`) e o RU alterna qual delas atualiza. O scraper consulta as duas e usa a primeira que tiver a semana atual. Se nenhuma tiver, a coleta falha em vez de gravar uma semana antiga.

## Rastreabilidade

- **PRs:** [#92](https://github.com/unb-mds/2026-2-Cerradinho-API/pull/92), [#145](https://github.com/unb-mds/2026-2-Cerradinho-API/pull/145), [#227](https://github.com/unb-mds/2026-2-Cerradinho-API/pull/227)
- **Testes:** [`tests/scrapers/test_cardapio_parser.py`](https://github.com/unb-mds/2026-2-Cerradinho-API/blob/dev/backend/tests/scrapers/test_cardapio_parser.py), [`tests/scrapers/test_cardapio_scraper.py`](https://github.com/unb-mds/2026-2-Cerradinho-API/blob/dev/backend/tests/scrapers/test_cardapio_scraper.py), [`tests/domain/test_cardapio.py`](https://github.com/unb-mds/2026-2-Cerradinho-API/blob/dev/backend/tests/domain/test_cardapio.py)
- **Decisões:** [ADR 0002](https://github.com/unb-mds/2026-2-Cerradinho-API/blob/dev/docs/adr/0002-ferramentas-de-scraping.md)
- **Observação:** O RU monta a tabela do PDF de um jeito diferente a cada semana. Os testes rodam com seis PDFs reais (semanas de 14/09 a 12/10 e de 16/11), cada um com um layout, e o parser lê pela posição das datas na página em vez de pela linha ou coluna da tabela (#103). Na semana de 16/11 o RU passou a escrever a data entre parênteses, e a coleta de 16/11 falhou em produção até o parser aceitar esse formato.
