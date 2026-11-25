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

### Sprint 5 — Pendências da R1 e preparação do deploy (11/10 a 17/10)

**Objetivo:** fechar as pendências conhecidas da Release 1 (duplicidade de professor/sala, parser do RU, log de execução), avançar os protótipos de tela e preparar o deploy.

**Entregue:** Vitor corrigiu a duplicidade de professor (o SIGAA embute a carga horária da disciplina no nome do docente, e isso fazia o mesmo professor virar um registro por carga horária distinta) e a duplicidade de sala (separador e caixa inconsistentes no texto de local do SIGAA), e implementou o RF04 — busca de docente por nome normalizado (`GET /v1/professores?nome=`), tudo pelo PR #140. Arthur terminou o log de execução (RF16): os scrapers passaram a diferenciar falha de fonte de falha interna, toda execução é gravada em `execucao_logs`, e o endpoint `GET /v1/execucoes` expõe esse histórico; também fez o desenho do cache (RNF02). Gabriel corrigiu o parser do RU pros PDFs em layout novo (#145) e preparou o deploy (`REDIS_URL`, `docs/DEPLOY.md`). Daniel entregou os protótipos navegáveis da agenda do professor e da tela de salas vazias, já ligados ao protótipo único com o menu lateral completo, e o wireframe do portal do desenvolvedor. João Paulo atualizou o pipeline de CI e o workflow pra Node 24, e mediu a cobertura de testes do backend, definindo os módulos críticos do RNF09.

**Métricas:** PR #140 (professor/sala duplicados, RF04) e PR #145 (parser do RU) mergeados; RF16 entregue com testes cobrindo a classificação fonte/interna e o endpoint `/v1/execucoes`; módulos críticos do RNF09 definidos e registrados na spec.

**Retrospectiva:** as três limitações conhecidas da Release 1 — professor/sala duplicados, busca de professor sem normalização e parser do RU quebrado — fecharam nesta sprint, junto com o log de execução que também vinha como pendência. As variáveis de ambiente do deploy no Railway ficaram pra Sprint 6. O Ítalo saiu do projeto no início da Release 2: eventos (RF08) e editais (RF09) saíram do escopo, e o parser do RU, o cardápio semanal e a CLI foram redistribuídos entre Gabriel e João Paulo.

### Sprint 6 — Salas vazias, cardápio semanal, cache e rate limit (18/10 a 24/10)

**Objetivo:** entregar o RF17 (salas vazias), o RF19 (cardápio semanal), o cache (RNF02) e avançar a infraestrutura de leitura (rate limit, testes de contrato) pra Release 2.

**Entregue:** Vitor implementou o RF17 (`GET /v1/salas/vazias`, PR #149) e, rodando o scraper contra todas as unidades, corrigiu um lote de bugs de produção no Darcy: código de horário com vários segmentos estourando a coluna e sendo ignorado no cálculo de ocupação, raspagem inteira quebrando por uma turma ou unidade com erro, sala duplicada por normalização inconsistente ("LAB"/andar/separador do Darcy), e turma com sala diferente por dia que não marcava a ocupação certa — resolvido movendo a sala da turma pro horário (ADR 0010, PR #230). Gabriel corrigiu o parser do RU e o formato do Redis no Railway (#145), implementou o RF19 — cardápio semanal agrupado por dia (#227) —, revisou a `dev` antes do merge pra `main` (#233) e publicou a release note da v1.2, mergeando a `dev` na `main` pela primeira vez desde a `Release_1` (#235, #236). Daniel entregou a navegação por semana e o portal do desenvolvedor com Swagger UI no cardápio (RF14, #148) e a tela de Salas Vazias no frontend (#228). Arthur implementou o cache em Redis (RNF02, #150) e o rate limit por IP (RNF01, #229). João Paulo mediu a cobertura e os módulos críticos do RNF09 (#147) e escreveu os testes de contrato de salas vazias, cardápio semanal e log de execução (#231).

**Métricas:** 9 PRs mergeados na `dev` (#145, #148, #149, #150, #227, #228, #229, #230, #231), mais a release note e o merge pra `main` (#233, #235, #236); CI verde em todos, incluindo as migrations de banco novas (`0003`, `0004`, `0005`).

**Retrospectiva:** a sprint entregou tudo que planejava (RF17, RF19, cache, rate limit) e ainda fechou, de bônus, um lote de bugs de produção que só apareceram testando contra o Darcy de verdade — sinal de que vale continuar validando contra dado real antes de fechar uma funcionalidade, não só contra a fixture de uma unidade. A sala por horário (ADR 0010) foi a decisão de arquitetura mais relevante da sprint, e já é consumida pelo RF17 e pelo `GET /v1/disciplinas` sem quebrar o contrato público. Com o merge na `main`, a Release 2 passa a ter uma versão publicada de verdade (v1.2) — o deploy no Railway continua como a principal pendência pra próxima sprint.

### Sprint 7 — Agenda do professor, rate limit e versão candidata (25/10 a 31/10)

**Objetivo:** entregar o RF18 (agenda do professor), o rate limit (RNF01), avançar a observabilidade e preparar uma versão candidata em produção.

**Entregue:** Vitor implementou o RF18 (`GET /v1/professores/{id}/agenda`, PR #237), reaproveitando a grade de horário do RF17 pra decompor em dia/início/fim sem duplicar a regra no front, com a sala já por bloco (compatível com turma de sala por dia, ADR 0010); no caminho, corrigiu a grade noturna (achado do Daniel: faltava a N4 e os horários estavam errados), confirmada contra turma real de várias unidades. Daniel entregou a tela da agenda do professor e tirou do front o remendo que cobria o bug da grade noturna, agora corrigida no backend (#238). Arthur implementou o rate limit por IP com slowapi (RNF01, #229). Gabriel decidiu trocar o destino do deploy de Railway para AWS Lightsail (ADR 0011) — o teste grátis do Railway acaba antes da entrega, e o crédito de conta nova da AWS cobre os 6 meses seguintes — e atualizou o guia de deploy, a arquitetura, o Documento de Visão e o planejamento de sprints de acordo (#240). João Paulo adicionou `GET /v1/saude` pro UptimeRobot, documentou os estudos de teste de mutação e UptimeRobot, e fechou o contrato da agenda do professor (#239).

**Métricas:** 4 PRs mergeados na `dev` (#237, #238, #239, #240); CI verde em todos; uma decisão de arquitetura nova (ADR 0011) substituindo a anterior (ADR 0009) antes de qualquer deploy real acontecer.

**Retrospectiva:** a sprint fechou tudo que planejava, incluindo uma correção de prioridade alta (grade noturna) que só apareceu porque o Daniel testou a tela da agenda contra turma real antes de confiar no horário — o mesmo padrão de "validar contra dado real" que fechou os bugs do Darcy na Sprint 6. A troca de Railway pra AWS Lightsail, decidida e documentada nesta sprint, evita um corte abrupto de acesso perto da entrega (o teste grátis do Railway acaba em 18/11, uma semana antes do prazo) — vale a atenção de todo o time pro novo passo a passo de deploy em `docs/DEPLOY.md`, porque o deploy na Lightsail é manual (sem a esteira automática que o Railway dava). Com o RF18 fechado, falta só o SDK/CLI (RF13, Sprint 8) entre as features novas planejadas pra Release 2.

### Sprint 8 — SDK, portal do desenvolvedor e deploy definitivo (01/11 a 07/11)

**Objetivo:** estruturar o SDK Python (RF13), fechar o portal do desenvolvedor e o deploy definitivo na AWS (RNF06).

**Entregue:** Vitor estruturou o SDK Python do zero — cliente gerado a partir do OpenAPI do backend (RF11), com `CerradinhoClient` por cima encapsulando um método por endpoint de `/v1/` — e corrigiu a sala do Darcy com o código de horário embutido no campo (achado rodando o scraper contra produção) e os 9 achados da revisão do Gabriel no PR do SDK (PR #241, mergeado já no primeiro dia da Sprint 9). Daniel fechou os estados que faltavam na agenda do professor (carregamento, erro, "Professor não encontrado", grade vazia) e os horários noturnos reais do SIGAA nos filtros de Salas Vazias e Disciplinas (#238). João Paulo fechou pendências da Sprint 7 — contrato da agenda cobrindo turma noturna sem sala, estudo de teste de mutação com cosmic-ray e de UptimeRobot, com a rota `/health` pro monitor da API (#239). Gabriel trocou o destino do deploy pra AWS Lightsail de verdade (ADR 0011) e registrou os endereços de produção no ar — site e API, com Swagger em `/docs` (#240, #242).

**Métricas:** 4 PRs mergeados na janela da sprint (#238, #239, #240, #242); 4 issues fechadas.

**Retrospectiva:** o marco da sprint foi o deploy definitivo entrando no ar de verdade (site e API acessíveis publicamente, não só um ambiente de teste) e o SDK começando do zero com revisão real do Gabriel no mesmo PR. Por outro lado, o Arthur não teve nenhum PR mergeado nesta sprint — o item planejado ("cache e rate limit finalizados; teste simples de carga") só fechou na Sprint 10, com o PR #243. Primeiro sinal de atraso que valeria ter sido conversado na própria semana, não só identificado depois.

### Sprint 9 — SDK fechado, CLI e portal finalizados (08/11 a 14/11)

**Objetivo:** fechar e documentar o SDK (RF13), finalizar o portal do desenvolvedor, entregar a CLI (RF13) e os monitores do UptimeRobot (RNF03), e deixar o worker/agendamento estáveis em produção (RF15).

**Entregue:** Vitor fechou o README do SDK com exemplos de uso, e documentou a decisão de que "publicar" o SDK é uma tag no GitHub quando entrar na `main`, não PyPI (PR #246). Daniel fechou o portal do desenvolvedor — o cartão da CLI deixou de ser "em breve", com comandos reais contra a API em produção (#244, #247). João Paulo entregou a CLI em Typer sobre o SDK, com um comando por método do `CerradinhoClient`, e os monitores do UptimeRobot criados por script a partir da API deles (#245).

**Métricas:** 5 PRs mergeados na janela da sprint (#241, #244, #245, #246, #247); 28 issues fechadas (inclui um lote de 23 fechadas em 10/11, provavelmente uma limpeza de board em bloco, não 23 entregas distintas nesse dia).

**Retrospectiva:** segunda sprint seguida sem nenhum PR do Arthur nem do Gabriel — o item do Arthur (RF15, worker estável em produção) e os dois do Gabriel (#203 ajustes pós-deploy, #204 rastreabilidade das specs) carregaram pra Sprint 10 sem terem sido sequer abertos como PR. Com a R2 entregando em 25/11, duas sprints de silêncio de duas pessoas do time é um risco real que devia ter sido escalado na reunião, não só registrado na ata depois.

### Sprint 10 — Fechamento das features e da qualidade de testes (15/11 a 21/11)

**Objetivo:** fechar os ajustes finais de cada feature (salas vazias, agenda, cardápio), as metas de qualidade de teste do RNF09 e os itens que ficaram das Sprints 8 e 9.

**Entregue:** Vitor removeu o `"A DEFINIR DOCENTE"` da listagem de professores (mais de 150 disciplinas acumuladas num só registro, agenda ilegível) e expôs o `X-Total-Count` no CORS, entre outros ajustes (PR #250). Daniel resolveu o caso de 12 turmas simultâneas na agenda virando colunas ilegíveis (#251) e começou o recorte do frontend pro campus Gama — home "Agora no Gama", chamada da API visível em cada tela (#257). Gabriel voltou com força: corrigiu o parser do RU que tinha quebrado em produção (#252, #258), reescreveu `/v1/disciplinas` pra paginar no banco (de ~9,5s pra ~20ms em `limite=10`) e `/v1/salas/vazias` pra semana em blocos de 2h (#256), corrigiu o `/v1/resumo` que ainda contava o placeholder do Vitor (#254), preparou o repositório pra contribuição externa (#253) e publicou a release note da v1.4 (#259). Arthur também voltou: o teste de carga pendente desde a Sprint 8 (#243), o log de execução informando as unidades que falharam (#255) e a atualização da spec do RF15 (#249). João Paulo fechou as metas do RNF09 — cobertura de 81% pra 98%, mutação medida em todos os 8 módulos críticos, sabotagem nos 8 de 8, achando 3 falhas silenciosas reais no scraper do SIGAA (#248) — e não teve mais nenhum PR depois disso na sprint.

**Métricas:** 13 PRs mergeados na janela da sprint (#243, #248, #249, #250, #251, #252, #253, #254, #255, #256, #257, #258, #259) — mais do que o dobro de qualquer sprint anterior da R2; 12 issues fechadas.

**Retrospectiva:** sprint de recuperação — o Arthur e o Gabriel fecharam de uma vez o que tinha ficado pra trás nas duas sprints anteriores, e o RNF09 bateu a meta de qualidade de teste. O lado de risco: 13 PRs numa semana só é um volume concentrado, bem acima do ritmo normal da R2 (3 a 6 PRs por sprint até aqui) — maior chance de revisão superficial sob pressão de prazo, mesmo com CI verde em todos. O João Paulo, que vinha entregando toda sprint desde o início da R2, não teve PR depois do #248 (16/11) — o item dele planejado pra esta sprint (contratos completos do RNF04) não avançou.

### Sprint 11 — Correções finais e entrega da R2 (22/11 a 25/11)

**Objetivo:** sprint curta e final — só corrigir o que falta, sem feature nova (regra combinada desde o planejamento da Sprint 10), e entregar a Release 2 em 25/11.

**Entregue até o momento deste registro (24/11, um dia antes da entrega):** Vitor fechou os bugs restantes de disciplinas/features derivadas/SDK (issue #216) — o SDK tinha ficado sem o parâmetro `fim` de `/v1/salas/vazias` desde o #256, e o script de geração do cliente (`gerar_cliente.sh`) podia gerar código importando um pacote diferente do que o projeto declara, se o ambiente tivesse esse pacote instalado por qualquer outra dependência; o script agora falha alto nesse caso em vez de deixar passar. Testou o parser de sala do Darcy e as funções de disciplinas/salas vazias/agenda contra as 6577 turmas reais de produção, sem achar bug novo. Daniel fez o pente-fino do frontend antes do feature freeze — cardápio como "RU UnB", um erro de hidratação real em Cardápio/Salas Vazias e o filtro de horário de Disciplinas que só olhava o primeiro horário da turma (#260, #261).

**Pendente até a entrega:** Gabriel escrever a release note da R2 e mergear a `dev` na `main` com a tag da release; Arthur confirmar que a API e o frontend estão acessíveis em produção; João Paulo conferir o checklist final do board contra a entrega, com CI verde e SAST sem achado alto no commit da entrega.

**Métricas (parciais):** 2 PRs mergeados até agora (#260, #261), mais 1 em revisão (#262); 3 issues fechadas.

**Retrospectiva (parcial — esta seção pode precisar de atualização depois da entrega de 25/11):** sprint corretamente curta e sem feature nova, como planejado. O risco maior entrando no último dia é a concentração de trabalho de entrega (release note, merge pra `main`, tag, checklist final) em só 3 das 5 pessoas do time, sem folga — qualquer imprevisto de última hora tem pouco espaço de manobra até o prazo de 25/11.

## Velocity da Release 2 (PRs e issues por sprint)

Contagem de PRs mergeados na `dev`/`main` e issues fechadas, por data, uma linha por sprint — inclui a Release 1 (Sprints 0 a 3) pra comparação.

| Sprint | Período | PRs mergeados | Issues fechadas |
|---|---|---|---|
| 0 | até 06/09 | 4 | 1 |
| 1 | 07/09 a 13/09 | 24 | 16 |
| 2 | 14/09 a 20/09 | 8 | 11 |
| 3 | 21/09 a 27/09 | 13 | 13 |
| 4 | 04/10 a 10/10 | 4 | 3 |
| 5 | 11/10 a 17/10 | 3 | 0 |
| 6 | 18/10 a 24/10 | 6 | 0 |
| 7 | 25/10 a 31/10 | 12 | 35 |
| 8 | 01/11 a 07/11 | 4 | 4 |
| 9 | 08/11 a 14/11 | 5 | 28 |
| 10 | 15/11 a 21/11 | 13 | 12 |
| 11 | 22/11 a 25/11 (parcial) | 2 (+1 em revisão) | 3 |

**O que isso mostra:** a contagem de issues fechadas por data bate em blocos (31 em 27/10, 23 em 10/11), não em ritmo constante — a equipe fecha issues em lote perto de marcos (merge pra `main`, limpeza de board), não uma por uma conforme termina. Isso significa que "issues fechadas na sprint X" mede quando o board foi arrumado, não necessariamente quando o trabalho aconteceu — o número de PRs mergeados, puxado pela data real do merge, é o indicador mais confiável de ritmo de entrega sprint a sprint neste projeto. Por esse indicador, a R2 teve duas sprints de baixo volume (5 e 6, ainda em estudo/preparação) e um pico claro na Sprint 10 (13 PRs) puxado pela recuperação do atraso do Arthur e do Gabriel das Sprints 8 e 9 — ver a retrospectiva de cada sprint para o detalhe de quem entregou o quê.
