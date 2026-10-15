from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.domain.execucoes import listar_execucoes
from app.schemas.api.execucao import Execucao

router = APIRouter(prefix="/execucoes", tags=["execucoes"])

@router.get("", response_model=list[Execucao],
            summary="Listar execuções recentes dos scrapers",
            description=("Histórico de execuções agendadas, da mais recente pra mais antiga."),
            )

def listar(limite: int = Query(default = 50, ge = 1,le = 200, description="Número máximo de execuções a retornar."),
    db: Session = Depends(get_db)) -> list[Execucao]:
    return listar_execucoes(db, limite)