from datetime import datetime
from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.db.models.event import Event
from app.db.models.place import Place


class EventRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def upsert(self, event_data: dict) -> Event:
        place_data = event_data.pop("place", None)

        if place_data:
            stmt = insert(Place).values(**place_data)
            stmt = stmt.on_conflict_do_update(
                index_elements=["id"],
                set_={col: stmt.excluded[col] for col in place_data if col != "id"},
            )
            await self.session.execute(stmt)

        stmt = insert(Event).values(**event_data)
        stmt = stmt.on_conflict_do_update(
            index_elements=["id"],
            set_={col: stmt.excluded[col] for col in event_data if col != "id"},
        )
        await self.session.execute(stmt)
        await self.session.flush()

        result = await self.session.execute(
            select(Event).where(Event.id == event_data["id"])
        )
        return result.scalar_one()

    async def get_by_id(self, event_id: UUID) -> Event | None:
        result = await self.session.execute(
            select(Event).options(selectinload(Event.place)).where(Event.id == event_id)
        )
        return result.scalar_one_or_none()

    async def get_list(
        self,
        date_from: datetime | None = None,
        page: int = 1,
        page_size: int = 20,
    ) -> tuple[list[Event], int]:
        query = select(Event).options(selectinload(Event.place))
        count_query = select(func.count()).select_from(Event)

        if date_from:
            query = query.where(Event.event_time >= date_from)
            count_query = count_query.where(Event.event_time >= date_from)

        total_result = await self.session.execute(count_query)
        total = total_result.scalar_one()

        offset = (page - 1) * page_size
        query = query.order_by(Event.event_time.desc()).offset(offset).limit(page_size)
        result = await self.session.execute(query)
        events = list(result.scalars().all())

        return events, total
