from datetime import datetime

from sqlalchemy import DateTime, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db import Base


class SyncState(Base):
    __tablename__ = "sync_state"
    id: Mapped[int] = mapped_column(primary_key=True)

    last_sync_time: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    last_changed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    sync_status: Mapped[str] = mapped_column(String(20), default="success")
