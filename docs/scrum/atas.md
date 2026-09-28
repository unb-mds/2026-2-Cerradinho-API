# Atas de reunião — Cerradinho

Registro das reuniões do time: presença, o que foi feito e o que ficou combinado. Os horários e o papel de cada reunião estão no [PROCESSO.md](../PROCESSO.md#2-sprints-e-ritos); o calendário das sprints, no [planejamento](sprint-planning.md).

## Registros

### Segunda-feira, 07/09 — Planning da Sprint 1

**Presentes:** Gabriel, Daniel, Arthur, Ítalo, Vitor, João Paulo

**Progresso:** O time no geral finalizou o planejamento para seguir o que havia sido planejado conforme a sprint 1 começando a partir de hoje, além de estudos em suas futuras áreas de trabalho. Além disso, foram esclarecidas algumas regras de trabalho no Git/GitHub.

**Pendências / próximos passos:** Finalizar estudos sobre ferramentas a serem utilizadas por cada membro (individual) e finalizar até a próxima segunda-feira o que estava planejado para cada membro para a sprint 1 (coletivo).

---

### Quinta-feira, 10/09 — Acompanhamento da Sprint 1

**Presentes:** Gabriel, Daniel, Arthur, Vitor, João Paulo

**Progresso:**

- **Vitor:** Mandou a documentação de skills do claude e já realizou o scraper e o parser do SIGAA de disciplinas, professores e salas, falta commit até segunda-feira (14/09) em /backend.

- **Arthur:** Realizou estudos sobre celery e redis, já documentados e falta ainda fazer o docker compose com celery e redis rodando localmente até segunda-feira (14/09).

- **Gabriel:** Realizou a documentação final de requisitos, arquitetura, processo, fez os templates de issues e pull request para facilitar o uso do github, além de arquivos complementares na raiz do projeto. Fez o schema inicial, falta finalização para cumprir sprint. Organizou storymap no github projects e implementou estrutura de pastas final do sistema.

- **Daniel:** Realizou estudos sobre HTML e JS, além de começar os estudos no NEXT.JS, após finalização desse estudo já implementará o protótipo para as telas/endpoints do sistema.

- **João Paulo:** Realizou estudos sobre Pytest , Mocking, Schemathesis, Postman e API, tudo já documentado, além disso já implementou Pytest e Ruff no projeto, para finalizar sprint falta integrar um teste de segurança até segunda-feira (14/09).

- **Ítalo:** Já havia realizado e documentado estudos sobre BeautifulSoup e SQLAlchemy, falta implementação do scraper do cardápio do RU até segunda-feira (14/09) no /backend.

**Pendências / próximos passos:** Finalização das Sprints 1 de cada membro até segunda-feira (14/09) para já dar início ao começo da sprint 2 e avanço das sub-áreas do projeto.

---

### Segunda-feira, 14/09 — Review da Sprint 1 e planning da Sprint 2

**Presentes:** Gabriel, Daniel, Arthur, Vitor, João Paulo

**Progresso:** A Sprint 1 do Cerradinho foi concluída com sucesso por todo o time, com cada integrante entregando exatamente o que estava planejado. No back-end, Vitor criou as Claude Skills do projeto, implementou o scraper de turmas do SIGAA via Playwright (com throttling) e o parser de disciplina/turma/professor/sala/horário/vagas, além de já adiantar da Sprint 3 a persistência que conecta esse parser aos models do banco (get-or-create e upsert sem duplicação), cobrindo tudo com 8 testes e fechando a issue #60. Gabriel estruturou a base do projeto — templates e issues de todos os requisitos, milestone e labels da sprint, o board organizado por journey/step — e entregou os models SQLAlchemy ajustados ao contrato de dados, a migration inicial via Alembic e o docker-compose do Postgres com as 7 tabelas validadas. Arthur aprofundou estudos em Redis, FastAPI/infra de jobs e rate limit com slowapi, e junto com Gabriel colocou o docker-compose com Celery e Redis rodando localmente. No front-end, Daniel estudou React, configurou o Next.js e já iniciou os protótipos de telas e endpoints. João estruturou o pipeline de CI (lint e testes automáticos a cada push) e validou a estabilidade das fontes de dados do SIGAA e do RU, fechando os dois critérios de aceitação de sua issue. Por fim, Ítalo estudou scraping de PDFs e concluiu a extração do cardápio do RU já integrada ao banco de dados do Gabriel. No geral, a sprint fechou com todas as frentes — scraping, persistência, infraestrutura, CI e frontend — avançando de forma coordenada e nos prazos previstos.

- **Vitor:** criou as Claude Skills usadas pelo projeto; implementou o scraper de turmas de Disciplinas do SIGAA via Playwright com throttling (RF01) e o parser que extrai disciplina/turma/professor/sala/horário/vagas do HTML capturado, além de adiantar da Sprint 3 a camada de persistência que liga esse parser aos models de banco do Gabriel (get-or-create de Disciplina/Sala/Professor e upsert de Turma+Horário, sem duplicar turma em reagendamentos), com 8 testes cobrindo a persistência e correções de manutenção pelo caminho (imports pro ruff, bug no pytest.ini, limpeza do .gitignore), fechando o PR feature/conexao-banco-parser-disciplinas (issue #60), finalizou o que devia na semana.

- **Arthur:** realizou mais três estudos sobre: cache redis, fastapi mais infra de jobs, e de rate limit slowapi. Implementou o docker-compose.yml junto com o Gabriel, com Celery e Redis rodando localmente, finalizando o que era previsto na sua sprint 1 semanal.

- **Gabriel:** realizou os templates de issues, criou as issues para todos os requisitos e as issues semanais da sprint 1 (milestone + label), projects do github organizado (campos journey/step). Models SQLalchemy ajustados ao contrato de dados do Vitor. Migration inicial via alembic. Docker-compose.yml com postgres, sobe e aplica schema automaticamente. Testes unitários dos models validado localmente, as 7 tabelas sobem corretamente. Concluiu a sprint 1 prevista para hoje.

- **Daniel:** realizou estudos de react, fez a configuração do Next.JS e já começou os protótipos de telas e endpoints do sistema, dessa maneira finalizando o que havia sido previsto para conclusão da sprint 1.

- **João Paulo:** Configurou o pipeline de integração contínua do projeto, de forma que lint e testes passassem a rodar automaticamente a cada push no repositório, reforçando a qualidade do código antes da integração nas branches principais. Além disso, validou a disponibilidade e a estabilidade das fontes de dado utilizadas pelos scrapers do sistema — SIGAA e RU —, confirmando que ambas estavam aptas a serem consumidas de forma confiável pelo restante do time. Com isso, os dois critérios de aceitação da issue foram atendidos.

- **Ítalo:** Realizou estudos sobre scraping em cima de documentos PDF, e concluiu o scraping do cardápio do RU integrando com o banco de dados do Gabriel conforme era previsto para sua sprint 1 que finaliza na reunião de hoje.

**Pendências / próximos passos:** com a Sprint 1 encerrada, o time entra na Sprint 2, cujo foco é provar que cada fonte de dado funciona ponta a ponta: Vitor valida o scraper de Disciplinas contra o SIGAA real (fora do fixture de teste) e apoia o wiring do pipeline completo (scraper → parser → banco) numa task agendada; Ítalo faz a PoC de scraping do cardápio do RU com BeautifulSoup; Daniel revisa com o time os wireframes das telas de consulta antes de implementar; Arthur monta uma PoC de task Celery agendada simples; Gabriel revisa o schema inicial à luz do que as PoCs encontrarem; e João Paulo deixa o CI rodando de fato (lint + testes) a cada push, com o relatório de risco das fontes atualizado com os achados das PoCs.

---

### Quinta-feira, 17/09 — Acompanhamento da Sprint 2 (não realizada)
**Presentes:** ninguém

**Progresso:** Não conseguimos realizar reunião nesse dia pela demanda dos membros nas suas tarefas universitárias mas o desenvolvimento continua sendo organizado por mensagens e no individual.

---

### Segunda-feira, 21/09 — Review da Sprint 2 e planning da Sprint 3

**Presentes:** Gabriel, Daniel, Arthur, Vitor, João Paulo

**Planejado para a Sprint 3:**

- **Vitor**: vai estabilizar o scraper de Disciplinas, resolvendo os bugs identificados.

- **Arthur**: vai validar a execução automática dos scrapers agendados, sem necessidade de intervenção manual.

- **Gabriel**: vai preparar a release note do Release 1 e o checklist final da documentação OpenAPI.

- **Daniel**: vai fazer os ajustes finais de UX, validando a exibição dos dados reais na interface.

- **João Paulo**: vai concluir os testes de contrato, garantir o CI verde e conferir o checklist board vs. entrega.

- **Ítalo**: vai estabilizar o scraper de RU, resolvendo os bugs identificados.

**Review da Sprint 2:** A Sprint 2 foi concluída conforme planejado. O scraper de Disciplinas passou a gravar os dados no banco de forma estável, já com a associação entre Disciplina, Professor e Sala funcionando corretamente. Em paralelo, o scraper de RU foi agendado no Celery e o histórico de cardápio começou a ser acumulado. Arthur configurou o agendamento automático dos dois scrapers, com logs de execução, enquanto Gabriel entregou os endpoints REST sob /v1/ para os dois domínios, já com documentação OpenAPI gerada automaticamente. Do lado do frontend, Daniel conectou as telas à API real, e João Paulo implementou os testes de contrato nos endpoints publicados, com o CI já rodando essas validações. Com isso, a equipe encerra a sprint com a base de dados e a API funcionando de ponta a ponta, pronta para os ajustes finos da Sprint 3.

---

### Domingo, 27/09 — Acompanhamento da Sprint 3

**Presentes:** Vitor, Arthur, João Paulo, Gabriel, Daniel

**Progresso:**

- **Vitor**: estabilizou o scraper de Disciplinas (RF01/RF15): corrigiu um bug crítico na task do Celery, que importava uma função inexistente e por isso nunca rodava de verdade nem persistia nada no banco; fez o scraper varrer todas as unidades preservando de qual unidade cada turma veio, informação que antes se perdia; e corrigiu dois bugs de parsing encontrados testando contra o SIGAA real — código de horário vindo com a data grudada e estourando a coluna do banco, e turma com docente "a definir" vindo com vagas em branco e quebrando o parser no meio da unidade. Tudo isso ficou coberto por teste de regressão, validado ao vivo contra o SIGAA antes do commit.

- **Arthur**: estabilizou a execução automática dos scrapers agendados: corrigiu o import quebrado, o discovery de tasks e o timezone do agendamento de Disciplinas (RF15), agendou o scraper de Cardápio do RU no Celery (RF16/RF07), limitou a concorrência do worker a 1, corrigiu um typo no nome da classe do scraper de Disciplinas, e ajustou a imagem base do container e a instalação do navegador do Playwright pra rodar em produção.

- **Gabriel**: entregou os endpoints `/v1/professores` e `/v1/salas`, configurou o acesso do worker do Celery ao banco no docker-compose, completou a documentação OpenAPI das rotas `/v1`, definiu as personas no Documento de Visão, e reestruturou a documentação do projeto (reorganização de `docs/estudos`, `docs/fontes` e renomeação de `dailies.md` pra `atas.md`).

- **Daniel**: conectou as telas de Disciplinas, Cardápio, Professores e Salas aos dados reais da API, tratou os estados de carregamento e erro na Visão Geral e nas mensagens de lista vazia (incluindo escondê-la durante carregamento/erro), e atualizou o README do frontend com o status e link do protótipo.

- **João Paulo**: adicionou análise estática de segurança com bandit no CI, criou teste de integração do pipeline de Disciplinas contra Postgres real (rodando no pipeline via serviço postgres), e adicionou testes de registro/agendamento das tasks do Celery.

- **Ítalo**: tem que estabilizar o scraper do cardápio do RU e corrigir os bugs essenciais pré Release 1.

---
