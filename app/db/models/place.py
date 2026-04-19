from uuid import UUID

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base
from app.db.mixins import TimestampMixin


class Place(Base, TimestampMixin):
    __tablename__ = "places"

    id: Mapped[UUID] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255))
    city: Mapped[str] = mapped_column(String(100))
    address: Mapped[str] = mapped_column(String(500))
    seats_pattern: Mapped[str] = mapped_column(String(1000))
