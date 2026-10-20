# RNF04 · Validar a API contra testes de contrato

| Release | Responsável | Issue |
|---|---|---|
| R1 | João Paulo | [#69](https://github.com/unb-mds/2026-2-Cerradinho-API/issues/69) |

**Critérios de aceitação**
- Toda rota pública é validada automaticamente contra o `/openapi.json` publicado (schemathesis) no pipeline de CI.
- Uma rota cuja resposta real diverge do schema documentado falha o CI, não passa despercebida.

**Regra de negócio**
- O contrato validado é o OpenAPI gerado (RF11), não um schema mantido à mão — evita o contrato e a implementação divergirem.

## Rastreabilidade

- **PRs:** [#112](https://github.com/unb-mds/2026-2-Cerradinho-API/pull/112), [#114](https://github.com/unb-mds/2026-2-Cerradinho-API/pull/114)
- **Testes:** [`tests/contract/test_openapi_contract.py`](https://github.com/unb-mds/2026-2-Cerradinho-API/blob/dev/backend/tests/contract/test_openapi_contract.py)
