# ADR 0003 — Celery e Redis para o agendamento

## Status
Aceito

## Contexto
Os dados precisam ser atualizados sem intervenção manual (RF15), e cada execução precisa registrar sucesso ou falha (RF16). O scraper do SIGAA percorre todas as unidades e pode levar bastante tempo.

## Decisão
Celery com Redis como broker. O Celery Beat agenda as tasks e um worker separado as executa. O agendamento fica em `backend/app/celery_app.py`, e o log de sucesso/falha usa os sinais `task_success` e `task_failure` do Celery.

## Alternativas descartadas
- **Cron simples:** resolve o agendamento, mas não oferece retries nem registro de execução de forma nativa; isso teria de ser escrito à mão.

## Consequências
- Mais dois serviços para operar (Redis e o worker, além do Beat), tanto no `docker-compose.yml` quanto em produção.
- O Redis também fica disponível para o cache da API ([ADR 0007](0007-cache-e-rate-limit-na-api.md)).
