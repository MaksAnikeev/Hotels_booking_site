import typing

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base

if typing.TYPE_CHECKING:
    from src.models import RoomsORM


class HotelsORM(Base):
    __tablename__ = "hotels"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(100))
    location: Mapped[str]
    description: Mapped[str | None]

    rooms: Mapped[list["RoomsORM"]] = relationship(
        back_populates="hotel",
    )
