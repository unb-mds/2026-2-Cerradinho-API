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


def test_listar_salas_vazias_turma_com_sala_por_dia_ocupa_so_o_dia_certo(client, db_session):
    """Achado real: "24M5 24T1" com "FCTE - S1 / MOCAP" é segunda na S1 e
    quarta na MOCAP - a S1 não pode aparecer ocupada na quarta, nem a MOCAP
    na segunda."""
    persistir_turma(
        db_session,
        _turma_capturada(
            horarios=[Horario(codigo="24M5 24T1", descricao="Segunda e quarta, 12:00 às 13:50")],
            sala=Sala(descricao="FCTE - S1 / MOCAP"),
        ),
        unidade="FCTE",
    )
    db_session.commit()

    segunda_meio_dia = client.get("/v1/salas/vazias", params={"dia": "segunda", "horario": "12:00"})
    quarta_meio_dia = client.get("/v1/salas/vazias", params={"dia": "quarta", "horario": "12:00"})

    assert [s["nome"] for s in segunda_meio_dia.json()] == ["MOCAP"]
    assert [s["nome"] for s in quarta_meio_dia.json()] == ["S1"]


def test_listar_salas_vazias_exclui_sala_ocupada_a_noite(client, db_session):
    """Achado do Daniel: a grade noturna estava com os horários errados -
    confirmado contra turma real ("2N1234" ocupa de 19:00 às 22:30)."""
    persistir_turma(
        db_session,
        _turma_capturada(horarios=[Horario(codigo="2N1234", descricao="Segunda-feira 19:00 às 22:30")]),
        unidade="FCTE",
    )
    db_session.commit()

    response = client.get("/v1/salas/vazias", params={"dia": "segunda", "horario": "19:00"})

    assert response.json() == []


def test_listar_salas_vazias_turma_so_com_n3_e_n4_nao_ocupa_o_horario_da_n2(client, db_session):
    """"2N34" só ocupa a partir das 20:50 - não pode aparecer ocupada às
    19:50 (início da N2, que essa turma não usa)."""
    persistir_turma(
        db_session,
        _turma_capturada(horarios=[Horario(codigo="2N34", descricao="Segunda-feira 20:50 às 22:30")]),
        unidade="FCTE",
    )
    db_session.commit()

    as_19_50 = client.get("/v1/salas/vazias", params={"dia": "segunda", "horario": "19:50"})
    as_20_50 = client.get("/v1/salas/vazias", params={"dia": "segunda", "horario": "20:50"})

    assert [s["nome"] for s in as_19_50.json()] == ["I9/I10"]
    assert as_20_50.json() == []


def test_listar_salas_vazias_com_fim_exige_sala_livre_no_intervalo_todo(client, db_session):
    """De 14:00 a 15:50 cobre T2 e T3, então uma turma só na T3 já ocupa."""
    persistir_turma(
        db_session,
        _turma_capturada(horarios=[Horario(codigo="6T3", descricao="Sexta-feira 14:55 às 15:50")]),
        unidade="FCTE",
    )
    db_session.commit()

    as_14_sem_fim = client.get("/v1/salas/vazias", params={"dia": "sexta", "horario": "14:00"})
    das_14_as_15_50 = client.get("/v1/salas/vazias", params={"dia": "sexta", "horario": "14:00", "fim": "15:50"})
    das_16_as_17_50 = client.get("/v1/salas/vazias", params={"dia": "sexta", "horario": "16:00", "fim": "17:50"})

    assert [s["nome"] for s in as_14_sem_fim.json()] == ["I9/I10"]
    assert das_14_as_15_50.json() == []
    assert [s["nome"] for s in das_16_as_17_50.json()] == ["I9/I10"]


def test_listar_salas_vazias_meio_dia_cobre_a_virada_m5_t1(client, db_session):
    persistir_turma(
        db_session,
        _turma_capturada(horarios=[Horario(codigo="6T1", descricao="Sexta-feira 12:55 às 13:50")]),
        unidade="FCTE",
    )
    db_session.commit()

    response = client.get("/v1/salas/vazias", params={"dia": "sexta", "horario": "12:00", "fim": "13:50"})

    assert response.json() == []


def test_listar_salas_vazias_turma_em_sala_combinada_ocupa_cada_sala(client, db_session):
    """Turma em "I9/I10" ocupa a I9 e a I10, que existem como salas próprias."""
    persistir_turma(db_session, _turma_capturada(numero="01"), unidade="FCTE")
    for numero, sala in (("02", "FCTE - I9"), ("03", "FCTE - I10"), ("04", "FCTE - S1")):
        persistir_turma(
            db_session,
            _turma_capturada(
                numero=numero,
                horarios=[Horario(codigo="2M12", descricao="Segunda-feira 08:00 às 09:50")],
                sala=Sala(descricao=sala),
            ),
            unidade="FCTE",
        )
    db_session.commit()

    response = client.get("/v1/salas/vazias", params={"dia": "sexta", "horario": "14:00", "fim": "15:50"})

    assert [s["nome"] for s in response.json()] == ["S1"]


def test_listar_salas_vazias_nome_com_detalhe_ocupa_a_sala_certa(client, db_session):
    com_detalhe = _turma_capturada(numero="01", sala=Sala(descricao="FCTE - S10  (120 VAGAS)"))
    persistir_turma(db_session, com_detalhe, unidade="FCTE")
    persistir_turma(
        db_session,
        _turma_capturada(
            numero="02",
            horarios=[Horario(codigo="2M12", descricao="Segunda-feira 08:00 às 09:50")],
            sala=Sala(descricao="FCTE - S10"),
        ),
        unidade="FCTE",
    )
    db_session.commit()

    response = client.get("/v1/salas/vazias", params={"dia": "sexta", "horario": "14:00"})

    assert response.json() == []


def test_listar_salas_vazias_fim_mal_formatado_e_422(client):
    response = client.get("/v1/salas/vazias", params={"dia": "sexta", "horario": "14:00", "fim": "15h50"})

    assert response.status_code == 422


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
