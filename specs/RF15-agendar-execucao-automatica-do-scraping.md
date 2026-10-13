# RF15 · Agendar execução automática do scraping

| Release | Responsável | Issue | Situação |
|---|---|---|---|
| R1 | Arthur | [#45](https://github.com/unb-mds/2026-2-Cerradinho-API/issues/45) | Parcial |

**Critérios de aceitação**
- O scraper de cada domínio roda automaticamente, sem intervenção manual, numa frequência definida (disciplinas: semanal; cardápio: diária).
- Uma execução agendada persiste o resultado no banco real, não só executa a raspagem.

**Regra de negócio**
- O agendamento (Celery beat) só dispara a task; ano/período da oferta de disciplinas são parâmetros explícitos do agendamento, porque o SIGAA público não expõe em lugar nenhum qual é o período letivo corrente — precisam ser atualizados manualmente a cada novo semestre.

## Rastreabilidade

- **PRs:** [#89](https://github.com/unb-mds/2026-2-Cerradinho-API/pull/89), [#96](https://github.com/unb-mds/2026-2-Cerradinho-API/pull/96), [#121](https://github.com/unb-mds/2026-2-Cerradinho-API/pull/121)
- **Testes:** [`tests/tasks/test_celery_app.py`](https://github.com/unb-mds/2026-2-Cerradinho-API/blob/dev/backend/tests/tasks/test_celery_app.py), [`tests/tasks/test_scraping.py`](https://github.com/unb-mds/2026-2-Cerradinho-API/blob/dev/backend/tests/tasks/test_scraping.py)
- **Decisões:** [ADR 0003](https://github.com/unb-mds/2026-2-Cerradinho-API/blob/dev/docs/adr/0003-celery-e-redis-para-agendamento.md), [ADR 0004](https://github.com/unb-mds/2026-2-Cerradinho-API/blob/dev/docs/adr/0004-coleta-desacoplada-da-api.md)
- **Observação:** Disciplinas e cardápio estão agendados, mas a execução do cardápio falha enquanto o parser do RU não for corrigido (#103).
