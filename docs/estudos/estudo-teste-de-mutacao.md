# Guia de Estudo: Teste de Mutação

Base para a meta de mutação do RNF09 (qualidade dos testes), planejada para as Sprints 9 e 10.

## 1. O problema que o teste de mutação resolve

Cobertura de código mede quais linhas **rodaram** durante os testes, não quais linhas foram **verificadas**. Um teste sem nenhum `assert` cobre 100% da função que chama e não pega bug nenhum.

O teste de mutação mede outra coisa: **se os testes percebem quando o código muda**. A ferramenta faz pequenas alterações no código (os *mutantes*), roda os testes contra cada uma e conta quantas foram detectadas.

| Resultado | Significado |
|---|---|
| Mutante **morto** | Algum teste falhou com a alteração. Bom: o teste protege aquele trecho |
| Mutante **sobrevivente** | Todos os testes passaram mesmo com o código errado. É uma lacuna de teste, ou um mutante equivalente (seção 4) |

O **score de mutação** é a porcentagem de mutantes mortos.

É a versão automática da sabotagem que já fazemos à mão no projeto: quebrar o código de propósito e confirmar que o teste falha.

## 2. Exemplos de mutação

| Operador | Original | Mutante |
|---|---|---|
| Troca de comparação | `if a == b:` | `if a <= b:` |
| Troca de número | `total // 60` | `total // 61` |
| Troca de operador lógico | `if a and b:` | `if a or b:` |
| Troca de controle de fluxo | `break` | `continue` |
| Troca de booleano | `return True` | `return False` |

## 3. Ferramentas para Python

| | mutmut | cosmic-ray |
|---|---|---|
| Versão testada | 3.8.1 | 8.7.0 |
| Windows nativo | **Não.** Ao rodar, pede para usar o WSL | **Sim** |
| Linux (CI) | Sim | Sim |
| Configuração | Seção `[tool.mutmut]` no `pyproject.toml` | Arquivo `.toml` próprio |
| Resultados | Pasta `mutants/` e `mutmut results` | Banco SQLite e `cr-report` |
| Uso típico | Simples, pensado para rodar direto no projeto | Mais configurável, com sessões que podem ser retomadas |

Testei os dois em 03/11/2026 numa cópia do backend.

### Pegadinha do cosmic-ray no Windows

O `test-command` com `python -m pytest` falhou no baseline, sem mensagem de erro. O Windows resolve `python` para o Python do sistema, que não tem o pytest, mesmo com o venv ativo.

A solução é usar o caminho completo do Python do venv no `test-command`. Por isso, todo mutante aparecia como "morto" na primeira tentativa: o teste falhava sempre. **Sempre confira o baseline antes de confiar no score.**

### Configuração usada

```toml
[cosmic-ray]
module-path = "app/domain/salas.py"
timeout = 60.0
excluded-modules = []
test-command = "C:/caminho/do/venv/Scripts/python.exe -m pytest -x -q tests/domain/test_salas.py tests/routers/test_salas_router.py"

[cosmic-ray.distributor]
name = "local"
```

```bash
cosmic-ray init cr.toml cr.sqlite     # gera os mutantes
cosmic-ray baseline cr.toml           # confere que os testes passam sem mutação
cosmic-ray exec cr.toml cr.sqlite     # roda os testes contra cada mutante
cr-report cr.sqlite                   # resumo e mutantes sobreviventes
```

## 4. Resultado do teste em `app/domain/salas.py`

**128 mutantes, 7 sobreviventes, score de 94,5%, em 4 min 45 s.** Cada mutante roda a suíte escolhida inteira, por isso o tempo cresce rápido.

Os sobreviventes caem em três tipos, e cada um pede uma resposta diferente.

**Lacuna real de teste.** Na linha 128, trocar `turno_codigo == turno` por `<=` ou `>=` não faz nenhum teste falhar. Nenhum teste tem uma sala ocupada na mesma aula e no mesmo dia, mas em **outro turno** (por exemplo, aula 1 da manhã e aula 1 da tarde). Com o mutante, uma sala com aula de manhã apareceria como ocupada à tarde. A resposta é escrever esse teste.

**Mutante equivalente.** Trocar `==` por `is` em comparação de strings curtas e trocar `break` por `continue` no fim de um laço não mudam o comportamento. Nenhum teste consegue matar esses mutantes, porque o código continua certo. Por isso, a meta de mutação não pode ser 100%.

**Código testado em outro arquivo.** O mutante em `_fim_aula` (`total // 60` → `total // 61`) sobreviveu porque quem testa essa função são os testes da agenda do professor, que não entraram no `test-command`. O score depende de quais testes rodam, não só do módulo.

## 5. Como aplicar no Cerradinho (Sprints 9 e 10)

- **Ferramenta: cosmic-ray.** É a única que roda nos dois ambientes do time (Windows local e Linux no CI). O mutmut só serviria no CI ou no WSL.
- **Escopo: os módulos críticos**, e não o projeto inteiro. São os oito módulos listados na "Situação atual" do RNF09 (parsers, domínio e tasks). Rodar tudo levaria horas.
- **Onde rodar:** localmente, ou num workflow separado acionado manualmente (`workflow_dispatch`). Não deve rodar em todo push, porque é lento demais para ser porta de qualidade.
- **Meta:** definir por módulo depois da primeira rodada, descontando os mutantes equivalentes. Um score de 80% nos módulos críticos é um ponto de partida razoável.
- **Primeira ação:** o teste de turno diferente em salas vazias (lacuna da linha 128).

## Referências

- cosmic-ray: https://cosmic-ray.readthedocs.io
- mutmut: https://mutmut.readthedocs.io
- Issue do mutmut sobre o suporte a Windows: https://github.com/boxed/mutmut/issues/397
