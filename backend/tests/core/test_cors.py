from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from app.core.database import get_db
from app.main import app
from app.models import Base


def test_x_total_count_e_exposto_no_cors():
    engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False}, poolclass=StaticPool)
    Base.metadata.create_all(engine)
    app.dependency_overrides[get_db] = lambda: Session(engine)

    client = TestClient(app)
    resposta = client.get("/v1/disciplinas?limite=5", headers={"Origin": "http://localhost:3000"})

    app.dependency_overrides.clear()
    assert "X-Total-Count" in resposta.headers.get("access-control-expose-headers", "")
