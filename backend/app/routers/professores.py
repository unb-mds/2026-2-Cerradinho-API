from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.domain.professores import listar_professores
from app.schemas.api.professor import Professor

router = APIRouter(prefix="/professores", tags=["professores"])


@router.get("", response_model=list[Professor])
def listar_docentes(db: Session = Depends(get_db)) -> list[Professor]:
    return listar_professores(db)
