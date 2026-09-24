from datetime import date

from app.domain.cardapio import persistir_cardapio
from app.schemas.cardapio import ItemCardapio


def test_listar_cardapio_semana_retorna_itens_desagrupados(client, db_session):
    itens = [
        ItemCardapio(
            data=date(2026, 9, 14), refeicao="almoco", categoria="Prato Principal Padrão", item="Frango grelhado"
        ),
        ItemCardapio(data=date(2026, 9, 14), refeicao="almoco", categoria="Guarnição", item="Arroz e feijão"),
    ]
    persistir_cardapio(db_session, itens)
    db_session.commit()

    response = client.get("/v1/cardapio/semana", params={"data_inicio": "2026-09-14"})

    assert response.status_code == 200
    assert response.json() == [
        {
            "data": "2026-09-14",
            "refeicao": "almoco",
            "categoria": "Prato Principal Padrão",
            "item": "Frango grelhado",
        },
        {"data": "2026-09-14", "refeicao": "almoco", "categoria": "Guarnição", "item": "Arroz e feijão"},
    ]


def test_listar_cardapio_semana_fora_do_intervalo_nao_aparece(client, db_session):
    persistir_cardapio(
        db_session,
        [ItemCardapio(data=date(2026, 9, 1), refeicao="jantar", categoria="Sopa", item="Sopa de legumes")],
    )
    db_session.commit()

    response = client.get("/v1/cardapio/semana", params={"data_inicio": "2026-09-14"})

    assert response.status_code == 200
    assert response.json() == []


def test_listar_cardapio_semana_sem_data_inicio_usa_hoje(client):
    response = client.get("/v1/cardapio/semana")

    assert response.status_code == 200
    assert response.json() == []
