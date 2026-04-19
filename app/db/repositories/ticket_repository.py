from uuid import UUID, uuid4

from sqlalchemy import select, delete as sa_delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.ticket import Ticket


class TicketRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(
        self,
        ticket_id: UUID,
        event_id: UUID,
        first_name: str,
        last_name: str,
        email: str,
        seat: str,
    ) -> Ticket:
        ticket = Ticket(
            id=uuid4(),
            ticket_id=ticket_id,
            event_id=event_id,
            first_name=first_name,
            last_name=last_name,
            email=email,
            seat=seat,
        )
        self.session.add(ticket)
        await self.session.flush()
        return ticket

    async def get_by_ticket_id(self, ticket_id: UUID) -> Ticket | None:
        result = await self.session.execute(
            select(Ticket).where(Ticket.ticket_id == ticket_id)
        )
        return result.scalar_one_or_none()

    async def delete(self, ticket_id: UUID) -> bool:
        result = await self.session.execute(
            sa_delete(Ticket).where(Ticket.ticket_id == ticket_id)
        )
        await self.session.flush()
        return result.rowcount > 0
