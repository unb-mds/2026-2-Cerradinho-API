from datetime import date, timedelta

from app.domain.cardapio import persistir_cardapio
from app.schemas.cardapio import ItemCardapio


def test_listar_cardapio_semana_agrupa_por_dia_e_refeicao(client, db_session):
    itens = [
        ItemCardapio(
            data=date(2026, 9, 14), refeicao="almoco", categoria="Prato Principal Padrão", item="Frango grelhado"
        ),
        ItemCardapio(data=date(2026, 9, 14), refeicao="almoco", categoria="Guarnição", item="Arroz e feijão"),
        ItemCardapio(data=date(2026, 9, 14), refeicao="jantar", categoria="Sopa", item="Caldo verde"),
    ]
    persistir_cardapio(db_session, itens)
    db_session.commit()

    response = client.get("/v1/cardapio/semana", params={"data_inicio": "2026-09-14"})

    assert response.status_code == 200
    corpo = response.json()
    assert (corpo["data_inicio"], corpo["data_fim"]) == ("2026-09-14", "2026-09-20")
    assert corpo["dias"][0] == {
        "data": "2026-09-14",
        "cafe_da_manha": [],
        "almoco": [
            {"categoria": "Prato Principal Padrão", "item": "Frango grelhado"},
            {"categoria": "Guarnição", "item": "Arroz e feijão"},
        ],
        "jantar": [{"categoria": "Sopa", "item": "Caldo verde"}],
        "publicado": True,
    }


def test_listar_cardapio_semana_devolve_os_sete_dias_mesmo_sem_cardapio(client, db_session):
    persistir_cardapio(
        db_session,
        [ItemCardapio(data=date(2026, 9, 16), refeicao="almoco", categoria="Sopa", item="Sopa de legumes")],
    )
    db_session.commit()

    response = client.get("/v1/cardapio/semana", params={"data_inicio": "2026-09-14"})

    dias = response.json()["dias"]
    assert [dia["data"] for dia in dias] == [str(date(2026, 9, 14) + timedelta(days=n)) for n in range(7)]
    assert [dia["publicado"] for dia in dias] == [False, False, True, False, False, False, False]
    assert dias[0] == {"data": "2026-09-14", "cafe_da_manha": [], "almoco": [], "jantar": [], "publicado": False}


def test_listar_cardapio_semana_fora_do_intervalo_nao_aparece(client, db_session):
    persistir_cardapio(
        db_session,
        [ItemCardapio(data=date(2026, 9, 1), refeicao="jantar", categoria="Sopa", item="Sopa de legumes")],
    )
    db_session.commit()

    response = client.get("/v1/cardapio/semana", params={"data_inicio": "2026-09-14"})

    assert response.status_code == 200
    assert not any(dia["publicado"] for dia in response.json()["dias"])


def test_listar_cardapio_semana_sem_data_inicio_usa_hoje(client):
    response = client.get("/v1/cardapio/semana")

    hoje = date.today()
    assert response.status_code == 200
    assert response.json()["data_inicio"] == hoje.isoformat()
    assert response.json()["data_fim"] == (hoje + timedelta(days=6)).isoformat()
