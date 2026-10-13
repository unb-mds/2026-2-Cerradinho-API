# Planejamento de sprints — Cerradinho

Calendário e entregas de cada sprint. Papéis, ritos e Definition of Done estão no [PROCESSO.md](../PROCESSO.md); o registro das reuniões, nas [atas](atas.md); o fechamento de cada sprint (objetivo, entregue, métricas, retrospectiva), nas [retrospectivas](retrospectivas.md).

Sprints de 1 semana, de domingo a sábado. A semana de 28/09 a 03/10, da apresentação da R1, ficou fora das sprints. As tarefas de cada sprint ficam na milestone correspondente no GitHub.

## Calendário

| Sprint | Período | Release | Foco |
|---|---|---|---|
| 0 | até 06/09 | R1 | Documentação base e estudos |
| 1 | 07/09 a 13/09 | R1 | Primeiros scrapers, schema, compose, CI |
| 2 | 14/09 a 20/09 | R1 | Persistência, agendamento, API `/v1`, telas com dado real |
| 3 | 21/09 a 27/09 | R1 | Estabilização e fechamento da R1 |
| 4 | 04/10 a 10/10 | R2 | Estudos, revisão e correção |
| 5 | 11/10 a 17/10 | R2 | Pendências da R1 (RU, duplicados, log), protótipos, preparação do deploy |
| 6 | 18/10 a 24/10 | R2 | Salas vazias, cache, cardápio semanal, deploy de teste |
| 7 | 25/10 a 31/10 | R2 | Agenda do professor, rate limit, observabilidade, versão candidata |
| 8 | 01/11 a 07/11 | R2 | SDK, CLI, portal do desenvolvedor, deploy definitivo |
| 9 | 08/11 a 14/11 | R2 | SDK, CLI e portal fechados; mutação e sabotagem |
| 10 | 15/11 a 21/11 | R2 | Fechamento das features e da qualidade de testes |
| 11 | 22/11 a 25/11 | R2 | Correções finais, release note e entrega (25/11) |

## Release 1 (Sprints 0 a 3)

**Objetivo:** dois domínios de dados (disciplinas e cardápio do RU) com scraping agendado e OpenAPI documentada. A apresentação foi em 28/09.

- **Sprint 0:** só estudos e arquivos iniciais do projeto, para todos.
- **Sprints 1 a 3:** desenvolvimento.

| Sprint | Vitor | Ítalo | Daniel | Arthur | Gabriel | João Paulo |
|---|---|---|---|---|---|---|
| **0** (até 06/09) | Estudo de Git/GitHub, web scraping, FastAPI e Playwright | Estudo de BeautifulSoup e SQLAlchemy | Estudo de HTML e JavaScript | Estudo de Celery e Redis | Arquivos iniciais: requisitos, arquitetura, processo e templates de issue e PR | Estudo de Postman, Pytest com mocking e schemathesis |
| **1** (07/09 a 13/09) | Scraper de disciplinas com Playwright, capturando dados reais do SIGAA (#60) | Scraper do cardápio do RU completo (#61) | Setup do Next.js e protótipo das telas de consulta (#62) | `docker-compose.yml` com Celery e Redis rodando localmente (#63) | Schema inicial no SQLAlchemy (Disciplina, Professor, Sala, Cardápio) integrado ao Docker Compose (#64) | Pipeline de CI (lint e testes) e validação das fontes de dado (#65, #84, #87) |
| **2** (14/09 a 20/09) | Scraper de disciplinas gravando no banco de forma estável; associação disciplina ↔ professor ↔ sala (#97) | Scraper do RU agendado no Celery, com o histórico de cardápio acumulando (#98, passou para a R2) | Telas conectadas à API real (#99) | Agendamento dos scrapers de disciplinas e do RU no Celery; log de execução (#95) | Endpoints REST sob `/v1/` para os dois domínios; documentação OpenAPI automática (#100) | Testes de contrato nos endpoints publicados, rodando no CI (#101, #111, #113, #115) |
| **3** (21/09 a 27/09) | Estabilizar o scraper de disciplinas e resolver bugs (#102) | Estabilizar o scraper do RU e resolver bugs (#103, passou para a R2) | Ajustes finais de UX e validação da exibição do dado real (#104) | Validar a execução automática dos scrapers agendados, sem intervenção manual (#105) | Release note da R1 (publicada na Sprint 4) e checklist final da OpenAPI (#106) | Testes de contrato completos, CI verde e checklist do board contra a entrega (#107, #123, #126, #128) |

**Marco:** apresentação da Release 1 em 28/09, com disciplinas e cardápio coletados, gravados no banco e expostos pela API `/v1`.

## Release 2 (Sprints 4 a 11)

**Objetivo:** features derivadas, cache, rate limit, SDK e CLI, portal do desenvolvedor e API em produção.

**Mudança no time:** o Ítalo saiu do projeto no início da R2.
- Os scrapers de eventos (RF08) e de editais (RF09), que eram dele, saíram do escopo da R2.
- O que o projeto precisa para funcionar foi redistribuído:

| Tarefa do Ítalo | Passou para |
|---|---|
| Parser do RU com os PDFs novos (#103, #98) | Gabriel, com as fixtures feitas pelo João Paulo |
| Cardápio semanal (RF19) | Gabriel |
| CLI (RF13) | João Paulo, em cima do SDK do Vitor |

### Sprints 4 a 11

Sprints de uma semana, de domingo a sábado. O plano é revisado na planning de cada sprint.

- **Sprint 4:** estudos, revisão e correção. O grupo estuda o que a R2 pede, revisa o que foi entregue na R1 e corrige a documentação e o processo antes de voltar a desenvolver.
- **Sprints 5 a 10:** só desenvolvimento.
- **Sprint 11:** sprint curta e final, só para terminar o que falta, corrigir erros e bugs e acertar os pequenos detalhes.

Área de cada pessoa na R2: **Vitor**, disciplinas, features derivadas e SDK; **Daniel**, frontend e portal do desenvolvedor; **Arthur**, agendamento, cache e rate limit; **Gabriel**, cardápio do RU e deploy; **João Paulo**, qualidade, observabilidade e CLI.

| Sprint | Vitor | Daniel | Arthur | Gabriel | João Paulo |
|---|---|---|---|---|---|
| **4** (04/10 a 10/10) | Reestruturar os requisitos como pediu a professora (#136); site de documentação no GitHub Pages; arquitetura no modelo C4; retrospectivas das Sprints 0 a 4 | Release note da R1, com o Gabriel; estudar como embutir o Swagger UI no portal do desenvolvedor | Revisar o agendamento e o log de execução (RF15, RF16); estudar cache com Redis e rate limit com slowapi | Release note da R1, com o Daniel; padrão de branches `R2-nome`; licença, código de conduta e changelog; especificação em `/specs`; estudar o deploy no Railway | Levar a `dev` para a `main` (#138); limpar as branches antigas; checklist da R1 (#128); estudar teste de mutação e UptimeRobot |
| **5** (11/10 a 17/10) | Remover professores e salas duplicados da API; busca de docente por nome normalizado (RF04) | Protótipos das telas novas (salas vazias, agenda, cardápio semanal) e wireframe do portal (RF14) | Log de execução consultável (RF16); desenho do cache (RNF02) | Corrigir o parser do RU para os PDFs novos (#103, #98); variáveis de produção no Railway | PDFs do RU como fixtures de teste; medir a cobertura e definir os módulos críticos (RNF09) |
| **6** (18/10 a 24/10) | Salas vazias (RF17) | Swagger UI no portal (RF14); ajustes de UX do cardápio | Cache Redis nas rotas mais consultadas (RNF02) | Deploy de teste no Railway (API, banco e worker); cardápio semanal (RF19) | Contrato de salas vazias e do cardápio semanal; teste do log de execução (RF16) |
| **7** (25/10 a 31/10) | Agenda do professor (RF18) | Telas de salas vazias e da agenda | Rate limit com slowapi (RNF01) | Versão candidata no Railway, com o frontend | Observabilidade com UptimeRobot (RNF03); contrato da agenda |
| **8** (01/11 a 07/11) | SDK Python (RF13) | Portal do desenvolvedor (RF14); tela do cardápio semanal | Cache e rate limit finalizados; teste simples de carga | Deploy definitivo (RNF06) | CLI com Typer em cima do SDK (RF13) |
| **9** (08/11 a 14/11) | SDK fechado e documentado | Portal finalizado; frontend em produção, com o Gabriel | Worker e agendamento estáveis em produção (RF15) | Ajustes pós-deploy; rastreabilidade das specs atualizada | CLI fechada; mutação e sabotagem (RNF09) |
| **10** (15/11 a 21/11) | Ajustes finais de salas vazias e agenda; exemplos de uso do SDK | Telas finais; GitPage com visão de produto (prints e fluxo de navegação) | Ajustes finais de cache, rate limit e log de execução | Produção estável; ajustes finais do cardápio semanal | Cobertura, mutação e sabotagem nas metas do RNF09; contratos completos (RNF04) |
| **11** (22/11 a 25/11) | Correções finais; retrospectiva final e análise das métricas da R2 (velocity, issues e PRs por sprint) | Correções finais; slides da apresentação final | Correções finais; conferir que a API e o frontend estão acessíveis em produção | Correções finais; release note da R2, merge da `dev` na `main` e tag da release | Correções finais; checklist final do board contra a entrega; CI verde e SAST sem achado alto no commit da entrega |

**Marcos:**
- Sprint 4: release note da R1 publicada e documentação revisada contra o plano de ensino.
- Sprint 10: todas as features prontas e em produção até 21/11. Depois disso não entra feature nova.
- Sprint 11: Release 2 entregue em **25/11**, em produção e com release note publicada.

**Dependências-chave:**
- Cache e rate limit não podem quebrar os testes de contrato. Rodar a suíte de contrato antes de cada merge dessas mudanças.
- O CLI depende do SDK. O João Paulo começa o CLI na Sprint 8, com a interface do SDK já combinada com o Vitor.
- As telas novas dependem dos protótipos da Sprint 5, revisados com o time antes de implementar.
- O cardápio semanal (RF19) depende do parser do RU corrigido na Sprint 5.

## Riscos

| Risco | Quando pesa mais | Mitigação |
|---|---|---|
| O SIGAA (JSF) muda o formulário ou a sessão | Toda a coleta de disciplinas | Scraper falha de forma isolada por unidade (RNF05); [plano de monitoramento](../fontes/plano-de-monitoramento.md) |
| O RU muda o layout do PDF | Toda semana; já aconteceu em 21/09 e 28/09 | PDFs reais como fixtures de teste; falha sem apagar o histórico |
| Período letivo fixo no código | Virada de semestre | Atualizar `ano`/`periodo` em `celery_app.py` antes do semestre começar |
| Dívida de cobertura de testes | Sprints 8 a 10 | Medir a cobertura desde a Sprint 5, não só no fechamento |
| Cache ou rate limit causando regressão na API | Sprints 6 a 8 | Suíte de contrato antes de cada merge |
| Limites do plano gratuito do Railway | Sprints 6 a 11 | Deploy de teste cedo (Sprint 6) para descobrir limites antes do fechamento |
| Carga extra com a saída do Ítalo | Sprints 5 a 10 | Eventos e editais fora do escopo; o que é essencial foi redistribuído |
