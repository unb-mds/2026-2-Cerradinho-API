"""Leitura das salas gravadas pelo domínio de disciplinas (RF05, RF17).

Não existe fonte própria de salas: a tabela é preenchida por
`app/domain/disciplinas.py` a partir da sala de cada turma capturada.
"""

from collections import defaultdict

from sqlalchemy.orm import Session

from app.domain.disciplinas import decompor_codigo_horario
from app.models import Horario, Sala
from app.schemas.api.sala import Espaco

DIA_PARA_DIGITO = {
    "domingo": "1",
    "segunda": "2",
    "terca": "3",
    "quarta": "4",
    "quinta": "5",
    "sexta": "6",
    "sabado": "7",
}

# Início de cada aula, extraído das descrições reais de horário do SIGAA
# (ex. "6T2345" -> "Sexta-feira 14:00 às 17:50"): aulas de manhã/tarde com
# 55 min e aulas de noite com 50 min (ver _DURACAO_AULA_MINUTOS), com 10 min
# de intervalo entre a 2ª e a 3ª aula de cada turno — exceto na virada
# M5->T1, que é direto, sem intervalo. T6->N1 tem 5 min de intervalo.
# Confirmado contra turma real (Administração, Contábeis, Computação,
# Direito, Educação, 2026.2): "24N12" -> 19:00 às 20:40, "24N34" ->
# 20:50 às 22:30, "6N1234" -> 19:00 às 22:30. Só o início de N2 (19:50) foi
# deduzido do fim de N1 (nenhuma turma observada começa nela).
_INICIO_AULA: dict[str, dict[str, str]] = {
    "M": {"1": "08:00", "2": "08:55", "3": "10:00", "4": "10:55", "5": "12:00"},
    "T": {"1": "12:55", "2": "14:00", "3": "14:55", "4": "16:00", "5": "16:55", "6": "18:00"},
    "N": {"1": "19:00", "2": "19:50", "3": "20:50", "4": "21:40"},
}
_DURACAO_AULA_MINUTOS: dict[str, int] = {"M": 55, "T": 55, "N": 50}


_TURNO_AULA_POR_HORARIO: dict[str, tuple[str, str]] = {
    inicio: (turno, aula) for turno, aulas in _INICIO_AULA.items() for aula, inicio in aulas.items()
}

# Ordem cronológica das aulas (pra agrupar aulas consecutivas num bloco só,
# ex. "6T2345" -> um bloco de 14:00 às 17:50, não 4 blocos separados -
# ver RF18, horario_para_intervalos_por_dia).
_ORDEM_AULAS: list[tuple[str, str]] = [
    (turno, aula) for turno in ("M", "T", "N") for aula in sorted(_INICIO_AULA[turno], key=int)
]
_POSICAO_AULA: dict[tuple[str, str], int] = {par: i for i, par in enumerate(_ORDEM_AULAS)}


def _localizar_turno_aula(horario: str) -> tuple[str, str] | None:
    return _TURNO_AULA_POR_HORARIO.get(horario)


def _fim_aula(turno: str, inicio: str) -> str:
    horas, minutos = (int(parte) for parte in inicio.split(":"))
    total = horas * 60 + minutos + _DURACAO_AULA_MINUTOS[turno]
    return f"{total // 60:02d}:{total % 60:02d}"


def _intervalos_do_dia(pares_turno_aula: set[tuple[str, str]]) -> list[tuple[str, str]]:
    """Agrupa (turno, aula) em blocos de posições consecutivas na grade, um
    intervalo (início, fim) por bloco — do jeito que o SIGAA mostra (ex.
    "6T2345" é T2,T3,T4,T5, um bloco só do início de T2 ao fim de T5, com o
    intervalo de 10 min entre T2 e T3 embutido no meio, não um corte)."""
    posicoes = sorted(_POSICAO_AULA[par] for par in pares_turno_aula if par in _POSICAO_AULA)

    blocos: list[tuple[int, int]] = []
    inicio_bloco = fim_bloco = None
    for posicao in posicoes:
        if fim_bloco is not None and posicao == fim_bloco + 1:
            fim_bloco = posicao
            continue
        if inicio_bloco is not None:
            blocos.append((inicio_bloco, fim_bloco))
        inicio_bloco = fim_bloco = posicao
    if inicio_bloco is not None:
        blocos.append((inicio_bloco, fim_bloco))

    intervalos = []
    for posicao_inicio, posicao_fim in blocos:
        turno_inicio, aula_inicio = _ORDEM_AULAS[posicao_inicio]
        turno_fim, aula_fim = _ORDEM_AULAS[posicao_fim]
        inicio = _INICIO_AULA[turno_inicio][aula_inicio]
        fim = _fim_aula(turno_fim, _INICIO_AULA[turno_fim][aula_fim])
        intervalos.append((inicio, fim))
    return intervalos


def horario_para_intervalos_por_dia(codigo: str) -> dict[str, list[tuple[str, str]]]:
    """Decompõe um código de horário em {dia: [(início, fim), ...]}, com
    aulas consecutivas da grade juntas num bloco só (RF18)."""
    pares_por_dia: dict[str, set[tuple[str, str]]] = defaultdict(set)
    for dias, turno, aulas in decompor_codigo_horario(codigo):
        for dia in dias:
            for aula in aulas:
                pares_por_dia[dia].add((turno, aula))
    return {dia: _intervalos_do_dia(pares) for dia, pares in pares_por_dia.items()}


def listar_salas(session: Session) -> list[Espaco]:
    salas = session.query(Sala).order_by(Sala.predio, Sala.nome).all()
    return [Espaco(id=sala.id, nome=sala.nome, predio=sala.predio) for sala in salas]


def listar_salas_vazias(session: Session, dia: str, horario: str) -> list[Espaco]:
    """Salas sem nenhuma turma cadastrada no dia/horário dados. `dia` é um dos
    nomes de `DIA_PARA_DIGITO`; `horario` é o início de uma aula, "HH:MM"
    (ex. "14:00"). Dia ou horário fora da grade de aulas (sem turma possível)
    devolve todas as salas, em vez de erro."""
    dia_digito = DIA_PARA_DIGITO.get(dia)
    turno_aula = _localizar_turno_aula(horario)

    ocupadas: set[int] = set()
    if dia_digito is not None and turno_aula is not None:
        turno, aula = turno_aula
        linhas = (
            session.query(Horario.codigo, Horario.sala_id)
            .filter(Horario.sala_id.isnot(None))
            .all()
        )
        for codigo, sala_id in linhas:
            for dias, turno_codigo, aulas in decompor_codigo_horario(codigo):
                if turno_codigo == turno and dia_digito in dias and aula in aulas:
                    ocupadas.add(sala_id)
                    break

    salas = (
        session.query(Sala)
        .filter(Sala.id.notin_(ocupadas))
        .order_by(Sala.predio, Sala.nome)
        .all()
    )
    return [Espaco(id=sala.id, nome=sala.nome, predio=sala.predio) for sala in salas]
