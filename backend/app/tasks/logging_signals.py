from datetime import datetime, timezone
 
from celery.signals import task_failure, task_success

from app.core.database import SessionLocal
from app.core.exceptions import ErroFonteIndisponivel
from app.models import ExecucaoLog
 
 
@task_success.connect
def log_success(sender=None, result=None, **kwargs):
    print(f"[{datetime.now(timezone.utc)}] SUCESSO - {sender.name}")
    _gravar(task_name=sender.name, status="sucesso")
 
 
@task_failure.connect
def log_failure(sender=None, task_id=None, exception=None, **kwargs):
    print(f"[{datetime.now(timezone.utc)}] FALHA - {sender.name} - {exception}")
    tipo_falha = "fonte" if isinstance(exception, ErroFonteIndisponivel) else "interna"
    _gravar(task_name = sender.name, status = "falha", tipo_falha = tipo_falha, mensagem = str(exception))

def _gravar(task_name, status, tipo_falha=None, mensagem=None):
    db = SessionLocal()
    try:
        db.add(ExecucaoLog(
            task_name=task_name,
            status=status,
            tipo_falha=tipo_falha,
            mensagem=mensagem,
            criado_em=datetime.now(timezone.utc),
        ))
        db.commit()
    finally:
        db.close()