# Cerradinho

[![CI](https://github.com/unb-mds/2026-2-Cerradinho-API/actions/workflows/ci.yml/badge.svg?branch=dev)](https://github.com/unb-mds/2026-2-Cerradinho-API/actions/workflows/ci.yml)
[![Docs](https://img.shields.io/badge/docs-GitHub%20Pages-blue)](https://unb-mds.github.io/2026-2-Cerradinho-API/)
[![Licença MIT](https://img.shields.io/badge/licen%C3%A7a-MIT-green)](LICENSE)
[![Python 3.12](https://img.shields.io/badge/python-3.12-blue)](backend/README.md)
[![PRs bem-vindos](https://img.shields.io/badge/PRs-bem--vindos-brightgreen)](CONTRIBUTING.md)

**API aberta com os dados públicos da UnB.** Disciplinas, turmas, professores, salas vazias e o cardápio do RU numa API REST só, documentada e atualizada sozinha por scrapers agendados.

[Documentação da API](https://api.3-147-228-104.sslip.io/docs) · [Portal do desenvolvedor](https://3-147-228-104.sslip.io/desenvolvedores) · [Site de demonstração](https://3-147-228-104.sslip.io) · [Como contribuir](CONTRIBUTING.md)

> O Cerradinho não é um serviço oficial da UnB. Os dados são copiados do SIGAA e do site do RU e podem estar desatualizados ou incompletos. Para matrícula e decisões importantes, confira sempre a fonte oficial.

## Por que existe

Os dados da UnB estão espalhados em sistemas sem API pública, como o SIGAA e o site do RU. Quem quer usar esses dados num projeto acaba escrevendo o próprio scraper, que quebra na primeira mudança da fonte. O Cerradinho faz a coleta uma vez, normaliza o resultado e entrega tudo por uma API versionada, um SDK Python e uma CLI.

## A API é o produto, o site é um exemplo

O Cerradinho é a API. O [site](https://3-147-228-104.sslip.io) existe só para mostrar uma aplicação real do que dá para construir com esses dados. Ele foi pensado para o campus Gama, com salas livres agora, o RU de hoje e a agenda dos professores, e usa apenas as rotas públicas de `/v1`, sem nenhum acesso especial ao banco.

Qualquer pessoa pode fazer o mesmo para outro campus, um bot, um widget ou um app, usando a API, o SDK ou a CLI. O site não é o foco do projeto, e contribuições na API e na coleta têm prioridade.

## O que a API oferece

| Rota | O que devolve |
|---|---|
| `GET /v1/disciplinas` | Turmas com horário, sala e professores, com busca, filtro por departamento e paginação |
| `GET /v1/professores` | Docentes e as disciplinas de cada um, com busca por nome |
| `GET /v1/professores/{id}/agenda` | Agenda semanal do professor, com dia, início, fim e sala |
| `GET /v1/salas` | Salas e prédios, derivados das turmas |
| `GET /v1/salas/vazias` | Salas sem aula num dia e horário, ou num intervalo |
| `GET /v1/cardapio/semana` | Cardápio do RU da semana, por dia e refeição |
| `GET /v1/resumo` | Contagens de turmas, disciplinas, professores e salas |
| `GET /v1/execucoes` | Histórico das coletas, com sucesso e falha de cada uma |

A API aceita até 60 requisições por minuto por IP. Os detalhes de cada rota estão na [documentação interativa](https://api.3-147-228-104.sslip.io/docs).

## Começo rápido

Salas sem aula na segunda às 14h:

```bash
curl "https://api.3-147-228-104.sslip.io/v1/salas/vazias?dia=segunda&horario=14:00"
```

Com o [SDK Python](sdk/README.md), que também instala a CLI `cerradinho`:

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

## Rodar localmente

Precisa de Docker com Docker Compose e de Node.js 20 ou mais novo.

```bash
git clone https://github.com/unb-mds/2026-2-Cerradinho-API.git
cd 2026-2-Cerradinho-API
cp backend/.env.example backend/.env
docker compose up
```

Isso sobe o PostgreSQL, aplica as migrations e sobe a API em `http://localhost:8000`, junto com o Redis e o Celery. Para subir também o site de demonstração, em outro terminal:

```bash
cd frontend
cp .env.example .env.local
npm install
npm run dev
```

O site abre em `http://localhost:3000`. Testes, variáveis de ambiente e como rodar uma coleta na hora estão no [README do backend](backend/README.md).

## Como funciona

```
SIGAA, site do RU  →  scrapers (Celery)  →  PostgreSQL  →  API FastAPI /v1  →  site, SDK, CLI
                                                            ↳ cache e rate limit no Redis
```

| Parte | Tecnologias |
|---|---|
| Coleta | Playwright, requests, BeautifulSoup, pdfplumber |
| Agendamento | Celery, Redis |
| Banco | PostgreSQL 16, SQLAlchemy 2, Alembic |
| API | FastAPI, Pydantic |
| Site de demonstração | Next.js, Tailwind |
| SDK e CLI | httpx, Typer |
| Qualidade | pytest, schemathesis, ruff, bandit, GitHub Actions |

```
backend/    API, scrapers, tasks do Celery, migrations e testes
frontend/   site de demonstração em Next.js, que consome a API
sdk/        SDK e CLI em Python
docs/       documentação técnica, publicada no GitHub Pages
```

A arquitetura completa e as decisões de projeto estão no [site de documentação](https://unb-mds.github.io/2026-2-Cerradinho-API/).

## Fontes de dado

| Dado | Fonte | Atualização |
|---|---|---|
| Disciplinas, turmas, professores e salas | [SIGAA](https://sigaa.unb.br/sigaa/public/turmas/listar.jsf) | Todo domingo às 3h |
| Cardápio do RU (Darcy Ribeiro) | [Site do RU](https://ru.unb.br/cardapio) | Todo dia às 5h |

"Sala vazia" quer dizer sala sem aula cadastrada no SIGAA. Reserva informal e eventos não aparecem. Os riscos de cada fonte estão em [`docs/fontes/`](docs/fontes/).

## Contribuindo

Toda ajuda é bem-vinda, de código e documentação a um dado errado que você encontrou.

- **Achou um bug ou um dado errado?** Abra uma [issue](https://github.com/unb-mds/2026-2-Cerradinho-API/issues/new/choose).
- **Quer programar?** As issues com [`good first issue`](https://github.com/unb-mds/2026-2-Cerradinho-API/labels/good%20first%20issue) são um bom começo.
- **Tem uma ideia?** Abra uma issue de feature antes do código, para combinar o caminho.

O [CONTRIBUTING.md](CONTRIBUTING.md) explica como preparar o ambiente, rodar os testes e abrir um pull request. Quem participa segue o [Código de Conduta](CODE_OF_CONDUCT.md).

## Suporte e segurança

- Dúvidas e bugs vão nas [issues](https://github.com/unb-mds/2026-2-Cerradinho-API/issues).
- Falha de segurança não vai em issue pública. Siga a [política de segurança](SECURITY.md).
- O que mudou em cada versão está nas [Releases](https://github.com/unb-mds/2026-2-Cerradinho-API/releases) e no [CHANGELOG](CHANGELOG.md).

## Contribuidores

Gabriel, Vitor, Daniel, Arthur, João Paulo e Ítalo, estudantes da UnB FCTE, criaram o Cerradinho em 2026.

[![Contribuidores](https://contrib.rocks/image?repo=unb-mds/2026-2-Cerradinho-API)](https://github.com/unb-mds/2026-2-Cerradinho-API/graphs/contributors)

## Licença

Distribuído sob a licença MIT. Veja o arquivo [LICENSE](LICENSE).
