# ADR 001 — Base técnica do backend (Python, SQLAlchemy síncrono, dependências)

## Status
Aceito

## Contexto
`ARQUITETURA.md` já definia a stack em nível de tecnologia (Python/FastAPI, SQLAlchemy, Alembic, PostgreSQL), mas nenhuma decisão concreta de projeto tinha sido tomada: versão do Python, driver de banco, SQLAlchemy síncrono ou assíncrono, e formato do arquivo de dependências. Como essas escolhas afetam todo código Python do backend — não só o schema inicial da issue #64 — precisavam ser fechadas antes do primeiro código ser escrito.

## Decisão
- Python 3.12
- SQLAlchemy 2.0, estilo síncrono (`Session`, não `AsyncSession`)
- Driver `psycopg2-binary` para conexão com PostgreSQL
- Dependências listadas em `backend/requirements.txt` (sem Poetry/Pipenv)
- Configuração via `pydantic-settings`, lendo de `backend/.env`

## Alternativas descartadas
- **SQLAlchemy assíncrono + `asyncpg`**: mais alinhado ao uso comum de FastAPI, mas adiciona complexidade (async/await em toda a camada de dados) sem necessidade clara no volume de dados do projeto; os scrapers agendados via Celery tendem a se integrar melhor com código síncrono.
- **Poetry/Pipenv**: adiciona uma ferramenta extra de gerenciamento de dependências; `requirements.txt` é suficiente pro tamanho atual do projeto.

## Consequências
- Qualquer código futuro que acesse o banco (routers da API, scrapers) deve seguir o padrão síncrono estabelecido aqui, para não misturar os dois estilos no mesmo projeto.
- Se o volume de requisições da API exigir depois, migrar para async é uma mudança grande (revisão de toda a camada de acesso a dados), não incremental.
