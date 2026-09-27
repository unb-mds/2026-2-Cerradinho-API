from app.domain.disciplinas import persistir_turma
from app.schemas.disciplina import Horario, Professor, Sala, Turma


def _turma_capturada(**overrides) -> Turma:
    base = dict(
        disciplina_codigo="FGA0242",
        disciplina_nome="Métodos de Desenvolvimento de Software",
        numero="01",
        ano_periodo="2026.2",
        professores=[Professor(nome="Ana Souza")],
        horarios=[Horario(codigo="6T2345", descricao="Sexta-feira 14:00 às 17:50")],
        sala=Sala(descricao="FCTE - I9/I10"),
        vagas_ofertadas=40,
        vagas_ocupadas=38,
    )
    base.update(overrides)
    return Turma(**base)


def test_listar_salas_retorna_predio_e_nome_separados(client, db_session):
    persistir_turma(db_session, _turma_capturada(), unidade="FCTE")
    db_session.commit()

    response = client.get("/v1/salas")

    assert response.status_code == 200
    body = response.json()
    assert len(body) == 1
    assert body[0]["predio"] == "FCTE"
    assert body[0]["nome"] == "I9/I10"
    assert isinstance(body[0]["id"], int)


def test_listar_salas_nao_repete_sala_usada_por_varias_turmas(client, db_session):
    persistir_turma(db_session, _turma_capturada(numero="01"), unidade="FCTE")
    persistir_turma(db_session, _turma_capturada(numero="02"), unidade="FCTE")
    db_session.commit()

    response = client.get("/v1/salas")

    assert len(response.json()) == 1


def test_listar_salas_ordena_por_predio_e_nome(client, db_session):
    persistir_turma(db_session, _turma_capturada(numero="01", sala=Sala(descricao="FCTE - S1")), unidade="FCTE")
    persistir_turma(db_session, _turma_capturada(numero="02", sala=Sala(descricao="BSA SUL - A1")), unidade="FCTE")
    persistir_turma(db_session, _turma_capturada(numero="03", sala=Sala(descricao="FCTE - I9/I10")), unidade="FCTE")
    db_session.commit()

    response = client.get("/v1/salas")

    assert [(s["predio"], s["nome"]) for s in response.json()] == [
        ("BSA SUL", "A1"),
        ("FCTE", "I9/I10"),
        ("FCTE", "S1"),
    ]


def test_listar_salas_turma_sem_sala_nao_cria_espaco(client, db_session):
    persistir_turma(db_session, _turma_capturada(sala=Sala(descricao="")), unidade="FCTE")
    db_session.commit()

    response = client.get("/v1/salas")

    assert response.json() == []
