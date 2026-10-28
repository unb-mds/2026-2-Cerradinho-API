import subprocess
import sys
from pathlib import Path

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

import app.tasks.cardapio as cardapio_task
import app.tasks.logging_signals as logging_signals
import app.tasks.scraping as scraping_task
from app.core.exceptions import ErroFonteIndisponivel
from app.models import Base, ExecucaoLog

BACKEND_DIR = Path(__file__).resolve().parents[2]

# sobe o celery_app como o worker sobe e roda duas tasks; o log tem que sair
# sem ninguém importar app.tasks.logging_signals na mão
_WORKER_COM_TASKS = """
import sys
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import app.core.database as database
database.SessionLocal = sessionmaker(bind=create_engine(sys.argv[1]))

from app.celery_app import celery_app
from app.core.exceptions import ErroFonteIndisponivel

@celery_app.task(name="teste.sucesso")
def sucesso():
    return 1

@celery_app.task(name="teste.falha")
def falha():
    raise ErroFonteIndisponivel("RU fora do ar")

sucesso.apply()
falha.apply()
"""


@pytest.fixture
def banco(monkeypatch):
    engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False}, poolclass=StaticPool)
    Base.metadata.create_all(engine)
    sessao = sessionmaker(bind=engine)
    monkeypatch.setattr(logging_signals, "SessionLocal", sessao)
    monkeypatch.setattr(cardapio_task, "SessionLocal", sessao)
    monkeypatch.setattr(scraping_task, "SessionLocal", sessao)
    return sessao()


def _registros(banco):
    return [(r.task_name, r.status, r.tipo_falha) for r in banco.query(ExecucaoLog)]


def _fonte_fora_do_ar(*args, **kwargs):
    raise ErroFonteIndisponivel("fonte fora do ar")


async def _sigaa_fora_do_ar(*args, **kwargs):
    raise ErroFonteIndisponivel("SIGAA fora do ar")


def test_task_do_cardapio_que_roda_bem_gera_log_de_sucesso(banco, monkeypatch):
    monkeypatch.setattr(cardapio_task, "raspar_cardapio", lambda: [])

    cardapio_task.scrape_cardapio_task.apply()

    assert _registros(banco) == [("app.tasks.cardapio.scrape_cardapio_task", "sucesso", None)]


@pytest.mark.parametrize(
    "task, modulo, funcao, raspagem, kwargs",
    [
        (cardapio_task.scrape_cardapio_task, cardapio_task, "raspar_cardapio", _fonte_fora_do_ar, {}),
        (
            scraping_task.scrape_disciplinas_task,
            scraping_task,
            "raspar_disciplinas_varias_unidades",
            _sigaa_fora_do_ar,
            {"nivel": "G", "ano": "2026", "periodo": "2"},
        ),
    ],
    ids=["cardapio", "disciplinas"],
)
def test_fonte_fora_do_ar_gera_log_de_falha_da_fonte(banco, monkeypatch, task, modulo, funcao, raspagem, kwargs):
    # se a task engolir o erro do scraper, o log diz "sucesso" e ninguém fica sabendo
    monkeypatch.setattr(modulo, funcao, raspagem)

    task.apply(kwargs=kwargs)

    assert _registros(banco) == [(task.name, "falha", "fonte")]


def test_worker_grava_log_sem_importar_os_signals_na_mao(tmp_path):
    # regressão: se o import de logging_signals sair do celery_app.py, os testes
    # acima continuam passando, mas em produção nenhuma execução é registrada
    url = f"sqlite:///{(tmp_path / 'log.db').as_posix()}"
    engine = create_engine(url)
    Base.metadata.create_all(engine)

    subprocess.run(
        [sys.executable, "-c", _WORKER_COM_TASKS, url], cwd=BACKEND_DIR, capture_output=True, text=True, check=True
    )

    with sessionmaker(bind=engine)() as banco:
        assert sorted(_registros(banco)) == [("teste.falha", "falha", "fonte"), ("teste.sucesso", "sucesso", None)]
    engine.dispose()
