import asyncio

from celery import shared_task

from app.scrapers.disciplinas.scraper import DisciplinasScraper
from app.scrapers.disciplinas.parser import parse_turmas
from app.core.database import SessionLocal
from app.domain.disciplinas import persistir_turma, persistir_turmas

NIVEL = "G"
UNIDADE_FCTE = "673"
ANO = "2026"
PERIODO = "2"

@shared_task
def scrape_disciplinas_task(unidade: str = "673"):
    scraper = DisciplinasScraper()
    html = asyncio.run(scraper.buscar_html(NIVEL, unidade, ANO, PERIODO))
    turmas = parse_turmas(html)

    db = SessionLocal()
    try:
        persistir_turmas(db, turmas, unidade)
        db.commit()
    finally:
        db.close()

    return {"unidade":unidade, "turmas_persistidas": len(turmas)}