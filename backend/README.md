# Backend — Cerradinho

## Setup local

```bash
cp .env.example .env
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Subir o banco (PostgreSQL) e aplicar as migrations

Na raiz do repositório:

```bash
docker compose up
```

Isso sobe o Postgres e roda `alembic upgrade head` automaticamente (serviço `migrate`), criando as tabelas `professores`, `salas`, `disciplinas` e `cardapios`.

## Rodar migrations manualmente (sem Docker, contra um Postgres já rodando)

```bash
cd backend
alembic upgrade head
```

## Rodar os testes

```bash
cd backend
pytest
```

## Adicionando novos models

Depois de criar/alterar um model em `app/models/`, gere uma nova migration:

```bash
cd backend
alembic revision --autogenerate -m "descrição da mudança"
alembic upgrade head
```

## Nota para quem for mexer no `docker-compose.yml`

Esse arquivo é compartilhado — hoje só tem o serviço `db` (Postgres) e `migrate`. Ao adicionar Celery/Redis, adicione novos serviços no mesmo arquivo em vez de recriá-lo.
