# Especificação · Cerradinho

Especificação viva do Cerradinho, com um arquivo por requisito. Cada arquivo traz os critérios de aceitação, a regra de negócio e a rastreabilidade do requisito (issue, PRs, testes e ADRs).

O objetivo do produto, as fontes de dados e o contexto estão no [`docs/REQUISITOS.md`](https://github.com/unb-mds/2026-2-Cerradinho-API/blob/dev/docs/REQUISITOS.md).

## Como manter

- Mudou o requisito, muda a spec no mesmo PR. Critério novo, critério removido ou regra de negócio diferente entram aqui antes ou junto do código.
- PR que implementa ou testa um requisito acrescenta o próprio número e os arquivos de teste na seção Rastreabilidade da spec.
- O andamento de cada requisito (a fazer, em andamento ou concluído) é acompanhado pela issue dele no GitHub Projects, não aqui.
- O Ítalo era o responsável por RF06 a RF09, pela CLI do RF13 e pelo RF19, e saiu do projeto no início da Release 2. Eventos (RF08) e editais (RF09) saíram do escopo, e os outros requisitos têm novos responsáveis nas tabelas abaixo.
- Requisito novo ganha arquivo novo (`RFNN-verbo-objeto.md`), issue própria e linha nesta tabela.

## Requisitos funcionais

| Requisito | Release | Responsável | Issue |
|---|---|---|---|
| [RF01 · Capturar oferta de disciplinas de todas as unidades](RF01-capturar-oferta-de-disciplinas-de-todas-as-unidades.md) | R1 | Vitor | [#35](https://github.com/unb-mds/2026-2-Cerradinho-API/issues/35) |
| [RF02 · Associar disciplina a professor](RF02-associar-disciplina-a-professor.md) | R1 | Vitor | [#36](https://github.com/unb-mds/2026-2-Cerradinho-API/issues/36) |
| [RF03 · Associar disciplina a sala/prédio](RF03-associar-disciplina-a-sala-predio.md) | R1 | Vitor | [#37](https://github.com/unb-mds/2026-2-Cerradinho-API/issues/37) |
| [RF04 · Cadastrar docentes vinculados às disciplinas](RF04-cadastrar-docentes-vinculados-as-disciplinas.md) | R1 | Vitor | [#38](https://github.com/unb-mds/2026-2-Cerradinho-API/issues/38) |
| [RF05 · Derivar identificação de salas e prédios a partir das turmas](RF05-derivar-identificacao-de-salas-e-predios-a-partir-das-turmas.md) | R1 | Vitor | [#39](https://github.com/unb-mds/2026-2-Cerradinho-API/issues/39) |
| [RF06 · Capturar cardápio diário do RU](RF06-capturar-cardapio-diario-do-ru.md) | R1 | Gabriel | [#40](https://github.com/unb-mds/2026-2-Cerradinho-API/issues/40) |
| [RF07 · Manter histórico de cardápios](RF07-manter-historico-de-cardapios.md) | R1 | Gabriel | [#41](https://github.com/unb-mds/2026-2-Cerradinho-API/issues/41) |
| [RF08 · Capturar eventos institucionais](RF08-capturar-eventos-institucionais.md) | R2 | Ninguém | [#47](https://github.com/unb-mds/2026-2-Cerradinho-API/issues/47) |
| [RF09 · Capturar editais publicados](RF09-capturar-editais-publicados.md) | R2 | Ninguém | [#48](https://github.com/unb-mds/2026-2-Cerradinho-API/issues/48) |
| [RF10 · Expor endpoints REST por domínio](RF10-expor-endpoints-rest-por-dominio.md) | R1 | Daniel | [#42](https://github.com/unb-mds/2026-2-Cerradinho-API/issues/42) |
| [RF11 · Documentar a API via OpenAPI/Swagger](RF11-documentar-a-api-via-openapi-swagger.md) | R1 | Daniel | [#43](https://github.com/unb-mds/2026-2-Cerradinho-API/issues/43) |
| [RF12 · Versionar a API desde o início](RF12-versionar-a-api-desde-o-inicio.md) | R1 | Gabriel | [#44](https://github.com/unb-mds/2026-2-Cerradinho-API/issues/44) |
| [RF13 · Disponibilizar SDK e CLI para integração de terceiros](RF13-disponibilizar-sdk-e-cli-para-integracao-de-terceiros.md) | R2 | Vitor (SDK), João Paulo (CLI) | [#49](https://github.com/unb-mds/2026-2-Cerradinho-API/issues/49) |
| [RF14 · Publicar portal do desenvolvedor](RF14-publicar-portal-do-desenvolvedor.md) | R2 | Daniel | [#52](https://github.com/unb-mds/2026-2-Cerradinho-API/issues/52) |
| [RF15 · Agendar execução automática do scraping](RF15-agendar-execucao-automatica-do-scraping.md) | R1 | Arthur | [#45](https://github.com/unb-mds/2026-2-Cerradinho-API/issues/45) |
| [RF16 · Registrar log de sucesso/falha de cada execução](RF16-registrar-log-de-sucesso-falha-de-cada-execucao.md) | R1 | Arthur | [#46](https://github.com/unb-mds/2026-2-Cerradinho-API/issues/46) |
| [RF17 · Calcular salas vazias por dia e horário](RF17-calcular-salas-vazias-por-dia-e-horario.md) | R2 | Vitor | [#53](https://github.com/unb-mds/2026-2-Cerradinho-API/issues/53) |
| [RF18 · Listar agenda de turmas por professor](RF18-listar-agenda-de-turmas-por-professor.md) | R2 | Vitor | [#50](https://github.com/unb-mds/2026-2-Cerradinho-API/issues/50) |
| [RF19 · Agrupar cardápio semanal](RF19-agrupar-cardapio-semanal.md) | R2 | Gabriel | [#51](https://github.com/unb-mds/2026-2-Cerradinho-API/issues/51) |

As features derivadas (RF17 a RF19) são calculadas em cima do que RF01 a RF07 já capturam, sem fonte nem scraper próprio.

## Requisitos não funcionais

| Requisito | Release | Responsável | Issue |
|---|---|---|---|
| [RNF01 · Limitar requisições por cliente/IP (rate limiting)](RNF01-limitar-requisicoes-por-cliente-ip-rate-limiting.md) | R2 | Arthur | [#66](https://github.com/unb-mds/2026-2-Cerradinho-API/issues/66) |
| [RNF02 · Cachear respostas para reduzir tempo de resposta e carga no banco](RNF02-cachear-respostas-para-reduzir-tempo-de-resposta-e-carga-no.md) | R2 | Arthur | [#67](https://github.com/unb-mds/2026-2-Cerradinho-API/issues/67) |
| [RNF03 · Monitorar disponibilidade das fontes e da API, com alertas](RNF03-monitorar-disponibilidade-das-fontes-e-da-api-com-alertas.md) | R2 | João Paulo | [#68](https://github.com/unb-mds/2026-2-Cerradinho-API/issues/68) |
| [RNF04 · Validar a API contra testes de contrato](RNF04-validar-a-api-contra-testes-de-contrato.md) | R1 | João Paulo | [#69](https://github.com/unb-mds/2026-2-Cerradinho-API/issues/69) |
| [RNF05 · Tratar falhas de scraping de forma resiliente](RNF05-tratar-falhas-de-scraping-de-forma-resiliente.md) | R1 | João Paulo | [#70](https://github.com/unb-mds/2026-2-Cerradinho-API/issues/70) |
| [RNF06 · Garantir disponibilidade do software implantado](RNF06-garantir-disponibilidade-do-software-implantado.md) | R2 | Gabriel | [#71](https://github.com/unb-mds/2026-2-Cerradinho-API/issues/71) |
| [RNF07 · Manter a documentação sincronizada com o estado real da API](RNF07-manter-a-documentacao-sincronizada-com-o-estado-real-da-api.md) | R1 | João Paulo | [#72](https://github.com/unb-mds/2026-2-Cerradinho-API/issues/72) |
| [RNF08 · Rodar pipeline de CI/CD](RNF08-rodar-pipeline-de-ci-cd.md) | R1 | João Paulo | [#73](https://github.com/unb-mds/2026-2-Cerradinho-API/issues/73) |
| [RNF09 · Garantir qualidade de testes](RNF09-garantir-qualidade-de-testes.md) | R2 | João Paulo | [#74](https://github.com/unb-mds/2026-2-Cerradinho-API/issues/74) |
