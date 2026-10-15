from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from app.domain.disciplinas import normalizar_nome_professor, normalizar_sala, persistir_turma
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
    assert normalizar_sala("Auditório Dois Candangos") == ("", "AUDITÓRIO DOIS CANDANGOS")


def test_normalizar_sala_ignora_espaco_no_inicio_do_texto():
    assert normalizar_sala(" FCTE - I2") == ("FCTE", "I2")


def test_normalizar_sala_aceita_barra_como_separador():
    assert normalizar_sala("FCTE / I2") == ("FCTE", "I2")


def test_normalizar_sala_aceita_traco_sem_espaco_antes():
    assert normalizar_sala("FCTE- LAB NEI 2") == ("FCTE", "LAB NEI 2")


def test_normalizar_sala_ignora_caixa_alta_ou_baixa():
    assert normalizar_sala("FCTE - Mocap") == normalizar_sala("FCTE - MOCAP")
    assert normalizar_sala("FCTE - Mocap") == ("FCTE", "MOCAP")


def test_normalizar_nome_professor_corta_carga_horaria():
    nome = "ALESSANDRO BORGES DE SOUSA OLIVEIRA (60h)"
    assert normalizar_nome_professor(nome) == "ALESSANDRO BORGES DE SOUSA OLIVEIRA"


def test_normalizar_nome_professor_sem_carga_horaria_fica_igual():
    assert normalizar_nome_professor("Ana Souza") == "Ana Souza"


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


def test_persistir_turmas_mesmo_professor_cargas_horarias_diferentes_nao_duplica():
    """Regressão: o SIGAA junta a carga horária da disciplina no nome do
    docente, e a carga varia por disciplina mesmo pro mesmo professor —
    sem normalizar, isso criava uma linha de Professor por carga horária."""
    session = _in_memory_session()

    persistir_turma(
        session,
        _turma_capturada(professores=[ProfessorCapturado(nome="Alessandro Borges de Sousa Oliveira (30h)")]),
        unidade="FCTE",
    )
    session.commit()

    persistir_turma(
        session,
        _turma_capturada(
            disciplina_codigo="FGA0001",
            disciplina_nome="Outra Disciplina",
            numero="02",
            professores=[ProfessorCapturado(nome="Alessandro Borges de Sousa Oliveira (60h)")],
        ),
        unidade="FCTE",
    )
    session.commit()

    professores = session.query(Professor).all()
    assert len(professores) == 1
    assert professores[0].nome == "Alessandro Borges de Sousa Oliveira"
    assert session.query(Turma).count() == 2


def test_persistir_turmas_mesma_sala_com_separador_e_caixa_diferentes_nao_duplica():
    """Regressão: o SIGAA descreve a mesma sala física com separador
    ("FCTE - Mocap" vs "FCTE / Mocap") e caixa ("Mocap" vs "MOCAP")
    inconsistentes — sem normalizar, a mesma sala virava várias linhas."""
    session = _in_memory_session()

    persistir_turma(
        session,
        _turma_capturada(
            sala=SalaCapturada(descricao="FCTE - Mocap"),
            horarios=[HorarioCapturado(codigo="6T2345", descricao="Sexta-feira 14:00 às 17:50")],
        ),
        unidade="FCTE",
    )
    session.commit()

    persistir_turma(
        session,
        _turma_capturada(
            disciplina_codigo="FGA0001",
            disciplina_nome="Outra Disciplina",
            numero="02",
            sala=SalaCapturada(descricao="FCTE / MOCAP"),
            horarios=[HorarioCapturado(codigo="2M1234", descricao="Terça-feira 08:00 às 09:50")],
        ),
        unidade="FCTE",
    )
    session.commit()

    salas = session.query(Sala).all()
    assert len(salas) == 1
    assert (salas[0].predio, salas[0].nome) == ("FCTE", "MOCAP")

    # as duas turmas continuam distintas, cada uma com seu próprio horário/dia,
    # só compartilhando a mesma sala
    turmas = session.query(Turma).order_by(Turma.numero).all()
    assert len(turmas) == 2
    assert [t.sala_id for t in turmas] == [salas[0].id, salas[0].id]
    assert [h.codigo for t in turmas for h in t.horarios] == ["6T2345", "2M1234"]
