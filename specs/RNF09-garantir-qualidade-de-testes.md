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

Medição de 19/10/2026 ([#146](https://github.com/unb-mds/2026-2-Cerradinho-API/issues/146)), no commit `ea31fab` (`dev` com o parser novo do RU do #145).

| Medição | Cobertura | Meta |
|---|---|---|
| Suíte completa (`pytest --cov=app`, com contrato e integração num Postgres) | **81%** (613 de 754 linhas) | ≥ 90% |
| Passo de testes do CI (sem contrato e integração) | **81%** (610 de 754 linhas) | ≥ 90% |

Faltam cerca de 66 linhas cobertas para chegar aos 90%.

### Módulos críticos

Critério: módulos que, se quebrarem em silêncio, gravam dado errado no banco ou param a coleta. São eles que entram nas metas de mutação (≥ 50%) e de sabotagem (100%).

| Módulo | Por que é crítico | Cobertura |
|---|---|---|
| `app/scrapers/disciplinas/parser.py` | Transforma o HTML do SIGAA nas turmas que vão para o banco | 70% |
| `app/scrapers/cardapio/parser.py` | Transforma o PDF do RU nos itens de cardápio | 91% |
| `app/domain/disciplinas.py` | Grava turmas, disciplinas, professores, salas e horários (get-or-create e upsert) | 99% |
| `app/domain/cardapio.py` | Grava e consulta o cardápio por data | 100% |
| `app/tasks/scraping.py` | Task agendada que raspa e persiste as disciplinas | 100% |
| `app/tasks/cardapio.py` | Task agendada que baixa, lê e persiste o cardápio | 35% |
| `app/tasks/logging_signals.py` | Registra sucesso e falha de cada execução (RF16) | 50% (testes em revisão no #143) |
| `app/domain/execucoes.py` | Grava e lista o histórico de execuções (RF16) | 100% |

Fora da lista: routers e schemas, cobertos pelos testes de contrato (RNF04), e models, cobertos pelos testes de domínio e de integração.

### Onde estão as lacunas

| Módulo | Cobertura | Motivo |
|---|---|---|
| `app/scrapers/disciplinas/scraper.py` | 26% | Navegação no SIGAA com Playwright; os testes usam HTML salvo e não passam por aqui |
| `app/scrapers/cardapio/scraper.py` | 38% | Download da página e do PDF do RU, sem teste com dublê de rede |
| `app/scrapers/disciplinas/__init__.py` e `app/scrapers/cardapio/__init__.py` | 40% e 44% | Funções que juntam scraper e parser, sem teste |
| `app/core/database.py` | 64% | `get_db`, sempre substituído nos testes |

Os módulos de scraper fazem acesso de rede e de navegador, então entram na meta de sabotagem (fonte fora do ar, sessão expirada, layout mudado), simulada com dublês, e não na de mutação.

## Rastreabilidade

- **PRs:** nenhum ainda.
- **Testes:** nenhum ainda.
- **Observação:** A cobertura é medida no CI, sem mínimo exigido; a medição atual e os módulos críticos estão em "Situação atual". Mutação e sabotagem ainda não foram implementadas.
