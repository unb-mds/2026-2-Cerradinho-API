from fastapi import APIRouter, Depends, Query, Response
from sqlalchemy.orm import Session

from app.core.cache import TTL_SEMANAL, resposta_cacheada
from app.core.database import get_db
from app.domain.disciplinas import listar_turmas, listar_turmas_filtradas
from app.schemas.disciplina import Turma

router = APIRouter(prefix="/disciplinas", tags=["disciplinas"])


@router.get(
    "",
    response_model=list[Turma],
    summary="Listar disciplinas",
    description=(
        "Lista as turmas ofertadas no período, com professores, horários, sala e vagas. Aceita "
        "busca parcial em `busca` (código ou nome da disciplina, nome de professor - sem "
        "diferenciar maiúsculas/minúsculas ou acentos), filtro por `departamento` (prefixo do "
        'código, ex. "FGA") e paginação com `limite`/`offset` (o total depois do filtro vem no '
        "cabeçalho `X-Total-Count`). Sem nenhum parâmetro, devolve todas as turmas, como sempre. "
        "Os dados vêm do SIGAA público e são atualizados semanalmente, aos domingos."
    ),
)
def listar_disciplinas(
    response: Response,
    busca: str | None = Query(default=None, description="Busca parcial por código, disciplina ou professor"),
    departamento: str | None = Query(default=None, description='Prefixo do código da disciplina, ex. "FGA"'),
    limite: int | None = Query(default=None, ge=1, le=1000, description="Máximo de turmas a devolver"),
    offset: int = Query(default=0, ge=0, description="Quantas turmas pular, pra paginar"),
    db: Session = Depends(get_db),
) -> list[Turma] | Response:
    if busca or departamento or limite is not None or offset:
        turmas, total = listar_turmas_filtradas(
            db, busca=busca, departamento=departamento, limite=limite, offset=offset
        )
        response.headers["X-Total-Count"] = str(total)
        return turmas
    return resposta_cacheada("cache:v1:disciplinas", TTL_SEMANAL, lambda: listar_turmas(db), list[Turma])

