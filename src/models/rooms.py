import typing

from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base

if typing.TYPE_CHECKING:
    from src.models import HotelsORM, FacilitiesORM


class RoomsORM(Base):
    __tablename__ = "rooms"

    id: Mapped[int] = mapped_column(primary_key=True)
    hotel_id: Mapped[int] = mapped_column(ForeignKey("hotels.id"))
    title: Mapped[str] = mapped_column(String(100))
    description: Mapped[str | None]
    price: Mapped[int]
    quantity: Mapped[int]

    hotel: Mapped["HotelsORM"] = relationship(back_populates="rooms")

    facilities: Mapped[list["FacilitiesORM"]] = relationship(
        secondary="rooms_facilities",
        back_populates="rooms",
    )
