# Deploy na AWS Lightsail

Como o Cerradinho sobe em produção numa instância da AWS Lightsail ([ADR 0011](adr/0011-aws-lightsail-para-deploy.md)), atendendo ao RNF06. O ambiente local continua sendo o `docker compose up` descrito no [README](https://github.com/unb-mds/2026-2-Cerradinho-API/blob/dev/README.md).

Nenhum segredo fica no repositório. A senha do banco fica só no `backend/.env` da máquina de produção.

## Como fica a produção

Uma máquina só roda o [`docker-compose.prod.yml`](https://github.com/unb-mds/2026-2-Cerradinho-API/blob/dev/docker-compose.prod.yml):

| Serviço | O que roda | Exposto para fora |
|---|---|---|
| caddy | Proxy com HTTPS automático ([`Caddyfile`](https://github.com/unb-mds/2026-2-Cerradinho-API/blob/dev/Caddyfile)) | Sim, portas 80 e 443 |
| frontend | Next.js com build de produção | Não, só pelo Caddy |
| api | FastAPI | Não, só pelo Caddy |
| worker | Celery com o beat embutido (`-B`) | Não |
| db | PostgreSQL 16 | Não |
| redis | Redis 7 | Não |
| migrate | `alembic upgrade head`, roda e termina | Não |

Endereços de produção, no IP fixo `3.147.228.104` (instância `cerradinho`, região `us-east-2`):

- frontend: [https://3-147-228-104.sslip.io](https://3-147-228-104.sslip.io)
- API: [https://api.3-147-228-104.sslip.io](https://api.3-147-228-104.sslip.io), com o Swagger em [`/docs`](https://api.3-147-228-104.sslip.io/docs)

Num deploy novo, o IP da máquina entra no lugar de `3-147-228-104`.

O [sslip.io](https://sslip.io) resolve qualquer nome com um IP dentro para esse IP, então não é preciso comprar domínio. O Caddy pede o certificado HTTPS para esses nomes na primeira vez que sobe.

Diferenças para o `docker-compose.yml` de desenvolvimento:

- o Postgres e o Redis não abrem porta para fora da máquina;
- a API roda sem `--reload` e confia no IP do cliente que o Caddy repassa (`--forwarded-allow-ips`). Sem isso, toda requisição parece vir do Caddy e o rate limit (RNF01) vira um limite só para todos os usuários;
- o beat roda dentro do worker para economizar memória. Por isso só pode existir um worker, senão os agendamentos rodam em dobro.

## Primeiro deploy

### 1. Conta e alerta de custo

1. Criar a conta na AWS. Contas novas recebem créditos que valem por 6 meses. Confira o saldo em **Billing → Credits**.
2. Em **Billing → Budgets**, criar um orçamento de **US$ 1** com alerta por e-mail. Assim qualquer cobrança fora dos créditos avisa antes de virar conta.

### 2. Máquina

No console do Lightsail:

1. **Create instance**: Linux, **Ubuntu 24.04 LTS**, plano de **2 GB** (US$ 12 por mês, coberto pelos créditos).
2. Em **Networking**, criar um **Static IP** e anexar à instância. O IP fixo é grátis enquanto está anexado.
3. No firewall IPv4 da instância, deixar abertas só as portas **22** (SSH), **80** (HTTP) e **443** (HTTPS).

### 3. Docker e memória extra

Pelo botão **Connect using SSH** do Lightsail:

```bash
curl -fsSL https://get.docker.com | sudo sh
sudo usermod -aG docker ubuntu

# 2 GB de swap: o build do frontend e o Chromium do scraper passam dos 2 GB de RAM em pico
sudo fallocate -l 2G /swapfile && sudo chmod 600 /swapfile
sudo mkswap /swapfile && sudo swapon /swapfile
echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab

exit
```

Sair e entrar de novo no SSH, para o usuário passar a usar o Docker sem `sudo`.

### 4. Código e configuração

```bash
git clone https://github.com/unb-mds/2026-2-Cerradinho-API.git
cd 2026-2-Cerradinho-API

cp backend/.env.example backend/.env
sed -i "s/^POSTGRES_PASSWORD=.*/POSTGRES_PASSWORD=$(openssl rand -hex 16)/" backend/.env

cp .env.prod.example .env
nano .env   # trocar 1-2-3-4 pelo IP fixo, com hífens no lugar dos pontos
```

A `main` é a branch de produção. O `backend/.env` e o `.env` da raiz estão no `.gitignore` e nunca vão para o repositório.

### 5. Subir

```bash
docker compose -f docker-compose.prod.yml up -d --build
```

O primeiro build leva alguns minutos, por causa do Chromium do Playwright e do build do Next.js.

### 6. Conferir

- `https://api.<ip>.sslip.io/docs` abre o Swagger;
- `https://<ip>.sslip.io` abre o site;
- `docker compose -f docker-compose.prod.yml logs worker` mostra `celery@... ready` e `beat: Starting...`.

As listas começam vazias. Para não esperar o agendamento (disciplinas no domingo às 3h, cardápio todo dia às 5h), as coletas podem ser disparadas uma vez:

```bash
docker compose -f docker-compose.prod.yml exec worker celery -A app.celery_app call app.tasks.cardapio.scrape_cardapio_task
docker compose -f docker-compose.prod.yml exec worker celery -A app.celery_app call app.tasks.scraping.scrape_disciplinas_task --kwargs '{"nivel": "G", "ano": "2026", "periodo": "2"}'
```

A de disciplinas leva cerca de 12 minutos. O resultado aparece em `/v1/execucoes`.

## Atualizar a produção

Depois de cada merge na `main`:

```bash
cd 2026-2-Cerradinho-API
git pull
docker compose -f docker-compose.prod.yml up -d --build
```

As migrations rodam sozinhas pelo serviço `migrate` antes de a API subir. Os dados ficam no volume `postgres_data` e não se perdem. Nunca use `down -v` em produção, porque o `-v` apaga o banco.

## Backup

```bash
docker compose -f docker-compose.prod.yml exec -T db sh -c 'pg_dump -U "$POSTGRES_USER" "$POSTGRES_DB"' > backup-$(date +%F).sql
```

O Lightsail também tira snapshots da máquina inteira (**Snapshots → Create snapshot**). Vale fazer um antes de cada atualização grande.

## Pontos de atenção

- **Período letivo:** o ano e o período da coleta de disciplinas estão fixos em `backend/app/celery_app.py` e precisam ser atualizados antes de cada semestre.
- **Endereço da API no frontend:** o Next.js grava o `NEXT_PUBLIC_API_URL` no build. Se o IP mudar, é preciso trocar o `.env` da raiz e rodar o `up -d --build` de novo, porque reiniciar não basta.
- **Créditos:** quando os créditos ou os 6 meses acabarem, a instância passa a custar US$ 12 por mês. O alerta de orçamento avisa antes.
- **Fuso horário:** o Celery usa `America/Sao_Paulo`, então os horários do agendamento não dependem do fuso do servidor.
