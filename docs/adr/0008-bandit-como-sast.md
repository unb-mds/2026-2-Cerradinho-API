# ADR 0008 — Bandit como análise estática de segurança

## Status
Aceito

## Contexto
O RNF08 exige análise estática de segurança (SAST) no pipeline, com achados críticos ou altos bloqueando a entrega.

## Decisão
Bandit no CI (`bandit -r app -lll`), rodando a cada push junto com lint e testes. Achado de severidade alta faz o CI falhar.

## Alternativas descartadas
- **Semgrep:** mais configurável, mas exige mais configuração para o mesmo objetivo. O Bandit é leve, feito para Python e não precisa de infraestrutura extra.

## Consequências
- A análise cobre só o backend Python. O frontend não tem SAST.
