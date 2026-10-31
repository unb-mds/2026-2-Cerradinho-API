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


def test_listar_professores_busca_por_nome_parcial(client, db_session):
    persistir_turma(
        db_session,
        _turma_capturada(professores=[Professor(nome="André Luis Araújo"), Professor(nome="Carlos Lima")]),
        unidade="FCTE",
    )
    db_session.commit()

    response = client.get("/v1/professores", params={"nome": "luis"})

    assert [p["nome"] for p in response.json()] == ["André Luis Araújo"]


def test_listar_professores_busca_ignora_acento_e_caixa(client, db_session):
    persistir_turma(db_session, _turma_capturada(professores=[Professor(nome="André Luis Araújo")]), unidade="FCTE")
    db_session.commit()

    response = client.get("/v1/professores", params={"nome": "andre araujo"})

    assert len(response.json()) == 1
    assert response.json()[0]["nome"] == "André Luis Araújo"


def test_listar_professores_busca_sem_match_retorna_lista_vazia(client, db_session):
    persistir_turma(db_session, _turma_capturada(), unidade="FCTE")
    db_session.commit()

    response = client.get("/v1/professores", params={"nome": "zzz"})

    assert response.json() == []


def test_obter_agenda_professor_inexistente_e_404(client):
    response = client.get("/v1/professores/999/agenda")

    assert response.status_code == 404


def test_obter_agenda_decompoe_horario_em_dia_inicio_fim_com_sala(client, db_session):
    persistir_turma(db_session, _turma_capturada(), unidade="FCTE")
    db_session.commit()
    professor_id = client.get("/v1/professores").json()[0]["id"]

    response = client.get(f"/v1/professores/{professor_id}/agenda")

    assert response.status_code == 200
    body = response.json()
    assert body["nome"] == "Ana Souza"
    assert len(body["turmas"]) == 1
    turma = body["turmas"][0]
    assert turma["disciplina_codigo"] == "FGA0242"
    assert turma["numero"] == "01"
    assert len(turma["horarios"]) == 1
    bloco = turma["horarios"][0]
    assert (bloco["dia"], bloco["inicio"], bloco["fim"]) == ("sexta", "14:00", "17:50")
    assert isinstance(bloco["sala"]["id"], int)
    assert (bloco["sala"]["predio"], bloco["sala"]["nome"]) == ("FCTE", "I9/I10")


def test_obter_agenda_turma_sem_sala_vem_com_sala_nula(client, db_session):
    persistir_turma(db_session, _turma_capturada(sala=Sala(descricao="")), unidade="FCTE")
    db_session.commit()
    professor_id = client.get("/v1/professores").json()[0]["id"]

    response = client.get(f"/v1/professores/{professor_id}/agenda")

    assert response.json()["turmas"][0]["horarios"][0]["sala"] is None


def test_obter_agenda_junta_aulas_consecutivas_num_bloco_so(client, db_session):
    persistir_turma(
        db_session,
        _turma_capturada(horarios=[Horario(codigo="2M12", descricao="Segunda-feira 08:00 às 09:50")]),
        unidade="FCTE",
    )
    db_session.commit()
    professor_id = client.get("/v1/professores").json()[0]["id"]

    response = client.get(f"/v1/professores/{professor_id}/agenda")

    blocos = response.json()["turmas"][0]["horarios"]
    assert len(blocos) == 1
    assert blocos[0]["dia"] == "segunda"
    assert blocos[0]["inicio"] == "08:00"
    assert blocos[0]["fim"] == "09:50"


def test_obter_agenda_turma_com_sala_por_dia_mostra_a_sala_certa_em_cada_bloco(client, db_session):
    """Achado real do Vitor (RF17/ADR 0010): "24M5 24T1" com "FCTE - S1 /
    MOCAP" é segunda na S1 e quarta na MOCAP - a agenda do professor
    precisa mostrar a sala certa em cada dia, não a mesma nos dois."""
    persistir_turma(
        db_session,
        _turma_capturada(
            horarios=[Horario(codigo="24M5 24T1", descricao="Segunda e quarta, 12:00 às 13:50")],
            sala=Sala(descricao="FCTE - S1 / MOCAP"),
        ),
        unidade="FCTE",
    )
    db_session.commit()
    professor_id = client.get("/v1/professores").json()[0]["id"]

    response = client.get(f"/v1/professores/{professor_id}/agenda")

    blocos = response.json()["turmas"][0]["horarios"]
    salas_por_dia = {b["dia"]: b["sala"]["nome"] for b in blocos}
    assert salas_por_dia == {"segunda": "S1", "quarta": "MOCAP"}
