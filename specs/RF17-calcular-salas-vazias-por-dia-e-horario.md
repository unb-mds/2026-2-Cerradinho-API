# RF17 · Calcular salas vazias por dia e horário

| Release | Responsável | Issue |
|---|---|---|
| R2 | Vitor | [#53](https://github.com/unb-mds/2026-2-Cerradinho-API/issues/53) |

**Critérios de aceitação**
- `GET /v1/salas/vazias?dia=segunda&horario=14:00` devolve as salas que não têm nenhuma turma cadastrada naquele dia/horário.
- Mudar a oferta de disciplinas (nova turma, turma removida) reflete automaticamente no resultado, sem reprocessamento manual.

**Regra de negócio**
- "Vazia" significa só "sem aula cadastrada via RF01" — não reflete reserva informal, evento ou uso fora da grade de disciplinas. É uma leitura otimista, não uma garantia de disponibilidade real.
- `horario` é o início de uma aula ("HH:MM"), na grade de 55 minutos do SIGAA derivada das descrições reais de horário (ex.: `"6T2345"` = sexta-feira 14:00 às 17:50). Dia ou horário fora dessa grade — sem turma possível — devolve todas as salas, em vez de erro.

## Rastreabilidade

- **PRs:** nenhum ainda.
- **Testes:** [`tests/routers/test_salas_router.py`](https://github.com/unb-mds/2026-2-Cerradinho-API/blob/dev/backend/tests/routers/test_salas_router.py)
