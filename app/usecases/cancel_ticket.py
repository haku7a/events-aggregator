from uuid import UUID

from app.db.repositories.ticket_repository import TicketRepository
from app.infrastructure.events_client import EventsProviderClient


class CancelTicketUsecase:
    def __init__(
        self,
        client: EventsProviderClient,
        ticket_repo: TicketRepository,
    ):
        self.client = client
        self.ticket_repo = ticket_repo

    async def execute(self, ticket_id: UUID) -> dict:
        ticket = await self.ticket_repo.get_by_ticket_id(ticket_id)
        if ticket is None:
            raise ValueError("Ticket not found")

        await self.client.unregister(
            event_id=str(ticket.event_id),
            ticket_id=str(ticket_id),
        )

        await self.ticket_repo.delete(ticket_id)

        return {"success": True}
