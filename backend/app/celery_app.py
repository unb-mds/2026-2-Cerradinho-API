from celery import Celery
from celery.schedules import crontab

from app.tasks import logging_signals  # noqa: F401 (importa os signals de log (RF16) para registrar no Celery)

# "redis" (não "localhost") porque, dentro da rede do docker compose,
# o nome do serviço funciona como hostname
celery_app = Celery(
    "cerradinho",
    broker="redis://redis:6379/0",
    backend="redis://redis:6379/1",
    include=[
        "app.tasks.scraping",
        "app.tasks.cardapio"
        ],
)

celery_app.conf.timezone = "America/Sao_Paulo"

# RF15 — roda o scraper de Disciplinas todo domingo às 5h da manhã
celery_app.conf.beat_schedule = {
    "scrape-disciplinas-semanal": {
        "task": "app.tasks.scraping.scrape_disciplinas_task",
        "schedule": crontab(hour=3, minute=0, day_of_week=0),
    },
    "scrape-cardapio-diario": {
        "task": "app.tasks.cardapio.scrape_cardapio_task",
        "schedule": crontab(hour=5, minute=0),
    },
}
