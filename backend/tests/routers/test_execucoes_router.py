from datetime import datetime, timedelta, timezone

from app.models import ExecucaoLog


def test_listar_execucoes_ordena_da_mais_recente(client, db_session):
    agora =  datetime.now(timezone.utc)
    db_session.add_all([
        ExecucaoLog(task_name = "t1", status = "sucesso", criado_em = agora - timedelta(minutes = 5)),
        ExecucaoLog(task_name = "t2", status = "falha", tipo_falha = "fonte", criado_em = agora)])
    db_session.commit()

    response = client.get("/v1/execucoes")

    assert response.status_code == 200
    assert [e["task_name"] for e in response.json()] == ["t2", "t1"]