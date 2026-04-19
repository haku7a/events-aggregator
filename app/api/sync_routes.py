from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_client
from app.db.repositories import EventRepository, SyncStateRepository
from app.db.session import get_session
from app.infrastructure.events_client import EventsProviderClient
from app.usecases import SyncEventsUsecase

router = APIRouter()


@router.post("/api/sync/trigger")
async def sync_trigger(
    session: AsyncSession = Depends(get_session),
    client: EventsProviderClient = Depends(get_client),
):
    event_repo = EventRepository(session)
    sync_repo = SyncStateRepository(session)
    usecase = SyncEventsUsecase(
        client=client, event_repo=event_repo, sync_repo=sync_repo
    )
    count = await usecase.execute()
    await session.commit()
    return {"synced": count}
