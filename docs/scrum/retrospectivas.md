# Retrospectivas de sprint — Cerradinho

Fechamento de cada sprint: objetivo, o que foi entregue, métricas e retrospectiva. O planejamento (calendário e tarefas previstas) está no [planejamento de sprints](sprint-planning.md); o registro reunião a reunião está nas [atas](atas.md). Esse arquivo é escrito no fechamento de cada sprint, uma seção por sprint — sprints em andamento ainda não entram aqui.

### Sprint 0 — Base do projeto (até 06/09)

**Objetivo:** alinhar documentação base e estudos antes de começar a implementação.

**Entregue:** Gabriel produziu a documentação inicial do projeto — requisitos, arquitetura, processo e os templates de issue e PR. Vitor, Daniel e João Paulo fizeram os primeiros estudos de fundamentação (Git/GitHub, web scraping, HTML, Postman) antes de entrar em código.

**Métricas:** sem métrica numérica nesta sprint — entrega foi de documentação e estudo, não de código.

**Retrospectiva:** primeira sprint do projeto, sem reunião de review registrada nas atas (a primeira ata é a planning da Sprint 1, em 07/09). Serviu pra alinhar o time antes de qualquer linha de código.

### Sprint 1 — Primeiros scrapers e infraestrutura (07/09 a 13/09)

**Objetivo:** primeiros scrapers funcionando, schema inicial do banco, `docker-compose` e CI no ar.

**Entregue:** Vitor implementou o scraper de turmas do SIGAA via Playwright (com throttling) e o parser completo de disciplina/turma/professor/sala/horário/vagas, adiantando da Sprint 3 a camada de persistência ligada aos models do banco. Gabriel organizou os templates de issue/PR, o board e as milestones, e entregou os models SQLAlchemy, a migration inicial via Alembic e o `docker-compose` do Postgres. Arthur colocou o `docker-compose` com Celery e Redis rodando localmente. Daniel configurou o Next.js e iniciou os protótipos de tela. João Paulo estruturou o pipeline de CI (lint + testes a cada push) e validou a disponibilidade das fontes SIGAA/RU. Ítalo entregou o scraper do cardápio do RU já integrado ao banco.

**Métricas:** 8 testes cobrindo a persistência de disciplinas (Vitor); 7 tabelas do schema validadas subindo corretamente via `docker-compose` (Gabriel); 2 critérios de aceitação fechados na validação das fontes (João Paulo).

**Retrospectiva:** segundo a própria ata de revisão (14/09), todas as frentes — scraping, persistência, infraestrutura, CI e frontend — fecharam no prazo previsto, sem bloqueio registrado.

### Sprint 2 — Dado de ponta a ponta (14/09 a 20/09)

**Objetivo:** provar que cada fonte de dado funciona de ponta a ponta (scraper → banco → API).

**Entregue:** Vitor associou disciplina a professor e sala na persistência (#97), com o scraper gravando no banco de forma estável. Arthur implementou o agendamento automático com log de execução (#95). Gabriel entregou os endpoints `/v1/disciplinas` e `/v1/cardapio/semana` com OpenAPI (#100). Daniel conectou as telas à API real (#99). João Paulo implementou os testes de contrato com schemathesis no CI e adicionou SAST com bandit (#101, #111, #113, #115).

**Métricas:** issues #95, #97, #99, #100, #101, #111, #113, #115 fechadas na sprint.

**Retrospectiva:** a reunião de acompanhamento de 17/09 não aconteceu (ninguém presente, por demanda de outras disciplinas) — o trabalho continuou por mensagem, sem travar a entrega. Um item não fechou no prazo: o scraper do RU agendado com histórico acumulando (#98) escorregou pra Sprint 4, o que já fica registrado aqui como aprendizado — nem toda pendência de sprint é resolvida na sprint seguinte imediata.

### Sprint 3 — Estabilização e fechamento da R1 (21/09 a 27/09)

**Objetivo:** estabilizar os scrapers já construídos e fechar a Release 1.

**Entregue:** Vitor corrigiu um bug crítico na task do Celery (import quebrado, scraper nunca persistia nada), fez o scraper varrer todas as unidades do SIGAA, e corrigiu dois bugs de parsing (código de horário com data grudada, vagas em branco quebrando o parser), tudo coberto por teste de regressão e validado ao vivo contra o SIGAA. Arthur corrigiu o agendamento de Disciplinas (import, discovery, timezone), agendou o scraper do RU, limitou a concorrência do worker e ajustou a imagem Docker/Playwright pra produção. Gabriel entregou os endpoints `/v1/professores` e `/v1/salas`, completou a documentação OpenAPI, definiu as personas no Documento de Visão e reorganizou a estrutura de `docs/`. Daniel conectou as quatro telas (disciplinas, cardápio, professores, salas) a dado real, com estados de carregamento e erro. João Paulo adicionou bandit ao CI, um teste de integração contra Postgres real e testes das tasks do Celery.

**Métricas:** sem cobertura/mutação formalmente medida ainda nesta sprint (RNF09 é meta da Release 2) — o foco foi corrigir bugs encontrados testando contra as fontes reais, não medir qualidade de teste.

**Retrospectiva:** a Release 1 fechou com a base de dados e a API funcionando de ponta a ponta para disciplinas e cardápio, mas o scraper do RU não terminou de ser estabilizado dentro da sprint — ficou como pendência explícita pra Sprint 4, junto com duplicidade de professor/sala e log de execução não consultável pela API (esses dois últimos nem chegaram a entrar no escopo da Sprint 3).

### Sprint 4 — Pendências da R1 e release note (28/09 a 04/10)

**Objetivo:** fechar as pendências deixadas pela Release 1 e publicar a release note.

**Entregue:** Gabriel e Daniel escreveram e publicaram a Release Note da Release 1 no GitHub (tag `Release_1`), cobrindo as Sprints 0 a 3 — o marco principal da sprint foi cumprido.

**Métricas:** Release Note publicada com a tag `Release_1`.

**Retrospectiva:** a própria Release Note documenta, com transparência, que nem todas as pendências planejadas pra esta sprint fecharam a tempo — ficaram como limitações conhecidas, carregadas pra Release 2: o parser do cardápio do RU ainda falha em alguns layouts de PDF, professor e sala aparecem duplicados em algumas respostas, a busca de professor não tem normalização, e o log de execução ainda não é consultável pela API. Em vez de esconder essas lacunas, o time optou por documentá-las explicitamente na release note — é uma prática que vale manter nas próximas releases.
