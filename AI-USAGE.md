# Registro de uso de IA — Cerradinho

Conforme a política de uso de IA da disciplina (MDS 2026/2): o uso de assistentes e agentes de IA é **esperado, não tolerado**, desde que registrado. Este arquivo documenta onde e como IA foi usada no projeto.

**Não é permitido uso de IA em**: arguições individuais, quizzes, avaliação por pares, ensaio de reflexão crítica. Esses instrumentos avaliam o que cada pessoa entende individualmente.

**É esperado e deve ser registrado em**: implementação, testes, documentação, exploração de bibliotecas, refatoração.

## Formato de registro

Cada entrada deve conter: data, pessoa, ferramenta usada, o que foi pedido, o que foi aceito/rejeitado/ajustado.

## Registros

### Release 1

| Data | Pessoa | Ferramenta | O que foi feito | Aceito/ajustado/rejeitado |
|---|---|---|---|---|
| 13/09/2026 | Gabriel | Claude Code | Auxícilio no schema inicial SQLAlchemy (Professor, Sala, Disciplina, Turma, Horario, Cardapio, ajustado pra bater com o contrato de dados real do scraper de RF01 já mergeado), e correção de um bug pré-existente em `backend/pytest.ini` (`pythonpath` apontava pra um caminho que não existia) | a primeira versão modelou Disciplina/Turma como uma única tabela; após puxar o `origin/dev` e o schema já mergeado do Vitor, foi refeita como Disciplina + Turma separadas |

| 13/09/2026 | Vitor | Claude Code | Camada `app/domain/disciplinas.py` ligando o parser de RF01 (`app/schemas/disciplina.py`) aos models de banco do Gabriel: get-or-create de Disciplina/Sala/Professor, split de "PRÉDIO - SALA" e upsert de Turma+Horario pela chave natural (disciplina, numero, ano_periodo) pra não duplicar linha quando o scraper reagendar. Testes em `tests/domain/test_disciplinas.py` cobrindo criação, atualização sem duplicar, troca de professores/horários sem acumular órfão, e reaproveitamento de Sala/Professor entre turmas. Também corrigido bug pré-existente em `backend/pytest.ini` (chave `pythonpath` duplicada, que quebrava toda a suíte) | Aceito sem ajuste |

### Release 2

| Data | Pessoa | Ferramenta | O que foi feito | Aceito/ajustado/rejeitado |
| ---- | ------ | ---------- | --------------- | ------------------------- |
|      |        |            |                 |                           |

## Observações gerais

- Código gerado por IA passa pela mesma revisão de PR que qualquer outro código (ver `PROCESSO.md`)
- Testes gerados por IA são revisados quanto a asserção real (não aceitar teste que só verifica "não lançou exceção")
- Dependências sugeridas por IA são conferidas antes de instalar (existe de verdade, é mantida, não é maliciosa)
