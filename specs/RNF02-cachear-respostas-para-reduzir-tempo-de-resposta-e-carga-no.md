# RNF02 · Cachear respostas para reduzir tempo de resposta e carga no banco

| Release | Responsável | Issue |
|---|---|---|
| R2 | Arthur | [#67](https://github.com/unb-mds/2026-2-Cerradinho-API/issues/67) |

**Critérios de aceitação**
- Requisição repetida ao mesmo endpoint, dentro da janela de cache, não gera nova consulta ao banco.
- Dado que mudou (nova raspagem concluída) invalida o cache daquele domínio.

**Regra de negócio**
- O cache é por domínio (disciplinas, cardápio, etc.), alinhado à frequência de atualização de cada um (RF15) — não faz sentido cachear por mais tempo que o intervalo entre raspagens.

## Rastreabilidade

- **PRs:** nenhum ainda.
- **Testes:** nenhum ainda.
- **Decisões:** [ADR 0007](https://github.com/unb-mds/2026-2-Cerradinho-API/blob/dev/docs/adr/0007-cache-e-rate-limit-na-api.md)
