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
- O SIGAA pode listar mais de uma sala pra mesma turma, quando ela usa salas diferentes em dias diferentes (ex.: `"FCTE - S1 / MOCAP"`). Cada sala listada vira uma entidade própria — a correspondência com o dia certo é do RF17 (ver [ADR 0010](https://github.com/unb-mds/2026-2-Cerradinho-API/blob/dev/docs/adr/0010-sala-por-horario-nao-por-turma.md)).
- O Darcy separa prédio e sala só com espaço, sem `-`/`/` (ex.: `"PAT AT 125"`, `"ICC ANF.16"`) — só é reconhecido como prédio quando o primeiro token é um prédio confirmado (`ICC`, `PAT`, `BSA`, `FCTE`); um prefixo desconhecido fica tudo como nome, pra não arriscar separar errado. "TÉRREO"/"SUBSOLO" são andar, não prédio, e não são promovidos a prédio mesmo quando aparecem antes do separador.
- Ainda não coberto: sala com o código de horário embutido no nome (ex.: `"3M12(ICC ANF.12) 56M12(ICC ANF. 5)"`) — precisa da turma completa (horários + sala) pra confirmar a correspondência sem chutar.

## Rastreabilidade

- **PRs:** [#88](https://github.com/unb-mds/2026-2-Cerradinho-API/pull/88), [#119](https://github.com/unb-mds/2026-2-Cerradinho-API/pull/119)
- **Testes:** [`tests/domain/test_disciplinas.py`](https://github.com/unb-mds/2026-2-Cerradinho-API/blob/dev/backend/tests/domain/test_disciplinas.py), [`tests/routers/test_salas_router.py`](https://github.com/unb-mds/2026-2-Cerradinho-API/blob/dev/backend/tests/routers/test_salas_router.py)
- **Decisões:** [ADR 0006](https://github.com/unb-mds/2026-2-Cerradinho-API/blob/dev/docs/adr/0006-salas-derivadas-das-turmas.md), [ADR 0010](https://github.com/unb-mds/2026-2-Cerradinho-API/blob/dev/docs/adr/0010-sala-por-horario-nao-por-turma.md)
