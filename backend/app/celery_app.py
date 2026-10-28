from celery import Celery
from celery.schedules import crontab

from app.core.config import settings
from app.tasks import logging_signals  # noqa: F401 (importa os signals de log (RF16) para registrar no Celery)

# O endereço vem do REDIS_URL (ver app/core/config.py): no docker compose o
# padrão aponta para o serviço "redis", e no Railway para o Redis do projeto
celery_app = Celery(
    "cerradinho",
    broker=settings.redis_url,
    backend=settings.redis_url,
    include=[
        "app.tasks.scraping",
        "app.tasks.cardapio"
        ],
)

celery_app.conf.timezone = "America/Sao_Paulo"

# RF15: disciplinas todo domingo às 3h e cardápio todo dia às 5h
celery_app.conf.beat_schedule = {
    "scrape-disciplinas-semanal": {
        "task": "app.tasks.scraping.scrape_disciplinas_task",
        "schedule": crontab(hour=3, minute=0, day_of_week=0),
        "kwargs": {"nivel": "G", "ano": "2026", "periodo": "2"},
    },
    "scrape-cardapio-diario": {
        "task": "app.tasks.cardapio.scrape_cardapio_task",
        "schedule": crontab(hour=5, minute=0),
    },
}
