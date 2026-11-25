# RF14 · Publicar portal do desenvolvedor

| Release | Responsável | Issue |
|---|---|---|
| R2 | Daniel | [#52](https://github.com/unb-mds/2026-2-Cerradinho-API/issues/52) |

**Critérios de aceitação**
- Existe uma página pública explicando como consumir a API: endpoints disponíveis, exemplos de uso, e onde encontrar o SDK/CLI.

**Regra de negócio**
- O portal é documentação orientada a quem consome a API de fora (outras squads), diferente da documentação de processo/arquitetura do time, que mora em `docs/`.

## Rastreabilidade

- **PRs:** [#148](https://github.com/unb-mds/2026-2-Cerradinho-API/pull/148), [#244](https://github.com/unb-mds/2026-2-Cerradinho-API/pull/244)
- **Testes:** nenhum automatizado; o frontend ainda não tem suíte de testes. A página é conferida com `tsc`, `eslint`, `next build` e aberta no navegador em 375px e 1440px.
- **Observação:** O portal fica em `/desenvolvedores` ([`frontend/app/(portal)/desenvolvedores`](https://github.com/unb-mds/2026-2-Cerradinho-API/tree/dev/frontend/app/(portal)/desenvolvedores)), com layout próprio, sem a barra lateral do app. Traz a URL base, a tabela de endpoints, exemplos de chamada em curl, Python e JavaScript, o Swagger UI embutido lendo o `/openapi.json` da API (RF11) e os cartões do SDK e da CLI (RF13), com instalação, exemplo de uso e link para a pasta `sdk/`. A tabela de endpoints é escrita à mão e precisa acompanhar os routers do backend.
