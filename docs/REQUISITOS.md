# Requisitos — Cerradinho

Objetivo, fontes de dados e mapa dos requisitos da API. O porquê do produto está no [Documento de Visão](DOCUMENTO-VISAO.md), o como no [ARQUITETURA.md](ARQUITETURA.md) e o quando no [planejamento de sprints](scrum/sprint-planning.md).

A especificação de cada requisito fica em um arquivo próprio na pasta [`/specs`](https://github.com/unb-mds/2026-2-Cerradinho-API/tree/dev/specs) da raiz do repositório. Cada requisito é nomeado no formato **verbo + objeto** e detalhado com **critérios de aceitação** (o que precisa ser verdade pra considerar o requisito pronto, testável), **regra de negócio** (restrições e decisões de domínio específicas daquele requisito) e **rastreabilidade** (issue, PRs, testes e ADRs).

## 1. Objetivo

API pública que consolida dados da UnB hoje espalhados em vários sistemas: disciplinas, professores, salas e prédios, cardápio do RU. Eventos e editais estavam previstos e saíram do escopo da Release 2. Todas as fontes usadas são públicas, sem login.

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

## 3. Requisitos

Os requisitos estão agrupados por domínio abaixo. O responsável e a issue de cada um ficam no [índice do `/specs`](https://github.com/unb-mds/2026-2-Cerradinho-API/blob/dev/specs/README.md), e o andamento é acompanhado pela issue no GitHub Projects.

### Disciplinas, professores e salas

- [RF01 · Capturar oferta de disciplinas de todas as unidades](https://github.com/unb-mds/2026-2-Cerradinho-API/blob/dev/specs/RF01-capturar-oferta-de-disciplinas-de-todas-as-unidades.md)
- [RF02 · Associar disciplina a professor](https://github.com/unb-mds/2026-2-Cerradinho-API/blob/dev/specs/RF02-associar-disciplina-a-professor.md)
- [RF03 · Associar disciplina a sala/prédio](https://github.com/unb-mds/2026-2-Cerradinho-API/blob/dev/specs/RF03-associar-disciplina-a-sala-predio.md)
- [RF04 · Cadastrar docentes vinculados às disciplinas](https://github.com/unb-mds/2026-2-Cerradinho-API/blob/dev/specs/RF04-cadastrar-docentes-vinculados-as-disciplinas.md)
- [RF05 · Derivar identificação de salas e prédios a partir das turmas](https://github.com/unb-mds/2026-2-Cerradinho-API/blob/dev/specs/RF05-derivar-identificacao-de-salas-e-predios-a-partir-das-turmas.md)

### Cardápio do RU

- [RF06 · Capturar cardápio diário do RU](https://github.com/unb-mds/2026-2-Cerradinho-API/blob/dev/specs/RF06-capturar-cardapio-diario-do-ru.md)
- [RF07 · Manter histórico de cardápios](https://github.com/unb-mds/2026-2-Cerradinho-API/blob/dev/specs/RF07-manter-historico-de-cardapios.md)

### Eventos e editais (fora do escopo da R2)

- [RF08 · Capturar eventos institucionais](https://github.com/unb-mds/2026-2-Cerradinho-API/blob/dev/specs/RF08-capturar-eventos-institucionais.md)
- [RF09 · Capturar editais publicados](https://github.com/unb-mds/2026-2-Cerradinho-API/blob/dev/specs/RF09-capturar-editais-publicados.md)

### API pública, SDK e portal

- [RF10 · Expor endpoints REST por domínio](https://github.com/unb-mds/2026-2-Cerradinho-API/blob/dev/specs/RF10-expor-endpoints-rest-por-dominio.md)
- [RF11 · Documentar a API via OpenAPI/Swagger](https://github.com/unb-mds/2026-2-Cerradinho-API/blob/dev/specs/RF11-documentar-a-api-via-openapi-swagger.md)
- [RF12 · Versionar a API desde o início](https://github.com/unb-mds/2026-2-Cerradinho-API/blob/dev/specs/RF12-versionar-a-api-desde-o-inicio.md)
- [RF13 · Disponibilizar SDK e CLI para integração de terceiros](https://github.com/unb-mds/2026-2-Cerradinho-API/blob/dev/specs/RF13-disponibilizar-sdk-e-cli-para-integracao-de-terceiros.md)
- [RF14 · Publicar portal do desenvolvedor](https://github.com/unb-mds/2026-2-Cerradinho-API/blob/dev/specs/RF14-publicar-portal-do-desenvolvedor.md)

### Atualização de dados

- [RF15 · Agendar execução automática do scraping](https://github.com/unb-mds/2026-2-Cerradinho-API/blob/dev/specs/RF15-agendar-execucao-automatica-do-scraping.md)
- [RF16 · Registrar log de sucesso/falha de cada execução](https://github.com/unb-mds/2026-2-Cerradinho-API/blob/dev/specs/RF16-registrar-log-de-sucesso-falha-de-cada-execucao.md)

### Features derivadas

- [RF17 · Calcular salas vazias por dia e horário](https://github.com/unb-mds/2026-2-Cerradinho-API/blob/dev/specs/RF17-calcular-salas-vazias-por-dia-e-horario.md)
- [RF18 · Listar agenda de turmas por professor](https://github.com/unb-mds/2026-2-Cerradinho-API/blob/dev/specs/RF18-listar-agenda-de-turmas-por-professor.md)
- [RF19 · Agrupar cardápio semanal](https://github.com/unb-mds/2026-2-Cerradinho-API/blob/dev/specs/RF19-agrupar-cardapio-semanal.md)

### Requisitos não funcionais

- [RNF01 · Limitar requisições por cliente/IP (rate limiting)](https://github.com/unb-mds/2026-2-Cerradinho-API/blob/dev/specs/RNF01-limitar-requisicoes-por-cliente-ip-rate-limiting.md)
- [RNF02 · Cachear respostas para reduzir tempo de resposta e carga no banco](https://github.com/unb-mds/2026-2-Cerradinho-API/blob/dev/specs/RNF02-cachear-respostas-para-reduzir-tempo-de-resposta-e-carga-no.md)
- [RNF03 · Monitorar disponibilidade das fontes e da API, com alertas](https://github.com/unb-mds/2026-2-Cerradinho-API/blob/dev/specs/RNF03-monitorar-disponibilidade-das-fontes-e-da-api-com-alertas.md)
- [RNF04 · Validar a API contra testes de contrato](https://github.com/unb-mds/2026-2-Cerradinho-API/blob/dev/specs/RNF04-validar-a-api-contra-testes-de-contrato.md)
- [RNF05 · Tratar falhas de scraping de forma resiliente](https://github.com/unb-mds/2026-2-Cerradinho-API/blob/dev/specs/RNF05-tratar-falhas-de-scraping-de-forma-resiliente.md)
- [RNF06 · Garantir disponibilidade do software implantado](https://github.com/unb-mds/2026-2-Cerradinho-API/blob/dev/specs/RNF06-garantir-disponibilidade-do-software-implantado.md)
- [RNF07 · Manter a documentação sincronizada com o estado real da API](https://github.com/unb-mds/2026-2-Cerradinho-API/blob/dev/specs/RNF07-manter-a-documentacao-sincronizada-com-o-estado-real-da-api.md)
- [RNF08 · Rodar pipeline de CI/CD](https://github.com/unb-mds/2026-2-Cerradinho-API/blob/dev/specs/RNF08-rodar-pipeline-de-ci-cd.md)
- [RNF09 · Garantir qualidade de testes](https://github.com/unb-mds/2026-2-Cerradinho-API/blob/dev/specs/RNF09-garantir-qualidade-de-testes.md)

As features derivadas (RF17 a RF19) são calculadas em cima do que RF01 a RF07 já capturam, sem fonte nem scraper próprio.
