# RF03 · Associar disciplina a sala/prédio

| Release | Responsável | Issue |
|---|---|---|
| R1 | Vitor | [#37](https://github.com/unb-mds/2026-2-Cerradinho-API/issues/37) |

**Critérios de aceitação**
- Turma com local informado no SIGAA aparece com sala e prédio preenchidos na resposta da API.
- Turma sem local informado aparece com sala nula, nunca com erro.

**Regra de negócio**
- O texto de local do SIGAA vem no formato `"PRÉDIO - SALA"` (ex: `"FCTE - I9/I10"`); o prédio é tudo antes do primeiro `" - "`, o resto é o nome da sala.
- Texto sem o separador `" - "` vira só o nome da sala, com prédio vazio, em vez de ser descartado.

## Rastreabilidade

- **PRs:** [#88](https://github.com/unb-mds/2026-2-Cerradinho-API/pull/88), [#118](https://github.com/unb-mds/2026-2-Cerradinho-API/pull/118)
- **Testes:** [`tests/domain/test_disciplinas.py`](https://github.com/unb-mds/2026-2-Cerradinho-API/blob/dev/backend/tests/domain/test_disciplinas.py), [`tests/test_models.py`](https://github.com/unb-mds/2026-2-Cerradinho-API/blob/dev/backend/tests/test_models.py)
- **Decisões:** [ADR 0006](https://github.com/unb-mds/2026-2-Cerradinho-API/blob/dev/docs/adr/0006-salas-derivadas-das-turmas.md)
- **Observação:** A associação é feita na turma (`turmas.sala_id`), não na disciplina. O texto do critério na issue ainda fala em `sala_id` na Disciplina.
