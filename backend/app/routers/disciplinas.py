from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.domain.disciplinas import listar_turmas
from app.schemas.disciplina import Turma

router = APIRouter(prefix="/disciplinas", tags=["disciplinas"])


@router.get(
    "",
    response_model=list[Turma],
    summary="Listar disciplinas",
    description=(
        "Lista as turmas ofertadas no período, com professores, horários, sala e vagas. "
        "Os dados vêm do SIGAA público e são atualizados semanalmente, aos domingos."
    ),
)
def listar_disciplinas(db: Session = Depends(get_db)) -> list[Turma]:
    return listar_turmas(db)
