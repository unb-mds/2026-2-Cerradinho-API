# Checklist board vs. entrega — Release 2

Conferência do que está no board do GitHub contra o que foi de fato entregue na `dev`, feita no fechamento da R2 ([#224](https://github.com/unb-mds/2026-2-Cerradinho-API/issues/224)). Segue o mesmo método do [checklist da R1](checklist-release-1.md).

- **Data da conferência:** 23/11/2026
- **Responsável:** João Paulo
- **Base conferida:** `dev` em `ffda2e7` (merge do #260), mais as correções da Sprint 11 da `R2-joao` (#225)

## Como foi conferido

Para cada issue da R2 (as de sprint S4 a S11 e as de requisito do escopo da R2), foram comparados:

1. o status no board (aberta ou fechada, e quantos critérios de aceitação estão marcados);
2. o que está mergeado na `dev`: código, testes e PRs ligados à issue;
3. a evidência de cada critério: PR mergeado, teste automatizado, run de CI ou documento no repositório.

Além do board, toda a suíte foi rodada de novo na base conferida, e a CLI foi testada de ponta a ponta contra a API rodando com Postgres.

Legenda da coluna **Entrega**: ✅ entregue com evidência · ⚠️ entregue em parte ou sem evidência registrada · ❌ não entregue · 🔄 em andamento (Sprint 11, que fecha em 25/11).

## Situação geral

| Item | Situação |
|---|---|
| CI na `dev` | ✅ Os 8 últimos runs passaram (lint, SAST, testes, contrato, integração com Postgres e o job do SDK) |
| SAST (bandit) | ✅ Nenhum achado em nenhuma severidade, nem baixa, no backend (`app/`) e no SDK (`cerradinho_sdk/`, sem o código gerado). O CI barra achado alto (`-lll`) |
| Testes | ✅ Backend: 260 testes, cobertura de 99% ([RNF09](../specs/RNF09-garantir-qualidade-de-testes.md)), contrato nas 8 rotas `/v1` com dados de exemplo e 5 testes de integração com Postgres. SDK: 43 testes |
| CLI de ponta a ponta | ✅ Os 11 comandos rodados contra a API local com Postgres e as migrations até a última: tabelas, `--json`, erro de professor inexistente (código 1) e o novo `--fim` de salas vazias |
| `main` | ⚠️ A `dev` está 134 commits à frente. A última release publicada é a v1.4 (20/11). A release final da R2 e o merge da `dev` na `main` são a #223 |
| Commits só na `main` | ✅ Nada se perde no próximo merge: a correção do parser do RU feita direto na `main` (`8cea82d`) já tem o equivalente na `dev`. Os outros dois são de documentação (requisitos em Markdown e link no README) |
| Workflow de mutação | ⚠️ O `mutacao.yml` só roda por `workflow_dispatch`, e o GitHub só mostra esse botão para workflows que estão na branch padrão. Como ele só existe na `dev`, nunca rodou no GitHub. Os números do RNF09 vêm de execuções locais. Resolve com o merge na `main` (#223) |
| Proteção de branch | ⚠️ Igual à R1: `dev` sem proteção; `main` protegida, mas sem check obrigatório e sem revisão mínima. O CI falha, mas não bloqueia o merge |
| Fechamento automático de issues | ⚠️ Igual à R1: o `Closes #` só fecha a issue em merge na `main`. Issues com PR mergeado na `dev` continuam abertas (ver "Divergências no board") |

## Issues de sprint

### Sprint 4

| Issue | Responsável | Board | Entrega | Evidência | Divergência |
|---|---|---|---|---|---|
| #151 Estudar o Swagger UI no portal | Daniel | Fechada, 2/2 | ✅ | Implementado no #148 | Sem documento de estudo em `docs/estudos/`: foi direto para a implementação |
| #152 Estudar cache e rate limit | Arthur | Fechada, 2/2 | ✅ | [ADR 0007](../adr/0007-cache-e-rate-limit-na-api.md) | — |
| #153 Estudar o deploy no Railway | Gabriel | Fechada, 2/2 | ✅ | [ADR 0009](../adr/0009-railway-para-deploy.md), depois substituído pelo [ADR 0011](../adr/0011-aws-lightsail-para-deploy.md) (AWS Lightsail) | — |
| #155 Arquitetura no modelo C4 | Vitor | Fechada, 2/2 | ✅ | [`ARQUITETURA.md`](../ARQUITETURA.md) | — |
| #156 Reestruturar os requisitos | Vitor | Fechada, 2/2 | ✅ | #137 | — |
| #157 Retrospectivas das Sprints 0 a 4 | Vitor | Fechada, 2/2 | ✅ | [`retrospectivas.md`](retrospectivas.md) | — |
| #158 Site de documentação no GitHub Pages | Vitor | Fechada, 3/3 | ✅ | #135, `docs.yml` | — |
| #159, #164 Release note da R1 | Gabriel, Daniel | Fechadas, 2/2 | ✅ | Release "Release 1" publicada em 06/10 (#138) | — |
| #160 Revisar agendamento e log (RF15, RF16) | Arthur | Fechada, 2/2 | ✅ | #141 | — |
| #161 Especificação em `/specs` | Gabriel | Fechada, 3/3 | ✅ | #139 | — |
| #162 Licença, código de conduta e changelog | Gabriel | Fechada, 4/4 | ✅ | #139 | — |
| #163 Padrão de branches `R2-nome` | Gabriel | Fechada, 2/2 | ✅ | #139 | — |
| #165 Checklist da R1 | João Paulo | Fechada, 1/2 | ✅ | #132 | Critério não marcado |
| #166 Levar a `dev` para a `main` | João Paulo | Fechada, 1/1 | ✅ | #138 | — |
| #167 Limpar as branches antigas | João Paulo | Fechada, 2/2 | ✅ | O remoto só tem `main`, `dev` e branches `R2-*` | — |
| #154 Estudar mutação e UptimeRobot | João Paulo | Fechada, 0/2 | ✅ | #239 ([mutação](../estudos/estudo-teste-de-mutacao.md), [UptimeRobot](../estudos/estudo-uptimerobot.md)) | Critérios não marcados; saiu da S4 e foi feita na S7 |

### Sprint 5

| Issue | Responsável | Board | Entrega | Evidência | Divergência |
|---|---|---|---|---|---|
| #168 Busca de docente normalizada (RF04) | Vitor | Fechada, 3/3 | ✅ | #140 | — |
| #169 Remover professores e salas duplicados | Vitor | Fechada, 3/3 | ✅ | #140 | — |
| #170 Protótipos das telas novas | Daniel | Fechada, 5/5 | ✅ | #144 | — |
| #171 Wireframe do portal (RF14) | Daniel | Fechada, 4/4 | ✅ | #144 | — |
| #172 Desenho do cache (RNF02) | Arthur | Fechada, 2/2 | ✅ | #143 | — |
| #173 Log de execução consultável (RF16) | Arthur | Fechada, 4/4 | ✅ | #141, #143 (`GET /v1/execucoes`) | — |
| #174 Parser do RU com os PDFs novos | Gabriel | Fechada, 3/4 | ✅ | #145 | 1 critério não marcado |
| #177 PDFs do RU como fixtures | João Paulo | Fechada, 3/3 | ✅ | #145 | Os PDFs entraram no PR do Gabriel |
| #176 Medir a cobertura e os módulos críticos | João Paulo | Fechada, 3/4 | ✅ | #147 | Duplicada da #146 |
| #146 Medir a cobertura e os módulos críticos | João Paulo | Fechada, 0/4 | ✅ | #147 | Duplicada da #176; critérios não marcados |

### Sprint 6

| Issue | Responsável | Board | Entrega | Evidência | Divergência |
|---|---|---|---|---|---|
| #178 Salas vazias (RF17) | Vitor | Fechada, 4/4 | ✅ | #149 | — |
| #179 Ajustes de UX do cardápio | Daniel | Fechada, 2/2 | ✅ | #148 | — |
| #180 Swagger UI no portal (RF14) | Daniel | Fechada, 2/2 | ✅ | #148 | — |
| #181 Cache Redis nas rotas (RNF02) | Arthur | Fechada, 0/4 | ✅ | #150 | Critérios não marcados |
| #184 Contrato de salas vazias e cardápio semanal | João Paulo | Fechada, 0/3 | ✅ | #231 | Critérios não marcados |
| #185 Teste do log de execução (RF16) | João Paulo | Fechada, 0/3 | ✅ | #231 | Critérios não marcados |

### Sprint 7

| Issue | Responsável | Board | Entrega | Evidência | Divergência |
|---|---|---|---|---|---|
| #182 Cardápio semanal (RF19) | Gabriel | Fechada, 1/4 | ✅ | #227 | 3 critérios não marcados |
| #183 Deploy de teste na AWS Lightsail | Gabriel | Fechada, 3/3 | ✅ | #240, #242 | — |
| #175 Variáveis de produção na AWS Lightsail | Gabriel | Fechada, 2/2 | ✅ | #242 | — |
| #186 Agenda do professor (RF18) | Vitor | Fechada, 0/4 | ✅ | #237 | Critérios não marcados |
| #187 Telas de salas vazias e da agenda | Daniel | Fechada, 4/4 | ✅ | #228, #238 | — |
| #188 Rate limit com slowapi (RNF01) | Arthur | Fechada, 3/3 | ✅ | #229 | — |
| #189 Versão candidata, com o frontend | Gabriel | Fechada, 0/3 | ✅ | #240, #242 | Critérios não marcados |
| #190 Contrato da agenda | João Paulo | Fechada, 0/2 | ✅ | #239 | Critérios não marcados |
| #191 Observabilidade com UptimeRobot (RNF03) | João Paulo | Fechada, 0/3 | ✅ | #239 (`/health`), #245 (monitores) | Critérios não marcados |

### Sprint 8

| Issue | Responsável | Board | Entrega | Evidência | Divergência |
|---|---|---|---|---|---|
| #192 SDK Python (RF13) | Vitor | Fechada, 0/4 | ✅ | #241 | Critérios não marcados |
| #193 Portal do desenvolvedor (RF14) | Daniel | Fechada, 3/3 | ✅ | #244 | — |
| #194 Tela do cardápio semanal | Daniel | Fechada, 2/2 | ✅ | #148, #244 | — |
| #195 Cache e rate limit finalizados | Arthur | Fechada, 0/3 | ✅ | #243 | Critérios não marcados |
| #196 Teste simples de carga | Arthur | Fechada, 0/2 | ✅ | #243 | Critérios não marcados |
| #197 Deploy definitivo (RNF06) | Gabriel | Fechada, 0/3 | ✅ | #240, #242 | Critérios não marcados |
| #198 CLI com Typer (RF13) | João Paulo | Fechada, 0/3 | ✅ | #245 | Critérios não marcados |

### Sprint 9

| Issue | Responsável | Board | Entrega | Evidência | Divergência |
|---|---|---|---|---|---|
| #199 SDK fechado e documentado | Vitor | Aberta, 0/2 | ✅ | #241, #250; README do SDK com exemplos | PR mergeado, issue aberta |
| #200 Frontend em produção | Daniel | Fechada, 0/2 | ✅ | #242 | Critérios não marcados. Acesso em produção é conferido na #220 |
| #201 Portal finalizado | Daniel | Fechada, 0/2 | ✅ | #247 | Critérios não marcados |
| #202 Worker e agendamento estáveis em produção (RF15) | Arthur | Fechada, 0/2 | ✅ | #249: a spec do RF15 registra o `GET /v1/execucoes` de produção em 16/11, com as execuções de domingo (08/11 e 15/11) com sucesso | Critérios não marcados |
| #203 Ajustes pós-deploy | Gabriel | Fechada, 0/2 | ✅ | #252, #258 | Critérios não marcados |
| #204 Rastreabilidade das specs | Gabriel | Fechada, 0/2 | ✅ | #252 | Critérios não marcados |
| #205 CLI fechada | João Paulo | Fechada, 0/2 | ✅ | #245 | Critérios não marcados |
| #206 Mutação e sabotagem (RNF09) | João Paulo | Fechada, 1/2 | ✅ | #248 | 1 critério não marcado |

### Sprint 10

| Issue | Responsável | Board | Entrega | Evidência | Divergência |
|---|---|---|---|---|---|
| #207 Ajustes finais de salas vazias e agenda | Vitor | Aberta, 0/2 | ✅ | #250, #256 | PRs mergeados, issue aberta |
| #208 Exemplos de uso do SDK | Vitor | Aberta, 0/2 | ✅ | #250 | PR mergeado, issue aberta |
| #209 GitPage com visão de produto | Daniel | Fechada, 2/2 | ✅ | #260 | — |
| #210 Telas finais | Daniel | Fechada, 2/2 | ✅ | #257, #260 | — |
| #211 Ajustes finais de cache, rate limit e log | Arthur | Aberta, 0/2 | ⚠️ | #255 (log informa as unidades que falharam) | Nenhum PR ligado à issue. Conferir com o Arthur o que falta |
| #212 Ajustes finais do cardápio semanal | Gabriel | Fechada, 0/2 | ✅ | #252 | Critérios não marcados |
| #213 Produção estável | Gabriel | Fechada, 0/2 | ✅ | #258 | Critérios não marcados |
| #214 Cobertura, mutação e sabotagem (RNF09) | João Paulo | Aberta, 0/3 | ✅ | #248; cobertura de 99% medida nesta conferência | PR mergeado, issue aberta |
| #215 Contratos completos (RNF04) | João Paulo | Aberta, 0/2 | ✅ | #231, #239; as 8 rotas `/v1` respondem com dados de exemplo no contrato | Entregue, issue aberta |

### Sprint 11

| Issue | Responsável | Board | Entrega | Evidência | Divergência |
|---|---|---|---|---|---|
| #216 Correções finais: disciplinas, features e SDK | Vitor | Aberta, 0/2 | 🔄 | #254, #256 | — |
| #217 Retrospectiva final e métricas da R2 | Vitor | Aberta, 0/2 | 🔄 | — | — |
| #218 Correções finais: frontend e portal | Daniel | Fechada, 2/2 | ✅ | #257 | — |
| #219 Slides da apresentação final | Daniel | Aberta, 0/2 | 🔄 | — | — |
| #220 API e frontend acessíveis em produção | Arthur | Aberta, 0/2 | 🔄 | — | — |
| #221 Correções finais: agendamento, cache e rate limit | Arthur | Aberta, 0/2 | 🔄 | — | — |
| #222 Correções finais: cardápio do RU e deploy | Gabriel | Fechada, 0/2 | ✅ | #258 | Critérios não marcados |
| #223 Release note da R2, merge na `main` e tag | Gabriel | Aberta, 0/3 | 🔄 | Release note da v1.4 (#259) | Falta a release final da R2 e o merge da `dev` na `main` |
| #224 Checklist final do board | João Paulo | Aberta, 0/3 | 🔄 | Este documento | CI verde no commit da entrega só pode ser conferido depois da #223 |
| #225 Correções finais: qualidade, observabilidade e CLI | João Paulo | Aberta, 0/2 | 🔄 | SDK regenerado e `--fim` em `salas-vazias` (ver "Correções da Sprint 11") | — |

## Requisitos do escopo da R2

| Issue | Responsável | Board | Entrega | Evidência | Divergência |
|---|---|---|---|---|---|
| #49 RF13 SDK e CLI | Vitor (SDK), João Paulo (CLI) | Aberta, 0/2 | ✅ | #241, #245, #250 | Ainda atribuída ao Ítalo, que saiu. Reatribuir e fechar |
| #52 RF14 Portal do desenvolvedor | Daniel | Fechada, 0/1 | ✅ | #148, #244, #247 | Critério não marcado |
| #53 RF17 Salas vazias | Vitor | Fechada, 0/1 | ✅ | #149, #250, #256 | Critério não marcado |
| #50 RF18 Agenda do professor | Vitor | Fechada, 0/1 | ✅ | #237, #238 | Critério não marcado |
| #51 RF19 Cardápio semanal | Gabriel | Fechada, 0/1 | ✅ | #227, #252 | Critério não marcado; ainda atribuída ao Ítalo |
| #47 RF08 Eventos, #48 RF09 Editais | — | Fechadas, 0/1 | — | Fora do escopo com a saída do Ítalo ([planejamento](sprint-planning.md)) | — |
| #45 RF15 Agendamento automático | Arthur | Fechada, 0/1 | ✅ | #121, #127, #249, #255 | Critério não marcado |
| #46 RF16 Log de execução | Arthur | Fechada, 0/1 | ✅ | #141, #143, #231, #255 | Critério não marcado |
| #66 RNF01 Rate limit | Arthur | Fechada, 0/2 | ✅ | #229, #243 | Critérios não marcados |
| #67 RNF02 Cache | Arthur | Aberta, 0/2 | ✅ | #150, #243 | PRs mergeados, issue aberta |
| #68 RNF03 Observabilidade | João Paulo | Fechada, 0/2 | ✅ | #239, #245 | Critérios não marcados |
| #70 RNF05 Resiliência | João Paulo | Aberta, 0/2 | ✅ | Unidade do SIGAA com erro não derruba as outras (commit por unidade em `tasks/scraping.py`); o log diz quais unidades falharam (#255), o que resolve a pendência 8 da R1; sabotagem dos scrapers (#248) | Pode ser fechada |
| #71 RNF06 Disponibilidade | Gabriel | Fechada, 0/2 | ✅ | #240, #242 ([ADR 0011](../adr/0011-aws-lightsail-para-deploy.md)) | Critérios não marcados |
| #72 RNF07 Doc viva | João Paulo | Aberta, 0/2 | ✅ | OpenAPI completa; contrato nas 8 rotas quebra o CI se a resposta divergir do documentado; SDK regenerado a partir do OpenAPI atual (#225) | Critério 1 é um processo contínuo. Fechar com o aval do PO (pendência 12 da R1) |
| #73 RNF08 CI/CD | João Paulo | Fechada, 1/2 | ⚠️ | Lint, SAST, testes, contrato e integração no backend; lint, SAST e testes no SDK | O CI ainda não bloqueia o merge (sem check obrigatório), como na R1 |
| #74 RNF09 Qualidade de testes | João Paulo | Fechada, 0/3 | ✅ | #147, #248 | Critérios não marcados |

## Correções da Sprint 11 (#225)

O que a varredura de qualidade, observabilidade e CLI encontrou na base conferida:

| Problema | Situação |
|---|---|
| O SDK estava fora de sincronia com a API. O `fim` de `/v1/salas/vazias` (#256) não existia no SDK nem na CLI, e o `limite` de disciplinas e professores ainda aceitava `null`, que a API deixou de aceitar no `a18250e` | ✅ Cliente regenerado a partir do OpenAPI atual com o `openapi-python-client` 0.29; `fim` exposto em `CerradinhoClient.listar_salas_vazias` e na CLI (`cerradinho salas-vazias segunda 14:00 --fim 15:50`), com testes |
| Bandit, ruff e testes do backend e do SDK | ✅ Sem achado e sem falha |
| CLI contra a API real | ✅ Os 11 comandos rodados de ponta a ponta |

## Divergências no board

Ajustes a fazer no GitHub para o board refletir a entrega:

**Fechar (entrega concluída, issue ainda aberta)**
- #199, #207, #208: PRs mergeados.
- #214 e #215: metas do RNF09 atingidas e contrato completo.
- #67: cache entregue.
- #49 e #51: reatribuir (ainda estão com o Ítalo) e fechar.
- #70: resiliência entregue. #72 depois do aval do PO.

**Marcar critérios cumpridos**
- Todas as issues fechadas da tabela com "Critérios não marcados", principalmente as de requisito (#45, #46, #50, #52, #53, #66, #68, #71, #74), que vão para a avaliação.

**Conferir com o responsável**
- #211: listar o que ainda falta ou fechar com o #255.

**Limpar**
- #146 e #176 são a mesma tarefa; manter uma só.

## Pendências para a entrega (25/11)

| # | Pendência | Responsável | Issue | Impacto |
|---|---|---|---|---|
| 1 | Release final da R2, merge da `dev` na `main` e tag | Gabriel | [#223](https://github.com/unb-mds/2026-2-Cerradinho-API/issues/223) | A `main` está 134 commits atrás da `dev` |
| 2 | Conferir o CI verde no commit da entrega, na `main` | João Paulo | [#224](https://github.com/unb-mds/2026-2-Cerradinho-API/issues/224) | Depende do item 1 |
| 3 | Rodar o workflow de mutação no GitHub depois que ele chegar à `main` | João Paulo | [#225](https://github.com/unb-mds/2026-2-Cerradinho-API/issues/225) | Hoje os números de mutação são só de execução local |
| 4 | Check obrigatório do CI em `dev` e `main` | Gabriel (admin do repositório) | [#73](https://github.com/unb-mds/2026-2-Cerradinho-API/issues/73) | Pendência desde a R1: um PR com CI vermelho ainda pode ser mergeado |
| 5 | Conferir que a API e o frontend estão acessíveis em produção | Arthur | [#220](https://github.com/unb-mds/2026-2-Cerradinho-API/issues/220) | — |
| 6 | Aval do PO para fechar o RNF07 | João Paulo, com o PO | [#72](https://github.com/unb-mds/2026-2-Cerradinho-API/issues/72) | — |

### Pendências da R1

Situação, na base conferida, das pendências levantadas no checklist da R1:

| Pendência da R1 | Situação |
|---|---|
| 1. Parser do RU com os PDFs novos | ✅ #145, #252, #258 |
| 2. Itens do café que valem para a semana inteira | — Não conferido nesta release |
| 3. Busca de docente por nome normalizado | ✅ #140 |
| 4. Professores e salas duplicados | ✅ #140 |
| 5. Log de execução consultável | ✅ #141, #143 |
| 6. Execução real do worker agendado | ✅ Verificada em produção em 16/11 ([spec do RF15](../specs/RF15-agendar-execucao-automatica-do-scraping.md), #249) |
| 7. Comentário do horário diferente do `crontab` | ✅ O comentário em `celery_app.py` diz "domingo às 3h", igual ao `crontab(hour=3)` |
| 8. Log de falha sem contexto de fonte ou unidade | ✅ #141 (falha da fonte vs. interna), #255 (unidades) |
| 9. Check obrigatório do CI | ❌ Pendente (item 4 acima) |
| 10. Release note da R1 e `dev` na `main` | ✅ #138 |
| 11. Critérios de RF02 e RF03 | ✅ Issues fechadas |
| 12. Aval do PO para o RNF07 | ❌ Pendente (item 6 acima) |
| 13. Evidência da revisão do protótipo | — Não conferido nesta release |
