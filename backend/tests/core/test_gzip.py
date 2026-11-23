from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_resposta_grande_vem_comprimida_quando_o_cliente_aceita_gzip():
    # O schema OpenAPI tem dezenas de KB, bem acima do mínimo de 1 KB.
    resposta = client.get("/openapi.json", headers={"Accept-Encoding": "gzip"})

    assert resposta.status_code == 200
    assert resposta.headers.get("content-encoding") == "gzip"
    assert "Accept-Encoding" in resposta.headers.get("vary", "")
    # O TestClient descomprime sozinho: o conteúdo continua o mesmo JSON.
    assert resposta.json()["info"]["title"] == "Cerradinho API"


def test_sem_accept_encoding_gzip_a_resposta_vai_sem_compressao():
    resposta = client.get("/openapi.json", headers={"Accept-Encoding": "identity"})

    assert resposta.status_code == 200
    assert "content-encoding" not in resposta.headers


def test_resposta_pequena_vai_sem_compressao():
    resposta = client.get("/health", headers={"Accept-Encoding": "gzip"})

    assert len(resposta.content) < 1000
    assert "content-encoding" not in resposta.headers
