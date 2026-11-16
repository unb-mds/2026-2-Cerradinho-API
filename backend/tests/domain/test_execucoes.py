"""Leitura do log de execução (RF16) direto no domínio, sem passar pela
rota. Escritos a partir dos mutantes sobreviventes do teste de mutação
(RNF09): o teste da rota só conferia a ordem."""

from datetime import datetime, timedelta, timezone

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from app.domain.execucoes import LIMITE_PADRAO, listar_execucoes
from app.models import Base, ExecucaoLog

INICIO = datetime(2026, 11, 1, 3, 0, tzinfo=timezone.utc)


def _sessao_com_execucoes(quantidade: int) -> Session:
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    sessao = Session(engine)
    sessao.add_all(
        ExecucaoLog(task_name=f"task-{n}", status="sucesso", criado_em=INICIO + timedelta(minutes=n))
        for n in range(quantidade)
    )
    sessao.commit()
    return sessao


def test_listar_execucoes_devolve_as_50_mais_recentes_por_padrao():
    sessao = _sessao_com_execucoes(LIMITE_PADRAO + 1)

    execucoes = listar_execucoes(sessao)

    assert LIMITE_PADRAO == 50
    assert len(execucoes) == 50
    assert execucoes[0].task_name == "task-50"
    assert execucoes[-1].task_name == "task-1"


def test_listar_execucoes_respeita_o_limite_pedido():
    sessao = _sessao_com_execucoes(5)

    assert [e.task_name for e in listar_execucoes(sessao, limite=2)] == ["task-4", "task-3"]


def test_listar_execucoes_devolve_criado_em_em_utc_mesmo_quando_o_banco_descarta_o_fuso():
    # o sqlite devolve o datetime sem fuso; a API tem que devolver com
    sessao = _sessao_com_execucoes(1)

    [execucao] = listar_execucoes(sessao)

    assert execucao.criado_em == INICIO
    assert execucao.criado_em.tzinfo == timezone.utc
