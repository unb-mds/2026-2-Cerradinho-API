# ADR 0007 — Cache e rate limit na camada da API

## Status
Aceito (implementação na Release 2)

## Contexto
A API precisa responder rápido nas consultas frequentes (RNF02) e se proteger de abuso (RNF01), sem complicar a persistência.

## Decisão
Cache em Redis e rate limit com `slowapi`, ambos na camada da API (FastAPI), e não no banco de dados.

## Alternativas descartadas
- **Resolver no banco (índices, views materializadas, limites de conexão):** deixaria a persistência mais complexa e o controle de tráfego longe de onde a requisição entra.

## Consequências
- O Redis já usado pelo Celery ([ADR 0003](0003-celery-e-redis-para-agendamento.md)) passa a ter dois usos.
- O cache precisa ser renovado quando os scrapers gravam dado novo, senão a API serve dado antigo.
- As mudanças não podem alterar o formato das respostas: os testes de contrato precisam passar antes do merge.
