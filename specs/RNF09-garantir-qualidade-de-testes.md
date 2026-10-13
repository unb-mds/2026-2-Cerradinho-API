# RNF09 · Garantir qualidade de testes

| Release | Responsável | Issue | Situação |
|---|---|---|---|
| R2 | João Paulo | [#74](https://github.com/unb-mds/2026-2-Cerradinho-API/issues/74) | Parcial |

**Critérios de aceitação**
- Cobertura de linhas do backend ≥ 90%.
- Escore de mutação ≥ 50% nos módulos críticos (scrapers, domínio, persistência).
- Teste de sabotagem (simular fonte quebrada/mudada) cobrindo 100% dos módulos críticos.

**Regra de negócio**
- Cobertura de linha sozinha não garante teste que realmente falha quando o código quebra — por isso mutação e sabotagem são métricas à parte, não substituídas por cobertura alta.

## Rastreabilidade

- **PRs:** nenhum ainda.
- **Testes:** nenhum ainda.
- **Observação:** A cobertura é medida no CI, sem mínimo exigido. Mutação e sabotagem ainda não foram implementadas.
