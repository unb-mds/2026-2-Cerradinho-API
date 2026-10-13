# RNF01 · Limitar requisições por cliente/IP (rate limiting)

| Release | Responsável | Issue | Situação |
|---|---|---|---|
| R2 | Arthur | [#66](https://github.com/unb-mds/2026-2-Cerradinho-API/issues/66) | Não iniciado |

**Critérios de aceitação**
- Cliente que ultrapassa o limite de requisições num intervalo recebe HTTP 429, não é simplesmente bloqueado em silêncio.

**Regra de negócio**
- Protege a API contra uso abusivo de terceiros (RF13) sem precisar de autenticação — o produto é público e sem login.

## Rastreabilidade

- **PRs:** nenhum ainda.
- **Testes:** nenhum ainda.
- **Decisões:** [ADR 0007](https://github.com/unb-mds/2026-2-Cerradinho-API/blob/dev/docs/adr/0007-cache-e-rate-limit-na-api.md)
