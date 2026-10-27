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


def test_listar_salas_vazias_exclui_sala_ocupada_no_dia_e_horario(client, db_session):
    persistir_turma(
        db_session,
        _turma_capturada(
            horarios=[Horario(codigo="6T2345", descricao="Sexta-feira 14:00 às 17:50")],
            sala=Sala(descricao="FCTE - I9/I10"),
        ),
        unidade="FCTE",
    )
    persistir_turma(
        db_session,
        _turma_capturada(
            numero="02",
            horarios=[Horario(codigo="2M12", descricao="Segunda-feira 08:00 às 09:50")],
            sala=Sala(descricao="FCTE - S1"),
        ),
        unidade="FCTE",
    )
    db_session.commit()

    response = client.get("/v1/salas/vazias", params={"dia": "sexta", "horario": "14:00"})

    assert response.status_code == 200
    assert [s["nome"] for s in response.json()] == ["S1"]


def test_listar_salas_vazias_sala_ocupada_so_em_outro_dia_nao_e_excluida(client, db_session):
    persistir_turma(
        db_session,
        _turma_capturada(horarios=[Horario(codigo="6T2345", descricao="Sexta-feira 14:00 às 17:50")]),
        unidade="FCTE",
    )
    db_session.commit()

    response = client.get("/v1/salas/vazias", params={"dia": "segunda", "horario": "14:00"})

    assert [s["nome"] for s in response.json()] == ["I9/I10"]


def test_listar_salas_vazias_sala_ocupada_so_em_outro_horario_nao_e_excluida(client, db_session):
    persistir_turma(
        db_session,
        _turma_capturada(horarios=[Horario(codigo="6T2345", descricao="Sexta-feira 14:00 às 17:50")]),
        unidade="FCTE",
    )
    db_session.commit()

    response = client.get("/v1/salas/vazias", params={"dia": "sexta", "horario": "08:00"})

    assert [s["nome"] for s in response.json()] == ["I9/I10"]


def test_listar_salas_vazias_dia_sem_aula_devolve_todas_as_salas(client, db_session):
    persistir_turma(
        db_session,
        _turma_capturada(horarios=[Horario(codigo="6T2345", descricao="Sexta-feira 14:00 às 17:50")]),
        unidade="FCTE",
    )
    db_session.commit()

    response = client.get("/v1/salas/vazias", params={"dia": "domingo", "horario": "14:00"})

    assert [s["nome"] for s in response.json()] == ["I9/I10"]


def test_listar_salas_vazias_horario_bem_formatado_mas_fora_da_grade_devolve_todas_as_salas(client, db_session):
    persistir_turma(
        db_session,
        _turma_capturada(horarios=[Horario(codigo="6T2345", descricao="Sexta-feira 14:00 às 17:50")]),
        unidade="FCTE",
    )
    db_session.commit()

    response = client.get("/v1/salas/vazias", params={"dia": "sexta", "horario": "09:00"})

    assert [s["nome"] for s in response.json()] == ["I9/I10"]


def test_listar_salas_vazias_exclui_sala_de_codigo_com_varios_segmentos(client, db_session):
    persistir_turma(
        db_session,
        _turma_capturada(horarios=[Horario(codigo="46M5  46T1", descricao="Quarta e sexta, 12:00 e 12:55")]),
        unidade="FCTE",
    )
    db_session.commit()

    quarta_meio_dia = client.get("/v1/salas/vazias", params={"dia": "quarta", "horario": "12:00"})
    sexta_doze_e_cinquenta_e_cinco = client.get("/v1/salas/vazias", params={"dia": "sexta", "horario": "12:55"})

    assert quarta_meio_dia.json() == []
    assert sexta_doze_e_cinquenta_e_cinco.json() == []


def test_listar_salas_vazias_horario_mal_formatado_e_422(client):
    response = client.get("/v1/salas/vazias", params={"dia": "sexta", "horario": "14h"})

    assert response.status_code == 422


def test_listar_salas_vazias_horario_com_digitos_de_outro_alfabeto_e_422(client):
    # \d do Python aceita dígitos de qualquer alfabeto ("١٤" em árabe), mas o
    # pattern da OpenAPI só aceita 0-9 e o teste de contrato acusava a diferença
    response = client.get("/v1/salas/vazias", params={"dia": "sexta", "horario": "١٤:٠٠"})

    assert response.status_code == 422


def test_listar_salas_vazias_dia_invalido_e_422(client):
    response = client.get("/v1/salas/vazias", params={"dia": "feriado", "horario": "14:00"})

    assert response.status_code == 422
