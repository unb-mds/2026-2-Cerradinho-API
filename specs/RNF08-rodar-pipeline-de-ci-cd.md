# RNF08 · Rodar pipeline de CI/CD

| Release | Responsável | Issue | Situação |
|---|---|---|---|
| R1 | João Paulo | [#73](https://github.com/unb-mds/2026-2-Cerradinho-API/issues/73) | Parcial |

**Critérios de aceitação**
- Todo push dispara lint, testes (unitários, contrato, integração) e SAST automaticamente, desde a Release 1.
- Achado de severidade crítica ou alta no SAST bloqueia o lançamento da nota daquela entrega.

**Regra de negócio**
- O pipeline é porta de qualidade da disciplina, não só conveniência de time — PR com CI vermelho não é elegível pra merge (ver [`CONTRIBUTING.md`](https://github.com/unb-mds/2026-2-Cerradinho-API/blob/dev/CONTRIBUTING.md)).

## Rastreabilidade

- **PRs:** [#85](https://github.com/unb-mds/2026-2-Cerradinho-API/pull/85), [#112](https://github.com/unb-mds/2026-2-Cerradinho-API/pull/112), [#114](https://github.com/unb-mds/2026-2-Cerradinho-API/pull/114), [#116](https://github.com/unb-mds/2026-2-Cerradinho-API/pull/116), [#124](https://github.com/unb-mds/2026-2-Cerradinho-API/pull/124)
- **Testes:** [`.github/workflows/ci.yml`](https://github.com/unb-mds/2026-2-Cerradinho-API/blob/dev/.github/workflows/ci.yml)
- **Decisões:** [ADR 0008](https://github.com/unb-mds/2026-2-Cerradinho-API/blob/dev/docs/adr/0008-bandit-como-sast.md)
- **Observação:** O pipeline roda lint, SAST e testes, mas ainda não é check obrigatório para o merge.
