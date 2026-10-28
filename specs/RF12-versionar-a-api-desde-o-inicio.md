# RF12 · Versionar a API desde o início

| Release | Responsável | Issue |
|---|---|---|
| R1 | Gabriel | [#44](https://github.com/unb-mds/2026-2-Cerradinho-API/issues/44) |

**Critérios de aceitação**
- Toda rota pública vive sob o prefixo `/v1/` desde a primeira versão publicada, não só quando uma v2 for necessária.

**Regra de negócio**
- Versionar desde o início evita quebrar clientes (frontend, SDK, squads externas) quando uma mudança incompatível for inevitável — uma v2 nasce como rota nova, sem alterar o contrato de `/v1/`.

## Rastreabilidade

- **PRs:** [#108](https://github.com/unb-mds/2026-2-Cerradinho-API/pull/108)
- **Testes:** [`tests/contract/test_openapi_contract.py`](https://github.com/unb-mds/2026-2-Cerradinho-API/blob/dev/backend/tests/contract/test_openapi_contract.py)
- **Decisões:** [ADR 0005](https://github.com/unb-mds/2026-2-Cerradinho-API/blob/dev/docs/adr/0005-api-versionada-desde-o-inicio.md)
