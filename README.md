# Cerradinho — API aberta da UnB

API pública que reúne, num só lugar, dados institucionais da UnB hoje espalhados em vários sistemas: disciplinas, professores, salas e cardápio do RU, com eventos e editais a caminho. Os dados vêm só de fontes públicas e são coletados automaticamente por scrapers agendados.

Projeto da disciplina de Métodos de Desenvolvimento de Software (MDS), UnB FCTE, 2026/2.

## Para quem é

- **Estudantes**, que consultam turmas, salas e cardápio pelo site, sem abrir o SIGAA e o site do RU.
- **Devs de outras squads**, que usam os dados nos próprios projetos pela API, sem refazer scraping.

## O que já funciona

| Domínio | Rota | Fonte | Atualização |
|---|---|---|---|
| Disciplinas e turmas | `GET /v1/disciplinas` | SIGAA público | Semanal |
| Professores | `GET /v1/professores` | Derivado das turmas | Semanal |
| Salas e prédios | `GET /v1/salas` | Derivado das turmas | Semanal |
| Cardápio do RU | `GET /v1/cardapio/semana` | PDF semanal do RU | Diária |

A documentação interativa da API fica em `http://localhost:8000/docs` com o projeto rodando. O frontend tem uma tela para cada domínio.

Na Release 2 entram eventos, editais, salas vazias, agenda do professor, cache, rate limit, SDK/CLI em Python, portal do desenvolvedor e a API em produção. O plano está no [planejamento de sprints](docs/scrum/sprint-planning.md).

## Stack

| Parte | Tecnologias |
|---|---|
| Coleta | Playwright, requests, BeautifulSoup, pdfplumber |
| Agendamento | Celery, Redis |
| Banco | PostgreSQL 16, SQLAlchemy 2, Alembic |
| API | FastAPI, Pydantic |
| Frontend | Next.js, Axios, Tailwind |
| Qualidade | pytest, schemathesis, ruff, bandit, GitHub Actions |

## Como rodar

Pré-requisitos: Docker com Docker Compose, e Node.js para o frontend.

```bash
cp backend/.env.example backend/.env
docker compose up
```

Isso sobe o PostgreSQL, aplica as migrations, e sobe a API em `http://localhost:8000`, o Redis, o worker e o agendador do Celery. Para o frontend:

```bash
cd frontend
cp .env.example .env.local
npm install
npm run dev
```

O site abre em `http://localhost:3000`. Detalhes de cada parte, testes e variáveis de ambiente estão no [README do backend](backend/README.md) e no [README do frontend](frontend/README.md).

## Estrutura

```
backend/    API FastAPI, scrapers, tasks Celery, migrations e testes
frontend/   telas de consulta em Next.js
sdk/        SDK/CLI em Python (Release 2)
docs/       documentação do projeto
```

## Documentação

| Documento | Conteúdo |
|---|---|
| [Documento de Visão](docs/DOCUMENTO-VISAO.md) | Problema, personas, escopo e prioridades |
| [Requisitos](docs/REQUISITOS.md) | Fontes de dado, requisitos funcionais e não funcionais, rastreabilidade |
| [Arquitetura](docs/ARQUITETURA.md) | Componentes, fluxo de coleta, camadas, modelo de dados |
| [Decisões (ADRs)](docs/adr/) | O que foi decidido e por quê |
| [Processo](docs/PROCESSO.md) | Papéis, sprints, ritos e Definition of Done |
| [Planejamento de sprints](docs/scrum/sprint-planning.md) | Calendário e entregas por sprint |
| [Atas](docs/scrum/atas.md) | Registro das reuniões |
| [Como contribuir](CONTRIBUTING.md) | Branches, commits, PRs e padrões de código |
| [Uso de IA](AI-USAGE.md) | Registro de uso de IA no projeto |
| [Índice completo](docs/README.md) | Todos os documentos, incluindo fontes de dado e estudos |

Quadro do time no Figma: [CERRADINHO](https://www.figma.com/board/5rJtm9JjYyqqEBMOvzG3Z0/CERRADINHO?node-id=0-1&p=f&t=OicOccXWe0GMmKtB-0).

## Time

| Pessoa | Papel |
|---|---|
| Gabriel | Product Owner; banco, Docker e deploy |
| Vitor | Scrum Master; scraping de disciplinas |
| Ítalo | Scraping do RU, eventos e editais |
| Daniel | Frontend e portal do desenvolvedor |
| Arthur | Agendamento, cache e rate limit |
| João Paulo | QA, testes de contrato e CI |
