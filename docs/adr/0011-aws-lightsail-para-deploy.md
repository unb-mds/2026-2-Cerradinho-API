# ADR 0011 — AWS Lightsail para hospedagem

## Status
Aceito. Substitui o [ADR 0009](0009-railway-para-deploy.md).

## Contexto
A Release 2 precisa estar implantada e acessível publicamente até 25/11/2026 (RNF06). O ADR 0009 escolheu o Railway, mas o período de teste dele acaba por volta de 18/11, antes da entrega. Depois disso o plano Hobby custa US$ 5 por mês, mais o uso que passar dos US$ 5 inclusos.

O projeto não tem orçamento. Contas novas da AWS, criadas depois de julho de 2025, recebem créditos que valem por 6 meses e cobrem uma máquina pequena até a entrega e além dela.

Medido em 28/10 com os dados reais, o sistema inteiro usa cerca de 550 MB parado. Durante a coleta do SIGAA, o Chromium do Playwright soma algumas centenas de MB, e com o frontend o pico fica entre 1,2 e 1,5 GB.

## Decisão
Hospedar tudo numa instância **AWS Lightsail de 2 GB** (Ubuntu), com o `docker-compose.prod.yml` do repositório:

- Postgres, Redis, API, worker (com o beat embutido, `-B`) e frontend em containers, como no ambiente local;
- **Caddy** na frente, como único serviço exposto (portas 80 e 443), com HTTPS automático;
- endereço público pelo **sslip.io** (`<ip>.sslip.io` para o frontend e `api.<ip>.sslip.io` para a API), sem comprar domínio.

O passo a passo está em [`docs/DEPLOY.md`](../DEPLOY.md).

## Alternativas descartadas
- **Railway (ADR 0009):** mais simples de operar, porque banco, Redis, HTTPS e deploy vêm prontos. Foi descartado pelo custo depois do período de teste.
- **Lightsail de 1 GB (US$ 7) ou EC2 t3.micro:** pouca memória para o Chromium do scraper junto com o resto do sistema.
- **EC2 t3.small com RDS e ElastiCache:** banco e Redis gerenciados, mas custo maior e muito mais configuração do que o projeto precisa.

## Consequências
- O custo fica em zero enquanto durarem os créditos da conta. Depois, a instância de 2 GB custa US$ 12 por mês. Um alerta de orçamento na AWS avisa antes de qualquer cobrança.
- O time passa a cuidar do que o Railway fazia sozinho: atualizar o sistema da máquina, fazer backup do banco e rodar o deploy, que é manual (`git pull` e `docker compose up -d --build` por SSH).
- Produção e ambiente local usam a mesma forma de subir o sistema (Docker Compose), o que reduz surpresas no deploy.
- Com tudo numa máquina só, se ela cair, o sistema inteiro cai. Para o escopo do RNF06, que pede o sistema acessível na entrega e não uptime contínuo, esse risco é aceitável.
