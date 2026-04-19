from uuid import UUID

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_client
from app.db.repositories import EventRepository, TicketRepository
from app.db.session import get_session
from app.infrastructure.events_client import EventsProviderClient
from app.usecases import CancelTicketUsecase, CreateTicketUsecase

router = APIRouter()


class CreateTicketRequest(BaseModel):
    event_id: UUID
    first_name: str
    last_name: str
    email: str
    seat: str


@router.post("/api/tickets", status_code=201)
async def create_ticket(
    body: CreateTicketRequest,
    session: AsyncSession = Depends(get_session),
    client: EventsProviderClient = Depends(get_client),
):
    event_repo = EventRepository(session)
    ticket_repo = TicketRepository(session)
    usecase = CreateTicketUsecase(
        client=client, event_repo=event_repo, ticket_repo=ticket_repo
    )
    try:
        result = await usecase.execute(
            event_id=body.event_id,
            first_name=body.first_name,
            last_name=body.last_name,
            email=body.email,
            seat=body.seat,
        )
        await session.commit()
        return result
    except ValueError as e:
        return JSONResponse(status_code=400, content={"detail": str(e)})


@router.delete("/api/tickets/{ticket_id}")
async def cancel_ticket(
    ticket_id: UUID,
    session: AsyncSession = Depends(get_session),
    client: EventsProviderClient = Depends(get_client),
):
    ticket_repo = TicketRepository(session)
    usecase = CancelTicketUsecase(client=client, ticket_repo=ticket_repo)
    try:
        result = await usecase.execute(ticket_id=ticket_id)
        await session.commit()
        return result
    except ValueError as e:
        return JSONResponse(status_code=404, content={"detail": str(e)})
