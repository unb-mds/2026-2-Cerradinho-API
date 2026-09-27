from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.domain.salas import listar_salas
from app.schemas.api.sala import Sala

router = APIRouter(prefix="/salas", tags=["salas"])


@router.get("", response_model=list[Sala])
def listar_espacos(db: Session = Depends(get_db)) -> list[Sala]:
    return listar_salas(db)
