"""Resposta de GET /v1/professores (RF04).

Separado de `app/schemas/disciplina.py`, que é o contrato de saída do
scraper: lá o Professor é só um nome solto dentro da Turma, aqui é o docente
já persistido, com id e as disciplinas que ele leciona.
"""

from pydantic import BaseModel


class Professor(BaseModel):
    id: int
    nome: str
    disciplinas: list[str]  # códigos das disciplinas, ex: ["FGA0242"]
