# RF16 · Registrar log de sucesso/falha de cada execução

| Release | Responsável | Issue |
|---|---|---|
| R1 | Arthur | [#46](https://github.com/unb-mds/2026-2-Cerradinho-API/issues/46) |

**Critérios de aceitação**
- Toda execução agendada (sucesso ou falha) gera um registro identificável — pessoa fazendo triagem de incidente consegue saber se o scraper rodou e o que aconteceu.
- O log diferencia falha da fonte (SIGAA/RU fora do ar) de falha do nosso código (exceção no parser).

**Regra de negócio**
- O log é por execução de task, não por turma/item individual — granularidade fina demais tornaria o log inútil pra triagem.

## Rastreabilidade

- **PRs:** [#96](https://github.com/unb-mds/2026-2-Cerradinho-API/pull/96)
- **Testes:** nenhum ainda.
- **Observação:** O log de sucesso e falha existe (`app/tasks/logging_signals.py`), mas não tem teste automatizado e ainda não pode ser consultado.
