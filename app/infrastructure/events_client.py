from typing import Any

import httpx

from app.core.config import settings


class EventsProviderClient:
    def __init__(self, settings=settings):
        self.base_url = settings.EVENTS_PROVIDER_BASE_URL.rstrip("/")
        self.api_key = settings.EVENTS_PROVIDER_API_KEY.get_secret_value()

        self.client = httpx.AsyncClient(
            headers={"x-api-key": self.api_key}, timeout=10.0
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
