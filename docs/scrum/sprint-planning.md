# Planejamento de sprints — Cerradinho

Calendário e entregas de cada sprint. Papéis, ritos e Definition of Done estão no [PROCESSO.md](../PROCESSO.md); o registro das reuniões, nas [atas](atas.md); o fechamento de cada sprint (objetivo, entregue, métricas, retrospectiva), nas [retrospectivas](retrospectivas.md).

Sprints de 1 semana. As tarefas de cada sprint ficam na milestone correspondente no GitHub.

## Calendário

| Sprint | Período | Release | Foco |
|---|---|---|---|
| 0 | até 06/09 | R1 | Documentação base e estudos |
| 1 | 07/09 a 13/09 | R1 | Primeiros scrapers, schema, compose, CI |
| 2 | 14/09 a 20/09 | R1 | Persistência, agendamento, API `/v1`, telas com dado real |
| 3 | 21/09 a 27/09 | R1 | Estabilização e fechamento da R1 |
| 4 | 28/09 a 04/10 | R2 | Pendências da R1 e release note |
| 5 | 05/10 a 11/10 | R2 | Eventos, salas vazias, desenho do cache, deploy de teste |
| 6 | 12/10 a 18/10 | R2 | Editais, agenda do professor, cache, versão candidata |
| 7 | 19/10 a 25/10 | R2 | Rate limit, observabilidade, telas das features derivadas |
| 8 | 26/10 a 01/11 | R2 | SDK, CLI, portal do desenvolvedor, deploy definitivo |
| 9 | 02/11 a 08/11 | R2 | SDK, CLI e portal fechados; qualidade de testes |
| 10 | 09/11 a 15/11 | R2 | Revisão final |
| 11 | 16/11 a 22/11 | R2 | Correções finais e release note da R2 |
| 12 | 23/11 a 25/11 | R2 | Entrega da R2 (25/11) |

## Release 1 — Sprints 0 a 3

**Objetivo:** dois domínios de dados com scraping agendado e OpenAPI documentada.

### Sprint 0 — Base do projeto
- Documentação inicial: requisitos, arquitetura, processo e templates de issue e PR (Gabriel).
- Estudos de Git/GitHub, web scraping, HTML e Postman (Vitor, Daniel, João Paulo).

### Sprint 1 — Primeiros scrapers e infraestrutura
| Pessoa | Entrega | Issue |
|---|---|---|
| Vitor | Scraper de turmas do SIGAA com Playwright, com dado real | #60 |
| Ítalo | Scraper do cardápio do RU | #61 |
| Daniel | Setup do Next.js e protótipo das telas de consulta | #62 |
| Arthur | `docker-compose.yml` com Celery e Redis | #63 |
| Gabriel | Schema inicial em SQLAlchemy, migration e Postgres no compose | #64 |
| João Paulo | Pipeline de CI e validação das fontes; relatório de risco | #65, #84, #87 |

Estudos: BeautifulSoup e SQLAlchemy (Ítalo), FastAPI e Playwright (Vitor), Pytest e mocking (João Paulo).

### Sprint 2 — Dado de ponta a ponta
| Pessoa | Entrega | Issue |
|---|---|---|
| Vitor | Persistência das turmas com associação a professor e sala | #97 |
| Ítalo | Scraper do RU agendado, com histórico acumulando | #98 (passou para a Sprint 4) |
| Daniel | Telas de consulta conectadas à API | #99 |
| Arthur | Agendamento automático com log de execução | #95 |
| Gabriel | Endpoints `/v1/disciplinas` e `/v1/cardapio/semana` com OpenAPI | #100 |
| João Paulo | Testes de contrato com schemathesis no CI; SAST com bandit | #101, #111, #113, #115 |

### Sprint 3 — Estabilização
| Pessoa | Entrega | Issue |
|---|---|---|
| Vitor | Estabilização do scraper de disciplinas (horário, vagas em branco, task) | #102 |
| Ítalo | Estabilização do scraper do RU | #103 (passou para a Sprint 4) |
| Daniel | Telas com dado real, estados de carregamento e erro | #104 |
| Arthur | Execução automática validada; task do cardápio; Chromium na imagem | #105 |
| Gabriel | Endpoints `/v1/professores` e `/v1/salas` (antecipados da R2); documentação OpenAPI completa | #106 |
| João Paulo | Teste de integração com Postgres; testes das tasks do Celery | #107, #123, #126 |

## Release 2 — Sprints 4 a 12

**Objetivo:** cinco domínios, features derivadas, cache, rate limit, SDK/CLI, portal do desenvolvedor e API em produção.

### Sprint 4 — Pendências da R1

A R1 terminou na Sprint 3 com itens em aberto, que abrem a R2.

| Pessoa | Tarefa |
|---|---|
| Ítalo | Corrigir o parser do RU para os novos layouts de PDF e adicionar os PDFs como fixtures (#103, #98) |
| Arthur | Tornar o log de execução consultável (RF16) |
| Vitor | Tratar professores e salas duplicados nas respostas da API |
| Daniel | Ajustes finais de UX com o dado do cardápio |
| Gabriel | Publicar a release note da R1 (#106) |
| João Paulo | Checklist do board contra a entrega e fechamento das issues da R1 (#128) |

**Marco:** release note da R1 publicada.

### Sprints 5 a 12

Plano proposto, revisado na planning de cada sprint.

| Sprint | Vitor | Ítalo | Daniel | Arthur | Gabriel | João Paulo |
|---|---|---|---|---|---|---|
| 5 | Início de salas vazias (RF17) | Scraper de eventos (RF08) | Wireframe do portal do dev (RF14) | Desenho do cache: quais rotas e por quanto tempo (RNF02) | Variáveis de produção no Railway e deploy de teste | Contrato dos novos domínios; medir cobertura |
| 6 | Salas vazias pronta; início da agenda do professor (RF18) | Scraper de editais (RF09) | Swagger UI no portal do dev; tela de salas vazias | Cache Redis nas rotas mais consultadas | Deploy de versão candidata | Contrato de eventos e editais |
| 7 | Agenda do professor pronta | Estabilização de eventos e editais | Telas da agenda, de eventos e de editais | Rate limit com slowapi (RNF01) | Ajuste das variáveis de produção | Observabilidade com UptimeRobot (RNF03) |
| 8 | SDK Python (RF13) | CLI com Typer (RF13) | Portal do dev | Rate limit e cache finalizados; teste simples de carga | Deploy definitivo (RNF06) | Cobertura rumo a 90% (RNF09) |
| 9 | SDK fechado e documentado | CLI fechada | Portal do dev finalizado | Estabilidade em produção | Ajustes pós-deploy | Mutação e sabotagem (RNF09); contratos completos (RNF04) |
| 10 | Revisão de RF01-05, RF17, RF18 | Revisão de RF06-09, RF19 | Polimento visual | Revisão de cache e rate limit | Revisão da documentação | Cobertura final (RNF09) |
| 11 | Correções finais | Correções finais | Correções finais | Correções finais | Release note da R2 | Checklist final do board contra a entrega |
| 12 | Entrega | Entrega | Entrega | Entrega | Entrega | Entrega |

**Marco:** Release 2 entregue em **25/11**, em produção e com release note publicada. A Sprint 12 tem só 3 dias e fica como folga para imprevistos.

**Dependência-chave:** as mudanças de cache e rate limit não podem quebrar os testes de contrato. Rodar a suíte de contrato antes de cada merge dessas mudanças.

## Riscos

| Risco | Quando pesa mais | Mitigação |
|---|---|---|
| O SIGAA (JSF) muda o formulário ou a sessão | Toda a coleta de disciplinas | Scraper falha de forma isolada por unidade (RNF05); [plano de monitoramento](../fontes/plano-de-monitoramento.md) |
| O RU muda o layout do PDF | Toda semana; já aconteceu em 21/09 e 28/09 | PDFs reais como fixtures de teste; falha sem apagar o histórico |
| Período letivo fixo no código | Virada de semestre | Atualizar `ano`/`periodo` em `celery_app.py` antes do semestre começar |
| Dívida de cobertura de testes | Sprints 7 a 10 | Medir a cobertura desde a Sprint 5, não só no fechamento |
| Cache ou rate limit causando regressão na API | Sprints 6 a 8 | Suíte de contrato antes de cada merge |
| Limites do plano gratuito do Railway | Sprints 5 a 12 | Deploy de teste cedo (Sprint 5) para descobrir limites antes do fechamento |
