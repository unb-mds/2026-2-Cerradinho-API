# Requisitos — Cerradinho

Requisitos funcionais e não funcionais da API. O porquê do produto está no [Documento de Visão](DOCUMENTO-VISAO.md), o como no [ARQUITETURA.md](ARQUITETURA.md) e o quando no [planejamento de sprints](scrum/sprint-planning.md).

## 1. Objetivo

API pública que consolida dados da UnB hoje espalhados em vários sistemas: disciplinas, professores, salas e prédios, cardápio do RU, eventos e editais. Todas as fontes usadas são públicas, sem login.

## 2. Fontes de dados

| Domínio | Fonte | Observação |
|---|---|---|
| Disciplinas | sigaa.unb.br/sigaa/public/turmas | JSF (ViewState/postback), precisa de Playwright. Ficha: [`fontes/sigaa-disciplinas.md`](fontes/sigaa-disciplinas.md) |
| Professores | Mesma página das turmas | Vem junto da turma, sem fonte própria |
| Salas/Prédios | Sem fonte própria | Derivado das turmas (RF05) |
| Cardápio do RU | ru.unb.br/cardapio-refeitorio | PDF semanal por campus. A URL `/cardapio` está desatualizada. Ficha: [`fontes/ru-cardapio.md`](fontes/ru-cardapio.md) |
| Eventos | noticias.unb.br/agenda | Agenda institucional pública |
| Editais | Portal público do SIGAA (pós-graduação) | Centralizado |
| Cursos/Estrutura curricular | sigaa.unb.br/sigaa/public/curso | Complemento possível, ainda não usado |
| Dados abertos | dadosabertos.unb.br (CKAN) | Complemento possível, ainda não usado. Turmas desatualizadas desde 2022 |

Os riscos de cada fonte estão no [relatório de risco](fontes/relatorio-de-risco.md) e no [plano de monitoramento](fontes/plano-de-monitoramento.md).

## 3. Requisitos funcionais

**Disciplinas**
- RF01 - Capturar oferta de disciplinas de todas as unidades (nome, código, turma, horário, vagas), com scraper por unidade e throttling
- RF02 - Associar disciplina a professor
- RF03 - Associar disciplina a sala/prédio

**Professores**
- RF04 - Cadastro de docentes vinculados às disciplinas

**Salas/Prédios**
- RF05 - Localização e identificação de salas e prédios (derivado de RF01)

**Cardápio do RU**
- RF06 - Capturar cardápio diário
- RF07 - Manter histórico de cardápios

**Eventos**
- RF08 - Capturar eventos institucionais (data, local, descrição)

**Editais**
- RF09 - Capturar editais publicados (título, data, link, órgão)

**API pública**
- RF10 - Endpoints REST por domínio
- RF11 - Documentação OpenAPI/Swagger
- RF12 - Versionamento (`/v1/`)
- RF13 - SDK/CLI para integração de terceiros e squads futuros
- RF14 - Portal do desenvolvedor

**Atualização de dados**
- RF15 - Agendamento automático de scraping
- RF16 - Log de sucesso/falha de cada execução

## 4. Features derivadas

Calculadas em cima do que os domínios acima já capturam, com pouco esforço extra.

- **RF17 - Salas vazias**: `GET /v1/salas/vazias?dia=segunda&horario=14:00`. Cruza Sala com Disciplina no horário pedido. Só reflete aula cadastrada, não reserva informal.
- **RF18 - Agenda do professor**: `GET /v1/professores/{nome}/agenda`. Lista as turmas de um docente.
- **RF19 - Cardápio semanal**: `GET /v1/cardapio/semana?data_inicio=...`. Agrupa 7 dias de histórico.

## 5. Requisitos não funcionais

| ID | Requisito | Descrição |
|---|---|---|
| RNF01 | Rate limiting | Limitar requisições por cliente/IP |
| RNF02 | Cache | Reduzir tempo de resposta e carga no banco |
| RNF03 | Observabilidade | Monitoramento de uptime e alertas |
| RNF04 | Testes de contrato | API não pode quebrar o formato esperado |
| RNF05 | Resiliência | Scraper falha de forma graciosa se a fonte mudar |
| RNF06 | Disponibilidade | **Porta de qualidade obrigatória da Release 2**: a nota da Release 2 só é lançada com software implantado e acessível. Não é meta de uptime, é bloqueador de avaliação. A Release 1 não precisa estar em produção |
| RNF07 | Doc viva | Documentação reflete o estado real da API |
| RNF08 | CI/CD | Pipeline de integração contínua (lint, testes, cobertura, SAST) configurado desde a Release 1. Achados críticos/altos em SAST bloqueiam o lançamento da nota |
| RNF09 | Qualidade de testes | Cobertura de linhas ≥90% no backend; escore de mutação ≥50% nos módulos críticos; teste de sabotagem cobrindo 100% dos módulos críticos |

## 6. Rastreabilidade

Cada requisito tem uma issue no GitHub, na milestone da release em que entra.

| Requisito | Release | Responsável | Issue |
|---|---|---|---|
| RF01 - Oferta de disciplinas | R1 | Vitor | #35 |
| RF02 - Disciplina ↔ professor | R1 | Vitor | #36 |
| RF03 - Disciplina ↔ sala | R1 | Vitor | #37 |
| RF04 - Docentes | R1 | Vitor | #38 |
| RF05 - Salas e prédios | R1 | Vitor | #39 |
| RF06 - Cardápio diário | R1 | Ítalo | #40 |
| RF07 - Histórico de cardápios | R1 | Ítalo | #41 |
| RF08 - Eventos | R2 | Ítalo | #47 |
| RF09 - Editais | R2 | Ítalo | #48 |
| RF10 - Endpoints REST | R1 | Daniel | #42 |
| RF11 - OpenAPI/Swagger | R1 | Daniel | #43 |
| RF12 - Versionamento `/v1/` | R1 | Gabriel | #44 |
| RF13 - SDK (Vitor) e CLI (Ítalo) | R2 | Vitor, Ítalo | #49 |
| RF14 - Portal do desenvolvedor | R2 | Daniel | #52 |
| RF15 - Agendamento | R1 | Arthur | #45 |
| RF16 - Log de execução | R1 | Arthur | #46 |
| RF17 - Salas vazias | R2 | Vitor | #53 |
| RF18 - Agenda do professor | R2 | Vitor | #50 |
| RF19 - Cardápio semanal | R2 | Ítalo | #51 |
| RNF01 - Rate limiting | R2 | Arthur | #66 |
| RNF02 - Cache | R2 | Arthur | #67 |
| RNF03 - Observabilidade | R2 | João Paulo | #68 |
| RNF04 - Testes de contrato | R1 | João Paulo | #69 |
| RNF05 - Resiliência | R1 | João Paulo | #70 |
| RNF06 - Disponibilidade | R2 | Gabriel | #71 |
| RNF07 - Doc viva | R1 | João Paulo | #72 |
| RNF08 - CI/CD | R1 | João Paulo | #73 |
| RNF09 - Qualidade de testes | R2 | João Paulo | #74 |
