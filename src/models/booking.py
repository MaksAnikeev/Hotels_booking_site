from datetime import datetime, date

from sqlalchemy import ForeignKey, DateTime, func
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import Mapped, mapped_column


from src.database import Base


class BookingORM(Base):
    __tablename__ = "booking"

    id: Mapped[int] = mapped_column(primary_key=True)
    room_id: Mapped[int] = mapped_column(ForeignKey("rooms.id", ondelete="CASCADE"))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    date_from: Mapped[date]
    date_to: Mapped[date]
    price: Mapped[int]
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )

    @hybrid_property
    def total_cost(self) -> int:
        return self.price * (self.date_to - self.date_from).days

    @total_cost.expression
    def total_cost(cls) -> int:
        return cls.price * func.date_part("day", cls.date_to - cls.date_from)
