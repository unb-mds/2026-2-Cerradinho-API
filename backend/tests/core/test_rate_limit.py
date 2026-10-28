from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from app.core.database import get_db
from app.core.rate_limit import limiter
from app.main import app
from app.models import Base


def test_excede_o_limite(monkeypatch):
    monkeypatch.setattr(limiter, "enabled", True)
    monkeypatch.setattr(limiter, "_default_limits", limiter._default_limits[:1])

    engine = create_engine( "sqlite:///:memory:", connect_args={"check_same_thread": False}, poolclass = StaticPool)
    Base.metadata.create_all(engine)
    app.dependency_overrides[get_db] = lambda: Session(engine)

    client = TestClient(app)
    respostas = [client.get("/v1/salas") for _ in range(65)]

    app.dependency_overrides.clear()
    assert any(r.status_code == 429 for r in respostas)