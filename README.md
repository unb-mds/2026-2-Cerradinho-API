# Cerradinho

[![CI](https://github.com/unb-mds/2026-2-Cerradinho-API/actions/workflows/ci.yml/badge.svg?branch=dev)](https://github.com/unb-mds/2026-2-Cerradinho-API/actions/workflows/ci.yml)
[![Docs](https://img.shields.io/badge/docs-GitHub%20Pages-blue)](https://unb-mds.github.io/2026-2-Cerradinho-API/)
[![Licença MIT](https://img.shields.io/badge/licen%C3%A7a-MIT-green)](LICENSE)
[![Python 3.12](https://img.shields.io/badge/python-3.12-blue)](backend/README.md)

API aberta da UnB. Reúne num só lugar dados institucionais hoje espalhados em vários sistemas, como disciplinas, professores, salas vazias e o cardápio do RU. Os dados vêm só de fontes públicas e são coletados automaticamente por scrapers agendados.

Projeto da disciplina de Métodos de Desenvolvimento de Software (MDS), UnB FCTE, 2026/2.

> O Cerradinho não é um serviço oficial da UnB. Os dados são copiados do SIGAA e do site do RU e podem estar desatualizados ou incompletos. Para matrícula e decisões importantes, confira sempre a fonte oficial.

## Em produção

- Site: [https://3-147-228-104.sslip.io](https://3-147-228-104.sslip.io)
- API: [https://api.3-147-228-104.sslip.io/v1](https://api.3-147-228-104.sslip.io/docs), com a documentação interativa em [`/docs`](https://api.3-147-228-104.sslip.io/docs)

Como a produção sobe está em [`docs/DEPLOY.md`](docs/DEPLOY.md).

## Exemplo de uso

Salas sem aula na segunda às 14h, direto pela API:

```bash
curl "https://api.3-147-228-104.sslip.io/v1/salas/vazias?dia=segunda&horario=14:00"
```

O mesmo pelo [SDK Python](sdk/README.md), que também instala a CLI `cerradinho`:

```bash
pip install "git+https://github.com/unb-mds/2026-2-Cerradinho-API.git#subdirectory=sdk"
```

```python
from cerradinho_sdk import CerradinhoClient

with CerradinhoClient("https://api.3-147-228-104.sslip.io") as cerradinho:
    salas = cerradinho.listar_salas_vazias(dia="segunda", horario="14:00")
    cardapio = cerradinho.obter_cardapio_semana()
```

```bash
export CERRADINHO_API_URL=https://api.3-147-228-104.sslip.io
cerradinho salas-vazias segunda 14:00
```

Todas as rotas estão na [documentação interativa](https://api.3-147-228-104.sslip.io/docs) e no [portal do desenvolvedor](https://3-147-228-104.sslip.io/desenvolvedores). A API aceita até 60 requisições por minuto por IP.

## Fontes de dado

| Dado | Fonte | Atualização |
|---|---|---|
| Disciplinas, turmas, professores e salas | [SIGAA](https://sigaa.unb.br/sigaa/public/turmas/listar.jsf) | Todo domingo às 3h |
| Cardápio do RU (Darcy Ribeiro) | [Site do RU](https://ru.unb.br/cardapio) | Todo dia às 5h |

"Sala vazia" quer dizer sala sem aula cadastrada no SIGAA. Reserva informal e eventos não aparecem. As limitações de cada fonte estão em [`docs/fontes/`](docs/fontes/).

## Para quem é

- **Estudantes**, que consultam turmas, salas e cardápio pelo site, sem abrir o SIGAA e o site do RU.
- **Devs de outras squads**, que usam os dados nos próprios projetos pela API, sem refazer scraping.

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
sdk/        SDK e CLI em Python
docs/       documentação do projeto
specs/      um arquivo por requisito, com critérios e rastreabilidade
```

## Documentação

| Documento | Conteúdo |
|---|---|
| [Documento de Visão](docs/DOCUMENTO-VISAO.md) | Problema, personas, escopo e prioridades |
| [Requisitos](docs/REQUISITOS.md) | Objetivo, fontes de dado e mapa dos requisitos |
| [Especificação](specs/README.md) | Um arquivo por requisito, com critérios de aceitação, regra de negócio e rastreabilidade |
| [Arquitetura](docs/ARQUITETURA.md) | Componentes, fluxo de coleta, camadas, modelo de dados |
| [Decisões (ADRs)](docs/adr/) | O que foi decidido e por quê |
| [Processo](docs/PROCESSO.md) | Papéis, sprints, ritos e Definition of Done |
| [Planejamento de sprints](docs/scrum/sprint-planning.md) | Calendário e entregas por sprint |
| [Atas](docs/scrum/atas.md) | Registro das reuniões |
| [Como contribuir](CONTRIBUTING.md) | Branches, commits, PRs e padrões de código |
| [Uso de IA](AI-USAGE.md) | Registro de uso de IA no projeto |
| [Changelog](CHANGELOG.md) | Histórico de versões |
| [Código de Conduta](CODE_OF_CONDUCT.md) | Regras de convivência no projeto |
| [Índice completo](docs/indice-completo.md) | Todos os documentos, incluindo fontes de dado e estudos |

Quadro do time no Figma: [CERRADINHO](https://www.figma.com/board/Xn4RLNLqWrNfUc7Zqxmmyq/Cerradinho---Story-Map?node-id=0-1&t=PSvWZ4M5sZV4Ru8U-1).

## Time

| Pessoa | Papel |
|---|---|
| Gabriel | Product Owner; banco, Docker, deploy e cardápio do RU |
| Vitor | Scrum Master; scraping de disciplinas, features derivadas e SDK |
| Daniel | Frontend e portal do desenvolvedor |
| Arthur | Agendamento, cache e rate limit |
| João Paulo | QA, testes de contrato, CI e CLI |

O Ítalo participou da Release 1 (scraping do RU) e saiu do projeto no início da Release 2.

## Como contribuir

Contribuições de fora do time são bem-vindas. O [CONTRIBUTING.md](CONTRIBUTING.md) explica como rodar os testes e abrir um pull request, e as issues marcadas com [`good first issue`](https://github.com/unb-mds/2026-2-Cerradinho-API/labels/good%20first%20issue) são um bom começo. Quem participa segue o [Código de Conduta](CODE_OF_CONDUCT.md).

## Suporte

- Bug ou dado errado: abra uma [issue](https://github.com/unb-mds/2026-2-Cerradinho-API/issues/new/choose).
- Falha de segurança: siga a [política de segurança](SECURITY.md) e não abra issue pública.

## Status

O desenvolvimento ativo vai até a entrega da Release 2, em 25/11/2026. As versões e o que mudou em cada uma estão nas [Releases](https://github.com/unb-mds/2026-2-Cerradinho-API/releases) e no [Changelog](CHANGELOG.md).

## Licença

Distribuído sob a licença MIT. Veja o arquivo [LICENSE](LICENSE).
