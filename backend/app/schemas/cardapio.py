"""Contrato de dados para o Cardápio do RU (RF06/RF07).

Representa o formato validado que sai do scraper de Cardápio antes de
seguir para o banco. O model SQLAlchemy guarda o dia inteiro em três
colunas de texto (cafe/almoco/jantar, ver app/models/cardapio.py), então
agrupar os itens de uma refeição num único bloco é responsabilidade da
camada de domínio (app/domain/cardapio.py), não deste contrato.
"""

from datetime import date
from typing import Literal

from pydantic import BaseModel, Field

Refeicao = Literal["cafe_da_manha", "almoco", "jantar"]


class ItemCardapio(BaseModel):
    data: date = Field(description="Dia do cardápio.", examples=["2026-09-28"])
    refeicao: Refeicao = Field(description="Refeição do dia.", examples=["almoco"])
    categoria: str = Field(
        description="Categoria do item, como aparece no cardápio do RU.", examples=["Prato Principal Padrão"]
    )
    item: str = Field(description="Descrição do item.", examples=["Frango grelhado"])
