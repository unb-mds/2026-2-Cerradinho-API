---
name: web-scraper
description: Build or modify a scraper for one of Cerradinho's public data sources (SIGAA turmas, RU cardapio PDF). Use when the task involves fetching or parsing HTML or PDF from any source listed in docs/REQUISITOS.md section 2.
---

# Web scraper

**Source:** adapted from [`openai/skills/playwright`](https://www.skills.sh/openai/skills/playwright)
(driving a real browser for JS-rendered sources) and
[`mindrally/skills/web-scraping`](https://www.skills.sh/mindrally/skills/web-scraping)
(static vs. dynamic site decision — `requests`+`BeautifulSoup`+`lxml` for static HTML,
Playwright/Selenium for JS-rendered pages), narrowed to Cerradinho's actual sources and
existing modules (`backend/app/scrapers/disciplinas/` and `backend/app/scrapers/cardapio/`).

Cerradinho scrapes public, no-login UnB sources (see `docs/REQUISITOS.md` §2) and stores
normalized data in Postgres; the API never scrapes on request (see "Decisões de
arquitetura" in `docs/ARQUITETURA.md`). Every scraper module lives under
`backend/app/scrapers/<dominio>/` and is split into exactly two files:

- `scraper.py` — talks to the network only. Knows how to navigate/fetch and returns
  **raw HTML or PDF bytes**. Never interprets content.
- `parser.py` — takes raw HTML/PDF in, returns validated Pydantic models (from
  `app/schemas/`) out. Never touches the network.

The module's `__init__.py` exposes the public entry point (`raspar_disciplinas_varias_unidades`,
`raspar_cardapio`) that glues the two together. Use `backend/app/scrapers/disciplinas/`
(HTML) and `backend/app/scrapers/cardapio/` (PDF) as the reference implementations.

## Sources in scope

Only two sources are scraped in Release 2. Eventos (`noticias.unb.br/agenda`, RF08) and
editais (RF09) were dropped from scope, and CKAN and the SIGAA curso pages are listed in
`docs/REQUISITOS.md` §2 only as possible complements. Don't start a scraper for them
without a new decision from the team.

- **SIGAA turmas** (RF01 to RF05): HTML behind JSF, see below.
- **RU cardápio** (RF06, RF07): a weekly PDF per campus, linked from two listing pages
  (`ru.unb.br/cardapio/` and `ru.unb.br/cardapio-refeitorio/`). The RU alternates which
  page it updates, so the scraper checks both and uses the first one with the current
  week (see `docs/fontes/ru-cardapio.md`, risk A2).

## When to use Playwright vs. plain HTTP

This is the static-vs-dynamic decision from the `web-scraping` skill above, applied to
our specific sources:

- SIGAA (`sigaa.unb.br`) is JSF (ViewState/postback-based) — it **requires Playwright**,
  a plain `requests.get` will not work. See RF01 and the "Riscos técnicos" table in
  `docs/REQUISITOS.md`.
- The RU listing pages are plain HTML, so `requests` + `BeautifulSoup` is enough to find
  the PDF link. The PDF itself is read with `pdfplumber` (ADR 0002).
- **The RU PDF layout changes from week to week** (merged cells, ghost columns, dates in
  different rows, and since 16/11/2026 dates in parentheses). The parser reads by
  position of the dates and cells on the page, not by table row or column. The full set
  of rules is in the "Regra de negócio" section of `specs/RF06-*.md`. Read it before
  touching `scrapers/cardapio/parser.py`, and add any new quirk there.

## Rules

- **Scraper never imports parser logic and vice versa's network calls.** If you catch
  yourself parsing inside the scraper class or fetching inside the parser function,
  split it back out.
- **Resilience (RNF05)**: a scraper must fail loudly and specifically when the source
  changes shape — never let an unhandled `AttributeError` from a missing selector
  propagate raw, and never return an empty result that gets logged as success. Raise
  `ErroFonteIndisponivel` (`app/core/exceptions.py`) when the source is down or has no
  data for the period, so RF16 logs it as `tipo_falha="fonte"`. Raise `ValueError` when
  the content is there but can't be parsed (layout change), which RF16 logs as `"interna"`. Log enough to diagnose (see
  RF16 — every run needs a success/failure log, wired through the Celery task in
  `app/tasks/`, not inside the scraper itself).
- **Throttling**: any loop over multiple units/pages must sleep between requests (see
  `atraso_segundos` in `DisciplinaScraper.buscar_html_varias_unidades`) — UnB's servers
  are a shared resource, all units get scraped, so this isn't optional.
- **Document non-obvious source quirks** where the next maintainer will find them: the
  source's file in `docs/fontes/` and the RF's spec in `specs/`, with a short pointer in
  the code (as `scrapers/cardapio/parser.py` points to `specs/RF06`). Future maintainers
  need the *why*, not just the workaround.
- **Output must be a schema, not a dict.** The parser returns instances of models from
  `app/schemas/` (see the `data-contract` skill) — never raw dicts crossing the module
  boundary into `app/domain/` or the DB layer.
- Scraper classes/functions are named after the domain, not `utils.py`/`scraper_helpers.py`
  (see "Nomenclatura" in `docs/ARQUITETURA.md`).

## Testing

- Parser tests use real HTML and PDF fixtures under `backend/tests/scrapers/fixtures/`,
  loaded from disk — never hit the live site in a unit test. See
  `test_disciplinas_parser.py` and `test_cardapio_parser.py` as the pattern: assert on
  real extracted fields (codes, names, dishes per day), not just "didn't crash."
- When a new RU layout breaks the parser, save that week's PDF as
  `fixtures/cardapio_darcy_<monday>.pdf`, add it to `SEMANAS` in
  `test_cardapio_parser.py`, and add one case that checks a dish on the right day.
- Sabotage tests in `backend/tests/sabotagem/` (RNF09) simulate the source being down,
  an expired session or a changed layout, and check the run ends in the right kind of
  failure. Run them after changing error handling in a scraper.
- Scraper (network) code is harder to unit test — keep it thin enough that most logic
  and edge cases live in the parser, which is fully testable offline.
