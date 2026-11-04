# Guia de Estudo: UptimeRobot

Base para a observabilidade do RNF03 (monitorar a disponibilidade das fontes e da API, com alertas). Complementa a camada 1 do [plano de monitoramento](../fontes/plano-de-monitoramento.md).

## 1. O que é

O UptimeRobot é um serviço externo que acessa um endereço de tempos em tempos e avisa quando ele para de responder. Como roda fora da nossa infraestrutura, continua alertando mesmo quando o Railway inteiro cai. Um log nosso, nesse caso, nunca seria gravado.

## 2. Tipos de monitor que interessam ao projeto

| Tipo | O que verifica | Uso no Cerradinho |
|---|---|---|
| **HTTP(s)** | Se o endereço responde com status de sucesso (2xx/3xx) | API (`/health`) e páginas do SIGAA e do RU |
| **Keyword** | Se uma palavra aparece, ou deixa de aparecer, no corpo da resposta | Pegar a página do RU de pé, mas sem o conteúdo esperado |
| Ping / Port | Se o servidor ou a porta responde | Não precisamos: o HTTP já cobre |

O plano gratuito atende ao projeto: intervalo mínimo de 5 minutos e alertas por e-mail. Os limites exatos de quantidade de monitores e de integrações (Slack, Discord, webhook) mudam com o tempo e devem ser conferidos na criação da conta.

## 3. O alerta precisa distinguir "fonte fora do ar" de "nosso serviço fora do ar"

É o segundo critério do RNF03, e muda a resposta ao incidente:

| Situação | O que fazer |
|---|---|
| SIGAA ou RU fora do ar | Nada no nosso código. A API continua servindo o último dado coletado e o scraper tenta de novo no próximo agendamento |
| API ou banco fora do ar | Incidente nosso: olhar o deploy no Railway |

Como separar no UptimeRobot:

1. **Prefixo no nome do monitor:** `[API]` ou `[FONTE]`. O nome do monitor vem no e-mail de alerta, então dá para saber do que se trata antes mesmo de abrir o painel.
2. **Página de status com dois grupos**, "Cerradinho" e "Fontes da UnB", para ver a situação de tudo num lugar só.

## 4. Por que a API precisa de uma rota `/health`

Monitorar `/docs` ou `/v1/disciplinas` tem problemas:

- `/docs` responde 200 mesmo com o banco fora do ar, porque é só a página do Swagger.
- `/v1/disciplinas` usa cache no Redis. Com o banco fora, a resposta em cache ainda sai com 200 por até uma semana.

A rota `/health` (`app/routers/saude.py`) roda `SELECT 1` no banco a cada chamada:
- **200**, com `{"status": "ok"}`, quando o banco responde;
- **503**, quando não responde.

O UptimeRobot só alerta com status de erro. Por isso a falha precisa vir no **status HTTP**, e não só no corpo da resposta. A rota fica fora do OpenAPI, porque não faz parte da API pública.

## 5. Monitores planejados

| Nome | Tipo | Alvo | Intervalo |
|---|---|---|---|
| `[API] Cerradinho` | HTTP(s) | `https://<endereço-da-api>/health` | 5 min |
| `[FONTE] SIGAA home` | HTTP(s) | `https://sigaa.unb.br/sigaa/public/` | 5 min |
| `[FONTE] SIGAA busca` | HTTP(s) | `https://sigaa.unb.br/sigaa/public/turmas/listar.jsf` | 5 min |
| `[FONTE] RU cardápio` | Keyword (alerta se "Cardápio" sumir) | `https://ru.unb.br/cardapio/` | 15 min |

Os alvos das fontes são os mesmos da seção 2 do plano de monitoramento. Em 03/11/2026, os três responderam 200, e a palavra "Cardápio" estava na página do RU. O monitor da API depende do endereço público da versão no Railway.

## 6. O que o UptimeRobot não cobre

- **Frescor do dado** (camada 3 do plano): a página do RU pode responder 200 com cardápio de semanas atrás. Isso é verificado pelo log de execução (`/v1/execucoes`, RF16) e pelas datas do cardápio, não pelo UptimeRobot.
- **Worker e beat do Celery:** não têm endereço HTTP. Se o worker parar, a API continua de pé, e só o log de execução mostra que a coleta parou. O monitor do tipo *heartbeat*, em que o próprio worker avisa que está vivo, resolveria isso, mas é recurso pago.

## Referências

- Documentação: https://uptimerobot.com/help/
