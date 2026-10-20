# RF19 · Agrupar cardápio semanal

| Release | Responsável | Issue |
|---|---|---|
| R2 | Gabriel | [#51](https://github.com/unb-mds/2026-2-Cerradinho-API/issues/51) |

**Critérios de aceitação**
- `GET /v1/cardapio/semana?data_inicio=...` devolve os 7 dias a partir da data informada; sem `data_inicio`, devolve de hoje até hoje+6 dias.
- Dia sem cardápio publicado aparece como ausente/vazio no agrupamento, não interrompe a resposta dos outros dias.

**Regra de negócio**
- O agrupamento é só uma leitura em janela de 7 dias sobre o histórico do RF07 — não dispara nova raspagem.

## Rastreabilidade

- **PRs:** nenhum ainda.
- **Testes:** nenhum ainda.
