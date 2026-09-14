from celery import Celery

# "redis" (não "localhost") porque, dentro da rede do docker compose,
# o nome do serviço funciona como hostname
celery_app = Celery(
    "cerradinho",
    broker="redis://redis:6379/0",
    backend="redis://redis:6379/1",
)


@celery_app.task
def ping():
    return "pong"