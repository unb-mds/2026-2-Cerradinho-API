from celery import shared_task

from app.core.cache import invalidar_prefixo
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
        invalidar_prefixo("cache:v1:cardapio:semana:")
    finally:
        db.close()

    return {"itens_persistidos": len(itens)}
