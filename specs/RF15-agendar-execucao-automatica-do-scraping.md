# RF15 · Agendar execução automática do scraping

| Release | Responsável | Issue |
|---|---|---|
| R1 | Arthur | [#45](https://github.com/unb-mds/2026-2-Cerradinho-API/issues/45) |

**Critérios de aceitação**
- O scraper de cada domínio roda automaticamente, sem intervenção manual, numa frequência definida (disciplinas: semanal; cardápio: diária).
- Uma execução agendada persiste o resultado no banco real, não só executa a raspagem.

**Regra de negócio**
- O agendamento (Celery beat) só dispara a task; ano/período da oferta de disciplinas são parâmetros explícitos do agendamento, porque o SIGAA público não expõe em lugar nenhum qual é o período letivo corrente — precisam ser atualizados manualmente a cada novo semestre.

## Rastreabilidade

- **PRs:** [#89](https://github.com/unb-mds/2026-2-Cerradinho-API/pull/89), [#96](https://github.com/unb-mds/2026-2-Cerradinho-API/pull/96), [#121](https://github.com/unb-mds/2026-2-Cerradinho-API/pull/121), [#145](https://github.com/unb-mds/2026-2-Cerradinho-API/pull/145), [#249](https://github.com/unb-mds/2026-2-Cerradinho-API/pull/249) (verificação em produção)
- **Testes:** [`tests/tasks/test_celery_app.py`](https://github.com/unb-mds/2026-2-Cerradinho-API/blob/dev/backend/tests/tasks/test_celery_app.py), [`tests/tasks/test_scraping.py`](https://github.com/unb-mds/2026-2-Cerradinho-API/blob/dev/backend/tests/tasks/test_scraping.py)
- **Decisões:** [ADR 0003](https://github.com/unb-mds/2026-2-Cerradinho-API/blob/dev/docs/adr/0003-celery-e-redis-para-agendamento.md), [ADR 0004](https://github.com/unb-mds/2026-2-Cerradinho-API/blob/dev/docs/adr/0004-coleta-desacoplada-da-api.md)
- **Observação:** Verificado contra a produção em 16/11/2026 (`GET /v1/execucoes` em `api.3-147-228-104.sslip.io`): o agendamento de disciplinas está estável, rodando sozinho aos domingos (08/11 e 15/11, sucesso nas duas). A única falha registrada foi isolada, no primeiro boot em produção (04/11, 04:05 — `scrape_disciplinas_task() missing 3 required positional arguments`, provavelmente uma imagem antiga ainda sem o `kwargs` do agendamento), corrigida por disparo manual 17 minutos depois e não repetida nos agendamentos seguintes.
