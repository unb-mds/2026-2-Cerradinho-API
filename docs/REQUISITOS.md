# Requisitos — Cerradinho

Requisitos funcionais e não funcionais da API. O porquê do produto está no [Documento de Visão](DOCUMENTO-VISAO.md), o como no [ARQUITETURA.md](ARQUITETURA.md) e o quando no [planejamento de sprints](scrum/sprint-planning.md).

Cada requisito é nomeado no formato **verbo + objeto** e detalhado com **critérios de aceitação** (o que precisa ser verdade pra considerar o requisito pronto, testável) e **regra de negócio** (restrições e decisões de domínio específicas daquele requisito, que não são óbvias só pelo título).

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

### Disciplinas

#### RF01 — Capturar oferta de disciplinas de todas as unidades

**Critérios de aceitação**
- Dado o código de uma unidade (ex: `673` = FCTE/Gama), o scraper devolve todas as turmas abertas daquela unidade com disciplina, código, número da turma, horário, vagas ofertadas e ocupadas.
- Sem unidade específica informada, o scraper varre todas as unidades listadas no formulário público do SIGAA, uma a uma.
- Rodar o scraper duas vezes seguidas para a mesma turma atualiza os dados existentes (vagas, sala, horário), sem criar linha duplicada.
- Uma unidade que falhar (sessão expirada, erro de rede) não derruba a raspagem das demais unidades.

**Regra de negócio**
- A chave natural de uma turma é (disciplina, número, ano/período) — é o que o SIGAA considera uma oferta única; é por essa chave que o upsert decide atualizar em vez de duplicar.
- O SIGAA junta o código do horário com o intervalo de datas da turma no mesmo texto (ex: `"6T2345 (10/08/2026 - 14/12/2026)"`); só o código antes do `(` é persistido — guardar o texto inteiro estoura a coluna do banco.
- Turma com docente "a definir" vem do SIGAA sem o número de vagas ofertadas publicado; nesse caso o valor é tratado como `0`, nunca como erro que interrompe a raspagem.
- Entre requisições a unidades diferentes, o scraper aguarda um intervalo mínimo (throttling) — etiqueta com o servidor da UnB, não é otimização.

#### RF02 — Associar disciplina a professor

**Critérios de aceitação**
- Toda turma capturada com professor(es) listado(s) no SIGAA aparece com esse(s) professor(es) vinculado(s) na resposta da API.
- O mesmo professor lecionando turmas diferentes aparece como uma única entidade (não duplica o cadastro).

**Regra de negócio**
- O nome do professor, como vem do SIGAA, é a chave de deduplicação (get-or-create por nome) — não há normalização de grafia diferente pro mesmo docente.
- Turma com docente "a definir" ainda não tem essa normalização tratada: o literal "A DEFINIR DOCENTE" pode ser persistido como se fosse um nome de professor.

#### RF03 — Associar disciplina a sala/prédio

**Critérios de aceitação**
- Turma com local informado no SIGAA aparece com sala e prédio preenchidos na resposta da API.
- Turma sem local informado aparece com sala nula, nunca com erro.

**Regra de negócio**
- O texto de local do SIGAA vem no formato `"PRÉDIO - SALA"` (ex: `"FCTE - I9/I10"`); o prédio é tudo antes do primeiro `" - "`, o resto é o nome da sala.
- Texto sem o separador `" - "` vira só o nome da sala, com prédio vazio, em vez de ser descartado.

### Professores

#### RF04 — Cadastrar docentes vinculados às disciplinas

**Critérios de aceitação**
- `GET /v1/professores` lista todo professor que leciona pelo menos uma turma capturada, com as disciplinas associadas.
- Professor sem nenhuma turma ativa não aparece na listagem (não há cadastro manual de professor).

**Regra de negócio**
- O cadastro de professor nasce exclusivamente do RF01/RF02 — não existe endpoint de criação direta de professor.

### Salas/Prédios

#### RF05 — Derivar identificação de salas e prédios a partir das turmas

**Critérios de aceitação**
- `GET /v1/salas` lista toda sala distinta encontrada nas turmas capturadas, ordenada por prédio e nome.
- A mesma sala referenciada em turmas diferentes aparece como uma única entidade.

**Regra de negócio**
- Não existe fonte própria pra sala/prédio (ver seção 2) — a existência de uma sala depende inteiramente de aparecer em pelo menos uma turma do RF01.
- A chave de deduplicação é o par (prédio, nome da sala) resultante da normalização do RF03.

### Cardápio do RU

#### RF06 — Capturar cardápio diário do RU

**Critérios de aceitação**
- O scraper baixa o PDF da semana corrente do campus configurado e extrai os itens por dia e por refeição (café, almoço, jantar).
- Célula do PDF que vale pra semana inteira (ex: "Leite integral OU Bebida de soja") é aplicada a todos os dias daquela semana, não só ao primeiro.

**Regra de negócio**
- A extração é posicional (coordenadas das células do PDF), não por leitura linear de texto — uma extração sequencial embaralha qual prato pertence a qual dia, porque o layout usa células mescladas.
- A fonte oficial documentada (`ru.unb.br/cardapio`) está desatualizada; a fonte usada de fato é `ru.unb.br/cardapio-refeitorio`.

#### RF07 — Manter histórico de cardápios

**Critérios de aceitação**
- Cardápios de semanas anteriores continuam consultáveis depois que uma semana nova é capturada (não é sobrescrita).
- Reprocessar a mesma semana atualiza os itens daquela semana em vez de duplicar.

**Regra de negócio**
- O histórico é por data — a chave de um item de cardápio é (data, refeição, categoria), não (semana, campus).

### Eventos

#### RF08 — Capturar eventos institucionais

**Critérios de aceitação**
- O scraper captura data, local e descrição de cada evento publicado na agenda institucional.
- Evento sem data ou sem descrição reconhecível é descartado, não persistido incompleto.

**Regra de negócio**
- Evento passa a ser "passado" quando sua data já ocorreu; eventos passados não são excluídos do histórico, só deixam de aparecer como próximos.

### Editais

#### RF09 — Capturar editais publicados

**Critérios de aceitação**
- O scraper captura título, data de publicação, link original e órgão responsável de cada edital listado no portal público.
- Edital sem link funcional não é persistido (um edital sem fonte verificável não é um dado confiável).

**Regra de negócio**
- A fonte é centralizada no portal público do SIGAA (pós-graduação); editais publicados em outros canais da UnB ficam fora do escopo desta versão.

### API pública

#### RF10 — Expor endpoints REST por domínio

**Critérios de aceitação**
- Cada domínio (disciplinas, professores, salas, cardápio) tem um endpoint `GET` próprio sob `/v1/`.
- Domínio sem dado nenhum retorna lista vazia (`[]`) com HTTP 200, nunca erro.

**Regra de negócio**
- Rota só lê e serve dado já persistido — nenhuma lógica de negócio (normalização, cálculo) roda no router; isso fica na camada de domínio (`app/domain/`).

#### RF11 — Documentar a API via OpenAPI/Swagger

**Critérios de aceitação**
- `/openapi.json` é gerado automaticamente a partir dos schemas Pydantic e reflete exatamente o formato que os endpoints retornam.
- `/docs` expõe a documentação interativa (Swagger UI) sem configuração manual adicional.

**Regra de negócio**
- A documentação não é escrita à parte — ela nasce do contrato de dados (`app/schemas/`) e do roteamento do FastAPI, pra nunca divergir do comportamento real (ver RNF04 e RNF07).

#### RF12 — Versionar a API desde o início

**Critérios de aceitação**
- Toda rota pública vive sob o prefixo `/v1/` desde a primeira versão publicada, não só quando uma v2 for necessária.

**Regra de negócio**
- Versionar desde o início evita quebrar clientes (frontend, SDK, squads externas) quando uma mudança incompatível for inevitável — uma v2 nasce como rota nova, sem alterar o contrato de `/v1/`.

#### RF13 — Disponibilizar SDK e CLI para integração de terceiros

**Critérios de aceitação**
- Existe um pacote Python instalável que encapsula chamadas HTTP à API num cliente (SDK) e numa interface de linha de comando (CLI).
- O SDK/CLI é publicado e versionado de forma independente do backend, mas segue o contrato de `/v1/`.

**Regra de negócio**
- SDK (cliente Python) e CLI (interface de linha de comando) são duas entregas sob o mesmo requisito, feitas por pessoas diferentes do time — ver rastreabilidade.

#### RF14 — Publicar portal do desenvolvedor

**Critérios de aceitação**
- Existe uma página pública explicando como consumir a API: endpoints disponíveis, exemplos de uso, e onde encontrar o SDK/CLI.

**Regra de negócio**
- O portal é documentação orientada a quem consome a API de fora (outras squads), diferente da documentação de processo/arquitetura do time, que mora em `docs/`.

### Atualização de dados

#### RF15 — Agendar execução automática do scraping

**Critérios de aceitação**
- O scraper de cada domínio roda automaticamente, sem intervenção manual, numa frequência definida (disciplinas: semanal; cardápio: diária).
- Uma execução agendada persiste o resultado no banco real, não só executa a raspagem.

**Regra de negócio**
- O agendamento (Celery beat) só dispara a task; ano/período da oferta de disciplinas são parâmetros explícitos do agendamento, porque o SIGAA público não expõe em lugar nenhum qual é o período letivo corrente — precisam ser atualizados manualmente a cada novo semestre.

#### RF16 — Registrar log de sucesso/falha de cada execução

**Critérios de aceitação**
- Toda execução agendada (sucesso ou falha) gera um registro identificável — pessoa fazendo triagem de incidente consegue saber se o scraper rodou e o que aconteceu.
- O log diferencia falha da fonte (SIGAA/RU fora do ar) de falha do nosso código (exceção no parser).

**Regra de negócio**
- O log é por execução de task, não por turma/item individual — granularidade fina demais tornaria o log inútil pra triagem.

## 4. Features derivadas

Calculadas em cima do que os domínios acima já capturam (RF01–RF07), com pouco esforço extra — não têm fonte própria nem scraper próprio.

#### RF17 — Calcular salas vazias por dia e horário

**Critérios de aceitação**
- `GET /v1/salas/vazias?dia=segunda&horario=14:00` devolve as salas que não têm nenhuma turma cadastrada naquele dia/horário.
- Mudar a oferta de disciplinas (nova turma, turma removida) reflete automaticamente no resultado, sem reprocessamento manual.

**Regra de negócio**
- "Vazia" significa só "sem aula cadastrada via RF01" — não reflete reserva informal, evento ou uso fora da grade de disciplinas. É uma leitura otimista, não uma garantia de disponibilidade real.

#### RF18 — Listar agenda de turmas por professor

**Critérios de aceitação**
- `GET /v1/professores/{nome}/agenda` devolve todas as turmas vinculadas àquele professor (RF02), com horário e sala.
- Professor inexistente devolve 404, não lista vazia.

**Regra de negócio**
- A agenda é só um recorte de RF01+RF02 por professor — não há dado de agenda que não venha das turmas já capturadas.

#### RF19 — Agrupar cardápio semanal

**Critérios de aceitação**
- `GET /v1/cardapio/semana?data_inicio=...` devolve os 7 dias a partir da data informada; sem `data_inicio`, devolve de hoje até hoje+6 dias.
- Dia sem cardápio publicado aparece como ausente/vazio no agrupamento, não interrompe a resposta dos outros dias.

**Regra de negócio**
- O agrupamento é só uma leitura em janela de 7 dias sobre o histórico do RF07 — não dispara nova raspagem.

## 5. Requisitos não funcionais

#### RNF01 — Limitar requisições por cliente/IP (rate limiting)

**Critérios de aceitação**
- Cliente que ultrapassa o limite de requisições num intervalo recebe HTTP 429, não é simplesmente bloqueado em silêncio.

**Regra de negócio**
- Protege a API contra uso abusivo de terceiros (RF13) sem precisar de autenticação — o produto é público e sem login.

#### RNF02 — Cachear respostas para reduzir tempo de resposta e carga no banco

**Critérios de aceitação**
- Requisição repetida ao mesmo endpoint, dentro da janela de cache, não gera nova consulta ao banco.
- Dado que mudou (nova raspagem concluída) invalida o cache daquele domínio.

**Regra de negócio**
- O cache é por domínio (disciplinas, cardápio, etc.), alinhado à frequência de atualização de cada um (RF15) — não faz sentido cachear por mais tempo que o intervalo entre raspagens.

#### RNF03 — Monitorar disponibilidade das fontes e da API, com alertas

**Critérios de aceitação**
- Queda de uma fonte externa (SIGAA, RU) ou da própria API gera um alerta, não só um log silencioso.
- O alerta distingue "fonte externa fora do ar" de "nosso serviço fora do ar" — são respostas de incidente diferentes.

**Regra de negócio**
- Disponibilidade (a fonte responde?) é só a primeira camada: estrutura (o formato esperado ainda existe?) e frescor (o dado é recente?) são verificadas à parte, no [plano de monitoramento](fontes/plano-de-monitoramento.md).

#### RNF04 — Validar a API contra testes de contrato

**Critérios de aceitação**
- Toda rota pública é validada automaticamente contra o `/openapi.json` publicado (schemathesis) no pipeline de CI.
- Uma rota cuja resposta real diverge do schema documentado falha o CI, não passa despercebida.

**Regra de negócio**
- O contrato validado é o OpenAPI gerado (RF11), não um schema mantido à mão — evita o contrato e a implementação divergirem.

#### RNF05 — Tratar falhas de scraping de forma resiliente

**Critérios de aceitação**
- Mudança no layout ou no fluxo de uma fonte externa derruba a raspagem daquela fonte com um erro explícito, sem gravar dado parcial/incorreto no banco.
- Sessão expirada do SIGAA é reconhecida e tratada com nova tentativa, não é interpretada como dado válido.

**Regra de negócio**
- Princípio geral: o scraper deve falhar alto e cedo. É preferível uma exceção explícita a um registro vazio ou incompleto persistido no banco — todo parser valida que encontrou o que esperava antes de gravar.

#### RNF06 — Garantir disponibilidade do software implantado

**Critérios de aceitação**
- Ao fim da Release 2, o sistema (API + frontend) está implantado e acessível publicamente, não só rodando localmente.

**Regra de negócio**
- **Porta de qualidade obrigatória da Release 2**: a nota da Release 2 só é lançada com o software implantado e acessível — não é meta de uptime contínuo, é bloqueador binário de avaliação. A Release 1 não precisa estar em produção.

#### RNF07 — Manter a documentação sincronizada com o estado real da API

**Critérios de aceitação**
- A documentação (OpenAPI, README, portal do desenvolvedor) reflete os endpoints e contratos realmente implementados, sem rota documentada que não existe ou existente que não está documentada.

**Regra de negócio**
- "Doc viva" depende do RF11 (documentação gerada do código, não escrita à parte) — é a forma de garantir esse requisito sem depender de disciplina manual de manter dois lugares sincronizados.

#### RNF08 — Rodar pipeline de CI/CD

**Critérios de aceitação**
- Todo push dispara lint, testes (unitários, contrato, integração) e SAST automaticamente, desde a Release 1.
- Achado de severidade crítica ou alta no SAST bloqueia o lançamento da nota daquela entrega.

**Regra de negócio**
- O pipeline é porta de qualidade da disciplina, não só conveniência de time — PR com CI vermelho não é elegível pra merge (ver `CONTRIBUTING.md`).

#### RNF09 — Garantir qualidade de testes

**Critérios de aceitação**
- Cobertura de linhas do backend ≥ 90%.
- Escore de mutação ≥ 50% nos módulos críticos (scrapers, domínio, persistência).
- Teste de sabotagem (simular fonte quebrada/mudada) cobrindo 100% dos módulos críticos.

**Regra de negócio**
- Cobertura de linha sozinha não garante teste que realmente falha quando o código quebra — por isso mutação e sabotagem são métricas à parte, não substituídas por cobertura alta.

## 6. Rastreabilidade

Cada requisito tem uma issue no GitHub, na milestone da release em que entra.

| Requisito | Release | Responsável | Issue |
|---|---|---|---|
| RF01 — Capturar oferta de disciplinas | R1 | Vitor | #35 |
| RF02 — Associar disciplina a professor | R1 | Vitor | #36 |
| RF03 — Associar disciplina a sala | R1 | Vitor | #37 |
| RF04 — Cadastrar docentes | R1 | Vitor | #38 |
| RF05 — Derivar salas e prédios | R1 | Vitor | #39 |
| RF06 — Capturar cardápio diário | R1 | Ítalo | #40 |
| RF07 — Manter histórico de cardápios | R1 | Ítalo | #41 |
| RF08 — Capturar eventos | R2 | Ítalo | #47 |
| RF09 — Capturar editais | R2 | Ítalo | #48 |
| RF10 — Expor endpoints REST | R1 | Daniel | #42 |
| RF11 — Documentar via OpenAPI/Swagger | R1 | Daniel | #43 |
| RF12 — Versionar a API (`/v1/`) | R1 | Gabriel | #44 |
| RF13 — Disponibilizar SDK (Vitor) e CLI (Ítalo) | R2 | Vitor, Ítalo | #49 |
| RF14 — Publicar portal do desenvolvedor | R2 | Daniel | #52 |
| RF15 — Agendar scraping automático | R1 | Arthur | #45 |
| RF16 — Registrar log de execução | R1 | Arthur | #46 |
| RF17 — Calcular salas vazias | R2 | Vitor | #53 |
| RF18 — Listar agenda do professor | R2 | Vitor | #50 |
| RF19 — Agrupar cardápio semanal | R2 | Ítalo | #51 |
| RNF01 — Limitar requisições (rate limiting) | R2 | Arthur | #66 |
| RNF02 — Cachear respostas | R2 | Arthur | #67 |
| RNF03 — Monitorar disponibilidade | R2 | João Paulo | #68 |
| RNF04 — Validar contrato da API | R1 | João Paulo | #69 |
| RNF05 — Tratar falhas de scraping | R1 | João Paulo | #70 |
| RNF06 — Garantir disponibilidade implantada | R2 | Gabriel | #71 |
| RNF07 — Manter documentação sincronizada | R1 | João Paulo | #72 |
| RNF08 — Rodar pipeline de CI/CD | R1 | João Paulo | #73 |
| RNF09 — Garantir qualidade de testes | R2 | João Paulo | #74 |
