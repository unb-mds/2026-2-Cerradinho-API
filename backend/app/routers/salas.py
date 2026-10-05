from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.domain.salas import listar_salas
from app.schemas.api.sala import Espaco

router = APIRouter(prefix="/salas", tags=["salas"])


@router.get(
    "",
    response_model=list[Espaco],
    summary="Listar salas",
    description=(
        "Lista as salas que têm aula no período, ordenadas por prédio e nome. Não existe "
        "fonte pública própria de salas: elas saem das turmas do SIGAA, atualizadas "
        "semanalmente, aos domingos."
    ),
)
def listar_espacos(db: Session = Depends(get_db)) -> list[Espaco]:
    return listar_salas(db)
