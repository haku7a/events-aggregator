from datetime import datetime

from app.db.repositories.event_repository import EventRepository


class GetEventsUsecase:
    def __init__(self, event_repo: EventRepository):
        self.event_repo = event_repo

    async def execute(
        self,
        date_from: datetime | None = None,
        page: int = 1,
        page_size: int = 20,
    ) -> dict:
        events, total = await self.event_repo.get_list(
            date_from=date_from, page=page, page_size=page_size
        )

        results = []
        for e in events:
            results.append({
                "id": str(e.id),
                "name": e.name,
                "place": {
                    "id": str(e.place.id),
                    "name": e.place.name,
                    "city": e.place.city,
                    "address": e.place.address,
                },
                "event_time": e.event_time.isoformat(),
                "registration_deadline": e.registration_deadline.isoformat(),
                "status": e.status,
                "number_of_visitors": e.number_of_visitors,
            })

        next_page = f"/api/events/?page={page + 1}" if page * page_size < total else None
        previous_page = f"/api/events/?page={page - 1}" if page > 1 else None

        return {
            "count": total,
            "next": next_page,
            "previous": previous_page,
            "results": results,
        }
