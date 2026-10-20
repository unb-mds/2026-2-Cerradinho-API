# RNF05 · Tratar falhas de scraping de forma resiliente

| Release | Responsável | Issue |
|---|---|---|
| R1 | João Paulo | [#70](https://github.com/unb-mds/2026-2-Cerradinho-API/issues/70) |

**Critérios de aceitação**
- Mudança no layout ou no fluxo de uma fonte externa derruba a raspagem daquela fonte com um erro explícito, sem gravar dado parcial/incorreto no banco.
- Sessão expirada do SIGAA é reconhecida e tratada com nova tentativa, não é interpretada como dado válido.

**Regra de negócio**
- Princípio geral: o scraper deve falhar alto e cedo. É preferível uma exceção explícita a um registro vazio ou incompleto persistido no banco — todo parser valida que encontrou o que esperava antes de gravar.

## Rastreabilidade

- **PRs:** nenhum ainda.
- **Testes:** [`tests/scrapers/test_cardapio_parser.py`](https://github.com/unb-mds/2026-2-Cerradinho-API/blob/dev/backend/tests/scrapers/test_cardapio_parser.py), [`tests/integration/test_pipeline_disciplinas_postgres.py`](https://github.com/unb-mds/2026-2-Cerradinho-API/blob/dev/backend/tests/integration/test_pipeline_disciplinas_postgres.py)
- **Observação:** Unidade do SIGAA que falha não derruba as outras, mas o log de falha não informa a fonte nem a unidade. Não há PR dedicado.
