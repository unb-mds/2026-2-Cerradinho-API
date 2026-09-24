from datetime import date

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.domain.cardapio import listar_cardapio_semana
from app.schemas.cardapio import ItemCardapio

router = APIRouter(prefix="/cardapio", tags=["cardapio"])


@router.get("/semana", response_model=list[ItemCardapio])
def listar_cardapio_da_semana(
    data_inicio: date = Query(default_factory=date.today, description="Primeiro dia da semana (default: hoje)"),
    db: Session = Depends(get_db),
) -> list[ItemCardapio]:
    return listar_cardapio_semana(db, data_inicio)
