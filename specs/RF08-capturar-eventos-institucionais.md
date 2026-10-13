# RF08 · Capturar eventos institucionais

| Release | Responsável | Issue | Situação |
|---|---|---|---|
| R2 | Ninguém | [#47](https://github.com/unb-mds/2026-2-Cerradinho-API/issues/47) | Fora do escopo |

**Critérios de aceitação**
- O scraper captura data, local e descrição de cada evento publicado na agenda institucional.
- Evento sem data ou sem descrição reconhecível é descartado, não persistido incompleto.

**Regra de negócio**
- Evento passa a ser "passado" quando sua data já ocorreu; eventos passados não são excluídos do histórico, só deixam de aparecer como próximos.

## Rastreabilidade

- **PRs:** nenhum ainda.
- **Testes:** nenhum ainda.
- **Observação:** Saiu do escopo da Release 2 com a saída do Ítalo, que era o responsável. Fica registrado para uma versão futura.
