# ADR 0006 — Salas derivadas das turmas

## Status
Aceito

## Contexto
Não existe fonte pública com a lista de salas e prédios da UnB. As turmas do SIGAA, porém, trazem a sala de cada aula no formato `PRÉDIO - SALA`.

## Decisão
Salas e prédios são extraídos das turmas pelo domínio de disciplinas (`app/domain/disciplinas.py`), que separa prédio e nome e faz get-or-create da sala. Não há scraper próprio de salas.

## Alternativas descartadas
- **Cadastro manual de salas:** exigiria manutenção contínua pelo time e sairia de sincronia com o SIGAA.

## Consequências
- Só aparecem salas que têm alguma aula no período. Salas sem turma não existem para a API.
- As salas vazias (RF17) refletem apenas as aulas cadastradas, não reservas informais.
