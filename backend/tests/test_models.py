from datetime import date

import pytest
from sqlalchemy import create_engine
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models import Base, Cardapio, Disciplina, Horario, Professor, Sala, Turma


def _in_memory_engine():
    return create_engine("sqlite:///:memory:")


def test_cria_todas_as_tabelas():
    engine = _in_memory_engine()
    Base.metadata.create_all(engine)

    assert set(Base.metadata.tables.keys()) == {
        "professores",
        "salas",
        "disciplinas",
        "turmas",
        "turma_professores",
        "horarios",
        "cardapios",
    }


def test_turma_associa_disciplina_sala_professores_e_horarios():
    engine = _in_memory_engine()
    Base.metadata.create_all(engine)

    with Session(engine) as session:
        turma = Turma(
            numero="01",
            ano_periodo="2026.2",
            unidade="FCTE",
            vagas_ofertadas=40,
            vagas_ocupadas=38,
            disciplina=Disciplina(codigo="FGA0242", nome="Métodos de Desenvolvimento de Software"),
            sala=Sala(nome="I9/I10", predio="FCTE"),
            professores=[Professor(nome="Ana Souza"), Professor(nome="Bruno Lima")],
            horarios=[Horario(codigo="6T2345", descricao="Sexta-feira 14:00 às 17:50")],
        )
        session.add(turma)
        session.commit()

        salva = session.query(Turma).one()
        assert salva.disciplina.codigo == "FGA0242"
        assert salva.sala.predio == "FCTE"
        assert {p.nome for p in salva.professores} == {"Ana Souza", "Bruno Lima"}
        assert salva.horarios[0].codigo == "6T2345"


def test_turma_permite_sala_nula():
    engine = _in_memory_engine()
    Base.metadata.create_all(engine)

    with Session(engine) as session:
        session.add(
            Turma(
                numero="02",
                ano_periodo="2026.2",
                unidade="FCTE",
                vagas_ofertadas=30,
                vagas_ocupadas=0,
                disciplina=Disciplina(codigo="FGA9999", nome="Tópicos Especiais"),
            )
        )
        session.commit()

        salva = session.query(Turma).one()
        assert salva.sala is None
        assert salva.professores == []
        assert salva.horarios == []


def test_turma_nao_permite_numero_duplicado_na_mesma_disciplina_e_periodo():
    engine = _in_memory_engine()
    Base.metadata.create_all(engine)

    with Session(engine) as session:
        disciplina = Disciplina(codigo="FGA0001", nome="Disciplina A")
        session.add(
            Turma(
                numero="01",
                ano_periodo="2026.2",
                unidade="FCTE",
                vagas_ofertadas=20,
                vagas_ocupadas=0,
                disciplina=disciplina,
            )
        )
        session.commit()

        session.add(
            Turma(
                numero="01",
                ano_periodo="2026.2",
                unidade="FCTE",
                vagas_ofertadas=20,
                vagas_ocupadas=0,
                disciplina=disciplina,
            )
        )
        with pytest.raises(IntegrityError):
            session.commit()


def test_disciplina_nao_permite_codigo_duplicado():
    engine = _in_memory_engine()
    Base.metadata.create_all(engine)

    with Session(engine) as session:
        session.add(Disciplina(codigo="FGA0242", nome="Métodos de Desenvolvimento de Software"))
        session.commit()

        session.add(Disciplina(codigo="FGA0242", nome="Outro nome"))
        with pytest.raises(IntegrityError):
            session.commit()


def test_cardapio_nao_permite_data_duplicada():
    engine = _in_memory_engine()
    Base.metadata.create_all(engine)

    with Session(engine) as session:
        session.add(Cardapio(data=date(2026, 9, 13), almoco="Arroz, feijão e frango"))
        session.commit()

        session.add(Cardapio(data=date(2026, 9, 13), almoco="Outro almoço"))
        with pytest.raises(IntegrityError):
            session.commit()
