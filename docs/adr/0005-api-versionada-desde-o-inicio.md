# ADR 0005 — API versionada desde o início

## Status
Aceito

## Contexto
A API é pensada para ser consumida por outras squads e pelo SDK/CLI (RF13). Uma mudança no formato de uma resposta pode quebrar quem já integrou.

## Decisão
Todas as rotas nascem sob o prefixo `/v1/` (RF12). Mudança incompatível no formato vai para uma nova versão, sem alterar a `/v1/`. Os testes de contrato com schemathesis (RNF04) verificam no CI que as rotas continuam respondendo conforme o `/openapi.json`.

## Alternativas descartadas
- **Rotas sem versão, versionando só quando precisar:** mais simples no começo, mas obriga a quebrar os clientes existentes na primeira mudança incompatível.

## Consequências
- Mudanças que alteram campos existentes precisam ser discutidas antes, em vez de entrarem direto.
- Adicionar campos novos não quebra clientes e pode entrar na `/v1/`.
