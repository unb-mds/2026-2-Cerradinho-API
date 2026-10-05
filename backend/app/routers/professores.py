from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.domain.professores import listar_professores
from app.schemas.api.professor import Docente

router = APIRouter(prefix="/professores", tags=["professores"])


@router.get(
    "",
    response_model=list[Docente],
    summary="Listar professores",
    description=(
        "Lista os docentes que dão aula no período, em ordem alfabética, com os códigos "
        "das disciplinas de cada um. Os dados vêm das turmas do SIGAA público, "
        "atualizadas semanalmente, aos domingos."
    ),
)
def listar_docentes(db: Session = Depends(get_db)) -> list[Docente]:
    return listar_professores(db)
