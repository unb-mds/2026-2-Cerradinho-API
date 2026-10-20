# RF17 · Calcular salas vazias por dia e horário

| Release | Responsável | Issue |
|---|---|---|
| R2 | Vitor | [#53](https://github.com/unb-mds/2026-2-Cerradinho-API/issues/53) |

**Critérios de aceitação**
- `GET /v1/salas/vazias?dia=segunda&horario=14:00` devolve as salas que não têm nenhuma turma cadastrada naquele dia/horário.
- Mudar a oferta de disciplinas (nova turma, turma removida) reflete automaticamente no resultado, sem reprocessamento manual.

**Regra de negócio**
- "Vazia" significa só "sem aula cadastrada via RF01" — não reflete reserva informal, evento ou uso fora da grade de disciplinas. É uma leitura otimista, não uma garantia de disponibilidade real.

## Rastreabilidade

- **PRs:** nenhum ainda.
- **Testes:** nenhum ainda.
