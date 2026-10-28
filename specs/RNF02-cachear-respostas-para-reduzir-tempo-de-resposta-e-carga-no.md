# RNF02 · Cachear respostas para reduzir tempo de resposta e carga no banco

| Release | Responsável | Issue |
|---|---|---|
| R2 | Arthur | [#67](https://github.com/unb-mds/2026-2-Cerradinho-API/issues/67) |

**Critérios de aceitação**
- Requisição repetida ao mesmo endpoint, dentro da janela de cache, não gera nova consulta ao banco.
- Dado que mudou (nova raspagem concluída) invalida o cache daquele domínio.

**Regra de negócio**
- O cache é por domínio (disciplinas, cardápio, etc.), alinhado à frequência de atualização de cada um (RF15) — não faz sentido cachear por mais tempo que o intervalo entre raspagens.

## Desenho do cache

**Banco lógico do Redis:** `db 2`. O Celery já usa `db 0` (broker) e
`db 1` (backend de resultado) — ver `app/celery_app.py` — então o cache
fica num terceiro banco lógico, sem risco de colidir com chave de job.

**Chave por domínio**, prefixada com a versão da API:
- `cache:v1:disciplinas`
- `cache:v1:professores`
- `cache:v1:salas`
- `cache:v1:cardapio:semana:{data_inicio}`

**Valor armazenado:** o JSON já serializado da resposta (o corpo que o
endpoint devolveria), não o objeto Python. Em cache hit, a rota devolve
esse JSON direto, sem rodar a query nem revalidar pelo `response_model`
(já foi validado quando foi gravado).

**TTL por domínio, alinhado à frequência de raspagem (RF15)** 
- `disciplinas` / `professores` / `salas`: ~7 dias (raspados juntos,
  semanalmente, pela mesma task)
- `cardapio:semana:*`: ~1 dia (raspado diariamente)

**Invalidação ativa, não só TTL** (critério de aceite: dado novo invalida
o cache do domínio). As próprias tasks do Celery apagam a chave depois
do `commit`:
- `scrape_disciplinas_task` → apaga `cache:v1:disciplinas`,
  `cache:v1:professores` e `cache:v1:salas` (as três mudam juntas,
  porque vêm da mesma raspagem — `persistir_turmas` cria/atualiza
  Professor e Sala também)
- `scrape_cardapio_task` → apaga todas as chaves que casam com
  `cache:v1:cardapio:semana:*` (a chave exata varia por semana, então
  precisa de `SCAN` + `DELETE` por padrão, nunca `KEYS` — bloqueia o
  Redis inteiro em produção)

**Onde plugar no FastAPI:** uma dependency simples por rota de leitura
(`disciplinas.py`, `cardapio.py`, `professores.py`, `salas.py`) que
checa o Redis antes de chamar a camada de domínio; em miss, chama a
função de domínio normalmente e grava o resultado serializado no cache
com o TTL do domínio.

**Biblioteca:** mão na massa (um helper pequeno de get/set), não uma lib
como `fastapi-cache2`. São só 4 rotas pra cachear — não compensa o custo
de avaliar/manter mais uma dependência externa pra um problema desse tamanho.

**Compatibilidade com os testes de contrato:** como o cache guarda o
JSON já serializado pelo `response_model`, o formato da resposta não
muda entre cache hit e miss — os testes de contrato (schemathesis)
devem passar sem alteração nenhuma.

## Rastreabilidade

- **PRs:** #150
- **Testes:** `tests/core/test_cache.py` (helper de cache: grava no miss, lê no hit, invalidação por chave e por prefixo), mais a cobertura indireta de `tests/routers/conftest.py` (fixture `cache_falso`, autouse em toda a suíte de rotas).
- **Observações:** implementado com uma função auxiliar (`resposta_cacheada`, em `app/core/cache.py`), não uma FastAPI dependency, mais simples pro caso de 4 rotas.
- **Decisões:** [ADR 0007](https://github.com/unb-mds/2026-2-Cerradinho-API/blob/dev/docs/adr/0007-cache-e-rate-limit-na-api.md)
