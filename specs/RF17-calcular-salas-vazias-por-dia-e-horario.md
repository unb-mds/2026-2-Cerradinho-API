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
- Um código de horário pode ter mais de um segmento dia+turno+aula colado com espaço, quando a turma tem aula em turnos diferentes (ex.: `"35M5 35T1"`); todos os segmentos contam pra ocupação, não só o primeiro.
- Turma com sala por dia (ver RF05) ocupa só a sala do dia certo — não todas as salas listadas em todos os dias (ver [ADR 0010](https://github.com/unb-mds/2026-2-Cerradinho-API/blob/dev/docs/adr/0010-sala-por-horario-nao-por-turma.md)).

## Rastreabilidade

- **PRs:** [#230](https://github.com/unb-mds/2026-2-Cerradinho-API/pull/230)
- **Testes:** [`tests/routers/test_salas_router.py`](https://github.com/unb-mds/2026-2-Cerradinho-API/blob/dev/backend/tests/routers/test_salas_router.py), [`tests/domain/test_disciplinas.py`](https://github.com/unb-mds/2026-2-Cerradinho-API/blob/dev/backend/tests/domain/test_disciplinas.py), [`tests/contract/test_openapi_contract.py`](https://github.com/unb-mds/2026-2-Cerradinho-API/blob/dev/backend/tests/contract/test_openapi_contract.py)
- **Decisões:** [ADR 0010](https://github.com/unb-mds/2026-2-Cerradinho-API/blob/dev/docs/adr/0010-sala-por-horario-nao-por-turma.md)
