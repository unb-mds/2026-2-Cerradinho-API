# RF02 · Associar disciplina a professor

| Release | Responsável | Issue | Situação |
|---|---|---|---|
| R1 | Vitor | [#36](https://github.com/unb-mds/2026-2-Cerradinho-API/issues/36) | Entregue |

**Critérios de aceitação**
- Toda turma capturada com professor(es) listado(s) no SIGAA aparece com esse(s) professor(es) vinculado(s) na resposta da API.
- O mesmo professor lecionando turmas diferentes aparece como uma única entidade (não duplica o cadastro).

**Regra de negócio**
- O nome do professor, normalizado, é a chave de deduplicação (get-or-create por nome). O SIGAA junta a carga horária da disciplina no nome do docente (ex: `"FULANO (60h)"`), e como a carga varia por disciplina pro mesmo professor, esse sufixo é cortado antes do dedup — senão o mesmo professor vira uma linha por carga horária distinta.
- Turma com docente "a definir" ainda não tem essa normalização tratada: o literal "A DEFINIR DOCENTE" pode ser persistido como se fosse um nome de professor.

## Rastreabilidade

- **PRs:** [#88](https://github.com/unb-mds/2026-2-Cerradinho-API/pull/88), [#118](https://github.com/unb-mds/2026-2-Cerradinho-API/pull/118)
- **Testes:** [`tests/domain/test_disciplinas.py`](https://github.com/unb-mds/2026-2-Cerradinho-API/blob/dev/backend/tests/domain/test_disciplinas.py), [`tests/test_models.py`](https://github.com/unb-mds/2026-2-Cerradinho-API/blob/dev/backend/tests/test_models.py), [`tests/integration/test_pipeline_disciplinas_postgres.py`](https://github.com/unb-mds/2026-2-Cerradinho-API/blob/dev/backend/tests/integration/test_pipeline_disciplinas_postgres.py)
- **Observação:** A associação é feita na turma (`turma_professores`), não na disciplina. O texto do critério na issue ainda fala em `professor_id` na Disciplina.
