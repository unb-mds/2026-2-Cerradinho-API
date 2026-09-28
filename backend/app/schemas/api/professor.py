"""Resposta de GET /v1/professores (RF04).

Separado de `app/schemas/disciplina.py`, que é o contrato de saída do
scraper: lá o Professor é só um nome solto dentro da Turma, aqui é o docente
já persistido, com id e as disciplinas que ele leciona. O nome Docente evita
colidir com aquele Professor no OpenAPI.
"""

from pydantic import BaseModel, Field


class Docente(BaseModel):
    id: int = Field(description="Identificador interno do docente.", examples=[12])
    nome: str = Field(description="Nome do docente como aparece no SIGAA.", examples=["Ana Souza"])
    disciplinas: list[str] = Field(
        description="Códigos das disciplinas que o docente leciona no período, sem repetição.",
        examples=[["FGA0071", "FGA0242"]],
    )
