# RF04 · Cadastrar docentes vinculados às disciplinas

| Release | Responsável | Issue |
|---|---|---|
| R1 | Vitor | [#38](https://github.com/unb-mds/2026-2-Cerradinho-API/issues/38) |

**Critérios de aceitação**
- `GET /v1/professores` lista todo professor que leciona pelo menos uma turma capturada, com as disciplinas associadas.
- Professor sem nenhuma turma ativa não aparece na listagem (não há cadastro manual de professor).
- `GET /v1/professores?nome=` filtra por busca parcial de nome, sem diferenciar maiúsculas/minúsculas ou acentos (ex: `nome=andre` acha "André").
- Professor com o mesmo nome em disciplinas diferentes aparece como um único registro, mesmo quando o SIGAA publica carga horária distinta por disciplina (ver RF02).

**Regra de negócio**
- O cadastro de professor nasce exclusivamente do RF01/RF02 — não existe endpoint de criação direta de professor.
- A busca por nome compara palavra a palavra, normalizadas (sem acento, sem diferenciar caixa) — cada termo buscado precisa aparecer em algum lugar do nome, em qualquer ordem.

## Rastreabilidade

- **PRs:** [#119](https://github.com/unb-mds/2026-2-Cerradinho-API/pull/119)
- **Testes:** [`tests/routers/test_professores_router.py`](https://github.com/unb-mds/2026-2-Cerradinho-API/blob/dev/backend/tests/routers/test_professores_router.py)
