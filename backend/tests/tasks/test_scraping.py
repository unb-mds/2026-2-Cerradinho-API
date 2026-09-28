from sqlalchemy import create_engine
from sqlalchemy.orm import Session

import app.tasks.scraping as scraping_task
from app.models import Base, Turma
from app.schemas.disciplina import Horario, Professor, Sala
from app.schemas.disciplina import Turma as TurmaCapturada


def _in_memory_session() -> Session:
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    return Session(engine)


def _turma_capturada(**overrides) -> TurmaCapturada:
    base = dict(
        disciplina_codigo="FGA0242",
        disciplina_nome="Métodos de Desenvolvimento de Software",
        numero="01",
        ano_periodo="2026.2",
        professores=[Professor(nome="Ana Souza")],
        horarios=[Horario(codigo="6T2345", descricao="Sexta-feira 14:00 às 17:50")],
        sala=Sala(descricao="FCTE - I9/I10"),
        vagas_ofertadas=40,
        vagas_ocupadas=38,
    )
    base.update(overrides)
    return TurmaCapturada(**base)


async def _raspagem_falsa(nivel, ano, periodo, unidades):
    # simula o retorno de raspar_disciplinas_varias_unidades pra duas
    # unidades, sem precisar subir Playwright/rede nenhuma
    return {
        "FCTE": [_turma_capturada()],
        "FUP": [_turma_capturada(disciplina_codigo="FUP0001", disciplina_nome="Outra Disciplina", numero="02")],
    }


def test_scrape_disciplinas_task_persiste_turmas_de_cada_unidade(monkeypatch):
    """Regressão do bug do Vitor: a task chamava uma função que não existe
    (`scrape_disciplinas`) e nunca gravava nada no banco. Esse teste chama a
    task de ponta a ponta (com o scraper trocado por um dublê) — é o teste
    que teria pego o ImportError antes de virar bug em produção."""
    session = _in_memory_session()
    monkeypatch.setattr(scraping_task, "SessionLocal", lambda: session)
    monkeypatch.setattr(scraping_task, "raspar_disciplinas_varias_unidades", _raspagem_falsa)

    total = scraping_task.scrape_disciplinas_task.run(nivel="G", ano="2026", periodo="2")

    assert total == 2
    turmas = session.query(Turma).all()
    assert {t.unidade for t in turmas} == {"FCTE", "FUP"}


def test_scrape_disciplinas_task_varre_todas_as_unidades_por_padrao(monkeypatch):
    """`unidades=None` (o default usado pelo agendamento em celery_app.py)
    precisa varrer todas as unidades, não uma só."""
    unidades_recebidas = {}

    async def raspagem_espia(nivel, ano, periodo, unidades):
        unidades_recebidas["valor"] = unidades
        return {}

    session = _in_memory_session()
    monkeypatch.setattr(scraping_task, "SessionLocal", lambda: session)
    monkeypatch.setattr(scraping_task, "raspar_disciplinas_varias_unidades", raspagem_espia)

    scraping_task.scrape_disciplinas_task.run(nivel="G", ano="2026", periodo="2")

    assert unidades_recebidas["valor"] is None
