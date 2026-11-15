# RNF09 · Garantir qualidade de testes

| Release | Responsável | Issue |
|---|---|---|
| R2 | João Paulo | [#74](https://github.com/unb-mds/2026-2-Cerradinho-API/issues/74) |

**Critérios de aceitação**
- Cobertura de linhas do backend ≥ 90%.
- Escore de mutação ≥ 50% nos módulos críticos (scrapers, domínio, persistência).
- Teste de sabotagem (simular fonte quebrada/mudada) cobrindo 100% dos módulos críticos.

**Regra de negócio**
- Cobertura de linha sozinha não garante teste que realmente falha quando o código quebra — por isso mutação e sabotagem são métricas à parte, não substituídas por cobertura alta.

## Situação atual

Medição de 15/11/2026, na `R2-joao`, com os testes de sabotagem e os testes escritos a partir dos mutantes sobreviventes. **As três metas foram atingidas.**

| Meta | Resultado | Antes (19/10) |
|---|---|---|
| Cobertura de linhas do backend ≥ 90% | **98%** (1.191 de 1.212 linhas no passo de testes do CI, sem contrato e integração) | 81% |
| Mutação ≥ 50% nos módulos críticos | **87,3% a 100%** por módulo (tabela abaixo) | não medido |
| Sabotagem em 100% dos módulos críticos | **8 de 8** (tabela em "Teste de sabotagem") | nenhum |

### Módulos críticos

Critério: módulos que, se quebrarem em silêncio, gravam dado errado no banco ou param a coleta. São eles que entram nas metas de mutação e de sabotagem.

| Módulo | Por que é crítico | Cobertura | Mutantes | Score de mutação |
|---|---|---|---|---|
| `app/scrapers/disciplinas/parser.py` | Transforma o HTML do SIGAA nas turmas que vão para o banco | 100% | 70 | **90,0%** |
| `app/scrapers/cardapio/parser.py` | Transforma o PDF do RU nos itens de cardápio | 99% | 347 | **87,3%** |
| `app/domain/disciplinas.py` | Grava turmas, disciplinas, professores, salas e horários (get-or-create e upsert) | 98% | 182 | **91,2%** |
| `app/domain/cardapio.py` | Grava e consulta o cardápio por data | 100% | 50 | **96,0%** |
| `app/tasks/scraping.py` | Task agendada que raspa e persiste as disciplinas | 100% | 5 | **100%** |
| `app/tasks/cardapio.py` | Task agendada que baixa, lê e persiste o cardápio | 100% | 1 | **100%** |
| `app/tasks/logging_signals.py` | Registra sucesso e falha de cada execução (RF16) | 100% | 3 | **100%** |
| `app/domain/execucoes.py` | Grava e lista o histórico de execuções (RF16) | 100% | 3 | **100%** |

Fora da lista: routers e schemas, cobertos pelos testes de contrato (RNF04), e models, cobertos pelos testes de domínio e de integração. As linhas sem cobertura que sobram estão em `app/core/cache.py` (ramos de erro do Redis), em `app/core/database.py` (`get_db`, sempre substituído nos testes) e em ramos defensivos de `app/domain/disciplinas.py`.

### Teste de mutação

Ferramenta: **cosmic-ray 8.7.0**, a escolhida no [estudo de teste de mutação](../docs/estudos/estudo-teste-de-mutacao.md) por rodar no Windows e no Linux. O script `backend/scripts/mutacao.py` roda um módulo crítico por vez, cada um com os testes que o exercitam, e sai com erro se algum ficar abaixo de 50%:

```bash
cd backend
python -m scripts.mutacao                          # os 8 módulos críticos
python -m scripts.mutacao app/domain/cardapio.py   # só um módulo
python -m scripts.mutacao --paralelo 4             # módulos em paralelo
```

- O cosmic-ray altera o arquivo no disco para criar cada mutante. Por isso o script copia o backend para uma pasta temporária antes de mutar: uma rodada interrompida não deixa mutante no código.
- Mutantes dentro de anotação de tipo (`str | None` virando `str + None`) são pulados. A anotação nunca é avaliada, então esses mutantes são equivalentes. Foram 132 dos 793 gerados.
- No CI, o workflow **Mutação** (`.github/workflows/mutacao.yml`) roda o mesmo script quando é acionado na aba Actions. Ele não roda em todo push: a rodada completa leva cerca de 30 minutos com os 8 módulos em paralelo.

A primeira rodada, só com os testes que já existiam, deu 42,9% no parser de disciplinas, 57,8% no domínio de disciplinas e 0% em `domain/execucoes.py`. Os sobreviventes viraram testes. Os principais:

| Mutante sobrevivente | Lacuna | Teste novo |
|---|---|---|
| Índice de coluna e `strip` trocados no parser do SIGAA | Nenhum teste conferia cada campo da turma | `test_parse_turmas_le_cada_coluna_no_campo_certo_e_sem_espacos` |
| `LIMITE_PADRAO = 50` trocado e fuso não aplicado | O teste da rota só conferia a ordem | `tests/domain/test_execucoes.py` |
| `!= 2` trocado por `<` ao ler o intervalo do link do RU | Link com três datas quebraria a seleção do PDF | `test_link_que_nao_tem_exatamente_duas_datas_e_ignorado` |
| Tolerância de altura do PDF do RU zerada | Célula um pouco acima da categoria perdia o prato | `test_le_categoria_por_altura_e_dia_por_posicao_ignorando_texto_sem_dia` |
| `continue` trocado por `break` em texto sem dia no PDF | Um texto solto descartaria o resto da página | o mesmo teste acima |
| `!=` trocado por `>` ao casar salas e dias | Com mais salas que dias, uma sala ficava de fora | `test_persistir_turma_com_mais_salas_que_dias_associa_tudo_a_todas` |
| `==` trocado por `<=` na cobertura dos pares código(sala) | Um par a mais no campo de sala inventaria aula | `test_persistir_turma_com_par_codigo_sala_a_mais_nao_inventa_aula` |
| `<=` trocado por `<` no fim da semana do cardápio | O domingo sumiria da semana | `test_listar_cardapio_semana_inclui_o_domingo_e_para_antes_da_segunda_seguinte` |

Os 69 sobreviventes restantes são, na maior parte, equivalentes ou fronteiras sem significado: `<=` trocado por `<` em coordenadas do PDF (um caractere exatamente na borda da célula), `/` trocado por `//` em contas com coordenadas inteiras, `maxsplit` que não muda o resultado e `is not` dentro de filtro do SQLAlchemy.

### Teste de sabotagem

Os testes em `backend/tests/sabotagem/` quebram a fonte de propósito e rodam a task de verdade pelo Celery, com o scraper, o parser, o domínio e os signals de log reais. Só a borda com o mundo externo é trocada por um dublê: o Playwright no SIGAA e o `requests.get` no RU. Cada cenário confere três coisas:

- o log registra a falha com o tipo certo (`fonte` ou `interna`, RF16), lido como a API lê (`listar_execucoes`);
- o banco fica como estava;
- o cache fica como estava.

Um caso de controle sem sabotagem prova que o dublê funciona.

| Fonte | Cenário | Tipo da falha no log |
|---|---|---|
| SIGAA | Fora do ar (timeout do Playwright) | fonte |
| SIGAA | Rede cai durante a busca das unidades | fonte |
| SIGAA | Sessão expirada em todas as tentativas | fonte |
| SIGAA | Formulário de busca sem a lista de unidades (layout mudado) | interna |
| SIGAA | Tabela de resultado com outro id (layout mudado) | interna |
| RU | Site fora do ar | fonte |
| RU | Listagem com erro 503 | fonte |
| RU | Listagem sem o PDF da semana | fonte |
| RU | PDF fora do ar (timeout) | fonte |
| RU | Link do PDF expirado (404) | fonte |
| RU | Página de erro com status 200 no lugar do PDF | fonte |
| RU | PDF corrompido | interna |
| RU | PDF com layout novo (coluna de categoria renomeada) | interna |

Além do fluxo completo, há testes de sabotagem por camada:

- no scraper do SIGAA, a nova tentativa com sessão expirada e com rede instável;
- no download do PDF do RU, o backoff de 2 s e 4 s;
- no parser do RU, o PDF real com datas por extenso, tabela sem bordas e categorias desconhecidas.

| Módulo crítico | Sabotado em |
|---|---|
| `app/scrapers/disciplinas/parser.py` | `test_sabotagem_sigaa.py` (layout mudado, colunas trocadas) |
| `app/scrapers/cardapio/parser.py` | `test_sabotagem_ru.py` (layout novo do PDF e da listagem) |
| `app/domain/disciplinas.py` | `test_sabotagem_sigaa.py` (turmas já gravadas continuam iguais) |
| `app/domain/cardapio.py` | `test_sabotagem_ru.py` (o cardápio já gravado continua sendo servido) |
| `app/tasks/scraping.py` | `test_sabotagem_sigaa.py` (falha não engolida, cache preservado) |
| `app/tasks/cardapio.py` | `test_sabotagem_ru.py` (falha não engolida, cache preservado) |
| `app/tasks/logging_signals.py` | os dois arquivos (tipo `fonte` ou `interna` em cada cenário) |
| `app/domain/execucoes.py` | os dois arquivos (a falha aparece na listagem da API) |

A sabotagem achou três falhas silenciosas no SIGAA, corrigidas no commit `f5a8fe1`:

- o timeout do Playwright ia para o log como falha interna;
- a sessão expirada em todas as unidades era registrada como sucesso com zero turmas;
- o layout novo também era registrado como sucesso com zero turmas, contra o RNF05.

## Rastreabilidade

- **PRs:** a abrir, da `R2-joao` para a `dev`.
- **Issues:** [#206](https://github.com/unb-mds/2026-2-Cerradinho-API/issues/206) (mutação e sabotagem, Sprint 9) e [#214](https://github.com/unb-mds/2026-2-Cerradinho-API/issues/214) (metas do RNF09, Sprint 10).
- **Testes:** [`tests/sabotagem/`](https://github.com/unb-mds/2026-2-Cerradinho-API/tree/dev/backend/tests/sabotagem), [`tests/scrapers/test_cardapio_parser_posicional.py`](https://github.com/unb-mds/2026-2-Cerradinho-API/blob/dev/backend/tests/scrapers/test_cardapio_parser_posicional.py), [`tests/domain/test_execucoes.py`](https://github.com/unb-mds/2026-2-Cerradinho-API/blob/dev/backend/tests/domain/test_execucoes.py) e os testes marcados como "escritos a partir dos mutantes sobreviventes" em `tests/domain/` e `tests/scrapers/`.
- **Observação:** a cobertura é medida no passo de testes do CI, sem mínimo exigido. A mutação roda sob demanda, pelo workflow **Mutação** ou por `python -m scripts.mutacao`. Ao mudar um módulo crítico, rode o script para ele antes do merge.
