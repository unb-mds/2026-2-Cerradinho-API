# Deploy no Railway

Como o Cerradinho sobe em produção no Railway ([ADR 0009](adr/0009-railway-para-deploy.md)), atendendo ao RNF06. O ambiente local continua sendo o `docker compose up` descrito no [README](https://github.com/unb-mds/2026-2-Cerradinho-API/blob/dev/README.md).

Nenhum segredo fica no repositório. Senhas e endereços são cadastrados nas variáveis de cada serviço, no painel do Railway.

## Serviços

O projeto no Railway tem os mesmos serviços do `docker-compose.yml`, com exceção do `migrate`, cujo comando passa a rodar no início da API.

| Serviço | Origem | Pasta raiz | Comando de início |
|---|---|---|---|
| Postgres | Banco gerenciado do Railway | | |
| Redis | Redis gerenciado do Railway | | |
| api | Este repositório, pelo `backend/Dockerfile` | `/backend` | `sh -c "alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port $PORT"` |
| worker | Este repositório, pelo `backend/Dockerfile` | `/backend` | `celery -A app.celery_app worker --loglevel=info --concurrency=1` |
| beat | Este repositório, pelo `backend/Dockerfile` | `/backend` | `celery -A app.celery_app beat --loglevel=info` |
| frontend | Este repositório | `/frontend` | `npm run start` (o build com `npm run build` é detectado pelo Railway) |

O `Dockerfile` do backend termina com `alembic upgrade head`, por isso cada serviço do backend precisa do próprio comando de início. A API roda as migrations antes de subir, e o worker só deve ser ligado depois do primeiro deploy da API, quando as tabelas já existem.

Se o plano gratuito não comportar todos os serviços, o beat pode rodar dentro do worker com `celery -A app.celery_app worker -B --loglevel=info --concurrency=1`. Nesse caso só pode existir um worker, senão os agendamentos rodam em dobro.

## Variáveis

O Railway gera as variáveis do Postgres e do Redis sozinho. Nos outros serviços, os valores que dependem deles são cadastrados como referência (`${{Serviço.VARIAVEL}}`), para acompanhar qualquer troca de senha ou endereço.

### api, worker e beat

Lidas em `backend/app/core/config.py`.

| Variável | Valor | Usada por |
|---|---|---|
| `POSTGRES_HOST` | `${{Postgres.PGHOST}}` | api, worker |
| `POSTGRES_PORT` | `${{Postgres.PGPORT}}` | api, worker |
| `POSTGRES_USER` | `${{Postgres.PGUSER}}` | api, worker |
| `POSTGRES_PASSWORD` | `${{Postgres.PGPASSWORD}}` | api, worker |
| `POSTGRES_DB` | `${{Postgres.PGDATABASE}}` | api, worker |
| `REDIS_URL` | `${{Redis.REDIS_URL}}` | worker, beat |
| `CORS_ORIGINS` | `["https://<endereço-do-frontend>"]` | api |

O `CORS_ORIGINS` é uma lista, então vai em JSON, com colchetes e aspas. Sem o endereço do frontend nele, o navegador bloqueia as chamadas à API.

No ambiente local o `REDIS_URL` não precisa ser definido, porque o padrão (`redis://redis:6379/0`) aponta para o serviço `redis` do docker compose.

### frontend

| Variável | Valor |
|---|---|
| `NEXT_PUBLIC_API_URL` | `https://<endereço-da-api>/v1` |

O Next.js grava as variáveis `NEXT_PUBLIC_` no código durante o build. Se o endereço da API mudar, é preciso fazer um novo deploy do frontend, porque reiniciar o serviço não basta.

## Ordem do primeiro deploy

1. Criar o projeto no Railway ligado ao repositório e adicionar o Postgres e o Redis.
2. Criar o serviço da API, cadastrar as variáveis e gerar um domínio público para ele.
3. Conferir se `https://<endereço-da-api>/docs` abre e se `/v1/disciplinas` responde, mesmo que vazio.
4. Criar o worker e o beat com as mesmas variáveis do banco e o `REDIS_URL`.
5. Criar o frontend com o `NEXT_PUBLIC_API_URL` e gerar um domínio público para ele.
6. Voltar na API e colocar o domínio do frontend no `CORS_ORIGINS`.

Para testar a coleta sem esperar o agendamento, as tasks podem ser disparadas uma vez pelo shell do worker, como no ambiente local.

## Pontos de atenção

- **Período letivo:** o ano e o período da coleta de disciplinas estão fixos em `backend/app/celery_app.py` e precisam ser atualizados antes de cada semestre.
- **Tamanho da imagem:** o `Dockerfile` instala o Chromium do Playwright, usado no scraper do SIGAA. A imagem fica grande e pode pesar no limite do plano gratuito. O deploy de teste da Sprint 6 serve para descobrir isso cedo.
- **Fuso horário:** o Celery usa `America/Sao_Paulo`, então os horários do agendamento não dependem do fuso do servidor.
