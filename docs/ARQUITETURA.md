# Arquitetura — Cerradinho

Como o sistema é construído. O que ele precisa fazer está em [REQUISITOS.md](REQUISITOS.md); as decisões técnicas e seus motivos estão nos [ADRs](adr/).

## Visão geral

A coleta e a API são separadas: scrapers agendados gravam no PostgreSQL, e a API só lê do banco. Uma requisição à API nunca depende de o SIGAA ou o site do RU estarem no ar naquele momento ([ADR 0004](adr/0004-coleta-desacoplada-da-api.md)).

```mermaid
flowchart LR
    subgraph Fontes["Fontes públicas"]
        SIGAA[SIGAA público]
        RU[Site do RU]
        NOT[Agenda de notícias]
    end

    subgraph Coleta["Coleta"]
        CELERY[Celery Beat + Worker]
        SCRAPER[Scrapers<br/>Playwright / requests]
        PARSER[Parsers<br/>BeautifulSoup / pdfplumber]
    end

    DB[(PostgreSQL)]

    subgraph API["API /v1"]
        FASTAPI[FastAPI]
        CACHE[Cache Redis]
        RATE[Rate limit]
    end

    subgraph Consumo["Consumo"]
        FRONT[Frontend Next.js]
        SWAGGER[Swagger /docs]
        SDK[SDK / CLI]
    end

    CELERY --> SCRAPER
    SIGAA --> SCRAPER
    RU --> SCRAPER
    NOT --> SCRAPER
    SCRAPER --> PARSER --> DB
    DB --> FASTAPI
    FASTAPI --> CACHE
    FASTAPI --> RATE
    FASTAPI --> FRONT
    FASTAPI --> SWAGGER
    FASTAPI --> SDK

    classDef planejado stroke-dasharray: 5 5
    class NOT,CACHE,RATE,SDK planejado
```

Os elementos tracejados entram na Release 2.

## Fluxo de coleta

```mermaid
sequenceDiagram
    participant Beat as Celery Beat
    participant Worker as Celery Worker
    participant Fonte as Fonte pública
    participant DB as PostgreSQL

    Beat->>Worker: dispara a task no horário agendado
    Worker->>Fonte: baixa HTML/PDF (com throttling)
    Fonte-->>Worker: conteúdo bruto
    Worker->>Worker: parser + validação no schema Pydantic
    Worker->>DB: upsert (não duplica em reexecuções)
    Worker->>Worker: log de sucesso ou falha (RF16)
```

| Task | Fonte | Quando roda |
|---|---|---|
| `scrape_disciplinas_task` | SIGAA, todas as unidades | Domingo, 3h (`America/Sao_Paulo`) |
| `scrape_cardapio_task` | PDF semanal do RU (Darcy Ribeiro) | Todo dia, 5h |

O agendamento fica em `backend/app/celery_app.py`. O período letivo (`ano`/`periodo`) da task de disciplinas é fixo no código e precisa ser atualizado a cada semestre, porque o SIGAA público não expõe o período corrente.

## Componentes

| Componente | Responsabilidade | Tecnologia | Release |
|---|---|---|---|
| Scrapers e parsers | Capturar e validar dados das fontes | Playwright, requests, BeautifulSoup, pdfplumber | R1 (SIGAA, RU), R2 (eventos, editais) |
| Agendador | Disparar os scrapers e registrar sucesso/falha | Celery, Redis | R1 |
| Banco de dados | Guardar os dados normalizados | PostgreSQL 16, SQLAlchemy 2 (síncrono), Alembic | R1 |
| API | Expor os dados via REST versionado | FastAPI | R1 |
| Frontend | Telas de consulta que consomem a API | Next.js, Axios, Tailwind | R1 |
| Documentação da API | Referência interativa das rotas | OpenAPI/Swagger (gerado pelo FastAPI) | R1 |
| CI | Lint, SAST, testes unitários, de contrato e de integração a cada push | GitHub Actions, ruff, bandit, pytest, schemathesis | R1 |
| Cache | Reduzir carga no banco em consultas frequentes | Redis | R2 |
| Rate limit | Limitar requisições por cliente | slowapi | R2 |
| Portal do desenvolvedor | Guia de uso além do Swagger | Next.js | R2 |
| SDK e CLI | Integração de terceiros sem HTTP manual | Python, Typer | R2 |
| Observabilidade | Monitorar uptime e alertar | UptimeRobot | R2 |
| Hospedagem | API, banco, Redis e worker em produção | Railway | R2 |

## Rotas da API

Todas sob `/v1/` ([ADR 0005](adr/0005-api-versionada-desde-o-inicio.md)). A documentação completa, com exemplos, fica em `/docs` com a API rodando.

| Rota | Retorna |
|---|---|
| `GET /v1/disciplinas` | Turmas com professores, horários, sala e vagas |
| `GET /v1/professores` | Docentes e os códigos das disciplinas de cada um |
| `GET /v1/salas` | Salas com prédio e nome separados |
| `GET /v1/cardapio/semana?data_inicio=` | Itens do cardápio de 7 dias, por refeição e categoria |

## Camadas do backend

| Camada | Pasta | Pode | Não pode |
|---|---|---|---|
| Scraper | `app/scrapers/<dominio>/scraper.py` | Acessar a fonte e devolver o conteúdo bruto | Parsear, gravar no banco |
| Parser | `app/scrapers/<dominio>/parser.py` | Transformar o conteúdo bruto no contrato Pydantic | Acessar rede ou banco |
| Contrato | `app/schemas/` | Definir o formato validado que sai do scraper | Ter regra de negócio |
| Domínio | `app/domain/` | Normalizar, persistir e montar respostas | Conhecer HTTP |
| Model | `app/models/` | Mapear as tabelas (SQLAlchemy) | Ter regra de negócio |
| Router | `app/routers/` | Receber a requisição e chamar o domínio | Consultar o banco direto, fazer scraping |
| Task | `app/tasks/` | Orquestrar scraper → parser → domínio | Ter regra de negócio |

Os schemas de resposta que diferem do contrato do scraper ficam em `app/schemas/api/` (por exemplo, `Docente` e `Espaco`).

## Modelo de dados

```mermaid
erDiagram
    DISCIPLINA ||--o{ TURMA : oferta
    TURMA }o--o| SALA : "tem aula em"
    TURMA }o--o{ PROFESSOR : "é dada por"
    TURMA ||--o{ HORARIO : tem
    CARDAPIO
```

`Turma` é única por (disciplina, número, ano/período), o que permite reexecutar o scraper sem duplicar. `Cardapio` guarda um dia por linha, com café, almoço e jantar em texto.

## Estrutura de pastas

```
2026-2-Cerradinho-API/
├── backend/
│   ├── app/
│   │   ├── core/          # configuração e sessão do banco
│   │   ├── domain/        # regras de negócio e persistência
│   │   ├── models/        # SQLAlchemy
│   │   ├── routers/       # rotas /v1
│   │   ├── schemas/       # contratos Pydantic (api/ = respostas da API)
│   │   ├── scrapers/      # um pacote por fonte (scraper + parser)
│   │   ├── tasks/         # tasks Celery e sinais de log
│   │   ├── celery_app.py  # agendamento
│   │   └── main.py        # app FastAPI
│   ├── alembic/           # migrations
│   └── tests/             # unit, contract, integration, routers, scrapers, tasks
├── frontend/
│   ├── app/               # páginas (App Router)
│   ├── components/        # componentes visuais
│   ├── hooks/             # chamadas à API, isoladas das telas
│   └── lib/               # cliente Axios
├── sdk/                   # SDK/CLI Python (Release 2)
├── docs/                  # documentação (índice em docs/README.md)
├── .github/               # CI, templates de issue e PR
└── docker-compose.yml     # db, migrate, api, redis, celery_worker, celery_beat
```

## Decisões de arquitetura

Cada decisão relevante tem um ADR em [`docs/adr/`](adr/):

| ADR | Decisão |
|---|---|
| [0001](adr/0001-base-tecnica-backend.md) | Python 3.12, SQLAlchemy síncrono, `requirements.txt` |
| [0002](adr/0002-ferramentas-de-scraping.md) | Playwright para o SIGAA; requests + BeautifulSoup/pdfplumber para as demais fontes |
| [0003](adr/0003-celery-e-redis-para-agendamento.md) | Celery e Redis para o agendamento |
| [0004](adr/0004-coleta-desacoplada-da-api.md) | Coleta desacoplada da API |
| [0005](adr/0005-api-versionada-desde-o-inicio.md) | API versionada desde o início (`/v1/`) |
| [0006](adr/0006-salas-derivadas-das-turmas.md) | Salas derivadas das turmas, sem scraper próprio |
| [0007](adr/0007-cache-e-rate-limit-na-api.md) | Cache e rate limit na camada da API |
| [0008](adr/0008-bandit-como-sast.md) | Bandit como análise estática de segurança |
| [0009](adr/0009-railway-para-deploy.md) | Railway para hospedagem |

Os padrões de código (separação de camadas, nomenclatura, tratamento de erro) estão no [CONTRIBUTING.md](../CONTRIBUTING.md).
