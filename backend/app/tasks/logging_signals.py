from datetime import datetime, timezone
 
from celery.signals import task_failure, task_success
 
 
@task_success.connect
def log_success(sender=None, result=None, **kwargs):
    print(f"[{datetime.now(timezone.utc)}] SUCESSO - {sender.name}")
 
 
@task_failure.connect
def log_failure(sender=None, task_id=None, exception=None, **kwargs):
    print(f"[{datetime.now(timezone.utc)}] FALHA - {sender.name} - {exception}")