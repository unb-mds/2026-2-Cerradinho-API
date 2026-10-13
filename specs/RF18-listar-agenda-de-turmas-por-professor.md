# RF18 · Listar agenda de turmas por professor

| Release | Responsável | Issue | Situação |
|---|---|---|---|
| R2 | Vitor | [#50](https://github.com/unb-mds/2026-2-Cerradinho-API/issues/50) | Não iniciado |

**Critérios de aceitação**
- `GET /v1/professores/{nome}/agenda` devolve todas as turmas vinculadas àquele professor (RF02), com horário e sala.
- Professor inexistente devolve 404, não lista vazia.

**Regra de negócio**
- A agenda é só um recorte de RF01+RF02 por professor — não há dado de agenda que não venha das turmas já capturadas.

## Rastreabilidade

- **PRs:** nenhum ainda.
- **Testes:** nenhum ainda.
