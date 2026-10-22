from enum import Enum

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.domain.salas import listar_salas, listar_salas_vazias
from app.schemas.api.sala import Espaco

router = APIRouter(prefix="/salas", tags=["salas"])


class DiaSemana(str, Enum):
    domingo = "domingo"
    segunda = "segunda"
    terca = "terca"
    quarta = "quarta"
    quinta = "quinta"
    sexta = "sexta"
    sabado = "sabado"


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


@router.get(
    "/vazias",
    response_model=list[Espaco],
    summary="Listar salas vazias por dia e horário",
    description=(
        "Lista as salas sem nenhuma turma cadastrada no dia e horário dados (RF17). "
        "`horario` é o início de uma aula, no formato \"HH:MM\" (ex.: \"14:00\"). "
        "\"Vazia\" é só \"sem aula cadastrada via RF01\" — não reflete reserva informal, "
        "evento ou uso fora da grade de disciplinas."
    ),
)
def listar_espacos_vazios(
    dia: DiaSemana = Query(description="Dia da semana"),
    horario: str = Query(
        pattern=r"^\d{2}:\d{2}$",
        description="Início de uma aula, no formato HH:MM",
        examples=["14:00"],
    ),
    db: Session = Depends(get_db),
) -> list[Espaco]:
    return listar_salas_vazias(db, dia.value, horario)
