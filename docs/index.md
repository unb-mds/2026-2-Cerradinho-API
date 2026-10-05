# Cerradinho

API aberta da UnB — dados institucionais reunidos num só lugar: disciplinas, professores, salas e cardápio do RU, coletados automaticamente por scrapers agendados a partir só de fontes públicas.

Projeto da disciplina de Métodos de Desenvolvimento de Software (MDS), UnB FCTE, 2026/2.

## Visão geral

O Cerradinho não produz dado próprio. Os dados hoje ficam espalhados em vários sistemas da UnB — SIGAA, site do RU — cada um com sua própria interface, sem API pública. O Cerradinho raspa essas fontes, normaliza o resultado, e expõe tudo por uma API REST única, versionada e documentada.

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

A documentação interativa da API (Swagger) fica em `/docs` com o projeto rodando localmente.

## Como navegar esta documentação

- **[Produto](DOCUMENTO-VISAO.md)** — por que o Cerradinho existe, pra quem, e o que ele entrega: visão de produto e requisitos.
- **[Arquitetura](ARQUITETURA.md)** — como o sistema é construído: componentes, camadas, as decisões de arquitetura (ADRs) e a ficha de cada fonte de dado com seus riscos.
- **[Processo](PROCESSO.md)** — como o time trabalha: papéis, ritos do Scrum e Definition of Done.
- **[Gestão](scrum/sprint-planning.md)** — o dia a dia do Scrum: planejamento de sprints, atas de reunião e o checklist da release.
- **[Estudos](estudos/estudo-git-github.md)** — o material que cada pessoa produziu antes de começar sua parte, da fundamentação técnica até as ferramentas usadas.

## Stack

| Parte | Tecnologias |
|---|---|
| Coleta | Playwright, requests, BeautifulSoup, pdfplumber |
| Agendamento | Celery, Redis |
| Banco | PostgreSQL 16, SQLAlchemy 2, Alembic |
| API | FastAPI, Pydantic |
| Frontend | Next.js, Axios, Tailwind |
| Qualidade | pytest, schemathesis, ruff, bandit, GitHub Actions |

## Time

| Pessoa | Papel |
|---|---|
| Gabriel | Product Owner; Banco de Dados |
| Vitor | Scrum Master; Backend |
| Ítalo | Backend |
| Daniel | Frontend |
| Arthur | Backend; Agendamento e Cache |
| João Paulo | QA; Testes e CI |

---

Código-fonte, issues e pull requests: [github.com/unb-mds/2026-2-Cerradinho-API](https://github.com/unb-mds/2026-2-Cerradinho-API). Como rodar o projeto localmente está no [README do repositório](https://github.com/unb-mds/2026-2-Cerradinho-API#como-rodar).
