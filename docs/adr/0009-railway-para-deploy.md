# ADR 0009 — Railway para hospedagem

## Status
Substituído pelo [ADR 0011](0011-aws-lightsail-para-deploy.md), em 03/11/2026, antes de o deploy ser feito.

## Contexto
A Release 2 precisa estar implantada e acessível publicamente (RNF06). A produção precisa de PostgreSQL, Redis e pelo menos dois serviços (API e worker do Celery), dentro de um orçamento de projeto acadêmico sem patrocínio.

## Decisão
Hospedar API, banco, Redis e worker no Railway.

## Alternativas descartadas
- **Infraestrutura própria (VPS ou Kubernetes):** exigiria configurar e manter servidores. O Railway provisiona os serviços mais rápido.

## Consequências
- O projeto depende dos limites do plano gratuito ou educacional do Railway.
- As variáveis de ambiente de produção precisam ser configuradas no Railway, fora do repositório.
