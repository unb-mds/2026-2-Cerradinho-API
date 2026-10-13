# RNF03 · Monitorar disponibilidade das fontes e da API, com alertas

| Release | Responsável | Issue | Situação |
|---|---|---|---|
| R2 | João Paulo | [#68](https://github.com/unb-mds/2026-2-Cerradinho-API/issues/68) | Não iniciado |

**Critérios de aceitação**
- Queda de uma fonte externa (SIGAA, RU) ou da própria API gera um alerta, não só um log silencioso.
- O alerta distingue "fonte externa fora do ar" de "nosso serviço fora do ar" — são respostas de incidente diferentes.

**Regra de negócio**
- Disponibilidade (a fonte responde?) é só a primeira camada: estrutura (o formato esperado ainda existe?) e frescor (o dado é recente?) são verificadas à parte, no [plano de monitoramento](https://github.com/unb-mds/2026-2-Cerradinho-API/blob/dev/docs/fontes/plano-de-monitoramento.md).

## Rastreabilidade

- **PRs:** nenhum ainda.
- **Testes:** nenhum ainda.
