from pathlib import Path

import pytest
from sqlalchemy.exc import DataError

from app.domain.disciplinas import normalizar_sala, persistir_turma, persistir_turmas
from app.models import Disciplina, Horario, Professor, Sala, Turma
from app.schemas.disciplina import Horario as HorarioCapturado
from app.scrapers.disciplinas.parser import parse_turmas

FIXTURE = Path(__file__).parents[1] / "scrapers" / "fixtures" / "turmas_fcte_gama_2026_2.html"


def _turmas_da_fixture():
    return parse_turmas(FIXTURE.read_text(encoding="utf-8"))


def test_pipeline_grava_todas_as_turmas_da_fixture_no_postgres(sessao_postgres):
    turmas = _turmas_da_fixture()

    persistir_turmas(sessao_postgres, turmas, unidade="FCTE")
    sessao_postgres.flush()

    assert sessao_postgres.query(Turma).count() == len(turmas)
    assert sessao_postgres.query(Disciplina).count() == len({t.disciplina_codigo for t in turmas})
    assert sessao_postgres.query(Professor).count() == len({p.nome for t in turmas for p in t.professores})
    assert sessao_postgres.query(Sala).count() == len(
        {normalizar_sala(t.sala.descricao) for t in turmas if t.sala.descricao.strip()}
    )
    assert sessao_postgres.query(Horario).count() == sum(len(t.horarios) for t in turmas)


def test_pipeline_grava_os_valores_extraidos_do_sigaa(sessao_postgres):
    persistir_turmas(sessao_postgres, _turmas_da_fixture(), unidade="FCTE")
    sessao_postgres.flush()

    turma = (
        sessao_postgres.query(Turma)
        .join(Disciplina)
        .filter(Disciplina.codigo == "FCTE0005", Turma.numero == "01")
        .one()
    )
    assert turma.disciplina.nome == "ALGORITMOS EM GRAFOS"
    assert turma.ano_periodo == "2026.2"
    assert turma.unidade == "FCTE"
    assert (turma.vagas_ofertadas, turma.vagas_ocupadas) == (80, 77)
    assert (turma.sala.predio, turma.sala.nome) == ("FCTE", "I9/I10")
    assert [p.nome for p in turma.professores] == ["EDSON ALVES DA COSTA JUNIOR (60h)"]
    # só o código, sem o intervalo de datas que o SIGAA junta no mesmo texto
    assert [(h.codigo, h.descricao) for h in turma.horarios] == [("6T2345", "Sexta-feira 14:00 às 17:50")]


def test_pipeline_rodado_duas_vezes_nao_duplica_turmas(sessao_postgres):
    # o agendamento (RF15) roda o scraper de novo sobre as mesmas turmas
    turmas = _turmas_da_fixture()

    persistir_turmas(sessao_postgres, turmas, unidade="FCTE")
    persistir_turmas(sessao_postgres, turmas, unidade="FCTE")
    sessao_postgres.flush()

    assert sessao_postgres.query(Turma).count() == len(turmas)
    assert sessao_postgres.query(Horario).count() == sum(len(t.horarios) for t in turmas)


def test_postgres_recusa_codigo_de_horario_maior_que_a_coluna(sessao_postgres):
    # regressão do bug do horário: no sqlite isso passava, no postgres estoura o String(20)
    turma = _turmas_da_fixture()[0].model_copy(
        update={"horarios": [HorarioCapturado(codigo="6T2345 (10/08/2026 - 14/12/2026)", descricao="Sexta-feira")]}
    )

    with pytest.raises(DataError):
        persistir_turma(sessao_postgres, turma, unidade="FCTE")
        sessao_postgres.flush()
