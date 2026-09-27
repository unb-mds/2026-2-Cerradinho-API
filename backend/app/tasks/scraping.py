import asyncio

from celery import shared_task

from app.core.database import SessionLocal
from app.domain.disciplinas import persistir_turmas
from app.scrapers.disciplinas import raspar_disciplinas_varias_unidades

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
            persistir_turmas(db, turmas, unidade)
            total += len(turmas)
        db.commit()
        return total
    finally:
        db.close()
