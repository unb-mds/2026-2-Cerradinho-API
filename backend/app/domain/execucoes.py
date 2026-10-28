from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.models import ExecucaoLog
from app.schemas.api.execucao import Execucao

LIMITE_PADRAO = 50


def _em_utc(momento: datetime) -> datetime:
    # o log é gravado em UTC, mas nem todo banco devolve o fuso junto (o sqlite descarta)
    return momento if momento.tzinfo else momento.replace(tzinfo=timezone.utc)


def listar_execucoes(session: Session, limite: int = LIMITE_PADRAO) -> list[Execucao]:

    execucoes = (session.query(ExecucaoLog).order_by(ExecucaoLog.criado_em.desc()).limit(limite).all())

    return [Execucao (id = e.id, task_name = e.task_name, status = e.status, tipo_falha = e.tipo_falha,
                      mensagem = e.mensagem, criado_em = _em_utc(e.criado_em)) for e in execucoes]
