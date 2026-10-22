"""Leitura das salas gravadas pelo domínio de disciplinas (RF05, RF17).

Não existe fonte própria de salas: a tabela é preenchida por
`app/domain/disciplinas.py` a partir da sala de cada turma capturada.
"""

import logging
import re

from sqlalchemy.orm import Session

from app.models import Horario, Sala, Turma
from app.schemas.api.sala import Espaco

logger = logging.getLogger(__name__)

# Código de horário do SIGAA: um ou mais dígitos de dia (2=segunda ... 7=sábado),
# um turno (M/T/N) e um ou mais dígitos de aula, ex. "246T23" (seg/qua/sex, tarde,
# aulas 2 e 3). Dia "1" (domingo) nunca aparece — não há aula nesse dia.
_PADRAO_CODIGO_HORARIO = re.compile(r"^([2-7]+)([MTN])([0-9]+)$")

_DIA_PARA_DIGITO = {
    "domingo": "1",
    "segunda": "2",
    "terca": "3",
    "quarta": "4",
    "quinta": "5",
    "sexta": "6",
    "sabado": "7",
}

# Início de cada aula, extraído das descrições reais de horário do SIGAA
# (ex. "6T2345" -> "Sexta-feira 14:00 às 17:50"): aulas de 55 min, com 10 min
# de intervalo entre a 2ª e a 3ª aula de cada turno — exceto na virada de
# turno (M5->T1 e T6->N1), que é direto, sem intervalo.
_INICIO_AULA: dict[str, dict[str, str]] = {
    "M": {"1": "08:00", "2": "08:55", "3": "10:00", "4": "10:55", "5": "12:00"},
    "T": {"1": "12:55", "2": "14:00", "3": "14:55", "4": "16:00", "5": "16:55", "6": "18:00"},
    "N": {"1": "18:55", "2": "20:00", "3": "20:55"},
}


_TURNO_AULA_POR_HORARIO: dict[str, tuple[str, str]] = {
    inicio: (turno, aula) for turno, aulas in _INICIO_AULA.items() for aula, inicio in aulas.items()
}


def _localizar_turno_aula(horario: str) -> tuple[str, str] | None:
    return _TURNO_AULA_POR_HORARIO.get(horario)


def _decompor_codigo_horario(codigo: str) -> tuple[set[str], str, set[str]] | None:
    match = _PADRAO_CODIGO_HORARIO.match(codigo)
    if match is None:
        return None
    dias, turno, aulas = match.groups()
    return set(dias), turno, set(aulas)


def listar_salas(session: Session) -> list[Espaco]:
    salas = session.query(Sala).order_by(Sala.predio, Sala.nome).all()
    return [Espaco(id=sala.id, nome=sala.nome, predio=sala.predio) for sala in salas]


def listar_salas_vazias(session: Session, dia: str, horario: str) -> list[Espaco]:
    """Salas sem nenhuma turma cadastrada no dia/horário dados. `dia` é um dos
    nomes de `_DIA_PARA_DIGITO`; `horario` é o início de uma aula, "HH:MM"
    (ex. "14:00"). Dia ou horário fora da grade de aulas (sem turma possível)
    devolve todas as salas, em vez de erro."""
    dia_digito = _DIA_PARA_DIGITO.get(dia)
    turno_aula = _localizar_turno_aula(horario)

    ocupadas: set[int] = set()
    if dia_digito is not None and turno_aula is not None:
        turno, aula = turno_aula
        linhas = (
            session.query(Horario.codigo, Turma.sala_id)
            .join(Turma, Horario.turma_id == Turma.id)
            .filter(Turma.sala_id.isnot(None))
            .all()
        )
        for codigo, sala_id in linhas:
            decomposto = _decompor_codigo_horario(codigo)
            if decomposto is None:
                logger.warning("Código de horário fora do padrão esperado, ignorado: %r", codigo)
                continue
            dias, turno_codigo, aulas = decomposto
            if turno_codigo == turno and dia_digito in dias and aula in aulas:
                ocupadas.add(sala_id)

    salas = (
        session.query(Sala)
        .filter(Sala.id.notin_(ocupadas))
        .order_by(Sala.predio, Sala.nome)
        .all()
    )
    return [Espaco(id=sala.id, nome=sala.nome, predio=sala.predio) for sala in salas]
