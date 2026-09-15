"""Persistência do Cardápio capturado pelo scraper do RU (RF06/RF07).

O model Cardapio guarda o dia inteiro em três colunas de texto
(cafe/almoco/jantar, ver app/models/cardapio.py), então cada grupo de
ItemCardapio de uma mesma (data, refeição) é agregado num único bloco
"categoria: item" por linha antes de gravar. A chave natural é a data — a
mesma UniqueConstraint do model — porque o scraper roda de novo a cada
agendamento (RF15) e um dia já visto só deve ter seu cardápio atualizado,
nunca virar uma linha duplicada.
"""

from __future__ import annotations

from collections import defaultdict
from datetime import date

from sqlalchemy.orm import Session

from app.models import Cardapio
from app.schemas.cardapio import ItemCardapio, Refeicao

_COLUNA_POR_REFEICAO: dict[Refeicao, str] = {
    "cafe_da_manha": "cafe",
    "almoco": "almoco",
    "jantar": "jantar",
}


def _formatar_bloco(itens: list[ItemCardapio]) -> str:
    """"categoria: item" por linha, na ordem em que apareceram no PDF."""
    return "\n".join(f"{item.categoria}: {item.item}" for item in itens)


def _agrupar_por_data_e_refeicao(itens: list[ItemCardapio]) -> dict[date, dict[Refeicao, list[ItemCardapio]]]:
    agrupado: dict[date, dict[Refeicao, list[ItemCardapio]]] = defaultdict(lambda: defaultdict(list))
    for item in itens:
        agrupado[item.data][item.refeicao].append(item)
    return agrupado


def _get_ou_cria_cardapio(session: Session, data: date) -> Cardapio:
    cardapio = session.query(Cardapio).filter_by(data=data).one_or_none()
    if cardapio is None:
        cardapio = Cardapio(data=data)
        session.add(cardapio)
        session.flush()
    return cardapio


def persistir_cardapio(session: Session, itens: list[ItemCardapio]) -> list[Cardapio]:
    """Grava (ou atualiza, se o dia já existir) os itens de cardápio capturados."""
    cardapios = []
    for data, refeicoes in _agrupar_por_data_e_refeicao(itens).items():
        cardapio = _get_ou_cria_cardapio(session, data)
        for refeicao, itens_da_refeicao in refeicoes.items():
            setattr(cardapio, _COLUNA_POR_REFEICAO[refeicao], _formatar_bloco(itens_da_refeicao))
        cardapios.append(cardapio)
    return cardapios
