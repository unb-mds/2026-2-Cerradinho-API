"""Resposta de GET /v1/salas (RF05).

Separado de `app/schemas/disciplina.py`, que é o contrato de saída do
scraper: lá a Sala é o texto cru "FCTE - I9/I10", aqui já vem separada em
prédio e nome pela camada de domínio.
"""

from pydantic import BaseModel


class Sala(BaseModel):
    id: int
    nome: str  # ex: "I9/I10"
    predio: str  # ex: "FCTE"; vazio quando o SIGAA não informa o prédio
