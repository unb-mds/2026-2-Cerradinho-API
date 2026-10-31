"""Resposta de GET /v1/professores/{id}/agenda (RF18).

A sala vive no horário, não na turma (ADR 0010) — por isso cada bloco da
agenda carrega sua própria sala, em vez de uma sala só por turma.
"""

from pydantic import BaseModel, Field

from app.schemas.api.sala import Espaco


class BlocoAgenda(BaseModel):
    dia: str = Field(
        description="Dia da semana, no mesmo formato de GET /v1/salas/vazias.",
        examples=["sexta"],
    )
    inicio: str = Field(description="Início do bloco, no formato HH:MM.", examples=["14:00"])
    fim: str = Field(description="Fim do bloco, no formato HH:MM.", examples=["17:50"])
    sala: Espaco | None = Field(description="Sala do bloco, nula se a turma não tem sala.")


class TurmaAgenda(BaseModel):
    disciplina_codigo: str = Field(description="Código da disciplina.", examples=["FGA0242"])
    disciplina_nome: str = Field(description="Nome da disciplina.", examples=["Métodos de Desenvolvimento de Software"])
    numero: str = Field(description="Número da turma dentro da disciplina.", examples=["01"])
    ano_periodo: str = Field(description="Ano e período letivo.", examples=["2026.2"])
    horarios: list[BlocoAgenda] = Field(description="Blocos de aula da turma, ordenados por dia e início.")


class Agenda(BaseModel):
    id: int = Field(description="Identificador interno do docente.", examples=[12])
    nome: str = Field(description="Nome do docente como aparece no SIGAA.", examples=["André Barros de Sales"])
    turmas: list[TurmaAgenda] = Field(description="Turmas do docente no período, com horário e sala.")
