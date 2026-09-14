from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base

if TYPE_CHECKING:
    from app.models.turma import Turma


class Horario(Base):
    __tablename__ = "horarios"

    id: Mapped[int] = mapped_column(primary_key=True)
    codigo: Mapped[str] = mapped_column(String(20), nullable=False)
    descricao: Mapped[str] = mapped_column(String(200), nullable=False)

    turma_id: Mapped[int] = mapped_column(ForeignKey("turmas.id"), nullable=False)

    turma: Mapped["Turma"] = relationship(back_populates="horarios")
