from sqlalchemy.exc import OperationalError

from app.core.database import get_db
from app.main import app


def test_health_responde_ok_com_banco_acessivel(client):
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok", "banco": "ok"}


def test_health_responde_503_sem_banco(client):
    class _BancoForaDoAr:
        def execute(self, *args, **kwargs):
            raise OperationalError("SELECT 1", {}, Exception("connection refused"))

    app.dependency_overrides[get_db] = lambda: _BancoForaDoAr()

    response = client.get("/health")

    assert response.status_code == 503
    assert response.json()["banco"] == "indisponivel"
