from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base

if TYPE_CHECKING:
    from app.models.turma import Turma


class Horario(Base):
    __tablename__ = "horarios"

    id: Mapped[int] = mapped_column(primary_key=True)
    # Turma com aula em vários turnos junta os segmentos num só código
    # ("35M5 35T1"), e algumas unidades (Darcy) chegam a 4+ segmentos
    # ("6M123 7M12345 7T1234 4N12") - 20 não sobrava espaço nem pros casos
    # mais comuns de 2 segmentos.
    codigo: Mapped[str] = mapped_column(String(100), nullable=False)
    descricao: Mapped[str] = mapped_column(String(200), nullable=False)

    turma_id: Mapped[int] = mapped_column(ForeignKey("turmas.id"), nullable=False)

    turma: Mapped["Turma"] = relationship(back_populates="horarios")
