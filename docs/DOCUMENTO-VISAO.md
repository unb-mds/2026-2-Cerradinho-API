# Documento de Visão — Cerradinho (API Aberta da UnB)

## 1. Introdução

Este documento define a visão do produto Cerradinho: por que ele será construído, para quem, e o que ele entrega em alto nível. Ele serve como referência compartilhada para o time antes de qualquer detalhamento técnico, e deve permanecer estável mesmo quando requisitos específicos mudarem ao longo do projeto. Requisitos funcionais e não-funcionais detalhados estão em [`REQUISITOS.md`](REQUISITOS.md), e as decisões técnicas de como construir o sistema estão em [`ARQUITETURA.md`](ARQUITETURA.md) e nos ADRs em [`adr/`](adr/).

**Escopo**: cobre as duas releases do projeto, distribuídas em 12 semanas (Release 1: semanas 1 a 6, Release 2: semanas 7 a 12), desenvolvido como parte da disciplina de Métodos de Desenvolvimento de Software (MDS) da FCTE/UnB.

## 2. Posicionamento

### 2.1 Declaração do problema

| Campo | Descrição |
|---|---|
| **O problema de** | fragmentação e falta de acesso programático aos dados institucionais públicos da UnB |
| **afeta** | estudantes de graduação e pós-graduação, e desenvolvedores de outras squads e projetos de extensão da universidade |
| **e o impacto disso é** | tempo perdido consultando manualmente múltiplos sistemas (SIGAA, site do RU, agenda de notícias, portal de dados abertos) para responder perguntas simples do cotidiano, e retrabalho de squads que reimplementam scraping próprio e descartável a cada novo projeto |
| **uma solução de sucesso seria** | uma API pública, unificada e versionada, que consolida esses dados automaticamente e os expõe de forma estruturada, documentada e reutilizável |

### 2.2 Declaração de posicionamento do produto

Para **estudantes da UnB e desenvolvedores de squads terceiras** que **precisam consultar dados institucionais espalhados em sistemas desconectados e, em alguns casos, tecnicamente hostis a automação**, o **Cerradinho** é uma **API pública REST** que **consolida disciplinas, professores, salas, cardápio do RU, eventos e editais em um único ponto de acesso, atualizado automaticamente**. Diferente de **continuar consultando cada sistema manualmente ou reimplementar scraping próprio a cada projeto novo**, nosso produto **entrega dado pronto para consumo via API, SDK ou CLI, com documentação viva e sem necessidade de qualquer time reconstruir a coleta do zero**.

## 3. Descrição dos stakeholders e usuários

### 3.1 Resumo dos stakeholders

| Stakeholder | Interesse no projeto |
|---|---|
| Equipe do projeto (Vitor, Ítalo, Daniel, Arthur, Gabriel, João Paulo) | Entregar o sistema dentro do prazo da disciplina, com qualidade avaliável (testes, CI, documentação) |
| Professor/avaliador da disciplina de MDS | Avaliar aderência ao processo (Scrum, ADRs, releases, DoD) e qualidade técnica do entregável |
| Estudantes da UnB | Usuários finais que consultam a API via frontend ou diretamente |
| Desenvolvedores de outras squads/projetos de extensão | Consumidores técnicos, via SDK/CLI, que integram o Cerradinho em seus próprios sistemas |
| UnB (SIGAA, RU, portal de notícias, CKAN) | Fonte dos dados públicos, não participa ativamente do projeto mas define os limites técnicos de coleta (throttling, robots.txt) |

### 3.2 Resumo dos usuários

| Usuário | Descrição | Responsabilidades/uso esperado |
|---|---|---|
| Aluno de graduação | Consulta a API via frontend web, quer respostas rápidas para decisões do dia a dia | Consultar disciplinas, salas vazias, cardápio, agenda de professor |
| Desenvolvedor de squad terceira | Consome a API programaticamente, prefere não lidar com scraping | Integrar via SDK Python ou CLI, consumir endpoints REST diretamente |
| Integrante do próprio time (QA/backend) | Usa a documentação OpenAPI para validar contrato e testar endpoints | Testes de contrato, validação de schema, debugging |

### 3.3 Ambiente do usuário

Os usuários finais (estudantes) acessam via navegador, em desktop ou celular, muitas vezes em rede Wi-Fi do campus com latência variável. Desenvolvedores de squads acessam via chamadas HTTP diretas ou através do SDK/CLI instalado localmente, tipicamente durante desenvolvimento de outros projetos acadêmicos.

### 3.4 Necessidades dos stakeholders e usuários

Síntese de conversas informais com estudantes de graduação da FCTE e integrantes de outras squads de extensão:

| Necessidade | Prioridade | Preocupações atuais | Solução proposta |
|---|---|---|---|
| Saber sala/horário de disciplina rapidamente | Alta | SIGAA lento, interface antiga (JSF) | Endpoint de disciplinas com sala e horário |
| Saber o que tem no RU sem abrir o site | Média | Site do RU pouco usado no celular | Endpoint de cardápio diário/semanal |
| Saber qual sala está livre para estudar | Alta | Não existe hoje, decisão informal ("na sorte") | RF17, salas vazias |
| Não perder prazo de edital | Média | Editais centralizados mas difíceis de acompanhar | Endpoint de editais |
| Reaproveitar dado de UnB sem scraping próprio | Alta (para squads) | Scraping feito do zero em projetos anteriores, descartado depois | SDK/CLI (RF13) |

## 4. Visão geral do produto

### 4.1 Perspectiva do produto

O Cerradinho é um sistema novo, autocontido (monorepo), que não substitui nenhum sistema existente da UnB, apenas consome dados públicos deles e os reoferece de forma consolidada. Ele não depende de nenhuma integração formal com o SIGAA ou o RU (não há parceria ou acordo, apenas consumo de páginas públicas), o que é ao mesmo tempo sua viabilidade (não depende de aprovação institucional) e seu maior risco (mudanças nessas páginas quebram a coleta sem aviso).

### 4.2 Resumo de funcionalidades

| Funcionalidade | Benefício para o usuário |
|---|---|
| Consulta de disciplinas, professores e salas | Elimina a necessidade de navegar o SIGAA público |
| Consulta de cardápio do RU (diário e semanal) | Resposta rápida sem visitar o site do RU |
| Consulta de eventos e editais institucionais | Centraliza informação hoje espalhada em notícias e portais de pós |
| Busca de salas vazias por horário | Funcionalidade nova, que não existe em nenhum sistema da UnB hoje |
| Agenda do professor | Visão consolidada que hoje exige cruzar múltiplas turmas manualmente |
| SDK e CLI Python | Permite que outras squads integrem sem reimplementar scraping |
| Documentação OpenAPI/Swagger | Portal do desenvolvedor autoexplicativo, sem necessidade de suporte manual |
| Atualização automática agendada | Garante que o dado não fique desatualizado sem intervenção humana |

### 4.3 Hipóteses e dependências

- Assume-se que o SIGAA público, o site do RU e o portal de notícias permanecerão acessíveis sem login durante todo o projeto (nenhum é garantido contratualmente).
- Assume-se throttling suficiente para não sobrecarregar os servidores da UnB nem disparar bloqueio de IP.
- O projeto depende de hospedagem em nuvem (Railway) que precisa suportar Postgres, Redis e ao menos dois serviços (API e worker) dentro de um orçamento compatível com um projeto acadêmico sem patrocínio.

## 5. Restrições

- **Prazo fixo**: 12 semanas, dividido em 2 releases de 6 semanas, sem possibilidade de extensão (calendário acadêmico da disciplina).
- **Equipe fixa de 6 pessoas**, com dedicação parcial (paralela a outras disciplinas do curso).
- **Fontes de dado fora do controle do time**: qualquer mudança de layout no SIGAA, RU ou portal de notícias exige manutenção reativa, não planejada.
- **Sem orçamento** para ferramentas pagas de infraestrutura, observabilidade ou segurança além de planos gratuitos/educacionais (ex: Railway free tier, UptimeRobot free).
- **Stack tecnológica fixada em ADR** (Python 3.12, SQLAlchemy síncrono, FastAPI, Next.js, Celery/Redis), mudanças de stack no meio do projeto teriam custo alto.
- **Avaliação acadêmica**: o processo (ADRs, sprints documentadas, PRs revisados) é tão avaliado quanto o produto final, o que impõe overhead de documentação além do desenvolvimento em si.

## 6. Faixas de qualidade

| Atributo | Faixa esperada | Requisito relacionado |
|---|---|---|
| Disponibilidade | Software implantado e acessível publicamente ao fim de cada release (gate obrigatório, não é meta de uptime contínuo) | RNF06 |
| Desempenho | Respostas de leitura da API servidas via cache quando o dado não muda a cada requisição | RNF02 |
| Segurança | Nenhum achado crítico ou alto em análise estática (SAST) bloqueando o release | RNF08 |
| Confiabilidade dos dados | Scrapers falham de forma isolada (uma unidade/fonte com erro não derruba as demais) | RNF05 |
| Qualidade de teste | Cobertura de linha ≥70% no módulo de domínio, escore de mutação ≥50% nos módulos críticos | RNF09 |
| Documentação | OpenAPI sempre reflete o estado real da API implantada, sem exemplos desatualizados | RNF07 |
| Capacidade de integração | Terceiros conseguem consumir a API sem depender de suporte manual do time (SDK, CLI, docs autoexplicativas) | RF13, RF14 |

## 7. Precedência e priorização

| Prioridade | Itens | Release |
|---|---|---|
| **Essencial (must have)** | Disciplinas + Professores + Salas (RF01-05), rotas REST versionadas (RF10-12), agendamento automático com log (RF15-16) | Release 1 |
| **Essencial (must have)** | Cardápio do RU (RF06-07) | Release 1 |
| **Importante (should have)** | Eventos e Editais (RF08-09), features derivadas (RF17-19), SDK/CLI (RF13), cache e rate limit (RNF01-02) | Release 2 |
| **Desejável (could have)** | Portal do desenvolvedor dedicado além do Swagger (RF14), observabilidade avançada além de uptime básico (RNF03) | Release 2, se sobrar tempo |
| **Fora de escopo (won't have, por ora)** | Autenticação de usuário, aplicativo mobile nativo, tradução multilíngue, recomendação com IA | Nenhuma release atual |

## 8. Documentação de apoio

- Requisitos detalhados: [`REQUISITOS.md`](REQUISITOS.md)
- Arquitetura e padrões de código: [`ARQUITETURA.md`](ARQUITETURA.md)
- Decisões técnicas registradas: [`adr/`](adr/)
- Processo de time, Git, ADR e story map: [`PROCESSO.md`](PROCESSO.md)
- Estudos de viabilidade técnica: [`estudos/`](estudos/)
- Planejamento de sprints e Definition of Done: [`scrum/sprint-planning.md`](scrum/sprint-planning.md)
