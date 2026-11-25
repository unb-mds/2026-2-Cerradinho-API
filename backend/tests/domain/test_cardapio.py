from datetime import date

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from app.domain.cardapio import listar_cardapio_semana, persistir_cardapio
from app.models import Base, Cardapio
from app.schemas.cardapio import ItemCardapio


def _in_memory_session() -> Session:
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    return Session(engine)


def _item(**overrides) -> ItemCardapio:
    base = dict(data=date(2026, 9, 14), refeicao="almoco", categoria="Prato principal", item="Frango grelhado")
    base.update(overrides)
    return ItemCardapio(**base)


def test_persistir_cardapio_cria_registro_com_bloco_formatado():
    session = _in_memory_session()

    persistir_cardapio(session, [
        _item(categoria="Prato principal", item="Frango grelhado"),
        _item(categoria="Guarnição", item="Arroz e feijão"),
    ])
    session.commit()

    cardapio = session.query(Cardapio).one()
    assert cardapio.data == date(2026, 9, 14)
    assert cardapio.almoco == "Prato principal: Frango grelhado\nGuarnição: Arroz e feijão"
    assert cardapio.cafe is None
    assert cardapio.jantar is None


def test_persistir_cardapio_separa_refeicoes_do_mesmo_dia():
    session = _in_memory_session()

    persistir_cardapio(session, [
        _item(refeicao="cafe_da_manha", categoria="Fruta", item="Banana"),
        _item(refeicao="almoco", categoria="Prato principal", item="Frango grelhado"),
        _item(refeicao="jantar", categoria="Sopa", item="Sopa de legumes"),
    ])
    session.commit()

    cardapio = session.query(Cardapio).one()
    assert cardapio.cafe == "Fruta: Banana"
    assert cardapio.almoco == "Prato principal: Frango grelhado"
    assert cardapio.jantar == "Sopa: Sopa de legumes"


def test_persistir_cardapio_repetido_atualiza_em_vez_de_duplicar():
    session = _in_memory_session()

    persistir_cardapio(session, [_item(item="Frango grelhado")])
    session.commit()

    persistir_cardapio(session, [_item(item="Carne de sol")])
    session.commit()

    cardapios = session.query(Cardapio).all()
    assert len(cardapios) == 1
    assert cardapios[0].almoco == "Prato principal: Carne de sol"


def test_persistir_cardapio_mantem_dias_diferentes_separados():
    session = _in_memory_session()

    persistir_cardapio(session, [
        _item(data=date(2026, 9, 14), item="Frango grelhado"),
        _item(data=date(2026, 9, 15), item="Carne de sol"),
    ])
    session.commit()

    assert session.query(Cardapio).count() == 2


# Testes escritos a partir dos mutantes sobreviventes do teste de mutação
# (RNF09, `python -m scripts.mutacao app/domain/cardapio.py`).


def test_listar_cardapio_semana_preserva_item_com_dois_pontos_no_texto():
    session = _in_memory_session()
    persistir_cardapio(session, [_item(categoria="Bebidas", item="Suco: laranja ou caju")])
    session.commit()

    segunda = listar_cardapio_semana(session, date(2026, 9, 14)).dias[0]

    assert [(i.categoria, i.item) for i in segunda.almoco] == [("Bebidas", "Suco: laranja ou caju")]


def test_listar_cardapio_semana_inclui_o_domingo_e_para_antes_da_segunda_seguinte():
    session = _in_memory_session()
    persistir_cardapio(session, [
        _item(data=date(2026, 9, 20), item="Domingo"),
        _item(data=date(2026, 9, 21), item="Segunda seguinte"),
    ])
    session.commit()

    semana = listar_cardapio_semana(session, date(2026, 9, 14))

    assert semana.data_fim == date(2026, 9, 20)
    assert [d.publicado for d in semana.dias] == [False] * 6 + [True]
    assert [i.item for i in semana.dias[-1].almoco] == ["Domingo"]
