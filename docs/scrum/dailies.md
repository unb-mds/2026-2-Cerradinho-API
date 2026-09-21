# Dailies — Projeto Cerradinho

Este arquivo será usado para registrar os progressos obtidos nas reuniões do time do projeto Cerradinho (disciplina MDS). Os progressos individuais por membro serão representados separadamente posteriormente seguindo o fluxo do projeto.

**Horários das reuniões:**

- **Segunda-feira:** após a aula
- **Quinta-feira:** às 19h
- **Reuniões emergenciais:** quando necessário, para resolver urgências e conflitos
- **Resoluções pontuais:** também podem ocorrer por mensagem (fora das reuniões fixas)

---

## Registros

### Segunda-feira, 07/09 (Sprint - planning)

**Presentes:** Gabriel, Daniel, Arthur, Ítalo, Vitor, João

**Progresso:** O time no geral finalizou o planejamento para seguir o que havia sido planejado conforme a sprint 1 começando a partir de hoje, além de estudos em suas futuras áreas de trabalho. Além disso foi clareado algumas regras de trabalho no git/github.

**Pendências / próximos passos:** Finalizar estudos sobre ferramentas a serem utilizadas por cada membro (individual) e finalizar até a próxima segunda-feira o que estava planejado para cada membro para a sprint 1 (coletivo).

---

### Quinta-Feira, 10/09 (Sprint - review)

**Presentes:** Gabriel, Daniel, Arthur, Vitor, João

**Progresso:**

- **Vitor:** Mandou a documentação de skills do claude e já realizou o scraper e o parser do SIGAA de disciplinas, professores e salas, falta commit até segunda-feira (14/09) em /backend.

- **Arthur:** Realizou estudos sobre celery e redis, já documentados e falta ainda fazer o docker compose com celery e redis rodando localmente até segunda-feira (14/09).

- **Gabriel:** Realizou a documentação final de requisitos, arquitetura, processo, fez os templates de issues e pull request para facilitar o uso do github, além de arquivos complementares na raiz do projeto. Fez o schema inicial, falta finalização para cumprir sprint. Organizou storymap no github projects e implementou estrutura de pastas final do sistema.

- **Daniel:** Realizou estudos sobre HTML e JS, além de começar os estudos no NEXT.JS, após finalização desse estudo já implementará o protótipo para as telas/endpoints do sistema.

- **Jõao:** Realizou estudos sobre Pytest , Mocking, Schemathesis, Postman e API, tudo já documentado, além disso já implementou Pytest e Ruff no projeto, para finalizar sprint falta integrar um teste de segurança até segunda-feira (14/09).

- **Ítalo:** Já havia realizado e documentado estudos sobre BeautifulSoup e SQLAlchemy, falta implementação do scraper do cardápio do RU até segunda-feira (14/09) no /backend.

**Pendências / próximos passos:** Finalização das Sprints 1 de cada membro até segunda-feira (14/09) para já dar início ao começo da sprint 2 e avanço das sub-áreas do projeto.

---

### Segunda-Feira, 14/09 (Sprint - Review)

**Presentes:** Gabriel, Daniel, Arthur, Vitor, João

**Progresso:** A Sprint 1 do Cerradinho foi concluída com sucesso por todo o time, com cada integrante entregando exatamente o que estava planejado. No back-end, Vitor criou as Claude Skills do projeto, implementou o scraper de turmas do SIGAA via Playwright (com throttling) e o parser de disciplina/turma/professor/sala/horário/vagas, além de já adiantar da Sprint 3 a persistência que conecta esse parser aos models do banco (get-or-create e upsert sem duplicação), cobrindo tudo com 8 testes e fechando a issue #60. Gabriel estruturou a base do projeto — templates e issues de todos os requisitos, milestone e labels da sprint, o board organizado por journey/step — e entregou os models SQLAlchemy ajustados ao contrato de dados, a migration inicial via Alembic e o docker-compose do Postgres com as 7 tabelas validadas. Arthur aprofundou estudos em Redis, FastAPI/infra de jobs e rate limit com slowapi, e junto com Gabriel colocou o docker-compose com Celery e Redis rodando localmente. No front-end, Daniel estudou React, configurou o Next.js e já iniciou os protótipos de telas e endpoints. João estruturou o pipeline de CI (lint e testes automáticos a cada push) e validou a estabilidade das fontes de dados do SIGAA e do RU, fechando os dois critérios de aceitação de sua issue. Por fim, Ítalo estudou scraping de PDFs e concluiu a extração do cardápio do RU já integrada ao banco de dados do Gabriel. No geral, a sprint fechou com todas as frentes — scraping, persistência, infraestrutura, CI e frontend — avançando de forma coordenada e nos prazos previstos.

- **Vitor:** criou as Claude Skills usadas pelo projeto; implementou o scraper de turmas de Disciplinas do SIGAA via Playwright com throttling (RF01) e o parser que extrai disciplina/turma/professor/sala/horário/vagas do HTML capturado, além de adiantar da Sprint 3 a camada de persistência que liga esse parser aos models de banco do Gabriel (get-or-create de Disciplina/Sala/Professor e upsert de Turma+Horário, sem duplicar turma em reagendamentos), com 8 testes cobrindo a persistência e correções de manutenção pelo caminho (imports pro ruff, bug no pytest.ini, limpeza do .gitignore), fechando o PR feature/conexao-banco-parser-disciplinas (issue #60), finalizou o que devia na semana.

- **Arthur:** realizou mais três estudos sobre: cache redis, fastapi mais infra de jobs, e de rate limit slowapi. Implementou o docker-compose.yml jutamente do Gabriel, com Celery e Redis rodando localmente, finalizando o que era previsto na sua sprint 1 semanal.

- **Gabriel:** realizou os templates de issues, criou as issues para todos os requisitos e as issues semanais da sprint 1 (milestone + label), projects do github organizado (campos journey/step). Models SQLalchemy ajustados ao contrato de dados do Vitor. Migration inicial via alembic. Docker-compose.yml com postgres, sobe e aplica schema automaticamente. Testes unitários dos models validado localmente, as 7 tabelas sobem corretamente. Concluiu a sprint 1 prevista para hoje.

- **Daniel:** realizou estudos de react, fez a configuração do Next.JS e já começou os protótipos de telas e endpoints do sistema, dessa maneira finalizando o que havia sido previsto para conclusão da sprint 1.

- **Jõao:** Configurei o pipeline de integração contínua do projeto Cerradinho, de forma que lint e testes passassem a rodar automaticamente a cada push no repositório, reforçando a qualidade do código antes da integração nas branches principais. Além disso, validei a disponibilidade e a estabilidade das fontes de dado utilizadas pelos scrapers do sistema — SIGAA e RU —, confirmando que ambas estavam aptas a serem consumidas de forma confiável pelo restante do time. Com isso, os dois critérios de aceitação da issue foram atendidos.

- **Ítalo:** Realizou estudos sobre scraping em cima de documentos PDF, e concluiu o scraping do cardápio do RU integrando com o banco de dados do Gabriel conforme era previsto para sua sprint 1 que finaliza na reunião de hoje.

**Pendências / próximos passos:** com a Sprint 1 encerrada, o time entra na Sprint 2, cujo foco é provar que cada fonte de dado funciona ponta a ponta: Vitor valida o scraper de Disciplinas contra o SIGAA real (fora do fixture de teste) e apoia o wiring do pipeline completo (scraper → parser → banco) numa task agendada; Ítalo faz a PoC de scraping do cardápio do RU com BeautifulSoup; Daniel revisa com o time os wireframes das telas de consulta antes de implementar; Arthur monta uma PoC de task Celery agendada simples; Gabriel revisa o schema inicial à luz do que as PoCs encontrarem; e João Paulo deixa o CI rodando de fato (lint + testes) a cada push, com o relatório de risco das fontes atualizado com os achados das PoCs.

---

### Quinta-Feira, 17/09 
**Presentes:** Nínguem

**Progresso:** Não conseguimos realizar reunião nesse dia pela demanda dos membros nas suas tarefas universitárias mas o desenvolvimento continua sendo organizado por mensagens e no individual.

---

### Quinta-Feira, 10/09 (Sprint - Planning)

**Presentes:** Gabriel, Daniel, Arthur, Vitor, João

**Progresso:**  

- **Vitor**: vai estabilizar o scraper de Disciplinas, resolvendo os bugs identificados.

- **Arthur**: vai validar a execução automática dos scrapers agendados, sem necessidade de intervenção manual.

- **Gabriel**: vai preparar a release note do Release 1 e o checklist final da documentação OpenAPI.

- **Daniel**: vai fazer os ajustes finais de UX, validando a exibição dos dados reais na interface.

- **João Paulo**: vai concluir os testes de contrato, garantir o CI verde e conferir o checklist board vs. entrega.

- **Ítalo**: vai estabilizar o scraper de RU, resolvendo os bugs identificados.

**Pendências / próximos passos:** A Sprint 2 foi concluída conforme planejado. O scraper de Disciplinas passou a gravar os dados no banco de forma estável, já com a associação entre Disciplina, Professor e Sala funcionando corretamente. Em paralelo, o scraper de RU foi agendado no Celery e o histórico de cardápio começou a ser acumulado. Arthur configurou o agendamento automático dos dois scrapers, com logs de execução, enquanto Gabriel entregou os endpoints REST sob /v1/ para os dois domínios, já com documentação OpenAPI gerada automaticamente. Do lado do frontend, Daniel conectou as telas à API real, e João Paulo implementou os testes de contrato nos endpoints publicados, com o CI já rodando essas validações. Com isso, a equipe encerra a sprint com a base de dados e a API funcionando de ponta a ponta, pronta para os ajustes finos da Sprint 3.

---
