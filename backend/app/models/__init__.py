from app.models.base import Base
from app.models.cardapio import Cardapio
from app.models.disciplina import Disciplina
from app.models.horario import Horario
from app.models.professor import Professor
from app.models.sala import Sala
from app.models.turma import Turma, turma_professores

__all__ = [
    "Base",
    "Cardapio",
    "Disciplina",
    "Horario",
    "Professor",
    "Sala",
    "Turma",
    "turma_professores",
]
