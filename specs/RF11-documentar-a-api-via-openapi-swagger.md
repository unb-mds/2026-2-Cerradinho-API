# RF11 · Documentar a API via OpenAPI/Swagger

| Release | Responsável | Issue |
|---|---|---|
| R1 | Daniel | [#43](https://github.com/unb-mds/2026-2-Cerradinho-API/issues/43) |

**Critérios de aceitação**
- `/openapi.json` é gerado automaticamente a partir dos schemas Pydantic e reflete exatamente o formato que os endpoints retornam.
- `/docs` expõe a documentação interativa (Swagger UI) sem configuração manual adicional.

**Regra de negócio**
- A documentação não é escrita à parte — ela nasce do contrato de dados (`app/schemas/`) e do roteamento do FastAPI, pra nunca divergir do comportamento real (ver RNF04 e RNF07).

## Rastreabilidade

- **PRs:** [#108](https://github.com/unb-mds/2026-2-Cerradinho-API/pull/108), [#129](https://github.com/unb-mds/2026-2-Cerradinho-API/pull/129)
- **Testes:** [`tests/contract/test_openapi_contract.py`](https://github.com/unb-mds/2026-2-Cerradinho-API/blob/dev/backend/tests/contract/test_openapi_contract.py)
