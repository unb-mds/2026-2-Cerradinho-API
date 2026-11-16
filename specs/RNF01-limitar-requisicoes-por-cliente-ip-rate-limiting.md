# RNF01 · Limitar requisições por cliente/IP (rate limiting)

| Release | Responsável | Issue |
|---|---|---|
| R2 | Arthur | [#66](https://github.com/unb-mds/2026-2-Cerradinho-API/issues/66) |

**Critérios de aceitação**
- Cliente que ultrapassa o limite de requisições num intervalo recebe HTTP 429, não é simplesmente bloqueado em silêncio.

**Regra de negócio**
- Protege a API contra uso abusivo de terceiros (RF13) sem precisar de autenticação — o produto é público e sem login.

## Rastreabilidade

- **PRs:** [#229](https://github.com/unb-mds/2026-2-Cerradinho-API/pull/229)
- **Testes:** `tests/core/test_rate_limit.py` (confirma 429 ao exceder o limite); `tests/conftest.py` desliga o limiter por padrão em toda a suíte (fixture `rate_limit_desligado`, autouse), pra não atrapalhar os testes de contrato.
- **Observação:** fallback em memória (`in_memory_fallback`) se o Redis cair, em vez de `swallow_errors` — esse segundo caminho tem um bug real no slowapi 0.1.10 (não seta `request.state.view_rate_limit` ao engolir o erro de conexão, quebrando a injeção de headers na resposta).
- **Decisões:** [ADR 0007](https://github.com/unb-mds/2026-2-Cerradinho-API/blob/dev/docs/adr/0007-cache-e-rate-limit-na-api.md)
