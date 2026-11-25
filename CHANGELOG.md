# Changelog

Mudanças relevantes do Cerradinho, por release. O formato segue o [Keep a Changelog](https://keepachangelog.com/pt-BR/1.1.0/). A descrição completa de cada release fica na [aba Releases do GitHub](https://github.com/unb-mds/2026-2-Cerradinho-API/releases).

## [2.0] - 2026-11-25

Entrega da Release 2, com as Sprints 10 e 11 (19/11 a 25/11/2026). O resumo da release inteira fica em `docs/releases/v2.0.md`.

### Adicionado

- `fim` opcional em `GET /v1/salas/vazias`, para pedir as salas livres num intervalo inteiro (RF17, #256).
- Home "Agora no Gama" no site, com as salas livres no bloco de agora, o RU de hoje e a busca de disciplinas (#257).
- Chamada `GET /v1/...` de cada tela visível no site, com Copiar, Ver JSON e Docs (#257).
- Unidades do SIGAA que falharam aparecem na mensagem de `GET /v1/execucoes` (RF16, #255).
- SDK ganha o `fim` de `GET /v1/salas/vazias`, que tinha ficado de fora quando a rota ganhou o parâmetro no #256 (RF13, #262).
- `id` do professor em cada turma de `GET /v1/disciplinas`, o mesmo de `GET /v1/professores` — pedido do Daniel, que cruzava turma e professor pelo nome no front, sem dar pra linkar direto pra agenda (RF01).
- Respostas da API comprimidas com gzip para quem manda `Accept-Encoding: gzip`. `GET /v1/disciplinas` sem limite cai de cerca de 2,4 MB para 240 KB (RNF02, #260).
- Aviso no cardápio e na home de que o RU do Gama não abre no fim de semana (#260).
- Página de telas e navegação, release notes e tema do Cerradinho no site de documentação (#260).
- Nome da disciplina ao lado do código na lista de Professores e na agenda do professor, que antes mostravam só o código.

### Alterado

- Salas Vazias mostra a semana inteira em blocos de 2h, das 8h às 17h50, só com as salas I1 a I10 e S1 a S10 da FCTE (RF17, #256).
- O site mostra só o campus Gama. A API continua servindo a UnB inteira (#257).
- README, CONTRIBUTING e templates de PR e issue voltados para quem contribui de fora, com um template novo para dado errado. O material de processo foi para a seção Histórico do site de documentação.

### Corrigido

- `GET /v1/disciplinas?limite=10` levando cerca de 9,5s, porque montava todas as turmas para devolver uma página. Agora pagina no banco e responde em cerca de 20ms (RF01, #256).
- Turma em sala combinada (`I9/I10`) não ocupava as salas individuais em `GET /v1/salas/vazias` (RF17, #256).
- Professores do Gama que dão disciplina de instituto, como Física 1 e Cálculo, não apareciam no site (#260).
- Deploy do site de documentação falhando desde 18/11 por links relativos nas specs RNF03 e RNF09 (#260).
- Erro de hidratação em Cardápio e Salas Vazias, que calculavam "hoje" com a data do build (#261).
- Filtro de horário de Disciplinas olhava só o primeiro horário da turma (#261).
- Portal do desenvolvedor sem o parâmetro `fim` de `GET /v1/salas/vazias` (RF14, #261).
- Produção sem cardápio de 16 a 19/11, porque o servidor não tinha a correção do #252. Corrigido com o deploy de 20/11 e o hotfix na `main` (#258).
- `sdk/scripts/gerar_cliente.sh` podia regerar o cliente importando `httpx2` em vez de `httpx` (o `sdk/pyproject.toml` só declara `httpx`), se o ambiente que roda o gerador tivesse o pacote `httpx2` instalado por qualquer outra dependência. O script agora falha alto em vez de deixar passar (RF13, #262).

## [1.4] - 2026-11-18

Sprints 8 a 10 da Release 2 (09/11 a 18/11/2026).

### Adicionado

- Portal do desenvolvedor em `/desenvolvedores`, com URL base, tabela de endpoints, exemplos em curl, Python e JavaScript, Swagger UI embutido e cartões do SDK e da CLI (RF14, #244, #247).
- CLI `cerradinho`, instalada junto com o SDK, com um comando por método do `CerradinhoClient` e saída em tabela ou JSON (RF13, #245).
- Um exemplo por método do `CerradinhoClient` no README do SDK e no portal (RF13, #250).
- Monitores do UptimeRobot criados por `backend/scripts/uptimerobot.py`, separando falha da API (`[API]`) de falha da fonte (`[FONTE]`) (RNF03, #245).
- Layout para celular no frontend, com barra de navegação embaixo e tabelas em cards, e listas com "Mostrar mais" de 50 em 50 (#244).
- Teste de mutação com cosmic-ray e teste de sabotagem com 13 cenários nos 8 módulos críticos, com cobertura de linhas em 98% (RNF09, #248).
- Teste de carga do cache e do rate limit em `backend/scripts/teste_carga.py` (RNF01, RNF02, #243).
- `SECURITY.md`, seção para quem não é do time no `CONTRIBUTING.md` e README com exemplo de uso, fontes de dado e aviso de serviço não oficial (#253).

### Corrigido

- Coleta do cardápio do RU falhando desde 16/11, porque o PDF passou a trazer a data entre parênteses. O parser agora acha a data mesmo colada em outro texto (RF06, #252).
- Três falhas silenciosas do scraper do SIGAA achadas pela sabotagem. Timeout do Playwright aparecia como falha interna, e sessão expirada ou layout novo viravam "sucesso" com 0 turmas (RNF05, #248).
- Agenda do professor (RF18) ilegível quando várias turmas caem no mesmo horário (ex. 12 turmas simultâneas de Música numa sexta). Turmas com o mesmo início e fim viram um bloco "N turmas", que abre a lista abaixo da grade (#251).
- `GET /v1/professores` mostrando `"A DEFINIR DOCENTE"` (placeholder do SIGAA pra turma sem docente, com mais de 150 disciplinas nesse registro só) como se fosse um professor real (RF04, RF18, #250). `GET /v1/resumo` também deixa de contar esse registro.
- CORS sem expor o `X-Total-Count` (RF10, #250). O cabeçalho chegava na resposta, mas o JS do navegador não conseguia ler.
- Timeout do dashboard subiu de 5s para 15s, que estourava com a listagem completa de turmas (#244).

## [1.3] - 2026-11-09

Sprint 7 e início da Sprint 8 da Release 2 (28/10 a 08/11/2026).

### Adicionado

- `docker-compose.prod.yml`, `Caddyfile` e `frontend/Dockerfile` para rodar a produção numa máquina só, com HTTPS automático e só as portas 80 e 443 expostas (RNF06).
- Agenda semanal do professor em `GET /v1/professores/{id}/agenda`, com o horário decomposto em dia/início/fim e a sala de cada bloco (RF18, #50).
- `GET /v1/resumo`, com as contagens de turmas, disciplinas, professores e salas, sem a lista inteira de cada domínio (RF20).
- Paginação (`limite`/`offset`, com `X-Total-Count`) em `GET /v1/disciplinas` e `GET /v1/professores`, e busca/filtro (`busca`, `departamento`) em `GET /v1/disciplinas` (RF01, RF04, RF10). Sem parâmetro, continua devolvendo tudo como antes.
- Estrutura inicial do SDK Python (`sdk/`), cliente HTTP gerado a partir do OpenAPI do backend, com uma interface ergonômica por cima (RF13).

### Corrigido

- Grade noturna de horário (RF17/RF18) com os horários errados e faltando a N4; agora confirmada contra turma real (aulas de 50 min, não 55, com 5 min de intervalo entre T6 e N1).
- Sala do Darcy com o código de horário embutido no próprio campo de sala (ex. `"2N12(ICC ANF.15) 4N12(ICC ANF.16)"`), que antes virava uma sala só sem separar os prédios/salas; e prédio cortado errado quando o separador caía dentro do código da sala (`"BSA S B1 34 - 10"`, `"ICC AT 114 - 092"`) em vez de entre prédio e sala (RF05).

### Alterado

- A hospedagem passa do Railway para a AWS Lightsail, porque o período de teste do Railway acaba antes da entrega da R2 ([ADR 0011](docs/adr/0011-aws-lightsail-para-deploy.md)). O `docs/DEPLOY.md` foi reescrito para a AWS.

## [1.2] - 2026-10-28

Sprint 6 e início da Sprint 7 da Release 2 (18/10 a 28/10/2026).

### Adicionado

- Salas vazias por dia e horário em `GET /v1/salas/vazias` (RF17, #149) e a página de salas vazias no frontend (#228).
- Cardápio da semana agrupado por dia e refeição em `GET /v1/cardapio/semana`, sempre com os 7 dias e os dias sem cardápio marcados como não publicados (RF19, #51).
- Cache em Redis nas rotas de leitura, limpo a cada nova coleta (RNF02, #150).
- Rate limit de 60 requisições por minuto por IP com slowapi (RNF01, #229).
- Página de desenvolvedores no frontend com a documentação interativa da API (RF14, #148).
- Navegação por semana e filtro por dia na página de cardápio (#148).
- ADR 0010, que move a sala da turma para o horário.

### Alterado

- `GET /v1/cardapio/semana` passa a devolver `data_inicio`, `data_fim` e a lista `dias`, no lugar de uma lista solta de itens (RF19).

### Corrigido

- Coleta do cardápio do RU, que falhava quando a página consultada ficava parada numa semana antiga. O scraper agora consulta as duas páginas onde o RU publica o PDF (#226).
- Prédio do Darcy escrito sem separador (`"PAT AT 125"`) e andar (`"TÉRREO"`) gravado como se fosse prédio (RF05).
- `criado_em` de `GET /v1/execucoes` sem fuso horário (RF16).
- Página de cardápio mostrando dado da semana anterior (#148).
- Gravação de turmas do Darcy, que falhava com `StringDataRightTruncation` em código de horário com vários segmentos (`"6M123 7M12345 7T1234 4N12"`); coluna alargada pra 100 caracteres (RF01).
- `GET /v1/salas/vazias` não contava código de horário com mais de um segmento (`"35M5 35T1"`), e mostrava sala com aula marcada como vazia num dos turnos (RF17).
- Uma turma com dado fora do esperado derrubava a gravação da unidade inteira, e uma unidade com erro derrubava a raspagem completa; agora cada turma tem sua própria transação e o commit é por unidade (RF01).
- Sala duplicada pelo ponto inconsistente do SIGAA depois de "LAB" (`"LAB NIT/LDS"` vs `"LAB. NIT/LDS"`), e salas/professores gravados antes da normalização existir, fundidos numa migration de dados (RF04, RF05).
- Turma com sala diferente por dia (ex. `"FCTE - S1 / MOCAP"`) gravava como uma sala só e nunca aparecia ocupada em nenhuma delas no `GET /v1/salas/vazias`; a sala agora é por horário, casada com o dia certo (RF05, RF17, ADR 0010).
- `GET /v1/salas/vazias` ficava em cache pro primeiro `dia`/`horario` consultado e devolvia esse mesmo resultado pra qualquer consulta seguinte, porque a chave de cache não incluía os parâmetros (RF17, RNF02).
- Cache e rate limit sem Redis em produção. O `REDIS_URL` do Railway vem sem o número do banco, e a troca do banco cortava a URL no lugar errado (RNF01, RNF02).
- `GET /v1/salas/vazias` continuava com as salas da raspagem anterior por até 7 dias, porque a raspagem semanal não limpava o cache por dia e horário (RF17, RNF02).
- Turma com salas que não casam com os dias aparecia com os horários repetidos em `GET /v1/disciplinas` (RF01).

## [1.1] - 2026-10-19

Sprint 4 e 5 da Release 2, encerradas em 17/10/2026.

### Adicionado

- Diagramas de arquitetura no modelo C4 (contexto, container e componente) em `docs/ARQUITETURA.md`.
- Retrospectivas das Sprints 0 a 5 em `docs/scrum/retrospectivas.md`.
- Licença MIT, Código de Conduta e este changelog.
- Guia de deploy no Railway em `docs/DEPLOY.md`, com os serviços, as variáveis de ambiente e a ordem do primeiro deploy.
- Busca de docente por nome normalizado, `GET /v1/professores?nome=`, sem diferenciar acento nem caixa (RF04, #140).
- Log de execução dos scrapers: toda execução é gravada em `execucao_logs`, diferenciando falha de fonte de falha interna, e exposta pelo endpoint `GET /v1/execucoes` (RF16).
- Medição da cobertura de testes do backend e definição dos módulos críticos (RNF09).

### Corrigido

- Parser do cardápio do RU, que falhava com os PDFs publicados a partir de 21/09 porque cada semana monta a tabela de um jeito. A leitura agora usa a posição das datas na página, e itens que valem para a semana inteira (como as bebidas do café) aparecem em todos os dias (#145).
- Professor duplicado quando o SIGAA publica carga horária diferente por disciplina no nome do docente (RF02, #140).
- Sala duplicada quando o SIGAA usa separador (`-`/`/`) ou caixa diferente pro mesmo espaço físico (RF03, #140).

### Alterado

- O endereço do Redis usado pelo Celery vem da variável `REDIS_URL`, com o docker compose como padrão.
- Uma branch `R2-nome` por pessoa na Release 2, no lugar de uma branch por tarefa (`CONTRIBUTING.md`).
- Pipeline de CI e workflow de deploy das docs atualizados para Node 24.

### Mudança no time

- O Ítalo saiu do projeto no início da Release 2. Eventos (RF08) e editais (RF09) saíram do escopo; o parser do RU, o cardápio semanal e a CLI foram redistribuídos entre Gabriel e João Paulo (`specs/README.md`).

## [Release_1] - 2026-10-06

Sprints 0 a 3, encerradas em 27/09/2026.

### Adicionado

- API versionada com `GET /v1/disciplinas`, `GET /v1/professores`, `GET /v1/salas` e `GET /v1/cardapio/semana`, com OpenAPI e Swagger UI em `/docs`.
- Scraper de turmas do SIGAA com Playwright, varrendo todas as unidades com intervalo entre requisições.
- Scraper do cardápio do RU a partir do PDF semanal, separando café, almoço e jantar.
- Agendamento com Celery e Redis, com disciplinas toda semana e cardápio todo dia, e log de sucesso e falha.
- Banco PostgreSQL 16 com SQLAlchemy 2 e migrations Alembic.
- `docker-compose.yml` com Postgres, migrations, API, Redis, worker e agendador.
- Frontend em Next.js com telas de Disciplinas, Professores, Salas e Cardápio usando dado real.
- CI com ruff, Bandit, testes unitários, testes de contrato com schemathesis e testes de integração com Postgres.
- Site de documentação com MkDocs no GitHub Pages.

### Corrigido

- Task de Disciplinas que importava uma função inexistente e não gravava no banco (#118).
- Código de horário com intervalo de datas estourando a coluna `String(20)` (#118).
- Turma com docente "a definir" quebrando o parser (#118).
- Tasks do Celery não registradas pelo `autodiscover_tasks` (#121).
- `celery_worker` sem acesso ao banco no Compose (#119).
- Imagem Docker sem o Chromium do Playwright (#121).
- CORS bloqueando o frontend (#109).
- Mensagem de lista vazia aparecendo durante o carregamento e em caso de erro (#125).

### Problemas conhecidos

- O parser do RU falha com os layouts de PDF a partir de 21/09, e o cardápio não é atualizado (#103).
- Professores e salas aparecem duplicados nas respostas da API.
- `/v1/professores` ainda não busca por nome normalizado (#38).

[2.0]: https://github.com/unb-mds/2026-2-Cerradinho-API/compare/v1.4...v2.0
[1.4]: https://github.com/unb-mds/2026-2-Cerradinho-API/compare/v1.3...v1.4
[1.3]: https://github.com/unb-mds/2026-2-Cerradinho-API/compare/v1.2...v1.3
[1.2]: https://github.com/unb-mds/2026-2-Cerradinho-API/compare/v1.1...v1.2
[1.1]: https://github.com/unb-mds/2026-2-Cerradinho-API/compare/Release_1...v1.1
[Release_1]: https://github.com/unb-mds/2026-2-Cerradinho-API/releases/tag/Release_1
