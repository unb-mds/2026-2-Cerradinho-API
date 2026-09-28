# Checklist board vs. entrega — Release 1

Conferência do que está no board do GitHub contra o que foi de fato entregue na `dev`, feita no fechamento da R1 ([#128](https://github.com/unb-mds/2026-2-Cerradinho-API/issues/128), sub-issue de [#107](https://github.com/unb-mds/2026-2-Cerradinho-API/issues/107)).

- **Data da conferência:** 28/09/2026
- **Responsável:** João Paulo
- **Base conferida:** `dev` em `e48e2d2` (merge do #130)

## Como foi conferido

Para cada issue da R1 (as de sprint S1 a S3, as sub-issues e as de requisito do escopo da R1), foram comparados:

1. o status no board (aberta ou fechada, e quais critérios de aceitação estão marcados);
2. o que está mergeado na `dev`: código, testes e PRs ligados à issue;
3. a evidência de cada critério: PR mergeado, teste automatizado ou run de CI.

Legenda da coluna **Entrega**: ✅ entregue com evidência · ⚠️ entregue em parte · ❌ não entregue.

## Situação geral

| Item | Situação |
|---|---|
| CI na `dev` | ✅ Os 6 últimos runs passaram (lint, SAST, testes, contrato e integração com Postgres) |
| `main` | ⚠️ Parada no #30. A `dev` está 126 commits à frente, então nada da R1 chegou à `main` |
| Release note | ❌ Nenhuma release publicada no GitHub (#106 aberta) |
| Proteção de branch | ⚠️ `dev` sem proteção; `main` protegida, mas sem nenhum check obrigatório. O CI falha, mas não bloqueia o merge |
| Fechamento automático de issues | ⚠️ Os PRs vão para a `dev`, mas o GitHub só fecha issues pelo `Closes #` em merges na branch padrão (`main`). Por isso issues com PR mergeado continuam abertas (ex.: #126) |

## Issues de sprint

### Sprint 1

| Issue | Responsável | Board | Entrega | Evidência | Divergência |
|---|---|---|---|---|---|
| #60 Scraper de Disciplinas (SIGAA) | Vitor | Fechada, 2/2 | ✅ | #75, #88 | — |
| #61 Scraper do Cardápio do RU | Ítalo | Fechada, 0/2 | ✅ | #92 (parser separa café, almoço e jantar; persistência em `persistir_cardapio`) | Critérios não marcados |
| #62 Setup do Next.js e protótipo | Daniel | Fechada, 1/2 | ⚠️ | #91, #93 | "Protótipo revisado com o time" sem evidência registrada |
| #63 docker-compose com Celery e Redis | Arthur | Fechada, 2/2 | ✅ | #89 | — |
| #64 Schema inicial no SQLAlchemy | Gabriel | Fechada, 2/2 | ✅ | #86 | — |
| #65 Pipeline de CI e validação das fontes | João Paulo | Fechada, 2/2 | ✅ | #57, #85, #90 | — |
| #34 Configurar pipeline de CI | João Paulo | Fechada, 0/3 | ✅ | #57 (`ci.yml` com ruff e pytest em PRs para `dev`/`main`) | Critérios não marcados |
| #84 Corrige lint e testes no CI | João Paulo | Fechada, 3/3 | ✅ | #85 | — |
| #87 Riscos das fontes de dado | João Paulo | Fechada, 5/5 | ✅ | #90 | — |

### Sprint 2

| Issue | Responsável | Board | Entrega | Evidência | Divergência |
|---|---|---|---|---|---|
| #95 Agendamento com log de execução | Arthur | Fechada, 2/2 | ✅ | #96; a task só passou a ser registrada no worker com o #121 | Fechada antes de o agendamento funcionar de fato (corrigido depois, no #121) |
| #97 Persistência estável de Disciplinas | Vitor | Fechada, 2/2 | ✅ | #88, #118; teste de integração com Postgres (#124) | — |
| #98 RU agendado com histórico acumulando | Ítalo | Aberta, 0/2 | ⚠️ | Agendamento diário do cardápio no #121, testado no #127 | Critério 1 cumprido e não marcado. Critério 2 depende do parser do RU (#103) |
| #99 Telas conectadas à API real | Daniel | Fechada, 2/2 | ✅ | #117 | — |
| #100 Endpoints `/v1` com OpenAPI | Gabriel | Fechada, 0/2 | ✅ | #108, #119; testes de contrato (#114) | Critérios não marcados |
| #101 Testes de contrato no CI | João Paulo | Fechada, 0/2 | ✅ | #112, #114 | Critérios não marcados |
| #111 Estrutura do schemathesis | João Paulo | Fechada, 0/4 | ✅ | #112 | Critérios não marcados |
| #113 Contrato com dados de exemplo e CI | João Paulo | Fechada, 0/4 | ✅ | #114 | Critérios não marcados |
| #115 SAST com Bandit e bloqueio de merge | João Paulo | Fechada, 5/5 | ⚠️ | #116 (Bandit no CI, sem achados) | Critério da proteção de branch marcado, mas não configurado |

### Sprint 3

| Issue | Responsável | Board | Entrega | Evidência | Divergência |
|---|---|---|---|---|---|
| #102 Estabilização do scraper de Disciplinas | Vitor | Fechada, 2/2 | ✅ | #118 (horário e vagas em branco corrigidos, com testes); regressão coberta pelo #124 | — |
| #103 Estabilização do scraper do RU | Ítalo | Aberta, 0/2 | ❌ | Nenhuma mudança no parser do RU desde o relato; os PDFs de 21/9 e 28/9 ainda não viraram fixtures | — (status correto) |
| #104 Ajustes de UX e dado real nas telas | Daniel | Fechada, 2/2 | ✅ | #117, #120, #122 | — |
| #105 Execução automática validada | Arthur | Fechada, 0/2 | ⚠️ | #121 (registro das tasks, Chromium na imagem, task do cardápio); registro e agendamento testados no #127 | Critérios não marcados; não há registro de uma execução real do worker nem do log de falha |
| #106 Release note e checklist da OpenAPI | Gabriel | Aberta, 0/2 | ⚠️ | OpenAPI completa no #129 | Critério 2 cumprido e não marcado. Release note não publicada |
| #107 Contrato completo e CI verde | João Paulo | Aberta, 0/3 | ⚠️ | Contrato cobre as 4 rotas `/v1` (#114); CI verde na `dev` | Critérios 1 e 2 cumpridos e não marcados. Critério 3 é esta conferência (#128) |
| #123 Integração com Postgres no CI | João Paulo | Fechada, 5/5 | ✅ | #124 | — |
| #126 Testes de registro das tasks do Celery | João Paulo | Aberta, 0/5 | ✅ | #127 | PR mergeado, mas a issue não fechou (merge na `dev`, ver "Situação geral") |

## Requisitos do escopo da R1

| Issue | Responsável | Board | Entrega | Evidência | Divergência |
|---|---|---|---|---|---|
| #35 RF01 Oferta de disciplinas | Vitor | Fechada, 2/2 | ✅ | #75, #88, #118 | — |
| #36 RF02 Disciplina ↔ professor | Vitor | Aberta, 0/1 | ✅ | Associação feita na turma (`turma_professores`), #97/#118; conferida no teste de integração (#124) | Critério fala em `professor_id` na tabela Disciplina, mas o modelo associa pela turma. Critério desatualizado |
| #37 RF03 Disciplina ↔ sala | Vitor | Aberta, 0/1 | ✅ | `turmas.sala_id` (ADR 0006), #97/#118; conferida no #124 | Mesmo caso do RF02: critério fala em `sala_id` na Disciplina |
| #38 RF04 Cadastro de docentes | Vitor | Aberta, 0/1 | ⚠️ | `/v1/professores` lista os docentes (#119) | Não há busca por nome normalizado, que é o critério (status correto) |
| #39 RF05 Localização de salas | Vitor | Fechada, 0/1 | ✅ | Salas criadas pelo scraper de RF01 (`_get_ou_cria_sala`, ADR 0006) | Critério não marcado |
| #40 RF06 Cardápio diário do RU | Ítalo | Aberta, 0/1 | ⚠️ | #92 | Parser falha nos layouts de PDF atuais (#103) (status correto) |
| #41 RF07 Histórico de cardápios | Ítalo | Aberta, 0/1 | ⚠️ | `/v1/cardapio/semana?data_inicio=<data>` consulta semanas passadas | Sem histórico acumulando enquanto o parser falhar (#98, #103) (status correto) |
| #42 RF10 Endpoints REST por domínio | Daniel | Fechada, 0/1 | ✅ | #108, #119; testes de contrato (#114) | Critério não marcado |
| #43 RF11 OpenAPI/Swagger | Daniel | Fechada, 0/1 | ✅ | `/docs` gerado pelo FastAPI (#108); descrições completas no #129 | Critério não marcado |
| #44 RF12 Versionamento `/v1` | Gabriel | Fechada, 0/1 | ✅ | Todas as rotas sob `/v1` (`app/main.py`, ADR 0005) | Critério não marcado |
| #45 RF15 Agendamento automático | Arthur | Aberta, 0/1 | ⚠️ | Disciplinas (semanal) e cardápio (diário) agendados no #121, testados no #127 | A execução do cardápio falha enquanto o parser do RU não for corrigido (#103) (status correto) |
| #46 RF16 Log de execução | Arthur | Fechada, 0/1 | ✅ | `tasks/logging_signals.py` registra sucesso e falha com timestamp (#96) | Critério não marcado |
| #69 RNF04 Testes de contrato | João Paulo | Fechada, 2/2 | ✅ | #112, #114 | — |
| #70 RNF05 Resiliência | João Paulo | Aberta, 0/2 | ⚠️ | Tasks separadas por fonte; unidade do SIGAA que falha fica de fora sem derrubar as outras (`buscar_html_varias_unidades`) | Log de falha só tem o nome da task e a exceção, sem contexto de fonte ou unidade (status correto) |
| #72 RNF07 Doc viva | João Paulo | Aberta, 0/2 | ⚠️ | OpenAPI completa (#129); contrato quebra o CI se uma rota divergir do documentado (#114) | Critério 2 cumprido e não marcado; critério 1 é um processo contínuo |
| #73 RNF08 CI/CD | João Paulo | Fechada, 1/2 | ⚠️ | Lint, testes, cobertura e SAST no CI (#57, #85, #116) | Fechada com o critério do bloqueio de merge não cumprido (sem check obrigatório) |

## Divergências no board

Ajustes a fazer no GitHub para o board refletir a entrega:

**Fechar (entrega concluída, issue ainda aberta)**
- #126: PR #127 mergeado.
- #36 e #37: associações entregues pela turma. Atualizar o texto do critério antes de fechar.

**Marcar critérios cumpridos**
- Todos os critérios de #34, #61, #100, #101, #111, #113, #39, #42, #43, #44 e #46 (fechadas com evidência, sem critério marcado).
- #98 (critério 1), #106 (critério 2), #107 (critérios 1 e 2), #72 (critério 2).

**Reabrir ou corrigir (fechada sem a entrega completa)**
- #73 e #115: SAST roda, mas não bloqueia o merge. Reabrir ou desmarcar o critério até alguém com admin configurar o check obrigatório em `dev` e `main`.
- #105: comentar com a evidência de uma execução real do worker (log de sucesso e de falha) ou reabrir.
- #62: comentar a evidência da revisão do protótipo com o time ou desmarcar o critério.
