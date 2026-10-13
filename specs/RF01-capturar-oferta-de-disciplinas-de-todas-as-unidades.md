# RF01 · Capturar oferta de disciplinas de todas as unidades

| Release | Responsável | Issue | Situação |
|---|---|---|---|
| R1 | Vitor | [#35](https://github.com/unb-mds/2026-2-Cerradinho-API/issues/35) | Entregue |

**Critérios de aceitação**
- Dado o código de uma unidade (ex: `673` = FCTE/Gama), o scraper devolve todas as turmas abertas daquela unidade com disciplina, código, número da turma, horário, vagas ofertadas e ocupadas.
- Sem unidade específica informada, o scraper varre todas as unidades listadas no formulário público do SIGAA, uma a uma.
- Rodar o scraper duas vezes seguidas para a mesma turma atualiza os dados existentes (vagas, sala, horário), sem criar linha duplicada.
- Uma unidade que falhar (sessão expirada, erro de rede) não derruba a raspagem das demais unidades.

**Regra de negócio**
- A chave natural de uma turma é (disciplina, número, ano/período) — é o que o SIGAA considera uma oferta única; é por essa chave que o upsert decide atualizar em vez de duplicar.
- O SIGAA junta o código do horário com o intervalo de datas da turma no mesmo texto (ex: `"6T2345 (10/08/2026 - 14/12/2026)"`); só o código antes do `(` é persistido — guardar o texto inteiro estoura a coluna do banco.
- Turma com docente "a definir" vem do SIGAA sem o número de vagas ofertadas publicado; nesse caso o valor é tratado como `0`, nunca como erro que interrompe a raspagem.
- Entre requisições a unidades diferentes, o scraper aguarda um intervalo mínimo (throttling) — etiqueta com o servidor da UnB, não é otimização.

## Rastreabilidade

- **PRs:** [#75](https://github.com/unb-mds/2026-2-Cerradinho-API/pull/75), [#81](https://github.com/unb-mds/2026-2-Cerradinho-API/pull/81), [#88](https://github.com/unb-mds/2026-2-Cerradinho-API/pull/88), [#118](https://github.com/unb-mds/2026-2-Cerradinho-API/pull/118)
- **Testes:** [`tests/scrapers/test_disciplinas_parser.py`](https://github.com/unb-mds/2026-2-Cerradinho-API/blob/dev/backend/tests/scrapers/test_disciplinas_parser.py), [`tests/domain/test_disciplinas.py`](https://github.com/unb-mds/2026-2-Cerradinho-API/blob/dev/backend/tests/domain/test_disciplinas.py), [`tests/tasks/test_scraping.py`](https://github.com/unb-mds/2026-2-Cerradinho-API/blob/dev/backend/tests/tasks/test_scraping.py), [`tests/integration/test_pipeline_disciplinas_postgres.py`](https://github.com/unb-mds/2026-2-Cerradinho-API/blob/dev/backend/tests/integration/test_pipeline_disciplinas_postgres.py)
- **Decisões:** [ADR 0002](https://github.com/unb-mds/2026-2-Cerradinho-API/blob/dev/docs/adr/0002-ferramentas-de-scraping.md)
