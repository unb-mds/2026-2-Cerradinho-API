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


def test_listar_disciplinas_sem_parametro_nao_tem_x_total_count(client, db_session):
    """Sem busca/departamento/limite/offset, continua devolvendo tudo como
    antes - não quebra quem já consome a rota sem esses parâmetros novos."""
    persistir_turma(db_session, _turma_capturada(), unidade="FCTE")
    db_session.commit()

    response = client.get("/v1/disciplinas")

    assert len(response.json()) == 1
    assert "X-Total-Count" not in response.headers


def test_listar_disciplinas_limite_e_offset_paginam_com_total_no_cabecalho(client, db_session):
    persistir_turma(db_session, _turma_capturada(numero="01"), unidade="FCTE")
    persistir_turma(db_session, _turma_capturada(numero="02"), unidade="FCTE")
    persistir_turma(db_session, _turma_capturada(numero="03"), unidade="FCTE")
    db_session.commit()

    primeira_pagina = client.get("/v1/disciplinas", params={"limite": 2, "offset": 0})
    segunda_pagina = client.get("/v1/disciplinas", params={"limite": 2, "offset": 2})

    assert [t["numero"] for t in primeira_pagina.json()] == ["01", "02"]
    assert primeira_pagina.headers["X-Total-Count"] == "3"
    assert [t["numero"] for t in segunda_pagina.json()] == ["03"]
    assert segunda_pagina.headers["X-Total-Count"] == "3"


def test_listar_disciplinas_busca_por_codigo_nome_ou_professor(client, db_session):
    persistir_turma(
        db_session,
        _turma_capturada(
            disciplina_codigo="FGA0242",
            disciplina_nome="Métodos de Desenvolvimento de Software",
            professores=[Professor(nome="André Luis Araújo")],
        ),
        unidade="FCTE",
    )
    persistir_turma(
        db_session,
        _turma_capturada(
            disciplina_codigo="FGA0001",
            disciplina_nome="Outra Disciplina",
            numero="02",
            professores=[Professor(nome="Carlos Lima")],
        ),
        unidade="FCTE",
    )
    db_session.commit()

    por_codigo = client.get("/v1/disciplinas", params={"busca": "fga0242"})
    por_nome = client.get("/v1/disciplinas", params={"busca": "desenvolvimento"})
    por_professor = client.get("/v1/disciplinas", params={"busca": "andre araujo"})

    assert [t["disciplina_codigo"] for t in por_codigo.json()] == ["FGA0242"]
    assert [t["disciplina_codigo"] for t in por_nome.json()] == ["FGA0242"]
    assert [t["disciplina_codigo"] for t in por_professor.json()] == ["FGA0242"]


def test_listar_disciplinas_filtra_por_departamento(client, db_session):
    persistir_turma(db_session, _turma_capturada(disciplina_codigo="FGA0242", numero="01"), unidade="FCTE")
    persistir_turma(db_session, _turma_capturada(disciplina_codigo="CIC0004", numero="02"), unidade="FCTE")
    db_session.commit()

    response = client.get("/v1/disciplinas", params={"departamento": "fga"})

    assert [t["disciplina_codigo"] for t in response.json()] == ["FGA0242"]
