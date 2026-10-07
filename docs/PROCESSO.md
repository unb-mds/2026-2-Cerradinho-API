# Processo — Cerradinho

Como o time se organiza: papéis, ritos do Scrum, critérios de pronto e registro do trabalho. As regras de git, pull request e código estão no [CONTRIBUTING.md](https://github.com/unb-mds/2026-2-Cerradinho-API/blob/dev/CONTRIBUTING.md).

## 1. Papéis

| Pessoa | Papel | Área | Tecnologias |
|---|---|---|---|
| Gabriel | Product Owner | Banco, Docker, deploy, release notes; prioriza o backlog e define critérios de aceitação | PostgreSQL, SQLAlchemy, Alembic, Docker, Railway |
| Vitor | Scrum Master | Scraping de Disciplinas/Professores/Salas e endpoints; facilita os ritos e o board | Playwright, FastAPI, SQLAlchemy |
| Ítalo | Desenvolvedor | Scraping de RU, Eventos e Editais e endpoints | BeautifulSoup, pdfplumber, FastAPI |
| Daniel | Desenvolvedor | Frontend e portal do desenvolvedor | Next.js, Axios, Swagger UI |
| Arthur | Desenvolvedor | Agendamento, cache e rate limit | Celery, Redis, slowapi |
| João Paulo | QA/Integração | Fontes de dado, testes de contrato, CI, observabilidade | pytest, schemathesis, UptimeRobot |

Quem responde por cada requisito está na [rastreabilidade do REQUISITOS.md](REQUISITOS.md#6-rastreabilidade).

## 2. Sprints e ritos

Sprints de **1 semana**, de segunda a segunda. O calendário e o que entra em cada sprint estão no [planejamento de sprints](scrum/sprint-planning.md).

| Reunião | Quando | Para quê |
|---|---|---|
| Principal | Segunda-feira, após a aula | Review da sprint que terminou, retrospectiva curta e planning da próxima |
| Acompanhamento | Quinta-feira, 19h | Andamento das tarefas, bloqueios e dependências entre as áreas |
| Emergencial | Sob demanda | Bug crítico ou decisão que não pode esperar a próxima reunião |

Dúvidas rápidas e alinhamentos simples ficam no grupo de mensagens do time, sem reunião.

Toda reunião é registrada nas [atas](scrum/atas.md), com lista de presença. Planning, review e retrospectiva são registrados em todas as sprints, inclusive nas últimas.

## 3. Definition of Done

Uma tarefa de código está pronta quando:

1. o PR foi aprovado por pelo menos um outro membro, com a revisão registrada no próprio PR;
2. os testes unitários (e de integração, quando aplicável) passam;
3. o CI está verde (lint, SAST e testes);
4. a documentação e a OpenAPI foram atualizadas, se a tarefa cria ou altera endpoint;
5. não há lógica de negócio duplicada entre scraper e router ([componentes do backend](ARQUITETURA.md#nivel-3-componente));
6. o uso de IA, se houve, está registrado no [AI-USAGE.md](https://github.com/unb-mds/2026-2-Cerradinho-API/blob/dev/AI-USAGE.md).

## 4. Ritmo individual

- Atividade constante ao longo do projeto, com pelo menos 3 commits por semana por pessoa, em vez de concentrar o trabalho no fim de cada release.
- Presença na planning e na retrospectiva de cada sprint.

## 5. Issues, board e story map

- Toda issue tem critério de aceitação, label de tamanho (S/M/L/XL) e label de tipo (feature, fix, docs, devops). Os templates ficam em `.github/ISSUE_TEMPLATE/`.
- Cada requisito tem uma issue na milestone da sua release; as tarefas de cada semana ficam na milestone da sprint.
- O story map fica no GitHub Projects: os campos `Journey` (jornada do usuário) e `Step` (etapa da jornada) são preenchidos em cada issue, e uma view de Board com coluna = `Step` e agrupamento = `Milestone` gera a grade do mapa.

## 6. Releases

- **Release 1:** Sprints 0 a 3. **Release 2:** Sprints 4 a 12, com entrega em 25/11.
- Cada release fechada tem uma release note publicada na aba Releases do GitHub, descrevendo o que foi entregue.
- A Release 2 precisa estar implantada e acessível publicamente (RNF06).

## 7. Protótipos

Telas de baixa e alta fidelidade são revisadas com o time **antes** de o frontend implementar cada tela. O link do protótipo fica no [README do frontend](https://github.com/unb-mds/2026-2-Cerradinho-API/blob/dev/frontend/README.md).

## 8. Decisões de arquitetura (ADR)

Toda decisão técnica relevante (nova biblioteca, padrão estrutural, troca de tecnologia) ganha um ADR em [`docs/adr/`](adr/), a partir do [template](adr/template.md). Decisões de implementação rotineiras não precisam de ADR.

## 9. Uso de IA

O uso de IA é esperado e precisa ser registrado no [AI-USAGE.md](https://github.com/unb-mds/2026-2-Cerradinho-API/blob/dev/AI-USAGE.md), na mesma entrega em que o trabalho entra: data, pessoa, ferramenta, o que foi feito e o que foi aceito, ajustado ou rejeitado. IA não pode ser usada em avaliações individuais (arguições, quizzes, avaliação por pares, ensaio de reflexão crítica).
