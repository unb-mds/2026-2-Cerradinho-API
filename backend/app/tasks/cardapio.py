from celery import shared_task

from app.core.database import SessionLocal
from app.domain.cardapio import persistir_cardapio
from app.scrapers.cardapio.parser import encontrar_pdf_da_semana, extrair_itens_cardapio, extrair_links_cardapio
from app.scrapers.cardapio.scraper import baixar_html, baixar_pdf


@shared_task
def scrape_cardapio_task():
    html = baixar_html()
    links = extrair_links_cardapio(html)
    url_pdf = encontrar_pdf_da_semana(links)
    if url_pdf is None:
        raise RuntimeError("Nenhum PDF de cardápio encontrado para a semana atual.")

    pdf_bytes = baixar_pdf(url_pdf)
    itens = extrair_itens_cardapio(pdf_bytes)

    db = SessionLocal()
    try:
        persistir_cardapio(db, itens)
        db.commit()
    finally:
        db.close()

    return {"itens_persistidos": len(itens)}