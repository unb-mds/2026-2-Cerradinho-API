# Cerradinho

API aberta com os dados públicos da UnB. Disciplinas, turmas, professores, salas vazias e o cardápio do RU numa API REST só, documentada e atualizada sozinha por scrapers agendados.

!!! warning "Não é um serviço oficial da UnB"
    Os dados são copiados do SIGAA e do site do RU e podem estar desatualizados ou incompletos. Para matrícula e decisões importantes, confira sempre a fonte oficial.

## Comece por aqui

- **Quero usar os dados.** A [documentação interativa da API](https://api.3-147-228-104.sslip.io/docs) tem todas as rotas, e o [portal do desenvolvedor](https://3-147-228-104.sslip.io/desenvolvedores) tem exemplos em curl, Python e JavaScript. Para Python, há o [SDK e a CLI](https://github.com/unb-mds/2026-2-Cerradinho-API/blob/dev/sdk/README.md).
- **Quero entender como funciona.** A [Arquitetura](ARQUITETURA.md) mostra os componentes e o fluxo da coleta, e as [decisões de arquitetura](adr/0001-base-tecnica-backend.md) explicam o porquê de cada escolha.
- **Quero contribuir.** O [guia de contribuição](CONTRIBUIR.md) explica como preparar o ambiente, rodar os testes e abrir um pull request.

## A API é o produto, o site é um exemplo

O Cerradinho é a API. O [site](https://3-147-228-104.sslip.io) é só uma demonstração do que dá para construir com esses dados, pensada para o campus Gama, e usa apenas as rotas públicas de `/v1`. Qualquer pessoa pode construir outra aplicação, para outro campus ou outro uso, com a API, o SDK ou a CLI.

## O que a API oferece

| Rota | O que devolve | Fonte | Atualização |
|---|---|---|---|
| `GET /v1/disciplinas` | Turmas com horário, sala e professores | SIGAA | Semanal |
| `GET /v1/professores` | Docentes e as disciplinas de cada um | Derivado das turmas | Semanal |
| `GET /v1/professores/{id}/agenda` | Agenda semanal do professor | Derivado das turmas | Semanal |
| `GET /v1/salas` | Salas e prédios | Derivado das turmas | Semanal |
| `GET /v1/salas/vazias` | Salas sem aula num dia e horário | Derivado das turmas | Semanal |
| `GET /v1/cardapio/semana` | Cardápio do RU por dia e refeição | PDF do RU | Diária |
| `GET /v1/resumo` | Contagens de turmas, disciplinas, professores e salas | Derivado | Semanal |
| `GET /v1/execucoes` | Histórico das coletas | Próprio | A cada coleta |

## Stack

| Parte | Tecnologias |
|---|---|
| Coleta | Playwright, requests, BeautifulSoup, pdfplumber |
| Agendamento | Celery, Redis |
| Banco | PostgreSQL 16, SQLAlchemy 2, Alembic |
| API | FastAPI, Pydantic |
| Site de demonstração | Next.js, Tailwind |
| SDK e CLI | httpx, Typer |
| Qualidade | pytest, schemathesis, ruff, bandit, GitHub Actions |

## Histórico do projeto

O Cerradinho começou em 2026 como projeto de estudantes da UnB FCTE. A visão de produto, os requisitos, o processo, as atas e os estudos dessa fase ficam na seção [Histórico](DOCUMENTO-VISAO.md), como registro.

---

Código-fonte, issues e pull requests em [github.com/unb-mds/2026-2-Cerradinho-API](https://github.com/unb-mds/2026-2-Cerradinho-API). Licença MIT.
