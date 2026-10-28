from enum import Enum

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.cache import TTL_SEMANAL, resposta_cacheada
from app.core.database import get_db
from app.domain.salas import DIA_PARA_DIGITO, listar_salas, listar_salas_vazias
from app.schemas.api.sala import Espaco

router = APIRouter(prefix="/salas", tags=["salas"])

# Gerado a partir de DIA_PARA_DIGITO pra não duplicar os nomes dos dias da semana.
DiaSemana = Enum("DiaSemana", {dia: dia for dia in DIA_PARA_DIGITO})


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
    return resposta_cacheada("cache:v1:salas", TTL_SEMANAL, lambda: listar_salas(db), list[Espaco])


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
        pattern=r"^[0-9]{2}:[0-9]{2}$",
        description="Início de uma aula, no formato HH:MM",
        examples=["14:00"],
    ),
    db: Session = Depends(get_db),
) -> list[Espaco]:
    # dia/horario são obrigatórios e mudam o resultado - sem entrar na chave,
    # a primeira consulta ficava em cache pra qualquer dia/horário seguinte.
    chave = f"cache:v1:salas:vazias:{dia.value}:{horario}"
    return resposta_cacheada(chave, TTL_SEMANAL, lambda: listar_salas_vazias(db, dia.value, horario), list[Espaco])
