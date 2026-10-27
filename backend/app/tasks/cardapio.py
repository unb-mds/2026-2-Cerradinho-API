from celery import shared_task

from app.core.database import SessionLocal
from app.domain.cardapio import persistir_cardapio
from app.scrapers.cardapio import raspar_cardapio


@shared_task
def scrape_cardapio_task():
    itens = raspar_cardapio()

    db = SessionLocal()
    try:
        persistir_cardapio(db, itens)
        db.commit()
    finally:
        db.close()

    return {"itens_persistidos": len(itens)}
