---
name: sdk-cli
description: Add or change code in the sdk/ package — the installable Python client/CLI for third-party integration (RF13). Use when building the SDK itself, not when consuming Cerradinho's API from the frontend (see frontend-data-hook for that).
---

# SDK / CLI (RF13)

**Source:** adapted from
[`speakeasy-api/skills/start-new-sdk-project`](https://skills.sh/speakeasy-api/skills/start-new-sdk-project)
(generate a client SDK directly from an OpenAPI spec — `speakeasy quickstart` with
schema/language/package options) for the SDK's client layer, and
[`sickn33/antigravity-awesome-skills/python-development-python-scaffold`](https://skills.sh/sickn33/antigravity-awesome-skills/python-development-python-scaffold)
(Typer + Rich scaffold) for the CLI layer on top of it.

`sdk/` is an installable Python package that lets other squads/consumers integrate with
Cerradinho's API without hand-rolling HTTP calls (RF13, Release 2: SDK owned by Vitor, CLI by João Paulo, per
the spec in `specs/RF13-*.md`).

## Rules

- **The low-level client is generated from the OpenAPI spec FastAPI already produces
  (RF11)**, with `openapi-python-client` instead of Speakeasy, into
  `sdk/cerradinho_sdk/_gerado/`. Never edit `_gerado/` by hand: after a router or schema
  change, run `sdk/scripts/gerar_cliente.sh` and commit the result.
- `CerradinhoClient` (`sdk/cerradinho_sdk/client.py`) is hand-written on top of the
  generated code, one method per `/v1/` endpoint, with `ProfessorNaoEncontrado` for 404
  and `RespostaInesperada` for any status outside the contract. A new endpoint needs a
  new method here too.
- **The CLI (`sdk/cerradinho_sdk/cli.py`, command `cerradinho`) uses `Typer`** and
  calls `CerradinhoClient`, one command per client method, with no HTTP calls of its
  own. The API address comes from `CERRADINHO_API_URL`. Argument parsing is not hand-rolled
  `argparse`/`sys.argv` parsing — see "Preferir bibliotecas prontas" in
  `docs/ARQUITETURA.md`, which calls this out by name as the intended example.
- The SDK is a **thin client**: it wraps `/v1/` endpoints (RF10) and mirrors the schemas
  the API returns — it does not reimplement domain logic (salas vazias, agenda do
  professor) that the API already computes server-side. If a computation exists in
  `app/domain/`, the SDK calls the endpoint for it, it doesn't recompute it locally.
- Version the SDK against the API version it targets (RF12) — a breaking `/v1/` → `/v2/`
  change needs a corresponding SDK major version, not a silent compatibility shim.
- Ship the SDK with its own tests against a mocked/recorded API response, not a live
  call to the deployed API in CI. `sdk/tests/test_client.py` and `sdk/tests/test_cli.py`
  use `respx` for this.
