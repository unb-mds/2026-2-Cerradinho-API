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


def test_listar_professores_retorna_docentes_com_disciplinas(client, db_session):
    persistir_turma(db_session, _turma_capturada(), unidade="FCTE")
    persistir_turma(
        db_session,
        _turma_capturada(disciplina_codigo="FGA0071", disciplina_nome="Engenharia de Requisitos"),
        unidade="FCTE",
    )
    db_session.commit()

    response = client.get("/v1/professores")

    assert response.status_code == 200
    body = response.json()
    assert len(body) == 1
    assert body[0]["nome"] == "Ana Souza"
    assert body[0]["disciplinas"] == ["FGA0071", "FGA0242"]
    assert isinstance(body[0]["id"], int)


def test_listar_professores_nao_repete_disciplina_com_varias_turmas(client, db_session):
    persistir_turma(db_session, _turma_capturada(numero="01"), unidade="FCTE")
    persistir_turma(db_session, _turma_capturada(numero="02"), unidade="FCTE")
    db_session.commit()

    response = client.get("/v1/professores")

    assert response.json()[0]["disciplinas"] == ["FGA0242"]


def test_listar_professores_ordena_por_nome(client, db_session):
    persistir_turma(
        db_session,
        _turma_capturada(professores=[Professor(nome="Carlos Lima"), Professor(nome="Ana Souza")]),
        unidade="FCTE",
    )
    db_session.commit()

    response = client.get("/v1/professores")

    assert [p["nome"] for p in response.json()] == ["Ana Souza", "Carlos Lima"]


def test_listar_professores_sem_dado_retorna_lista_vazia(client):
    response = client.get("/v1/professores")

    assert response.status_code == 200
    assert response.json() == []
