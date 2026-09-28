from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from app.domain.disciplinas import normalizar_sala, persistir_turma
from app.models import Base, Horario, Professor, Sala, Turma
from app.schemas.disciplina import Horario as HorarioCapturado
from app.schemas.disciplina import Professor as ProfessorCapturado
from app.schemas.disciplina import Sala as SalaCapturada
from app.schemas.disciplina import Turma as TurmaCapturada


def _in_memory_session() -> Session:
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    return Session(engine)


def _turma_capturada(**overrides) -> TurmaCapturada:
    base = dict(
        disciplina_codigo="FGA0242",
        disciplina_nome="Métodos de Desenvolvimento de Software",
        numero="01",
        ano_periodo="2026.2",
        professores=[ProfessorCapturado(nome="Ana Souza")],
        horarios=[HorarioCapturado(codigo="6T2345", descricao="Sexta-feira 14:00 às 17:50")],
        sala=SalaCapturada(descricao="FCTE - I9/I10"),
        vagas_ofertadas=40,
        vagas_ocupadas=38,
    )
    base.update(overrides)
    return TurmaCapturada(**base)


def test_normalizar_sala_separa_predio_e_nome():
    assert normalizar_sala("FCTE - I9/I10") == ("FCTE", "I9/I10")


def test_normalizar_sala_sem_separador_vira_so_nome():
    assert normalizar_sala("Auditório Dois Candangos") == ("", "Auditório Dois Candangos")


def test_persistir_turma_cria_disciplina_sala_professores_e_horarios():
    session = _in_memory_session()

    turma_salva = persistir_turma(session, _turma_capturada(), unidade="FCTE")
    session.commit()

    assert turma_salva.disciplina.codigo == "FGA0242"
    assert turma_salva.unidade == "FCTE"
    assert turma_salva.vagas_ofertadas == 40
    assert turma_salva.vagas_ocupadas == 38
    assert turma_salva.sala.predio == "FCTE"
    assert turma_salva.sala.nome == "I9/I10"
    assert [p.nome for p in turma_salva.professores] == ["Ana Souza"]
    assert [h.codigo for h in turma_salva.horarios] == ["6T2345"]


def test_persistir_turma_sem_texto_de_sala_fica_com_sala_nula():
    session = _in_memory_session()

    turma_salva = persistir_turma(
        session, _turma_capturada(sala=SalaCapturada(descricao=""), professores=[]), unidade="FCTE"
    )
    session.commit()

    assert turma_salva.sala is None
    assert turma_salva.professores == []


def test_persistir_turma_repetida_atualiza_em_vez_de_duplicar():
    session = _in_memory_session()

    persistir_turma(session, _turma_capturada(vagas_ocupadas=38), unidade="FCTE")
    session.commit()

    persistir_turma(session, _turma_capturada(vagas_ocupadas=40), unidade="FCTE")
    session.commit()

    turmas = session.query(Turma).all()
    assert len(turmas) == 1
    assert turmas[0].vagas_ocupadas == 40


def test_persistir_turma_troca_professores_e_horarios_em_vez_de_acumular():
    session = _in_memory_session()

    persistir_turma(session, _turma_capturada(), unidade="FCTE")
    session.commit()

    turma_atualizada = persistir_turma(
        session,
        _turma_capturada(
            professores=[ProfessorCapturado(nome="Bruno Lima")],
            horarios=[HorarioCapturado(codigo="2M1234", descricao="Terça-feira 08:00 às 09:50")],
        ),
        unidade="FCTE",
    )
    session.commit()

    assert [p.nome for p in turma_atualizada.professores] == ["Bruno Lima"]
    assert [h.codigo for h in turma_atualizada.horarios] == ["2M1234"]
    # o horário antigo não pode ficar órfão no banco
    assert session.query(Horario).count() == 1


def test_persistir_turmas_de_disciplinas_diferentes_reaproveita_sala_e_professor():
    session = _in_memory_session()

    persistir_turma(session, _turma_capturada(), unidade="FCTE")
    session.commit()

    persistir_turma(
        session,
        _turma_capturada(disciplina_codigo="FGA0001", disciplina_nome="Outra Disciplina", numero="02"),
        unidade="FCTE",
    )
    session.commit()

    assert session.query(Sala).count() == 1
    assert session.query(Professor).count() == 1
    assert session.query(Turma).count() == 2
