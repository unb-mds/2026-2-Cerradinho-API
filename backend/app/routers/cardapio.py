from datetime import date

from fastapi import APIRouter, Depends, Query, Response
from sqlalchemy.orm import Session

from app.core.cache import TTL_DIARIO, resposta_cacheada
from app.core.database import get_db
from app.domain.cardapio import listar_cardapio_semana
from app.schemas.api.cardapio import CardapioSemana

router = APIRouter(prefix="/cardapio", tags=["cardapio"])


@router.get(
    "/semana",
    response_model=CardapioSemana,
    summary="Cardápio da semana",
    description=(
        "Devolve o cardápio do RU (campus Darcy Ribeiro) dos sete dias a partir de "
        "`data_inicio`, agrupado por dia e por refeição (RF19). A resposta sempre tem os sete "
        "dias. Um dia sem cardápio coletado vem com `publicado` falso e as refeições vazias. "
        "O cardápio é atualizado diariamente a partir do PDF semanal publicado pelo RU."
    ),
)
def listar_cardapio_da_semana(
    data_inicio: date = Query(default_factory=date.today, description="Primeiro dia da semana (default: hoje)"),
    db: Session = Depends(get_db),
) -> CardapioSemana | Response:
    chave = f"cache:v1:cardapio:semana:{data_inicio.isoformat()}"
    return resposta_cacheada(chave, TTL_DIARIO, lambda: listar_cardapio_semana(db, data_inicio), CardapioSemana)
