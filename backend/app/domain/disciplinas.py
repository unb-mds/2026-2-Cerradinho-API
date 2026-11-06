"""Persistência das Turmas capturadas pelo scraper de Disciplinas (RF01-05).

Faz o get-or-create de Disciplina/Sala/Professor e o upsert de Turma+Horario
a partir do contrato validado em `app/schemas/disciplina.py`. A normalização
que aquele módulo deixa explicitamente para a camada de domínio (separar
"FCTE - I9/I10" em prédio+sala) mora aqui — não no scraper nem em router,
conforme docs/ARQUITETURA.md.
"""

from __future__ import annotations

import logging
import re
from collections import defaultdict

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.models import Disciplina, Horario, Professor, Sala, Turma
from app.schemas.disciplina import Horario as HorarioCapturado
from app.schemas.disciplina import Professor as ProfessorCapturado
from app.schemas.disciplina import Sala as SalaCapturada
from app.schemas.disciplina import Turma as TurmaCapturada

_SEPARADOR_SALA = re.compile(r"\s*[-/]\s*")
# O SIGAA também não é consistente em pôr ponto depois de "LAB" ("LAB NIT/LDS"
# vs "LAB. NIT/LDS" pra mesma sala) - sem normalizar, isso também duplica.
_PADRAO_LAB_COM_PONTO = re.compile(r"\bLAB\.\s*")
# Mais de uma sala no mesmo campo, quando a turma usa salas diferentes em
# dias diferentes: com espaço ao redor da barra ("S1 / MOCAP") é sempre
# separador de sala; sem espaço ("LAB NIT/LDS") só é separador quando os dois
# lados já vêm marcados com o dia da semana ("LDS(SEGUNDA)/I1(SEXTA)") -
# senão é o nome de uma sala só, que por acaso tem barra.
_SEPARADOR_MULTISSALA_ESPACADO = " / "
_PADRAO_DIA_ENTRE_PARENTESES = re.compile(
    r"\((?:domingo|segunda|ter[çc]a|quarta|quinta|sexta|s[áa]bado)(?:-feira)?\)\s*$", re.IGNORECASE
)
# O Darcy usa espaço simples (sem "-" nem "/") entre prédio e sala em vários
# casos ("PAT AT 125", "ICC ANF.16"). Só reconhece como prédio quando o
# primeiro token é um desses, confirmados contra turma real do Darcy -
# outro prefixo desconhecido fica tudo como nome, igual antes. Valor é
# (prédio real, prefixo a devolver pro nome) - "BSAS" é "BSA S" (BSA Sul)
# colado sem espaço nessa unidade, achado real também.
_PREDIOS_SEM_SEPARADOR: dict[str, tuple[str, str]] = {
    "ICC": ("ICC", ""),
    "PAT": ("PAT", ""),
    "BSA": ("BSA", ""),
    "FCTE": ("FCTE", ""),
    "PJC": ("PJC", ""),
    "BSAS": ("BSA", "S "),
}
# "TÉRREO"/"SUBSOLO" são andar, não prédio - o SIGAA às vezes escreve só
# isso antes da sala (ex. "TÉRREO/SUBSOLO"), e o separador "/" fazia virar
# prédio errado. Sem saber o prédio de verdade nesses casos, mantém vazio
# em vez de promover o andar a prédio.
_PALAVRAS_DE_ANDAR = {"TERREO", "TÉRREO", "SUBSOLO"}
# Código de horário do SIGAA: um ou mais dígitos de dia (2=segunda ... 7=sábado),
# um turno (M/T/N) e um ou mais dígitos de aula, ex. "246T23" (seg/qua/sex, tarde,
# aulas 2 e 3). Dia "1" (domingo) nunca aparece — não há aula nesse dia. Pode
# ter mais de um segmento colado com espaço, quando a turma tem aula em
# turnos diferentes (ex. "35M5 35T1").
_PADRAO_CODIGO_HORARIO = re.compile(r"^([2-7]+)([MTN])([0-9]+)$")
# Achado real do Darcy: o SIGAA também junta o código de horário com a sala
# daquele dia no próprio campo de sala, um par por dia (ex.
# "2N12(ICC ANF.15) 4N12(ICC ANF.16)" - segunda na ANF.15, quarta na
# ANF.16). Diferente de `_montar_horarios`, aqui o dia já vem casado com a
# sala certa, sem precisar adivinhar pela ordem.
_PADRAO_PAR_CODIGO_SALA = re.compile(r"([2-7]+[MTN][0-9]+)\(([^)]+)\)")

logger = logging.getLogger(__name__)


def normalizar_sala(descricao: str) -> tuple[str, str]:
    """"FCTE - I9/I10" -> ("FCTE", "I9/I10"); sem separador, tudo vira nome.

    O SIGAA não usa um separador único entre prédio e sala ("FCTE - I2",
    "FCTE / I2", "FCTE- LAB NEI 2" são a mesma sala) nem maiúsculas/minúsculas
    consistentes pro mesmo espaço físico ("Mocap" vs "MOCAP"). Sem
    normalizar os dois, a mesma sala vira várias linhas distintas."""
    return normalizar_salas(descricao)[0]


def normalizar_salas(descricao: str) -> list[tuple[str, str]]:
    """Como `normalizar_sala`, mas separa em mais de uma sala quando o SIGAA
    junta salas diferentes no mesmo campo (ver `_dividir_nome_em_varias_salas`).
    Sempre devolve pelo menos um item."""
    descricao = descricao.strip()
    match = _SEPARADOR_SALA.search(descricao)
    if not match:
        predio, nome_completo = _separar_predio_sem_separador(descricao)
    else:
        predio = descricao[: match.start()].strip().upper()
        nome_completo = descricao[match.end() :].strip()
        primeiro_token = predio.split(" ", 1)[0]
        segundo_token = predio[len(primeiro_token) :].strip().split(" ", 1)[0]
        if predio in _PALAVRAS_DE_ANDAR:
            # "andar" (TÉRREO/SUBSOLO) não é prédio - junta de volta ao nome
            # em vez de gravar um prédio errado.
            predio, nome_completo = "", f"{predio} {nome_completo}".strip()
        elif predio != primeiro_token and primeiro_token in _PREDIOS_SEM_SEPARADOR and len(segundo_token) <= 2:
            # achado real do Darcy: o separador que o regex casou tá dentro
            # do código da sala, não entre prédio e sala (ex. "BSA S B1 34 -
            # 10", "ICC AT 114 - 092") - distingue de "BSA SUL - A1" (prédio
            # de verdade, nome completo) pelo token logo depois do prédio
            # ser curto (sigla de ala/bloco: "S", "N", "AT"), não uma
            # palavra. O prédio de verdade é só o primeiro token, e o
            # código da sala fica inteiro, sem cortar no meio.
            predio_real, prefixo = _PREDIOS_SEM_SEPARADOR[primeiro_token]
            resto = re.sub(r"^[-/]\s*", "", descricao[len(primeiro_token) :].strip())
            predio, nome_completo = predio_real, f"{prefixo}{resto}"
    return [(predio, _normalizar_nome_sala(nome)) for nome in _dividir_nome_em_varias_salas(nome_completo)]


def _separar_predio_sem_separador(descricao: str) -> tuple[str, str]:
    """O Darcy também usa espaço simples, sem "-" nem "/", entre prédio e
    sala ("PAT AT 125", "ICC ANF.16"). Só separa quando o primeiro token é
    um prédio conhecido - um prefixo desconhecido fica tudo como nome,
    como antes dessa checagem existir."""
    primeiro_token, _, resto = descricao.partition(" ")
    alias = _PREDIOS_SEM_SEPARADOR.get(primeiro_token.upper())
    if alias is not None and resto.strip():
        predio, prefixo = alias
        return predio, f"{prefixo}{resto.strip()}"
    return "", descricao


def _dividir_nome_em_varias_salas(nome: str) -> list[str]:
    if _SEPARADOR_MULTISSALA_ESPACADO in nome:
        partes = nome.split(_SEPARADOR_MULTISSALA_ESPACADO)
    else:
        partes = nome.split("/")
        if len(partes) < 2 or not all(_PADRAO_DIA_ENTRE_PARENTESES.search(p.strip()) for p in partes):
            return [nome]
    return [parte.strip() for parte in partes if parte.strip()]


def _normalizar_nome_sala(nome: str) -> str:
    return _PADRAO_LAB_COM_PONTO.sub("LAB ", nome.upper()).strip()


def _decompor_segmento_horario(segmento: str) -> tuple[set[str], str, set[str]] | None:
    match = _PADRAO_CODIGO_HORARIO.match(segmento)
    if match is None:
        return None
    dias, turno, aulas = match.groups()
    return set(dias), turno, set(aulas)


def decompor_codigo_horario(codigo: str) -> list[tuple[set[str], str, set[str]]]:
    """Um código pode ter mais de um segmento dia+turno+aula colado com
    espaço, quando a turma tem aula em turnos diferentes (ex. "35M5 35T1").
    Segmentos que não casam o padrão são ignorados (com warning) sem
    descartar os outros segmentos válidos do mesmo código."""
    segmentos = []
    for parte in codigo.split():
        decomposto = _decompor_segmento_horario(parte)
        if decomposto is None:
            logger.warning(
                "Segmento de horário fora do padrão esperado, ignorado: %r (código completo: %r)",
                parte,
                codigo,
            )
            continue
        segmentos.append(decomposto)
    return segmentos


def _get_ou_cria_disciplina(session: Session, codigo: str, nome: str) -> Disciplina:
    disciplina = session.query(Disciplina).filter_by(codigo=codigo).one_or_none()
    if disciplina is None:
        disciplina = Disciplina(codigo=codigo, nome=nome)
        session.add(disciplina)
        session.flush()
    return disciplina


def normalizar_nome_professor(nome: str) -> str:
    """"ALESSANDRO BORGES DE SOUSA OLIVEIRA (60h)" -> "ALESSANDRO BORGES DE SOUSA OLIVEIRA".

    O SIGAA junta a carga horária da disciplina no nome do docente; como a
    carga varia por disciplina, usar o texto cru como chave de dedup cria uma
    linha de Professor por carga horária distinta do mesmo professor.
    """
    nome, _, _ = nome.partition(" (")
    return nome.strip()


def _get_ou_cria_professor(session: Session, nome: str) -> Professor:
    nome = normalizar_nome_professor(nome)
    professor = session.query(Professor).filter_by(nome=nome).one_or_none()
    if professor is None:
        professor = Professor(nome=nome)
        session.add(professor)
        session.flush()
    return professor


def _get_ou_cria_salas(session: Session, descricao: str) -> list[Sala]:
    descricao = descricao.strip()
    if not descricao:
        return []

    salas = []
    for predio, nome in normalizar_salas(descricao):
        sala = session.query(Sala).filter_by(predio=predio, nome=nome).one_or_none()
        if sala is None:
            sala = Sala(predio=predio, nome=nome)
            session.add(sala)
            session.flush()
        salas.append(sala)
    return salas


def _extrair_pares_codigo_sala(descricao: str) -> list[tuple[str, str]] | None:
    """Quando o campo de sala é feito só de pares "código(sala)" colados com
    espaço, devolve cada par; senão, `None` (ex. texto truncado pelo SIGAA,
    ou um segmento sem sala junto - achados reais do Darcy). Só aceita
    quando o texto inteiro é coberto pelos pares, pra não arriscar perder
    parte da informação de um formato que não bate exatamente."""
    descricao = descricao.strip()
    pares = _PADRAO_PAR_CODIGO_SALA.findall(descricao)
    if not pares:
        return None
    reconstruido = " ".join(f"{codigo}({sala})" for codigo, sala in pares)
    if reconstruido != descricao:
        return None
    return pares


def _montar_horarios_com_sala_explicita(
    session: Session, horarios: list[HorarioCapturado], pares_codigo_sala: list[tuple[str, str]]
) -> list[Horario]:
    descricao = horarios[0].descricao if horarios else ""
    novos_horarios = []
    for codigo, sala_texto in pares_codigo_sala:
        salas = _get_ou_cria_salas(session, sala_texto)
        sala_id = salas[0].id if salas else None
        novos_horarios.append(Horario(codigo=codigo, descricao=descricao, sala_id=sala_id))
    return novos_horarios


def _montar_horarios(horarios: list[HorarioCapturado], salas: list[Sala]) -> list[Horario]:
    """Associa cada horário à sala correspondente. Com uma sala só (o caso
    comum) ou nenhuma, todo horário usa a mesma. Com mais de uma, o SIGAA as
    lista na mesma ordem dos dias da turma (ex. "FCTE - S1 / MOCAP" é
    segunda na S1, quarta na MOCAP) — por isso a correspondência é por
    posição, em ordem crescente de dia. Quando o número de salas não bate
    com o de dias distintos, não arrisca casar errado: cada sala fica
    associada a todos os horários, em vez de só ao dia que calhou de casar."""
    if len(salas) <= 1:
        sala_id = salas[0].id if salas else None
        return [Horario(codigo=h.codigo, descricao=h.descricao, sala_id=sala_id) for h in horarios]

    aulas_por_dia: dict[str, dict[str, set[str]]] = defaultdict(lambda: defaultdict(set))
    descricao_por_dia: dict[str, str] = {}
    for horario in horarios:
        for dias, turno, aulas in decompor_codigo_horario(horario.codigo):
            for dia in dias:
                aulas_por_dia[dia][turno] |= aulas
                descricao_por_dia.setdefault(dia, horario.descricao)

    dias_ordenados = sorted(aulas_por_dia, key=int)
    if len(dias_ordenados) != len(salas):
        logger.warning(
            "Turma com %d salas mas %d dias distintos no horário - não dá pra casar sala por dia com segurança",
            len(salas),
            len(dias_ordenados),
        )
        return [
            Horario(codigo=h.codigo, descricao=h.descricao, sala_id=sala.id) for sala in salas for h in horarios
        ]

    novos_horarios = []
    for dia, sala in zip(dias_ordenados, salas):
        codigo_do_dia = " ".join(
            f"{dia}{turno}{''.join(sorted(aulas))}" for turno, aulas in sorted(aulas_por_dia[dia].items())
        )
        novos_horarios.append(Horario(codigo=codigo_do_dia, descricao=descricao_por_dia[dia], sala_id=sala.id))
    return novos_horarios


def persistir_turma(session: Session, turma: TurmaCapturada, unidade: str) -> Turma:
    """Grava (ou atualiza, se já existir) uma Turma capturada pelo scraper.

    A chave natural é (disciplina, numero, ano_periodo) — a mesma
    UniqueConstraint do model — porque o scraper roda de novo a cada
    agendamento (RF15) e uma turma já vista só deve ter vagas/sala/horário
    atualizados, nunca virar uma linha duplicada.
    """
    disciplina = _get_ou_cria_disciplina(session, turma.disciplina_codigo, turma.disciplina_nome)
    pares_codigo_sala = _extrair_pares_codigo_sala(turma.sala.descricao)
    salas = [] if pares_codigo_sala is not None else _get_ou_cria_salas(session, turma.sala.descricao)
    professores = [_get_ou_cria_professor(session, p.nome) for p in turma.professores]

    turma_existente = (
        session.query(Turma)
        .filter_by(disciplina_id=disciplina.id, numero=turma.numero, ano_periodo=turma.ano_periodo)
        .one_or_none()
    )
    if turma_existente is None:
        turma_existente = Turma(disciplina=disciplina, numero=turma.numero, ano_periodo=turma.ano_periodo)
        session.add(turma_existente)

    turma_existente.unidade = unidade
    turma_existente.vagas_ofertadas = turma.vagas_ofertadas
    turma_existente.vagas_ocupadas = turma.vagas_ocupadas
    turma_existente.professores = professores

    # Horario.turma_id não aceita nulo, então reassociar a lista sem excluir
    # antes deixaria a linha antiga órfã e o flush quebraria com IntegrityError.
    for horario_antigo in list(turma_existente.horarios):
        session.delete(horario_antigo)
    session.flush()
    if pares_codigo_sala is not None:
        turma_existente.horarios = _montar_horarios_com_sala_explicita(session, turma.horarios, pares_codigo_sala)
    else:
        turma_existente.horarios = _montar_horarios(turma.horarios, salas)

    return turma_existente


def persistir_turmas(session: Session, turmas: list[TurmaCapturada], unidade: str) -> list[Turma]:
    """Persiste cada turma em sua própria savepoint: uma turma com dado fora
    do esperado (ex. erro de integridade) não derruba as outras turmas já
    processadas da mesma unidade — só ela é descartada, e o erro vai pro log
    em vez de derrubar a raspagem inteira."""
    persistidas = []
    for turma in turmas:
        try:
            with session.begin_nested():
                persistidas.append(persistir_turma(session, turma, unidade))
        except SQLAlchemyError:
            logger.exception(
                "Falha ao persistir turma %s/%s (%s), pulando",
                turma.disciplina_codigo,
                turma.numero,
                unidade,
            )
    return persistidas


def _descricao_salas(turma: Turma) -> str:
    """Reconstrói a descrição original de sala a partir dos horários — o
    contrato público (`GET /v1/disciplinas`) continua expondo uma sala só
    por turma, mesmo com a sala agora vivendo por horário no banco."""
    salas_na_ordem: list[Sala] = []
    vistas: set[int] = set()
    for horario in turma.horarios:
        if horario.sala is not None and horario.sala.id not in vistas:
            vistas.add(horario.sala.id)
            salas_na_ordem.append(horario.sala)

    if not salas_na_ordem:
        return ""
    nomes = " / ".join(sala.nome for sala in salas_na_ordem)
    predio = salas_na_ordem[0].predio
    return f"{predio} - {nomes}" if predio else nomes


def _horarios_sem_repeticao(turma: Turma) -> list[HorarioCapturado]:
    """Quando as salas não casam com os dias, o mesmo horário é gravado uma
    vez por sala (ver `_montar_horarios`). No contrato público ele aparece
    uma vez só."""
    vistos: set[tuple[str, str]] = set()
    horarios = []
    for horario in turma.horarios:
        chave = (horario.codigo, horario.descricao)
        if chave not in vistos:
            vistos.add(chave)
            horarios.append(HorarioCapturado(codigo=horario.codigo, descricao=horario.descricao))
    return horarios


def _turma_para_contrato(turma: Turma) -> TurmaCapturada:
    return TurmaCapturada(
        disciplina_codigo=turma.disciplina.codigo,
        disciplina_nome=turma.disciplina.nome,
        numero=turma.numero,
        ano_periodo=turma.ano_periodo,
        professores=[ProfessorCapturado(nome=p.nome) for p in turma.professores],
        horarios=_horarios_sem_repeticao(turma),
        sala=SalaCapturada(descricao=_descricao_salas(turma)),
        vagas_ofertadas=turma.vagas_ofertadas,
        vagas_ocupadas=turma.vagas_ocupadas,
    )


def listar_turmas(session: Session) -> list[TurmaCapturada]:
    return [_turma_para_contrato(turma) for turma in session.query(Turma).all()]
