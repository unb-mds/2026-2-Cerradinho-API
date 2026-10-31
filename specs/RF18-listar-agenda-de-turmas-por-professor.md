# RF18 · Listar agenda de turmas por professor

| Release | Responsável | Issue |
|---|---|---|
| R2 | Vitor | [#50](https://github.com/unb-mds/2026-2-Cerradinho-API/issues/50) |

**Critérios de aceitação**
- `GET /v1/professores/{id}/agenda` devolve todas as turmas vinculadas àquele professor (RF02), com o horário decomposto em dia/início/fim e a sala de cada bloco de aula.
- Professor inexistente devolve 404, não lista vazia.

**Regra de negócio**
- A agenda é só um recorte de RF01+RF02 por professor — não há dado de agenda que não venha das turmas já capturadas.
- A rota usa o `id` do professor (o mesmo de `GET /v1/professores`), não o nome — nome vira slug sem acento no front, e comparar isso com o nome exato do SIGAA não acha o professor; `id` também resolve homônimos.
- `dia`/`início`/`fim` reaproveitam a grade de horário do RF17 (`app/domain/salas.py`) — aulas consecutivas da grade juntam num bloco só (ex. `"6T2345"` é um bloco de 14:00 às 17:50, não 4 blocos separados).
- A sala vem dentro de cada bloco de horário, não da turma — uma turma pode ter salas diferentes por dia (RF05, ADR 0010), e cada bloco mostra a sala do dia certo.
- Os horários N2/N3 (20:00 e 20:55) seguem o mesmo padrão de intervalo das outras aulas, mas não têm uma descrição real na fixture pra confirmar, diferente do resto da grade.

## Rastreabilidade

- **PRs:** nenhum ainda.
- **Testes:** [`tests/routers/test_professores_router.py`](https://github.com/unb-mds/2026-2-Cerradinho-API/blob/dev/backend/tests/routers/test_professores_router.py), [`tests/domain/test_salas.py`](https://github.com/unb-mds/2026-2-Cerradinho-API/blob/dev/backend/tests/domain/test_salas.py)
