"""Contagens agregadas de disciplinas, professores e salas (RF20).

Só um recorte de RF01/RF04/RF05 - não há dado novo nenhum, só a contagem
do que RF01 a RF05 já capturam.
"""

from sqlalchemy.orm import Session

from app.models import Disciplina, Professor, Sala, Turma
from app.schemas.api.resumo import Resumo


def obter_resumo(session: Session) -> Resumo:
    return Resumo(
        turmas=session.query(Turma).count(),
        disciplinas=session.query(Disciplina).count(),
        professores=session.query(Professor).count(),
        salas=session.query(Sala).count(),
    )
