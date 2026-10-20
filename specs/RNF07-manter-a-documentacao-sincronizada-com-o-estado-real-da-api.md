# RNF07 · Manter a documentação sincronizada com o estado real da API

| Release | Responsável | Issue |
|---|---|---|
| R1 | João Paulo | [#72](https://github.com/unb-mds/2026-2-Cerradinho-API/issues/72) |

**Critérios de aceitação**
- A documentação (OpenAPI, README, portal do desenvolvedor) reflete os endpoints e contratos realmente implementados, sem rota documentada que não existe ou existente que não está documentada.

**Regra de negócio**
- "Doc viva" depende do RF11 (documentação gerada do código, não escrita à parte) — é a forma de garantir esse requisito sem depender de disciplina manual de manter dois lugares sincronizados.

## Rastreabilidade

- **PRs:** [#114](https://github.com/unb-mds/2026-2-Cerradinho-API/pull/114), [#129](https://github.com/unb-mds/2026-2-Cerradinho-API/pull/129)
- **Testes:** [`tests/contract/test_openapi_contract.py`](https://github.com/unb-mds/2026-2-Cerradinho-API/blob/dev/backend/tests/contract/test_openapi_contract.py)
- **Observação:** O contrato quebra o CI se uma rota divergir do OpenAPI. Manter README e portal em dia é um processo contínuo.
