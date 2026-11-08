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


def test_obter_resumo_sem_dado_devolve_zeros(client):
    response = client.get("/v1/resumo")

    assert response.status_code == 200
    assert response.json() == {"turmas": 0, "disciplinas": 0, "professores": 0, "salas": 0}


def test_obter_resumo_conta_cada_dominio(client, db_session):
    persistir_turma(db_session, _turma_capturada(numero="01"), unidade="FCTE")
    persistir_turma(
        db_session,
        _turma_capturada(
            disciplina_codigo="FGA0001",
            disciplina_nome="Outra Disciplina",
            numero="02",
            professores=[Professor(nome="Carlos Lima")],
            sala=Sala(descricao="FCTE - S1"),
        ),
        unidade="FCTE",
    )
    db_session.commit()

    response = client.get("/v1/resumo")

    assert response.json() == {"turmas": 2, "disciplinas": 2, "professores": 2, "salas": 2}
