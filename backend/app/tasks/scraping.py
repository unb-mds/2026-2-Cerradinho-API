import asyncio
import logging

from celery import shared_task

from app.core.cache import invalidar
from app.core.database import SessionLocal
from app.domain.disciplinas import persistir_turmas
from app.scrapers.disciplinas import raspar_disciplinas_varias_unidades

logger = logging.getLogger(__name__)

NIVEL = "G"
UNIDADE_FCTE = "673"
ANO = "2026"
PERIODO = "2"

@shared_task
def scrape_disciplinas_task(
    nivel: str,
    ano: str,
    periodo: str,
    unidades: list[str] | None = None,
) -> int:
    """Roda o scraper de Disciplinas (RF01) e persiste o resultado (RF15).

    unidades=None varre todas as unidades listadas no formulário do SIGAA
    (é o modo usado pelo agendamento — ver celery_app.py). Devolve o total
    de turmas persistidas, pra aparecer no log de sucesso (RF16).
    """
    turmas_por_unidade = asyncio.run(raspar_disciplinas_varias_unidades(nivel, ano, periodo, unidades))

    db = SessionLocal()
    try:
        total = 0
        for unidade, turmas in turmas_por_unidade.items():
            try:
                persistidas = persistir_turmas(db, turmas, unidade)
                db.commit()
                total += len(persistidas)
            except Exception:
                # uma unidade com erro não pode levar as outras já persistidas
                # junto na rolagem de volta - commit por unidade, não um só no fim.
                db.rollback()
                logger.exception("Falha ao persistir a unidade %s, pulando", unidade)
        invalidar("cache:v1:disciplinas")
        invalidar("cache:v1:professores")
        invalidar("cache:v1:salas")
        return total
    finally:
        db.close()