# RF07 · Manter histórico de cardápios

| Release | Responsável | Issue |
|---|---|---|
| R1 | Gabriel | [#41](https://github.com/unb-mds/2026-2-Cerradinho-API/issues/41) |

**Critérios de aceitação**
- Cardápios de semanas anteriores continuam consultáveis depois que uma semana nova é capturada (não é sobrescrita).
- Reprocessar a mesma semana atualiza os itens daquela semana em vez de duplicar.

**Regra de negócio**
- O histórico é por data — a chave de um item de cardápio é (data, refeição, categoria), não (semana, campus).

## Rastreabilidade

- **PRs:** [#92](https://github.com/unb-mds/2026-2-Cerradinho-API/pull/92), [#108](https://github.com/unb-mds/2026-2-Cerradinho-API/pull/108), [#145](https://github.com/unb-mds/2026-2-Cerradinho-API/pull/145)
- **Testes:** [`tests/domain/test_cardapio.py`](https://github.com/unb-mds/2026-2-Cerradinho-API/blob/dev/backend/tests/domain/test_cardapio.py), [`tests/routers/test_cardapio_router.py`](https://github.com/unb-mds/2026-2-Cerradinho-API/blob/dev/backend/tests/routers/test_cardapio_router.py), [`tests/test_models.py`](https://github.com/unb-mds/2026-2-Cerradinho-API/blob/dev/backend/tests/test_models.py)
- **Observação:** A consulta de semanas passadas funciona. Em produção o histórico acumula desde 04/11 com a coleta diária (#98), e as semanas de 02/11 e 09/11 aparecem completas em `GET /v1/cardapio/semana` (verificado em 17/11/2026).
