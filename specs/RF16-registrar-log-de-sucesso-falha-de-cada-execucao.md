# RF16 · Registrar log de sucesso/falha de cada execução

| Release | Responsável | Issue | Situação |
|---|---|---|---|
| R1 | Arthur | [#46](https://github.com/unb-mds/2026-2-Cerradinho-API/issues/46) | Concluído |

**Critérios de aceitação**
- Toda execução agendada (sucesso ou falha) gera um registro identificável — pessoa fazendo triagem de incidente consegue saber se o scraper rodou e o que aconteceu.
- O log diferencia falha da fonte (SIGAA/RU fora do ar) de falha do nosso código (exceção no parser).

**Regra de negócio**
- O log é por execução de task, não por turma/item individual — granularidade fina demais tornaria o log inútil pra triagem.

## Rastreabilidade

- **PRs:** [#96](https://github.com/unb-mds/2026-2-Cerradinho-API/pull/96)
- **Testes:** `tests/tasks/test_loggin_signals.py` (classificação fonte/interna nos signal handlers), `tests/routers/test_execucoes_router.py` (endpoint, ordenação pela mais recente)
- **Observação:** O log grava em `execucao_logs` via signal handlers (`app/tasks/logging_signals.py`) e é consultável em `GET /v1/execucoes` (`app/routers/execucoes.py`).
