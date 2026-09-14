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
| 13/09/2026 | Gabriel | Claude Code | Schema inicial SQLAlchemy (Professor, Sala, Disciplina, Turma, Horario, Cardapio — ajustado pra bater com o contrato de dados real do scraper de RF01 já mergeado), config de banco, migração inicial via Alembic, docker-compose.yml com Postgres, testes unitários dos models, ADR 001 (base técnica do backend), e correção de um bug pré-existente em `backend/pytest.ini` (`pythonpath` apontava pra um caminho que não existia) | Aceito com retrabalho: a primeira versão modelou Disciplina/Turma como uma única tabela; após puxar o `origin/dev` e ler `.claude/skills/db-model` e o schema Pydantic já mergeado do Vitor, foi refeita como Disciplina + Turma separadas, com professores (N:N) e horários (1:N) por turma |

### Release 2

| Data | Pessoa | Ferramenta | O que foi feito | Aceito/ajustado/rejeitado |
| ---- | ------ | ---------- | --------------- | ------------------------- |
|      |        |            |                 |                           |

## Observações gerais

- Código gerado por IA passa pela mesma revisão de PR que qualquer outro código (ver `PROCESSO.md`)
- Testes gerados por IA são revisados quanto a asserção real (não aceitar teste que só verifica "não lançou exceção")
- Dependências sugeridas por IA são conferidas antes de instalar (existe de verdade, é mantida, não é maliciosa)
