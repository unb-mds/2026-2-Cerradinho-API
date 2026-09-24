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


def test_listar_disciplinas_retorna_turmas_persistidas(client, db_session):
    persistir_turma(db_session, _turma_capturada(), unidade="FCTE")
    db_session.commit()

    response = client.get("/v1/disciplinas")

    assert response.status_code == 200
    body = response.json()
    assert len(body) == 1
    assert body[0]["disciplina_codigo"] == "FGA0242"
    assert body[0]["sala"] == {"descricao": "FCTE - I9/I10"}
    assert body[0]["professores"] == [{"nome": "Ana Souza"}]
    assert body[0]["horarios"] == [{"codigo": "6T2345", "descricao": "Sexta-feira 14:00 às 17:50"}]


def test_listar_disciplinas_sem_sala_devolve_descricao_vazia(client, db_session):
    persistir_turma(db_session, _turma_capturada(sala=Sala(descricao="")), unidade="FCTE")
    db_session.commit()

    response = client.get("/v1/disciplinas")

    assert response.json()[0]["sala"] == {"descricao": ""}


def test_listar_disciplinas_sem_dado_retorna_lista_vazia(client):
    response = client.get("/v1/disciplinas")

    assert response.status_code == 200
    assert response.json() == []
