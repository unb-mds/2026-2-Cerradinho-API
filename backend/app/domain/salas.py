"""Leitura das salas gravadas pelo domínio de disciplinas (RF05).

Não existe fonte própria de salas: a tabela é preenchida por
`app/domain/disciplinas.py` a partir da sala de cada turma capturada.
"""

from sqlalchemy.orm import Session

from app.models import Sala
from app.schemas.api.sala import Sala as SalaResposta


def listar_salas(session: Session) -> list[SalaResposta]:
    salas = session.query(Sala).order_by(Sala.predio, Sala.nome).all()
    return [SalaResposta(id=sala.id, nome=sala.nome, predio=sala.predio) for sala in salas]
