"""Resposta de GET /v1/cardapio/semana (RF19).

Separado de `app/schemas/cardapio.py`, que é o contrato de saída do
scraper (um item por linha). Aqui os itens já vêm agrupados por dia e por
refeição, e a semana sempre tem os 7 dias, mesmo os que não têm cardápio.
"""

from datetime import date

from pydantic import BaseModel, Field


class ItemRefeicao(BaseModel):
    categoria: str = Field(
        description="Categoria do item, como aparece no cardápio do RU.", examples=["Prato Principal Padrão"]
    )
    item: str = Field(description="Descrição do item.", examples=["Frango grelhado"])


class CardapioDia(BaseModel):
    data: date = Field(description="Dia do cardápio.", examples=["2026-10-26"])
    cafe_da_manha: list[ItemRefeicao] = Field(description="Itens do café da manhã, na ordem do PDF.")
    almoco: list[ItemRefeicao] = Field(description="Itens do almoço, na ordem do PDF.")
    jantar: list[ItemRefeicao] = Field(description="Itens do jantar, na ordem do PDF.")
    publicado: bool = Field(
        description="Falso quando o RU ainda não publicou ou o Cerradinho não coletou o cardápio do dia. "
        "Nesse caso as três refeições vêm vazias."
    )


class CardapioSemana(BaseModel):
    data_inicio: date = Field(description="Primeiro dia da janela.", examples=["2026-10-26"])
    data_fim: date = Field(description="Último dia da janela (data_inicio + 6 dias).", examples=["2026-11-01"])
    dias: list[CardapioDia] = Field(description="Os 7 dias da janela, em ordem.")
