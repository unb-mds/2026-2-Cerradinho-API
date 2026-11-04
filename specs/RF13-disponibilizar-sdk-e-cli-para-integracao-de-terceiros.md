# RF13 · Disponibilizar SDK e CLI para integração de terceiros

| Release | Responsável | Issue |
|---|---|---|
| R2 | Vitor (SDK), João Paulo (CLI) | [#49](https://github.com/unb-mds/2026-2-Cerradinho-API/issues/49) |

**Critérios de aceitação**
- Existe um pacote Python instalável (`sdk/`) que encapsula chamadas HTTP à API num cliente (SDK) e numa interface de linha de comando (CLI).
- O SDK/CLI é publicado e versionado de forma independente do backend, mas segue o contrato de `/v1/`.

**Regra de negócio**
- SDK (cliente Python) e CLI (interface de linha de comando) são duas entregas sob o mesmo requisito, feitas por pessoas diferentes do time — ver rastreabilidade.
- O cliente de baixo nível (`cerradinho_sdk._gerado`) é **gerado** a partir do OpenAPI que o backend expõe (RF11), via `openapi-python-client` — não escrito à mão, pra nunca ficar fora de sincronia com os routers. `sdk/scripts/gerar_cliente.sh` regera depois de qualquer mudança num router.
- A interface pública do SDK (`CerradinhoClient`, em `cerradinho_sdk/client.py`) é um cliente fino: um método por endpoint de `/v1/`, sem recalcular nada que o backend já computa (salas vazias, agenda do professor continuam sendo só leitura do que a API responde).
- A versão do SDK acompanha a versão da API que ele cobre (RF12) — hoje, `1.0.0` pra `/v1/`.

## Rastreabilidade

- **PRs:** nenhum ainda.
- **Testes:** [`sdk/tests/test_client.py`](https://github.com/unb-mds/2026-2-Cerradinho-API/blob/dev/sdk/tests/test_client.py) — contra respostas HTTP mockadas (`respx`), validado também de ponta a ponta contra o backend real antes do commit.
