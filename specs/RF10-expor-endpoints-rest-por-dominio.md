# RF10 · Expor endpoints REST por domínio

| Release | Responsável | Issue |
|---|---|---|
| R1 | Daniel | [#42](https://github.com/unb-mds/2026-2-Cerradinho-API/issues/42) |

**Critérios de aceitação**
- Cada domínio (disciplinas, professores, salas, cardápio) tem um endpoint `GET` próprio sob `/v1/`.
- Domínio sem dado nenhum retorna lista vazia (`[]`) com HTTP 200, nunca erro.
- `GET /v1/disciplinas` e `GET /v1/professores` aceitam paginação com `limite`/`offset`; quando usada (ou quando algum filtro é dado), o total depois do filtro vem no cabeçalho `X-Total-Count`. Sem nenhum parâmetro novo, o comportamento continua sendo devolver tudo, sem o cabeçalho — não quebra quem já consome essas rotas.

**Regra de negócio**
- Rota só lê e serve dado já persistido — nenhuma lógica de negócio (normalização, cálculo) roda no router; isso fica na camada de domínio (`app/domain/`).
- `X-Total-Count` só é calculado quando algum parâmetro de paginação/filtro é usado — a listagem completa (cacheada) não paga o custo de uma contagem extra pra um cabeçalho que ninguém pediu.

## Rastreabilidade

- **PRs:** [#108](https://github.com/unb-mds/2026-2-Cerradinho-API/pull/108), [#119](https://github.com/unb-mds/2026-2-Cerradinho-API/pull/119)
- **Testes:** [`tests/routers/test_disciplinas_router.py`](https://github.com/unb-mds/2026-2-Cerradinho-API/blob/dev/backend/tests/routers/test_disciplinas_router.py), [`tests/routers/test_professores_router.py`](https://github.com/unb-mds/2026-2-Cerradinho-API/blob/dev/backend/tests/routers/test_professores_router.py), [`tests/routers/test_salas_router.py`](https://github.com/unb-mds/2026-2-Cerradinho-API/blob/dev/backend/tests/routers/test_salas_router.py), [`tests/routers/test_cardapio_router.py`](https://github.com/unb-mds/2026-2-Cerradinho-API/blob/dev/backend/tests/routers/test_cardapio_router.py), [`tests/contract/test_openapi_contract.py`](https://github.com/unb-mds/2026-2-Cerradinho-API/blob/dev/backend/tests/contract/test_openapi_contract.py)
