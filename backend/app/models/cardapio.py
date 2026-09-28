from datetime import date

from sqlalchemy import Date, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class Cardapio(Base):
    __tablename__ = "cardapios"

    id: Mapped[int] = mapped_column(primary_key=True)
    data: Mapped[date] = mapped_column(Date, nullable=False, unique=True)
    cafe: Mapped[str | None] = mapped_column(Text)
    almoco: Mapped[str | None] = mapped_column(Text)
    jantar: Mapped[str | None] = mapped_column(Text)
