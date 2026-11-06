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
- O Darcy separa prédio e sala só com espaço, sem `-`/`/` (ex.: `"PAT AT 125"`, `"ICC ANF.16"`) — só é reconhecido como prédio quando o primeiro token é um prédio confirmado (`ICC`, `PAT`, `BSA`, `PJC`, `FCTE`; `BSAS` funde com `BSA S`, SIGAA junta sem espaço); um prefixo desconhecido fica tudo como nome, pra não arriscar separar errado. "TÉRREO"/"SUBSOLO" são andar, não prédio, e não são promovidos a prédio mesmo quando aparecem antes do separador.
- Quando o separador (`-`/`/`) cai dentro do próprio código da sala, não entre prédio e sala (ex.: `"BSA S B1 34 - 10"`, `"ICC AT 114 - 092"`), o prédio continua sendo só o primeiro token — distinguido de um prédio de nome completo de verdade (ex.: `"BSA SUL - A1"`) pelo token seguinte ser curto (sigla de ala/bloco), não uma palavra.
- O SIGAA pode juntar o código de horário com a sala daquele dia no próprio campo de sala, um par por dia (ex.: `"2N12(ICC ANF.15) 4N12(ICC ANF.16)"` — segunda na ANF.15, quarta na ANF.16). Esse formato já vem com o dia casado com a sala certa, sem precisar da heurística de ordem do RF17/ADR 0010 — só é aceito quando o campo inteiro é feito desses pares; um campo truncado ou com um segmento sem sala (achados reais do Darcy) cai no comportamento anterior (sala única sem separar).

## Rastreabilidade

- **PRs:** [#88](https://github.com/unb-mds/2026-2-Cerradinho-API/pull/88), [#119](https://github.com/unb-mds/2026-2-Cerradinho-API/pull/119)
- **Testes:** [`tests/domain/test_disciplinas.py`](https://github.com/unb-mds/2026-2-Cerradinho-API/blob/dev/backend/tests/domain/test_disciplinas.py), [`tests/routers/test_salas_router.py`](https://github.com/unb-mds/2026-2-Cerradinho-API/blob/dev/backend/tests/routers/test_salas_router.py)
- **Decisões:** [ADR 0006](https://github.com/unb-mds/2026-2-Cerradinho-API/blob/dev/docs/adr/0006-salas-derivadas-das-turmas.md), [ADR 0010](https://github.com/unb-mds/2026-2-Cerradinho-API/blob/dev/docs/adr/0010-sala-por-horario-nao-por-turma.md)
