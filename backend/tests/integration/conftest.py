import os
from pathlib import Path

import pytest
from alembic.config import Config
from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import Session

from alembic import command
from app.core.config import settings

BACKEND_DIR = Path(__file__).resolve().parents[2]


@pytest.fixture(scope="session")
def engine_postgres():
    # sqlite não valida o tamanho de String(n), então estouros de coluna só
    # aparecem num postgres de verdade - por isso esses testes não usam sqlite
    engine = create_engine(settings.database_url, connect_args={"connect_timeout": 3})
    try:
        engine.connect().close()
    except OperationalError:
        # no CI o postgres é obrigatório: pular aqui esconderia uma falha
        if os.environ.get("CI"):
            raise
        pytest.skip(f"postgres indisponível em {settings.postgres_host}:{settings.postgres_port}")

    # schema criado pelas migrations, igual em produção (e não pelo create_all)
    config = Config()
    config.set_main_option("script_location", str(BACKEND_DIR / "alembic"))
    command.upgrade(config, "head")

    yield engine
    engine.dispose()


@pytest.fixture
def sessao_postgres(engine_postgres):
    # tudo roda dentro de uma transação desfeita no fim - nada fica gravado no banco
    conexao = engine_postgres.connect()
    transacao = conexao.begin()
    sessao = Session(bind=conexao, join_transaction_mode="create_savepoint")

    yield sessao

    sessao.close()
    transacao.rollback()
    conexao.close()
