from datetime import datetime

from app.db.repositories.event_repository import EventRepository
from app.db.repositories.sync_state_repository import SyncStateRepository
from app.infrastructure.events_client import EventsProviderClient
from app.infrastructure.paginator import EventsPaginator


class SyncEventsUsecase:
    def __init__(
        self,
        client: EventsProviderClient,
        event_repo: EventRepository,
        sync_repo: SyncStateRepository,
    ):
        self.client = client
        self.event_repo = event_repo
        self.sync_repo = sync_repo

    async def execute(self) -> int:
        state = await self.sync_repo.get()
        changed_at = "2000-01-01"
        if state and state.last_changed_at:
            changed_at = state.last_changed_at.strftime("%Y-%m-%d")

        count = 0
        max_changed_at: datetime | None = None

        async for event_data in EventsPaginator(self.client, changed_at):
            place_data = event_data.pop("place")
            place_data["created_at"] = datetime.fromisoformat(place_data["created_at"])
            place_data["changed_at"] = datetime.fromisoformat(place_data["changed_at"])

            event_data["place_id"] = place_data["id"]
            for field in (
                "event_time",
                "registration_deadline",
                "status_changed_at",
                "created_at",
                "changed_at",
            ):
                event_data[field] = datetime.fromisoformat(event_data[field])

            event_data["place"] = place_data

            await self.event_repo.upsert(event_data)
            count += 1

            event_changed = event_data["changed_at"]
            if max_changed_at is None or event_changed > max_changed_at:
                max_changed_at = event_changed

        await self.sync_repo.update(last_changed_at=max_changed_at, status="success")
        return count
