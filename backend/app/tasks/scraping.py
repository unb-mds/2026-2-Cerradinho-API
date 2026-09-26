from celery import shared_task

from app.scrapers.disciplinas.scraper import scrape_disciplinas


@shared_task
def scrape_disciplinas_task(unidade: str = "FCTE"):
    return scrape_disciplinas(unidade)