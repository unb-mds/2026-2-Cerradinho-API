from typing import TYPE_CHECKING

from sqlalchemy import Column, ForeignKey, Integer, String, Table, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base
from app.models.disciplina import Disciplina

if TYPE_CHECKING:
    from app.models.horario import Horario
    from app.models.professor import Professor

turma_professores = Table(
    "turma_professores",
    Base.metadata,
    Column("turma_id", ForeignKey("turmas.id"), primary_key=True),
    Column("professor_id", ForeignKey("professores.id"), primary_key=True),
)


class Turma(Base):
    __tablename__ = "turmas"
    __table_args__ = (UniqueConstraint("disciplina_id", "numero", "ano_periodo"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    numero: Mapped[str] = mapped_column(String(10), nullable=False)
    ano_periodo: Mapped[str] = mapped_column(String(10), nullable=False)
    unidade: Mapped[str] = mapped_column(String(100), nullable=False)
    vagas_ofertadas: Mapped[int] = mapped_column(Integer, nullable=False)
    vagas_ocupadas: Mapped[int] = mapped_column(Integer, nullable=False)

    disciplina_id: Mapped[int] = mapped_column(ForeignKey("disciplinas.id"), nullable=False)

    disciplina: Mapped[Disciplina] = relationship(back_populates="turmas")
    professores: Mapped[list["Professor"]] = relationship(
        secondary=turma_professores, back_populates="turmas"
    )
    # Sala mora no Horario (não na Turma): o SIGAA pode usar salas diferentes
    # em dias diferentes da mesma turma (ver app/domain/disciplinas.py).
    horarios: Mapped[list["Horario"]] = relationship(back_populates="turma")
