---
name: scheduled-task
description: Add or change a Celery task in backend/app/tasks/ that schedules a scraper run. Use for RF15 (automatic scheduling) and RF16 (success/failure logging) work.
---

# Scheduled task (Celery + Redis)

**Source:** adapted from the task-queue guidance in
[`sickn33/antigravity-awesome-skills/fastapi-pro`](https://skills.sh/sickn33/antigravity-awesome-skills/fastapi-pro)
("Task queues with Celery or Dramatiq" as part of production-ready async FastAPI
services), narrowed to Celery+Redis specifically since that's the choice already made in
`docs/ARQUITETURA.md` (and a candidate for its own ADR — see the `adr-writing` skill).

`backend/app/tasks/` wires scrapers into Celery jobs, scheduled via Redis (RF15). The
schedule (`beat_schedule`) is in `backend/app/celery_app.py`: disciplinas on Sundays at
3h and cardápio every day at 5h, in `America/Sao_Paulo`. The current tasks are
`scraping.scrape_disciplinas_task` and `cardapio.scrape_cardapio_task`.

Success/failure logging (RF16) is done by Celery signal handlers in
`app/tasks/logging_signals.py`, which write one row to `execucao_logs` per run
(readable at `GET /v1/execucoes`). A task doesn't log its own outcome: it just returns
or raises. An `ErroFonteIndisponivel` becomes `tipo_falha="fonte"` and any other
exception becomes `"interna"`, so raise the right one (see the `web-scraper` skill's
resilience rule).

## Rules

- **A task calls a scraper + parser, persists the result through `app/domain/`, and
  invalidates the API cache it affects** (`invalidar`/`invalidar_prefixo` from
  `app/core/cache.py`, e.g. `cache:v1:cardapio:semana:`). It does not contain scraping
  or parsing logic itself — that stays in `app/scrapers/<dominio>/`. Forgetting the
  cache invalidation leaves the API serving the previous run for up to the cache TTL.
- A new task module must be listed in `include=[...]` in `backend/app/celery_app.py` so
  the worker loads it, and `tests/tasks/test_log_das_tasks.py` should check that its
  runs reach `execucao_logs`.
- **Every task run logs success or failure (RF16)**, including *which* unit/source
  failed when scraping multiple units (e.g. one FCTE-Gama failure shouldn't blank out
  the log entry for a run that succeeded on other units). A failed unit should not raise
  and kill the whole task run — see RNF05 (resiliência) in `specs/RNF05-*.md` and the risks in
  `docs/scrum/sprint-planning.md`.
- **Schedule outside peak hours** and keep throttling between requests inside the
  scraper (already true of `buscar_html_varias_unidades`) — the task's job is *when*,
  the scraper's job is *how gently*.
- Tasks are idempotent where possible: re-running a task for the same period should
  update existing rows, not duplicate them — this matters for RF07 (cardápio history)
  where old data must be preserved, not overwritten by a naive upsert.
- Retries belong in the task layer (Celery's own retry mechanism), not hand-rolled
  inside the scraper — the scraper's own retry loop (see `_sessao_expirada` handling in
  `DisciplinaScraper.buscar_html`) is for a *specific* transient failure mode
  (SIGAA session expiry) it can detect and recover from directly; broader "the whole run
  failed, try again later" retries are a Celery concern.
