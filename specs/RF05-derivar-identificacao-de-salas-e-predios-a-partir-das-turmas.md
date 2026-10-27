# RF05 · Derivar identificação de salas e prédios a partir das turmas

| Release | Responsável | Issue |
|---|---|---|
| R1 | Vitor | [#39](https://github.com/unb-mds/2026-2-Cerradinho-API/issues/39) |

**Critérios de aceitação**
- `GET /v1/salas` lista toda sala distinta encontrada nas turmas capturadas, ordenada por prédio e nome.
- A mesma sala referenciada em turmas diferentes aparece como uma única entidade.

**Regra de negócio**
- Não existe fonte própria pra sala/prédio (ver seção 2) — a existência de uma sala depende inteiramente de aparecer em pelo menos uma turma do RF01.
- A chave de deduplicação é o par (prédio, nome da sala) resultante da normalização do RF03, incluindo o ponto inconsistente do SIGAA depois de "LAB" (`"LAB NIT/LDS"` e `"LAB. NIT/LDS"` são a mesma sala).
- Salas gravadas antes dessa normalização existir (ou com o ponto de "LAB" inconsistente) foram fundidas numa migration de dados ([`0004`](https://github.com/unb-mds/2026-2-Cerradinho-API/blob/dev/backend/alembic/versions/0004_funde_salas_e_professores_duplicados.py)) — não é algo que se repete em raspagens novas.

## Rastreabilidade

- **PRs:** [#88](https://github.com/unb-mds/2026-2-Cerradinho-API/pull/88), [#119](https://github.com/unb-mds/2026-2-Cerradinho-API/pull/119)
- **Testes:** [`tests/domain/test_disciplinas.py`](https://github.com/unb-mds/2026-2-Cerradinho-API/blob/dev/backend/tests/domain/test_disciplinas.py), [`tests/routers/test_salas_router.py`](https://github.com/unb-mds/2026-2-Cerradinho-API/blob/dev/backend/tests/routers/test_salas_router.py)
- **Decisões:** [ADR 0006](https://github.com/unb-mds/2026-2-Cerradinho-API/blob/dev/docs/adr/0006-salas-derivadas-das-turmas.md)
