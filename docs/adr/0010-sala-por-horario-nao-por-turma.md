# ADR 0010 — Sala por horário, não por turma

## Status
Aceito

## Contexto
O SIGAA pode listar mais de uma sala pra mesma turma, quando ela usa salas diferentes em dias diferentes (ex. `"FCTE - S1 / MOCAP"`, segunda na S1 e quarta na MOCAP). O modelo original (`Turma.sala_id`, uma sala só por turma) não tinha onde guardar essa distinção: a sala ficava associada à turma inteira, e o RF17 (salas vazias) marcava as duas salas como ocupadas nos dois dias, mesmo a turma só usando uma por vez.

## Decisão
A sala passa a viver em `Horario.sala_id`, não em `Turma.sala_id`. Quando uma turma só usa uma sala (o caso comum), todo horário aponta pra ela — equivalente ao modelo antigo. Quando usa mais de uma, `app/domain/disciplinas.py` desdobra o horário combinado (ex. `"24M5 24T1"`) em um horário por dia, casando cada dia com a sala na mesma posição da lista (as salas vêm na mesma ordem dos dias). Quando o número de salas não bate com o de dias distintos, não arrisca casar errado: cada sala fica associada a todos os horários da turma (igual ao comportamento antigo, só que repetido por sala).

O contrato público (`GET /v1/disciplinas`) continua expondo uma sala só por turma — `app/domain/disciplinas.py` reconstrói essa string a partir dos horários da turma na leitura, pra não quebrar quem já consome a API.

## Alternativas descartadas
- **Manter sala na turma e guardar as várias salas como texto bruto:** resolveria a duplicação de sala no `GET /v1/salas`, mas não corrigiria o RF17 — ainda não haveria como saber qual sala vale em qual dia.
- **Pedir confirmação humana pra cada turma multi-sala:** inviável em escala (dezenas de turmas por raspagem) e o SIGAA já dá o suficiente pra inferir a correspondência na maioria dos casos.

## Consequências
- Turma com sala por dia agora reflete corretamente no RF17: cada sala só aparece ocupada no dia em que é usada.
- Quando o pareamento sala×dia é ambíguo (contagem não bate), o RF17 prefere superestimar a ocupação (marcar as duas salas como ocupadas) a arriscar um pareamento errado.
- A migration `0005` move a referência existente sem desdobrar dados históricos por dia — isso só passa a valer a partir da próxima raspagem de cada turma (RF15 regrava os horários do zero a cada execução).
