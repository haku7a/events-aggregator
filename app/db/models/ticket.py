from uuid import UUID

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db import Base
from app.db.mixins import TimestampMixin


class Ticket(Base, TimestampMixin):
    __tablename__ = "tickets"
    id: Mapped[UUID] = mapped_column(primary_key=True)
    ticket_id: Mapped[UUID] = mapped_column(unique=True)
    event_id: Mapped[UUID] = mapped_column(ForeignKey("events.id"))

    first_name: Mapped[str] = mapped_column(String(255))
    last_name: Mapped[str] = mapped_column(String(255))
    email: Mapped[str] = mapped_column(String(500))
    seat: Mapped[str] = mapped_column(String(20))
    event: Mapped["Event"] = relationship()
