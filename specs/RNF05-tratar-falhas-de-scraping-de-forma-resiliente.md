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

- **PRs:** [#248](https://github.com/unb-mds/2026-2-Cerradinho-API/pull/248) (sabotagem dos scrapers)
- **Testes:** [`tests/scrapers/test_cardapio_parser.py`](https://github.com/unb-mds/2026-2-Cerradinho-API/blob/dev/backend/tests/scrapers/test_cardapio_parser.py), [`tests/integration/test_pipeline_disciplinas_postgres.py`](https://github.com/unb-mds/2026-2-Cerradinho-API/blob/dev/backend/tests/integration/test_pipeline_disciplinas_postgres.py), [`tests/sabotagem/`](https://github.com/unb-mds/2026-2-Cerradinho-API/tree/dev/backend/tests/sabotagem)
- **Observação:** Unidade do SIGAA que falha não derruba as outras. Os testes de sabotagem do RNF09 mostraram que o SIGAA fora do ar ia para o log como falha interna, e que a sessão expirada em todas as unidades ou um layout novo terminavam em "sucesso" com zero turmas. Desde o commit `f5a8fe1`, o SIGAA fora do ar e a sessão expirada em todas as unidades viram falha da fonte (`ErroFonteIndisponivel`). O formulário sem a lista de unidades e nenhuma turma em nenhuma unidade viram `ValueError`. O log ainda não informa qual unidade falhou.
