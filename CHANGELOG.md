# Changelog

Mudanças relevantes do Cerradinho, por release. O formato segue o [Keep a Changelog](https://keepachangelog.com/pt-BR/1.1.0/). A descrição completa de cada release fica na [aba Releases do GitHub](https://github.com/unb-mds/2026-2-Cerradinho-API/releases).

## [Não lançado]

### Adicionado

- Agenda semanal do professor em `GET /v1/professores/{id}/agenda`, com o horário decomposto em dia/início/fim e a sala de cada bloco (RF18, #50).

### Corrigido

- Grade noturna de horário (RF17/RF18) com os horários errados e faltando a N4; agora confirmada contra turma real (aulas de 50 min, não 55, com 5 min de intervalo entre T6 e N1).

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

[Não lançado]: https://github.com/unb-mds/2026-2-Cerradinho-API/compare/v1.1...dev
[1.1]: https://github.com/unb-mds/2026-2-Cerradinho-API/compare/Release_1...v1.1
[Release_1]: https://github.com/unb-mds/2026-2-Cerradinho-API/releases/tag/Release_1
