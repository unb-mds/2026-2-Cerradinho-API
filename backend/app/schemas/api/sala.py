"""Resposta de GET /v1/salas (RF05).

Separado de `app/schemas/disciplina.py`, que é o contrato de saída do
scraper: lá a Sala é o texto cru "FCTE - I9/I10", aqui já vem separada em
prédio e nome pela camada de domínio. O nome Espaco evita colidir com aquela
Sala no OpenAPI.
"""

from pydantic import BaseModel, Field


class Espaco(BaseModel):
    id: int = Field(description="Identificador interno da sala.", examples=[7])
    nome: str = Field(description="Nome da sala dentro do prédio.", examples=["I9/I10"])
    predio: str = Field(
        description="Prédio ou unidade. Vem vazio quando o SIGAA não informa o prédio.",
        examples=["FCTE"],
    )
