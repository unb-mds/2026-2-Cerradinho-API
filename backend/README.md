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

## Rodar os testes de contrato

Os testes em `tests/contract/` usam o `schemathesis` para gerar casos automaticamente a partir do `/openapi.json` da API e verificar se cada rota responde do jeito que está documentado (RNF04). Não precisa subir o servidor nem o Postgres: o schema é carregado direto do `app.main:app` e o banco é trocado por um SQLite em memória.

O `schemathesis` está no `requirements-dev.txt`:

```bash
cd backend
pip install -r requirements-dev.txt
pytest tests/contract
```

Os testes de contrato também rodam junto com o `pytest` geral. Se um deles falhar, a rota mudou o que retorna ou aceita sem atualizar o contrato — corrija a rota ou, se a mudança for intencional, discuta o versionamento da API (RF12) antes de alterar.

## Adicionando novos models

Depois de criar/alterar um model em `app/models/`, gere uma nova migration:

```bash
cd backend
alembic revision --autogenerate -m "descrição da mudança"
alembic upgrade head
```

## Nota para quem for mexer no `docker-compose.yml`

Esse arquivo é compartilhado — hoje só tem o serviço `db` (Postgres) e `migrate`. Ao adicionar Celery/Redis, adicione novos serviços no mesmo arquivo em vez de recriá-lo.
