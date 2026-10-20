# RF02 · Associar disciplina a professor

| Release | Responsável | Issue |
|---|---|---|
| R1 | Vitor | [#36](https://github.com/unb-mds/2026-2-Cerradinho-API/issues/36) |

**Critérios de aceitação**
- Toda turma capturada com professor(es) listado(s) no SIGAA aparece com esse(s) professor(es) vinculado(s) na resposta da API.
- O mesmo professor lecionando turmas diferentes aparece como uma única entidade (não duplica o cadastro).

**Regra de negócio**
- O nome do professor, como vem do SIGAA, é a chave de deduplicação (get-or-create por nome) — não há normalização de grafia diferente pro mesmo docente.
- Turma com docente "a definir" ainda não tem essa normalização tratada: o literal "A DEFINIR DOCENTE" pode ser persistido como se fosse um nome de professor.

## Rastreabilidade

- **PRs:** [#88](https://github.com/unb-mds/2026-2-Cerradinho-API/pull/88), [#118](https://github.com/unb-mds/2026-2-Cerradinho-API/pull/118)
- **Testes:** [`tests/domain/test_disciplinas.py`](https://github.com/unb-mds/2026-2-Cerradinho-API/blob/dev/backend/tests/domain/test_disciplinas.py), [`tests/test_models.py`](https://github.com/unb-mds/2026-2-Cerradinho-API/blob/dev/backend/tests/test_models.py), [`tests/integration/test_pipeline_disciplinas_postgres.py`](https://github.com/unb-mds/2026-2-Cerradinho-API/blob/dev/backend/tests/integration/test_pipeline_disciplinas_postgres.py)
- **Observação:** A associação é feita na turma (`turma_professores`), não na disciplina. O texto do critério na issue ainda fala em `professor_id` na Disciplina.
