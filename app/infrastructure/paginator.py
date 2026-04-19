from typing import Any, AsyncIterator, Protocol


class EventsProvider(Protocol):
    async def get_events(
        self, changed_at: str | None = None, url: str | None = None
    ) -> dict[str, Any]: ...


class EventsPaginator:
    def __init__(self, client: EventsProvider, changed_at: str):
        self.client = client
        self.changed_at = changed_at
        self._next_url: str | None = None
        self._started: bool = False
        self._buffer: list[dict[str, Any]] = []

    def __aiter__(self) -> AsyncIterator[dict[str, Any]]:
        return self

    async def __anext__(self) -> dict[str, Any]:
        if self._buffer:
            return self._buffer.pop(0)
        if not self._started:
            self._started = True
            data = await self.client.get_events(changed_at=self.changed_at)
        elif self._next_url:
            data = await self.client.get_events(url=self._next_url)
        else:
            raise StopAsyncIteration
        self._next_url = data.get("next")
        self._buffer = data.get("results", [])
        if not self._buffer:
            raise StopAsyncIteration
        return self._buffer.pop(0)
