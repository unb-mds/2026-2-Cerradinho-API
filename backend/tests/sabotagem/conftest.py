"""Testes de sabotagem (RNF09): quebram a fonte de propósito e conferem que
a falha aparece no log de execução com o tipo certo, sem apagar nem
sobrescrever o que já estava no banco.

Cada cenário roda a task de verdade pelo Celery (`.apply()`), com o
scraper, o parser, o domínio e os signals de log reais. Só a borda com o
mundo externo é trocada por um dublê: o Playwright no SIGAA e o
`requests.get` no RU. Todo cenário tem um caso de controle sem sabotagem,
para provar que o dublê funciona e que a falha vem da sabotagem, não do
próprio teste.
"""

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

import app.tasks.cardapio as cardapio_task
import app.tasks.logging_signals as logging_signals
import app.tasks.scraping as scraping_task
from app.domain.execucoes import listar_execucoes
from app.models import Base


@pytest.fixture
def banco(monkeypatch):
    """Sessão de um sqlite em memória compartilhado pelas tasks e pelos
    signals de log, como o Postgres é compartilhado em produção."""
    engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False}, poolclass=StaticPool)
    Base.metadata.create_all(engine)
    fabrica = sessionmaker(bind=engine)
    for modulo in (logging_signals, cardapio_task, scraping_task):
        monkeypatch.setattr(modulo, "SessionLocal", fabrica)
    with fabrica() as sessao:
        yield sessao
    engine.dispose()


@pytest.fixture
def execucao_registrada(banco):
    """Devolve a única execução gravada no log, lida como a API lê
    (`GET /v1/execucoes`)."""

    def ler():
        banco.expire_all()
        execucoes = listar_execucoes(banco)
        assert len(execucoes) == 1, f"esperava uma execução registrada, achei {len(execucoes)}"
        return execucoes[0]

    return ler
