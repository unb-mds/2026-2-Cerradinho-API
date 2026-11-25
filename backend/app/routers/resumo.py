from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session

from app.core.cache import TTL_SEMANAL, resposta_cacheada
from app.core.database import get_db
from app.domain.resumo import obter_resumo
from app.schemas.api.resumo import Resumo

router = APIRouter(prefix="/resumo", tags=["resumo"])


@router.get(
    "",
    response_model=Resumo,
    summary="Resumo com as contagens",
    description=(
        "Total de turmas, disciplinas, professores e salas, sem a lista inteira - pra um "
        "dashboard mostrar um número sem baixar `GET /v1/disciplinas` por completo."
    ),
)
def obter_resumo_geral(db: Session = Depends(get_db)) -> Resumo | Response:
    return resposta_cacheada("cache:v1:resumo", TTL_SEMANAL, lambda: obter_resumo(db), Resumo)
