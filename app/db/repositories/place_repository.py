from uuid import UUID

from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.place import Place


class PlaceRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def upsert(self, place_data: dict) -> Place:
        stmt = insert(Place).values(**place_data)
        stmt = stmt.on_conflict_do_update(
            index_elements=["id"],
            set_={col: stmt.excluded[col] for col in place_data if col != "id"},
        )
        await self.session.execute(stmt)
        await self.session.flush()

        result = await self.session.execute(
            select(Place).where(Place.id == place_data["id"])
        )
        return result.scalar_one()

    async def get_by_id(self, place_id: UUID) -> Place | None:
        result = await self.session.execute(
            select(Place).where(Place.id == place_id)
        )
        return result.scalar_one_or_none()
