# ADR 0004 — Coleta desacoplada da API

## Status
Aceito

## Contexto
As fontes são lentas (o SIGAA exige navegador) e ficam fora do controle do time. Se a API buscasse os dados na fonte a cada requisição, o tempo de resposta e a disponibilidade da API dependeriam do SIGAA e do site do RU.

## Decisão
Os scrapers rodam agendados e gravam no PostgreSQL. A API só lê do banco e nunca dispara scraping durante uma requisição.

## Alternativas descartadas
- **Scraping sob demanda na requisição:** o dado estaria sempre fresco, mas a resposta levaria segundos ou minutos e falharia sempre que a fonte estivesse fora do ar.

## Consequências
- O dado da API é tão recente quanto a última execução agendada (semanal para disciplinas, diária para o cardápio).
- Uma falha na coleta não derruba a API: ela continua servindo o último dado gravado.
- O esquema do banco vira o ponto de integração entre coleta e API, então mudanças nele exigem migration.
