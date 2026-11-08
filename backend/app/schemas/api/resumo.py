"""Resposta de GET /v1/resumo.

Só as contagens, pro dashboard não precisar baixar a lista inteira de
disciplinas (6500+ turmas, ~2,3 MB) só pra mostrar um número.
"""

from pydantic import BaseModel, Field


class Resumo(BaseModel):
    turmas: int = Field(description="Total de turmas capturadas no período.", examples=[6571])
    disciplinas: int = Field(description="Total de disciplinas distintas.", examples=[1842])
    professores: int = Field(description="Total de docentes distintos.", examples=[2844])
    salas: int = Field(description="Total de salas distintas.", examples=[74])
