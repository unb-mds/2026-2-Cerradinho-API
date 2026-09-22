from celery import Celery
from celery.schedules import crontab

# "redis" (não "localhost") porque, dentro da rede do docker compose,
# o nome do serviço funciona como hostname
celery_app = Celery(
    "cerradinho",
    broker="redis://redis:6379/0",
    backend="redis://redis:6379/1",
)

# RF15 — roda o scraper de Disciplinas todo dia às 3h da manhã
celery_app.conf.beat_schedule = {
    "scrape-disciplinas-semanal": {
        "task": "app.tasks.scraping.scrape_disciplinas_task",
        "schedule": crontab(hour=5, minute=0, day_of_week=0),
    },
}
 
# descobre as tasks dentro de app/tasks/ automaticamente
celery_app.autodiscover_tasks(["app.tasks"])

 # registra os signals de log (RF16) assim que o Celery inicializa
import app.tasks.logging_signals
