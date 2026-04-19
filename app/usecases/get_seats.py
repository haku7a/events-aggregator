from uuid import UUID

import httpx

from app.infrastructure.events_client import EventsProviderClient
from app.infrastructure.seats_cache import get_cached_seats, set_cached_seats


class GetSeatsUsecase:
    def __init__(self, client: EventsProviderClient):
        self.client = client

    async def execute(self, event_id: UUID) -> dict | None:
        event_id_str = str(event_id)

        cached = get_cached_seats(event_id_str)
        if cached is not None:
            return {"event_id": event_id_str, "available_seats": cached}

        try:
            data = await self.client.get_seats(event_id_str)
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                return None
            raise

        seats = data.get("seats", [])

        set_cached_seats(event_id_str, seats)

        return {"event_id": event_id_str, "available_seats": seats}
