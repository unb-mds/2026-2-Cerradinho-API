# RF20 · Resumir contagens agregadas

| Release | Responsável | Issue |
|---|---|---|
| R2 | Vitor | [#263](https://github.com/unb-mds/2026-2-Cerradinho-API/issues/263) |

**Critérios de aceitação**
- `GET /v1/resumo` devolve o total de turmas, disciplinas, professores e salas, sem a lista de cada um.

**Regra de negócio**
- É só uma contagem de RF01/RF04/RF05 — não há dado novo nenhum, só agregação do que já está gravado.
- Motivado pelo Daniel: `GET /v1/disciplinas` devolve todas as turmas de uma vez (~2,3 MB de JSON, 6500+ turmas), e um dashboard que só precisa mostrar um número não deveria baixar a lista inteira pra isso.

## Rastreabilidade

- **PRs:** [#241](https://github.com/unb-mds/2026-2-Cerradinho-API/pull/241)
- **Testes:** [`tests/routers/test_resumo_router.py`](https://github.com/unb-mds/2026-2-Cerradinho-API/blob/dev/backend/tests/routers/test_resumo_router.py)
