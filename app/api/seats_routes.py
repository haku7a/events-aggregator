from uuid import UUID

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from app.infrastructure.events_client import EventsProviderClient
from app.usecases import GetSeatsUsecase

router = APIRouter()


def get_client() -> EventsProviderClient:
    from app.main import client

    return client


@router.get("/api/events/{event_id}/seats")
async def get_seats(
    event_id: UUID,
    client: EventsProviderClient = Depends(get_client),
):
    usecase = GetSeatsUsecase(client=client)
    result = await usecase.execute(event_id=event_id)
    if result is None:
        return JSONResponse(status_code=404, content={"detail": "Seats not found"})
    return result
