def test_health_responde_ok_com_banco_acessivel(client):
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok", "banco": "ok"}
