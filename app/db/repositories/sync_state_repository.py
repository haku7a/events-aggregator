from datetime import datetime

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.sync_state import SyncState


class SyncStateRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get(self) -> SyncState | None:
        result = await self.session.execute(select(SyncState).limit(1))
        return result.scalar_one_or_none()

    async def update(self, last_changed_at: datetime | None, status: str) -> SyncState:
        state = await self.get()
        if state is None:
            state = SyncState(last_changed_at=last_changed_at, sync_status=status)
            self.session.add(state)
        else:
            state.last_sync_time = datetime.now()
            state.last_changed_at = last_changed_at
            state.sync_status = status
        await self.session.flush()
        return state
