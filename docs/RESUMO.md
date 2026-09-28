# Resumo do projeto — Cerradinho

API aberta que reúne dados públicos da UnB (disciplinas, professores, salas, cardápio do RU, eventos e editais), coletados automaticamente por scrapers. Atende estudantes, pelo site, e devs de outras squads, pela API.

## Objetivo

Os dados públicos da UnB estão espalhados em vários sistemas, como o SIGAA, o site do RU e a agenda de notícias. Por isso o estudante perde tempo consultando cada um, e cada squad que precisa desses dados refaz o próprio scraping. O objetivo é oferecer uma **API pública, unificada e versionada** que colete esses dados automaticamente e os disponibilize de forma estruturada e documentada, para que qualquer pessoa possa reutilizá-los.

## O que foi feito (Release 1, Sprints 0 a 3)

- Scraper de turmas do SIGAA e scraper do cardápio do RU (PDF semanal).
- Coleta agendada com Celery: disciplinas toda semana, cardápio todo dia, com log de execução.
- Banco PostgreSQL com migrations e ambiente completo subindo com `docker compose up`.
- API versionada com quatro rotas: `/v1/disciplinas`, `/v1/professores`, `/v1/salas` e `/v1/cardapio/semana`, com OpenAPI documentada.
- Frontend com uma tela para cada domínio, usando dado real.
- CI com lint, testes unitários, teste de integração com Postgres, testes de contrato e análise de segurança.

## O que vai ser feito (Release 2, Sprints 4 a 12, entrega em 25/11)

- **Sprint 4:** pendências da R1 (parser do RU para os novos PDFs, log consultável, duplicados na API, UX do cardápio).
- Novos domínios: eventos e editais.
- Features derivadas: salas vazias, agenda do professor e cardápio semanal.
- Cache e rate limit na API.
- SDK e CLI em Python e portal do desenvolvedor.
- Deploy público no Railway, monitoramento e cobertura de testes de 90%.

## Como (tecnologias)

| Parte | Tecnologias |
|---|---|
| Coleta | Playwright (SIGAA), requests, BeautifulSoup, pdfplumber (RU) |
| Agendamento | Celery, Redis |
| Banco | PostgreSQL 16, SQLAlchemy 2, Alembic |
| API | FastAPI, Pydantic |
| Frontend | Next.js, Axios, Tailwind |
| Qualidade | pytest, schemathesis, ruff, bandit, GitHub Actions |
| Infra | Docker Compose; Railway (R2) |
| R2 | slowapi (rate limit), Typer (CLI), UptimeRobot (monitoramento) |

Processo: Scrum com sprints de 1 semana, story map no Figma e decisões registradas em [ADRs](adr/).
