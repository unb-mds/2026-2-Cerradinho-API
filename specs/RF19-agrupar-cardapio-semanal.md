# RF19 · Agrupar cardápio semanal

| Release | Responsável | Issue |
|---|---|---|
| R2 | Gabriel | [#51](https://github.com/unb-mds/2026-2-Cerradinho-API/issues/51) |

**Critérios de aceitação**
- `GET /v1/cardapio/semana?data_inicio=...` devolve os 7 dias a partir da data informada; sem `data_inicio`, devolve de hoje até hoje+6 dias.
- Dia sem cardápio publicado aparece como ausente/vazio no agrupamento, não interrompe a resposta dos outros dias.

**Regra de negócio**
- O agrupamento é só uma leitura em janela de 7 dias sobre o histórico do RF07 — não dispara nova raspagem.

## Rastreabilidade

- **PRs:** [#227](https://github.com/unb-mds/2026-2-Cerradinho-API/pull/227)
- **Testes:** [`tests/routers/test_cardapio_router.py`](https://github.com/unb-mds/2026-2-Cerradinho-API/blob/dev/backend/tests/routers/test_cardapio_router.py), [`tests/contract/test_openapi_contract.py`](https://github.com/unb-mds/2026-2-Cerradinho-API/blob/dev/backend/tests/contract/test_openapi_contract.py)
- **Observação:** A resposta tem `data_inicio`, `data_fim` e a lista `dias`, sempre com 7 dias. Cada dia traz `cafe_da_manha`, `almoco` e `jantar` com os itens (`categoria` e `item`) e o campo `publicado`, que vem falso quando não há cardápio coletado para o dia. Antes o endpoint devolvia uma lista solta de itens e o dia sem cardápio sumia da resposta.
