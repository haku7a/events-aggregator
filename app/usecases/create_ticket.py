from uuid import UUID

from app.db.repositories.event_repository import EventRepository
from app.db.repositories.ticket_repository import TicketRepository
from app.infrastructure.events_client import EventsProviderClient


class CreateTicketUsecase:
    def __init__(
        self,
        client: EventsProviderClient,
        event_repo: EventRepository,
        ticket_repo: TicketRepository,
    ):
        self.client = client
        self.event_repo = event_repo
        self.ticket_repo = ticket_repo

    async def execute(
        self,
        event_id: UUID,
        first_name: str,
        last_name: str,
        email: str,
        seat: str,
    ) -> dict:
        event = await self.event_repo.get_by_id(event_id)
        if event is None:
            raise ValueError("Event not found")

        if event.status != "published":
            raise ValueError("Event is not available for registration")

        result = await self.client.register(
            event_id=str(event_id),
            first_name=first_name,
            last_name=last_name,
            email=email,
            seat=seat,
        )

        ticket_id = UUID(result["ticket_id"])

        await self.ticket_repo.create(
            ticket_id=ticket_id,
            event_id=event_id,
            first_name=first_name,
            last_name=last_name,
            email=email,
            seat=seat,
        )

        return {"ticket_id": str(ticket_id)}
