from typing import Any

import httpx

from app.core.config import settings


class EventsProviderClient:
    def __init__(self, settings=settings):
        self.base_url = settings.EVENTS_PROVIDER_BASE_URL.rstrip("/")
        self.api_key = settings.EVENTS_PROVIDER_API_KEY.get_secret_value()

        self.client = httpx.AsyncClient(
            headers={"x-api-key": self.api_key}, timeout=10.0, follow_redirects=True
        )

    async def close(self):
        await self.client.aclose()

    async def get_events(
        self, changed_at: str | None = None, url: str | None = None
    ) -> dict[str, Any]:
        if url:
            response = await self.client.get(url)
        else:
            params = {"changed_at": changed_at}
            response = await self.client.get(
                f"{self.base_url}/api/events/", params=params
            )

        response.raise_for_status()
        return response.json()

    async def get_seats(self, event_id: str) -> dict[str, Any]:
        response = await self.client.get(
            f"{self.base_url}/api/events/{event_id}/seats/"
        )
        response.raise_for_status()
        return response.json()

    async def register(self, event_id: str, first_name: str, last_name: str, email: str, seat: str) -> dict[str, Any]:
        data = {
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "seat": seat
        }
        response = await self.client.post(f"{self.base_url}/api/events/{event_id}/register/", json=data)
        response.raise_for_status()
        return response.json()

    async def unregister(self, event_id: str, ticket_id: str) -> dict[str, Any]:
        data = {"ticket_id": ticket_id}
        response = await self.client.request(
            "DELETE", f"{self.base_url}/api/events/{event_id}/unregister/", json=data
        )
        response.raise_for_status()
        return response.json()
