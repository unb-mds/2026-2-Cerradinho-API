---
name: fastapi-endpoint
description: Add or change a REST endpoint in backend/app/routers/. Use for any FastAPI route work — new domain endpoint, derived-feature endpoint (salas vazias, agenda do professor, cardapio semanal), or OpenAPI documentation.
---

# FastAPI endpoint

**Source:** adapted from [`wshobson/agents/fastapi-templates`](https://skills.sh/wshobson/agents/fastapi-templates)
("Production-ready FastAPI project structure with async patterns, dependency injection,
and layered architecture" — routes/services/repositories separation, async route
handlers, DI via `Depends`). That skill's generic `app/api/v1/endpoints` +
`services/` + `repositories/` layout is mapped onto Cerradinho's own layout
(`app/routers/`, `app/domain/`, `app/models/`) rather than adopting its folder names
verbatim, since the project's structure is already fixed in `docs/ARQUITETURA.md`.

Endpoints live in `backend/app/routers/`, one module per domain, mounted under `/v1/`
(RF12 — API is versioned from day one so consumers don't break on evolution; see
"Decisões de arquitetura" in `docs/ARQUITETURA.md`).

## Rules

- **Routers never scrape and never contain business logic.** Mirroring the
  routes/services split in `fastapi-templates`: a router's only job is to call into
  `app/domain/` (our equivalent of that skill's `services/`) or a repository/model layer
  for straight reads, and shape the HTTP response. If you're writing a
  `BeautifulSoup`/Playwright call or a "compute salas vazias" loop inside a router
  function, it belongs in `app/scrapers/` or `app/domain/` instead — move it.
- **No endpoint triggers scraping at request time.** Scraping and the API are decoupled:
  scrapers write to Postgres on a schedule (Celery), the API only reads. This keeps
  response times predictable and doesn't couple a user's HTTP request to SIGAA/RU/etc.
  being reachable right now.
- **DB access goes through a repository/model layer** (SQLAlchemy), not raw queries
  inlined in the route function — same repository pattern `fastapi-templates` uses for
  generic CRUD. See the `db-model` skill.
- Routes are plain `def` handlers with a sync SQLAlchemy `Session` from
  `Depends(get_db)`, unlike the async pattern in `fastapi-templates`. Keep new routes the
  same way, and never call the sync `Session` from an `async def` route (it would block
  the event loop).
- Every new route needs OpenAPI-visible docs (RF11) — FastAPI generates this from type
  hints, docstrings, and `response_model`; don't suppress it or leave a route
  undocumented with `include_in_schema=False` unless there's a real reason.
- Derived-feature endpoints (RF17 salas vazias, RF18 agenda do professor, RF19 cardápio
  semanal — see `specs/RF17-*.md` to `specs/RF19-*.md`) delegate the actual computation to
  `app/domain/`; the router just parses query params and calls the domain function.
- Contract tests (RNF04, `schemathesis`) run against whatever the router exposes — see
  the `contract-testing` skill. A route change that isn't backward compatible needs a
  version bump discussion, not a silent breaking change under `/v1/`.

## Rate limiting & cache

Both RNF01 (rate limit) and RNF02 (cache) are applied **at the API layer**, not the DB
layer — Postgres stays the single source of truth.

- **Rate limit:** `slowapi` with a global default of 60 requests per minute per IP,
  configured in `app/core/rate_limit.py` and applied to every route by the middleware
  in `app/main.py`. A new route is covered automatically.
- **Cache:** wrap the domain call in `resposta_cacheada(chave, ttl, calcular, tipo)` from
  `app/core/cache.py` (see `routers/cardapio.py`). Keys follow `cache:v1:<dominio>...`,
  with `TTL_SEMANAL` for disciplinas, professores and salas and `TTL_DIARIO` for
  cardápio. The Celery task that refreshes that data must invalidate the same key or
  prefix (see the `scheduled-task` skill), or the route keeps serving the previous run.
