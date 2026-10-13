# RF06 · Capturar cardápio diário do RU

| Release | Responsável | Issue | Situação |
|---|---|---|---|
| R1 | Gabriel | [#40](https://github.com/unb-mds/2026-2-Cerradinho-API/issues/40) | Parcial |

**Critérios de aceitação**
- O scraper baixa o PDF da semana corrente do campus configurado e extrai os itens por dia e por refeição (café, almoço, jantar).
- Célula do PDF que vale pra semana inteira (ex: "Leite integral OU Bebida de soja") é aplicada a todos os dias daquela semana, não só ao primeiro.

**Regra de negócio**
- A extração é posicional (coordenadas das células do PDF), não por leitura linear de texto — uma extração sequencial embaralha qual prato pertence a qual dia, porque o layout usa células mescladas.
- A fonte oficial documentada (`ru.unb.br/cardapio`) está desatualizada; a fonte usada de fato é `ru.unb.br/cardapio-refeitorio`.

## Rastreabilidade

- **PRs:** [#92](https://github.com/unb-mds/2026-2-Cerradinho-API/pull/92)
- **Testes:** [`tests/scrapers/test_cardapio_parser.py`](https://github.com/unb-mds/2026-2-Cerradinho-API/blob/dev/backend/tests/scrapers/test_cardapio_parser.py), [`tests/domain/test_cardapio.py`](https://github.com/unb-mds/2026-2-Cerradinho-API/blob/dev/backend/tests/domain/test_cardapio.py)
- **Decisões:** [ADR 0002](https://github.com/unb-mds/2026-2-Cerradinho-API/blob/dev/docs/adr/0002-ferramentas-de-scraping.md)
- **Observação:** O parser falha com os layouts de PDF publicados a partir de 21/09 (#103).
