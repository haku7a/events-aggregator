from uuid import UUID

from app.db.repositories.event_repository import EventRepository


class GetEventDetailUsecase:
    def __init__(self, event_repo: EventRepository):
        self.event_repo = event_repo

    async def execute(self, event_id: UUID) -> dict | None:
        event = await self.event_repo.get_by_id(event_id)
        if event is None:
            return None

        return {
            "id": str(event.id),
            "name": event.name,
            "place": {
                "id": str(event.place.id),
                "name": event.place.name,
                "city": event.place.city,
                "address": event.place.address,
                "seats_pattern": event.place.seats_pattern,
            },
            "event_time": event.event_time.isoformat(),
            "registration_deadline": event.registration_deadline.isoformat(),
            "status": event.status,
            "number_of_visitors": event.number_of_visitors,
        }
