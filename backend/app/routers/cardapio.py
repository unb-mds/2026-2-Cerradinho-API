from datetime import date

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.domain.cardapio import listar_cardapio_semana
from app.schemas.cardapio import ItemCardapio

router = APIRouter(prefix="/cardapio", tags=["cardapio"])


@router.get(
    "/semana",
    response_model=list[ItemCardapio],
    summary="Cardápio da semana",
    description=(
        "Devolve os itens do cardápio do RU (campus Darcy Ribeiro) de sete dias a partir "
        "de `data_inicio`, separados por refeição e categoria. O cardápio é atualizado "
        "diariamente a partir do PDF semanal publicado pelo RU."
    ),
)
def listar_cardapio_da_semana(
    data_inicio: date = Query(default_factory=date.today, description="Primeiro dia da semana (default: hoje)"),
    db: Session = Depends(get_db),
) -> list[ItemCardapio]:
    return listar_cardapio_semana(db, data_inicio)
