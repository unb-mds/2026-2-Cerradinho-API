# RF17 · Calcular salas vazias por dia e horário

| Release | Responsável | Issue |
|---|---|---|
| R2 | Vitor | [#53](https://github.com/unb-mds/2026-2-Cerradinho-API/issues/53) |

**Critérios de aceitação**
- `GET /v1/salas/vazias?dia=segunda&horario=14:00` devolve as salas que não têm nenhuma turma cadastrada naquele dia/horário.
- Mudar a oferta de disciplinas (nova turma, turma removida) reflete automaticamente no resultado, sem reprocessamento manual.
- `GET /v1/salas/vazias?dia=segunda&horario=14:00&fim=15:50` devolve só as salas sem aula em todas as aulas que começam entre `horario` e `fim`.
- A tela de Salas Vazias mostra a semana inteira, de segunda a sábado, para um bloco de 2h escolhido entre 08:00, 10:00, 12:00, 14:00 e 16:00, só com as salas I1 a I10 e S1 a S10 da FCTE.

**Regra de negócio**
- "Vazia" significa só "sem aula cadastrada via RF01" — não reflete reserva informal, evento ou uso fora da grade de disciplinas. É uma leitura otimista, não uma garantia de disponibilidade real.
- `horario` é o início de uma aula ("HH:MM"), na grade do SIGAA derivada de turma real: manhã/tarde com aulas de 55 min, noite com aulas de 50 min (ex.: `"6T2345"` = sexta-feira 14:00 às 17:50; `"6N1234"` = sexta-feira 19:00 às 22:30). Dia ou horário fora dessa grade — sem turma possível — devolve todas as salas, em vez de erro.
- Um código de horário pode ter mais de um segmento dia+turno+aula colado com espaço, quando a turma tem aula em turnos diferentes (ex.: `"35M5 35T1"`); todos os segmentos contam pra ocupação, não só o primeiro.
- Turma com sala por dia (ver RF05) ocupa só a sala do dia certo — não todas as salas listadas em todos os dias (ver [ADR 0010](https://github.com/unb-mds/2026-2-Cerradinho-API/blob/dev/docs/adr/0010-sala-por-horario-nao-por-turma.md)).
- `fim` é opcional. Sem ele, vale só a aula que começa em `horario`. Com ele, o bloco das 12:00 às 13:50 cobre a M5 e a T1.
- Turma em sala combinada (`I9/I10`) ocupa cada sala do nome no mesmo prédio, e nome com detalhe (`S10 (120 VAGAS)`) ocupa a sala principal.
- O filtro das salas I e S da FCTE é do site. A API continua devolvendo todas as salas, porque o campo de local do SIGAA é texto livre e fora do Gama gera nomes que não são salas.

## Rastreabilidade

- **PRs:** [#149](https://github.com/unb-mds/2026-2-Cerradinho-API/pull/149), [#227](https://github.com/unb-mds/2026-2-Cerradinho-API/pull/227), [#230](https://github.com/unb-mds/2026-2-Cerradinho-API/pull/230), [#228](https://github.com/unb-mds/2026-2-Cerradinho-API/pull/228) (tela), [#238](https://github.com/unb-mds/2026-2-Cerradinho-API/pull/238) (horários noturnos nos filtros), [#256](https://github.com/unb-mds/2026-2-Cerradinho-API/pull/256) (blocos de 2h, `fim` e salas combinadas)
- **Testes:** [`tests/routers/test_salas_router.py`](https://github.com/unb-mds/2026-2-Cerradinho-API/blob/dev/backend/tests/routers/test_salas_router.py), [`tests/domain/test_disciplinas.py`](https://github.com/unb-mds/2026-2-Cerradinho-API/blob/dev/backend/tests/domain/test_disciplinas.py), [`tests/contract/test_openapi_contract.py`](https://github.com/unb-mds/2026-2-Cerradinho-API/blob/dev/backend/tests/contract/test_openapi_contract.py)
- **Decisões:** [ADR 0010](https://github.com/unb-mds/2026-2-Cerradinho-API/blob/dev/docs/adr/0010-sala-por-horario-nao-por-turma.md)
