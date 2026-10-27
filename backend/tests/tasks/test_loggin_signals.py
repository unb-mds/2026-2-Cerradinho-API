from types import SimpleNamespace

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

import app.tasks.logging_signals as logging_signals
from app.core.exceptions import ErroFonteIndisponivel
from app.models import Base, ExecucaoLog


def _in_memory_session() -> Session:
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    return Session(engine)

def test_log_success_grava_execucao_com_sucesso(monkeypatch):
    session = _in_memory_session()
    monkeypatch.setattr(logging_signals, "SessionLocal", lambda: session)

    logging_signals.log_success(sender = SimpleNamespace(name = "app.tasks.cardapio.scrape_cardapio_task"))

    registro = session.query(ExecucaoLog).one()
    assert registro.status == "sucesso"
    assert registro.tipo_falha is None

def test_log_failure_classifica_falha_da_fonte(monkeypatch):
    session = _in_memory_session()
    monkeypatch.setattr(logging_signals, "SessionLocal", lambda: session)

    logging_signals.log_failure(sender = SimpleNamespace(name = "app.tasks.cardapio.scrape_disciplinas_task"),
                                 exception = ErroFonteIndisponivel("SIGAA fora do ar"))

    registro = session.query(ExecucaoLog).one()
    assert registro.status == "falha"
    assert registro.tipo_falha == "fonte"

def test_log_failure_classifica_falha_interna(monkeypatch):
    session = _in_memory_session()
    monkeypatch.setattr(logging_signals, "SessionLocal", lambda: session)

    logging_signals.log_failure(sender = SimpleNamespace(name = "app.tasks.cardapio.scrape_disciplinas_task"),
                                 exception = ValueError("bug de parsing"))

    registro = session.query(ExecucaoLog).one()
    assert registro.status == "falha"
    assert registro.tipo_falha == "interna"