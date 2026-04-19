from datetime import datetime

from fastapi import APIRouter, Depends, Query
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.repositories import EventRepository
from app.db.session import get_session
from app.usecases import GetEventDetailUsecase, GetEventsUsecase

router = APIRouter()


@router.get("/api/events")
async def get_events(
    date_from: datetime | None = Query(None),
    page: int = Query(1),
    page_size: int = Query(20),
    session: AsyncSession = Depends(get_session),
):
    repo = EventRepository(session)
    usecase = GetEventsUsecase(event_repo=repo)
    return await usecase.execute(date_from=date_from, page=page, page_size=page_size)


@router.get("/api/events/{event_id}")
async def get_event_detail(
    event_id: str,
    session: AsyncSession = Depends(get_session),
):
    repo = EventRepository(session)
    usecase = GetEventDetailUsecase(event_repo=repo)
    result = await usecase.execute(event_id=event_id)
    if result is None:
        return JSONResponse(status_code=404, content={"detail": "Event not found"})
    return result
