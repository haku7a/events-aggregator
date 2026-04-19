from unittest.mock import AsyncMock

from app.infrastructure.paginator import EventsProvider


def make_mock_provider(
    get_events_return=None, get_events_side_effect=None
) -> AsyncMock:
    mock = AsyncMock(spec=EventsProvider)
    if get_events_return is not None:
        mock.get_events = AsyncMock(return_value=get_events_return)
    if get_events_side_effect is not None:
        mock.get_events = AsyncMock(side_effect=get_events_side_effect)
    return mock
