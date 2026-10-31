from fastapi import APIRouter, Depends, HTTPException, Path, Query, Response
from sqlalchemy.orm import Session

from app.core.cache import TTL_SEMANAL, resposta_cacheada
from app.core.database import get_db
from app.domain.professores import listar_professores, obter_agenda_professor
from app.schemas.api.agenda import Agenda
from app.schemas.api.professor import Docente

router = APIRouter(prefix="/professores", tags=["professores"])


@router.get(
    "",
    response_model=list[Docente],
    summary="Listar professores",
    description=(
        "Lista os docentes que dão aula no período, em ordem alfabética, com os códigos "
        "das disciplinas de cada um. Aceita busca parcial por nome em `nome`, sem diferenciar "
        "maiúsculas/minúsculas ou acentos. Os dados vêm das turmas do SIGAA público, "
        "atualizadas semanalmente, aos domingos."
    ),
)
def listar_docentes(
    nome: str | None = Query(default=None, description="Busca parcial por nome, normalizada"),
    db: Session = Depends(get_db),
) -> list[Docente] | Response:
    if nome:
        return listar_professores(db, nome)
    return resposta_cacheada("cache:v1:professores", TTL_SEMANAL, lambda: listar_professores(db), list[Docente])


@router.get(
    "/{professor_id}/agenda",
    response_model=Agenda,
    summary="Agenda semanal do professor",
    description=(
        "Lista as turmas do docente no período, com o horário decomposto em dia/início/fim e "
        "a sala de cada bloco de aula. 404 se o docente não existir."
    ),
    responses={404: {"description": "Professor não encontrado"}},
)
def obter_agenda(
    # limitado ao alcance de Integer (coluna de professores.id) - fora
    # disso o banco estoura antes de dar a chance de responder 404.
    professor_id: int = Path(gt=0, le=2_147_483_647),
    db: Session = Depends(get_db),
) -> Agenda:
    agenda = obter_agenda_professor(db, professor_id)
    if agenda is None:
        raise HTTPException(status_code=404, detail="Professor não encontrado")
    return agenda
