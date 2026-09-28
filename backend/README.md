# Backend — Cerradinho

API FastAPI, scrapers, tasks Celery e migrations. A arquitetura está em [`docs/ARQUITETURA.md`](../docs/ARQUITETURA.md).

## Rodando com Docker (recomendado)

Na raiz do repositório:

```bash
cp backend/.env.example backend/.env
docker compose up
```

| Serviço | O que faz |
|---|---|
| `db` | PostgreSQL 16 na porta 5432 |
| `migrate` | Roda `alembic upgrade head` e termina |
| `api` | API em `http://localhost:8000`, com recarga automática ao editar o código |
| `redis` | Broker do Celery, na porta 6379 |
| `celery_worker` | Executa as tasks de scraping |
| `celery_beat` | Dispara as tasks nos horários agendados |

A documentação interativa fica em `http://localhost:8000/docs`.

Para rodar uma task na hora, sem esperar o agendamento:

```bash
docker compose exec celery_worker celery -A app.celery_app call app.tasks.cardapio.scrape_cardapio_task
```

## Rodando sem Docker

Precisa de um PostgreSQL acessível com os dados do `.env` (`POSTGRES_HOST=localhost`).

```bash
cd backend
cp .env.example .env
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
playwright install chromium
alembic upgrade head
uvicorn app.main:app --reload
```

## Variáveis de ambiente

Lidas de `backend/.env` por `app/core/config.py`.

| Variável | Padrão | Uso |
|---|---|---|
| `POSTGRES_USER` | `cerradinho` | Usuário do banco |
| `POSTGRES_PASSWORD` | `cerradinho` | Senha do banco |
| `POSTGRES_DB` | `cerradinho` | Nome do banco |
| `POSTGRES_HOST` | `localhost` | Host do banco (o Docker Compose troca para `db`) |
| `POSTGRES_PORT` | `5432` | Porta do banco |
| `CORS_ORIGINS` | `localhost:3000` e `127.0.0.1:3000` | Origens que podem chamar a API pelo navegador |

## Testes

Com a venv ativa, dentro de `backend/`:

| Comando | O que roda |
|---|---|
| `pytest` | Tudo |
| `pytest --cov=app` | Tudo, com relatório de cobertura |
| `pytest tests/contract` | Testes de contrato: o schemathesis gera casos a partir do `/openapi.json` e confere se cada rota responde como documentado (RNF04). Usam SQLite em memória, sem servidor nem Postgres |
| `pytest tests/integration` | Pipeline de disciplinas de ponta a ponta num Postgres real (fixture do SIGAA → parser → persistência). Precisam do banco do Docker Compose rodando; sem ele, são pulados |
| `ruff check .` | Lint |
| `bandit -r app -lll` | Análise de segurança (falha em achado alto) |

No CI todos rodam a cada push, e os testes de integração têm um Postgres próprio.

Se um teste de contrato falhar, a rota mudou o que aceita ou devolve sem atualizar o contrato. Corrija a rota ou, se a mudança for intencional, discuta o versionamento antes ([ADR 0005](../docs/adr/0005-api-versionada-desde-o-inicio.md)).

## Migrations

Depois de criar ou alterar um model em `app/models/`:

```bash
alembic revision --autogenerate -m "descrição da mudança"
alembic upgrade head
```

Confira o arquivo gerado em `alembic/versions/` antes de commitar: o autogenerate não detecta tudo (por exemplo, renomear coluna).
