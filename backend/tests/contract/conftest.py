import pytest
import schemathesis
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from app.core.database import get_db
from app.main import app
from app.models import Base


@pytest.fixture
def api_schema():
    # banco sqlite em memória no lugar do postgres, igual aos testes de routers -
    # o schemathesis chama o app via ASGI, sem precisar subir servidor nem banco real
    engine = create_engine(
        "sqlite:///:memory:", connect_args={"check_same_thread": False}, poolclass=StaticPool
    )
    Base.metadata.create_all(engine)
    db_session = Session(engine)

    app.dependency_overrides[get_db] = lambda: db_session
    yield schemathesis.openapi.from_asgi("/openapi.json", app)
    app.dependency_overrides.clear()
    db_session.close()
