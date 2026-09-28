"""Persistência das Turmas capturadas pelo scraper de Disciplinas (RF01-05).

Faz o get-or-create de Disciplina/Sala/Professor e o upsert de Turma+Horario
a partir do contrato validado em `app/schemas/disciplina.py`. A normalização
que aquele módulo deixa explicitamente para a camada de domínio (separar
"FCTE - I9/I10" em prédio+sala) mora aqui — não no scraper nem em router,
conforme docs/ARQUITETURA.md.
"""

from __future__ import annotations

from sqlalchemy.orm import Session

from app.models import Disciplina, Horario, Professor, Sala, Turma
from app.schemas.disciplina import Horario as HorarioCapturado
from app.schemas.disciplina import Professor as ProfessorCapturado
from app.schemas.disciplina import Sala as SalaCapturada
from app.schemas.disciplina import Turma as TurmaCapturada


def normalizar_sala(descricao: str) -> tuple[str, str]:
    """"FCTE - I9/I10" -> ("FCTE", "I9/I10"); sem separador, tudo vira nome."""
    predio, separador, nome = descricao.partition(" - ")
    if not separador:
        return "", descricao.strip()
    return predio.strip(), nome.strip()


def _get_ou_cria_disciplina(session: Session, codigo: str, nome: str) -> Disciplina:
    disciplina = session.query(Disciplina).filter_by(codigo=codigo).one_or_none()
    if disciplina is None:
        disciplina = Disciplina(codigo=codigo, nome=nome)
        session.add(disciplina)
        session.flush()
    return disciplina


def _get_ou_cria_professor(session: Session, nome: str) -> Professor:
    professor = session.query(Professor).filter_by(nome=nome).one_or_none()
    if professor is None:
        professor = Professor(nome=nome)
        session.add(professor)
        session.flush()
    return professor


def _get_ou_cria_sala(session: Session, descricao: str) -> Sala | None:
    descricao = descricao.strip()
    if not descricao:
        return None

    predio, nome = normalizar_sala(descricao)
    sala = session.query(Sala).filter_by(predio=predio, nome=nome).one_or_none()
    if sala is None:
        sala = Sala(predio=predio, nome=nome)
        session.add(sala)
        session.flush()
    return sala


def persistir_turma(session: Session, turma: TurmaCapturada, unidade: str) -> Turma:
    """Grava (ou atualiza, se já existir) uma Turma capturada pelo scraper.

    A chave natural é (disciplina, numero, ano_periodo) — a mesma
    UniqueConstraint do model — porque o scraper roda de novo a cada
    agendamento (RF15) e uma turma já vista só deve ter vagas/sala/horário
    atualizados, nunca virar uma linha duplicada.
    """
    disciplina = _get_ou_cria_disciplina(session, turma.disciplina_codigo, turma.disciplina_nome)
    sala = _get_ou_cria_sala(session, turma.sala.descricao)
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
    turma_existente.sala = sala
    turma_existente.professores = professores

    # Horario.turma_id não aceita nulo, então reassociar a lista sem excluir
    # antes deixaria a linha antiga órfã e o flush quebraria com IntegrityError.
    for horario_antigo in list(turma_existente.horarios):
        session.delete(horario_antigo)
    session.flush()
    turma_existente.horarios = [Horario(codigo=h.codigo, descricao=h.descricao) for h in turma.horarios]

    return turma_existente


def persistir_turmas(session: Session, turmas: list[TurmaCapturada], unidade: str) -> list[Turma]:
    return [persistir_turma(session, turma, unidade) for turma in turmas]


def _descricao_sala(sala: Sala | None) -> str:
    if sala is None:
        return ""
    if sala.predio:
        return f"{sala.predio} - {sala.nome}"
    return sala.nome


def _turma_para_contrato(turma: Turma) -> TurmaCapturada:
    return TurmaCapturada(
        disciplina_codigo=turma.disciplina.codigo,
        disciplina_nome=turma.disciplina.nome,
        numero=turma.numero,
        ano_periodo=turma.ano_periodo,
        professores=[ProfessorCapturado(nome=p.nome) for p in turma.professores],
        horarios=[HorarioCapturado(codigo=h.codigo, descricao=h.descricao) for h in turma.horarios],
        sala=SalaCapturada(descricao=_descricao_sala(turma.sala)),
        vagas_ofertadas=turma.vagas_ofertadas,
        vagas_ocupadas=turma.vagas_ocupadas,
    )


def listar_turmas(session: Session) -> list[TurmaCapturada]:
    return [_turma_para_contrato(turma) for turma in session.query(Turma).all()]
