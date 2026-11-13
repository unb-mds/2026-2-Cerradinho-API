# RNF06 · Garantir disponibilidade do software implantado

| Release | Responsável | Issue |
|---|---|---|
| R2 | Gabriel | [#71](https://github.com/unb-mds/2026-2-Cerradinho-API/issues/71) |

**Critérios de aceitação**
- Ao fim da Release 2, o sistema (API + frontend) está implantado e acessível publicamente, não só rodando localmente.

**Regra de negócio**
- **Porta de qualidade obrigatória da Release 2**: a nota da Release 2 só é lançada com o software implantado e acessível — não é meta de uptime contínuo, é bloqueador binário de avaliação. A Release 1 não precisa estar em produção.

## Rastreabilidade

- **PRs:** [#145](https://github.com/unb-mds/2026-2-Cerradinho-API/pull/145) (variáveis de ambiente e guia de deploy em [`docs/DEPLOY.md`](https://github.com/unb-mds/2026-2-Cerradinho-API/blob/dev/docs/DEPLOY.md)), [#240](https://github.com/unb-mds/2026-2-Cerradinho-API/pull/240) (compose de produção e deploy na AWS Lightsail)
- **Produção:** site em [https://3-147-228-104.sslip.io](https://3-147-228-104.sslip.io) e API em [https://api.3-147-228-104.sslip.io](https://api.3-147-228-104.sslip.io/docs), no ar desde 04/11/2026
- **Testes:** [`tests/tasks/test_celery_app.py`](https://github.com/unb-mds/2026-2-Cerradinho-API/blob/dev/backend/tests/tasks/test_celery_app.py) (endereço do Redis lido do `REDIS_URL`)
- **Decisões:** [ADR 0011](https://github.com/unb-mds/2026-2-Cerradinho-API/blob/dev/docs/adr/0011-aws-lightsail-para-deploy.md), que substitui o [ADR 0009](https://github.com/unb-mds/2026-2-Cerradinho-API/blob/dev/docs/adr/0009-railway-para-deploy.md)
