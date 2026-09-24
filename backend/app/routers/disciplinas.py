from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.domain.disciplinas import listar_turmas
from app.schemas.disciplina import Turma

router = APIRouter(prefix="/disciplinas", tags=["disciplinas"])


@router.get("", response_model=list[Turma])
def listar_disciplinas(db: Session = Depends(get_db)) -> list[Turma]:
    return listar_turmas(db)
