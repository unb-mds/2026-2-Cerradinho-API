# RNF03 · Monitorar disponibilidade das fontes e da API, com alertas

| Release | Responsável | Issue |
|---|---|---|
| R2 | João Paulo | [#68](https://github.com/unb-mds/2026-2-Cerradinho-API/issues/68) |

**Critérios de aceitação**
- Queda de uma fonte externa (SIGAA, RU) ou da própria API gera um alerta, não só um log silencioso.
- O alerta distingue "fonte externa fora do ar" de "nosso serviço fora do ar" — são respostas de incidente diferentes.

**Regra de negócio**
- Disponibilidade (a fonte responde?) é só a primeira camada: estrutura (o formato esperado ainda existe?) e frescor (o dado é recente?) são verificadas à parte, no [plano de monitoramento](https://github.com/unb-mds/2026-2-Cerradinho-API/blob/dev/docs/fontes/plano-de-monitoramento.md).

## Configuração

Monitores no UptimeRobot (plano gratuito), criados pelo script [`backend/scripts/uptimerobot.py`](https://github.com/unb-mds/2026-2-Cerradinho-API/blob/dev/backend/scripts/uptimerobot.py). A lista de monitores fica no código, e não só no painel, para ser revisada em PR e recriada se a conta mudar.

| Monitor | Tipo | Alvo | Intervalo |
|---|---|---|---|
| `[API] Cerradinho` | HTTP(s) | `https://api.3-147-228-104.sslip.io/health` | 5 min |
| `[FONTE] SIGAA home` | HTTP(s) | `https://sigaa.unb.br/sigaa/public/` | 5 min |
| `[FONTE] SIGAA busca de turmas` | HTTP(s) | `https://sigaa.unb.br/sigaa/public/turmas/listar.jsf?aba=p-ensino` | 5 min |
| `[FONTE] RU cardápio` | Palavra-chave: alerta se "Cardápio" sumir | `https://ru.unb.br/cardapio/` | 15 min |
| `[FONTE] RU cardápio refeitório` | Palavra-chave: alerta se "Cardápio" sumir | `https://ru.unb.br/cardapio-refeitorio/` | 15 min |

- **Alerta:** e-mail para os contatos de alerta da conta. Todos os contatos são ligados aos monitores na criação.
- **Fonte x nosso serviço:** o prefixo `[API]` ou `[FONTE]` vai no nome do monitor e, por isso, no assunto do e-mail. Com `[FONTE]`, não há nada a fazer no código: a API segue servindo o último dado coletado e o scraper tenta de novo no próximo agendamento. Com `[API]`, o incidente é nosso: olhar o deploy na AWS ([DEPLOY.md](../docs/DEPLOY.md)).
- **Por que `/health`:** a rota roda `SELECT 1` no banco e devolve 503 sem ele. O `/docs` e as rotas com cache no Redis responderiam 200 com o banco fora do ar.
- **Fontes iguais às da coleta:** um teste compara as URLs dos monitores `[FONTE]` com as constantes dos scrapers. Se um scraper mudar de URL, o teste falha até o monitor acompanhar.

Para criar ou recriar os monitores (na pasta `backend/`):

```bash
python -m scripts.uptimerobot --dry-run                          # mostra o plano
UPTIMEROBOT_API_KEY=<chave principal> python -m scripts.uptimerobot
```

O script não recria monitor com o mesmo nome. A chave principal (*Main API Key*) fica na seção de API do painel do UptimeRobot e não vai para o repositório.

**Fora do escopo do UptimeRobot:** frescor do dado (RU servindo cardápio antigo com 200) e worker do Celery parado. Os dois aparecem no log de execução (`/v1/execucoes`, RF16). Detalhes no [estudo do UptimeRobot](../docs/estudos/estudo-uptimerobot.md) e no [plano de monitoramento](../docs/fontes/plano-de-monitoramento.md).

## Rastreabilidade

- **PRs:** [#239](https://github.com/unb-mds/2026-2-Cerradinho-API/pull/239) (rota `/health` e estudo do UptimeRobot).
- **Testes:** [`tests/routers/test_saude_router.py`](https://github.com/unb-mds/2026-2-Cerradinho-API/blob/dev/backend/tests/routers/test_saude_router.py), [`tests/scripts/test_uptimerobot.py`](https://github.com/unb-mds/2026-2-Cerradinho-API/blob/dev/backend/tests/scripts/test_uptimerobot.py)
