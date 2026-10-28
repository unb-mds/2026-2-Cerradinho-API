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

- **PRs:** [#112](https://github.com/unb-mds/2026-2-Cerradinho-API/pull/112), [#114](https://github.com/unb-mds/2026-2-Cerradinho-API/pull/114), [#227](https://github.com/unb-mds/2026-2-Cerradinho-API/pull/227)
- **Testes:** [`tests/contract/test_openapi_contract.py`](https://github.com/unb-mds/2026-2-Cerradinho-API/blob/dev/backend/tests/contract/test_openapi_contract.py)
- **Observação:** os dados de exemplo ficam em [`tests/contract/conftest.py`](https://github.com/unb-mds/2026-2-Cerradinho-API/blob/dev/backend/tests/contract/conftest.py): duas turmas em salas, dias e turnos diferentes, cardápio para hoje e amanhã e uma execução de sucesso e outra de falha. Sem dados as rotas devolvem `[]` e o schemathesis não valida o formato dos itens. Foi assim que apareceram o `horario` aceitando dígitos que não são 0-9 em `/v1/salas/vazias` e o `criado_em` sem fuso em `/v1/execucoes`.
