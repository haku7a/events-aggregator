from unittest.mock import AsyncMock

import pytest

from app.infrastructure.paginator import EventsPaginator


PAGE_1_NO_NEXT = {
    "next": None,
    "results": [{"id": "1"}, {"id": "2"}],
}
PAGE_1 = {
    "next": "http://host/api/events/?cursor=abc",
    "results": [{"id": "1"}, {"id": "2"}],
}
PAGE_2 = {
    "next": None,
    "results": [{"id": "3"}],
}
EMPTY_PAGE = {
    "next": None,
    "results": [],
}


@pytest.mark.asyncio
async def test_single_page():
    from tests.conftest import make_mock_provider

    mock = make_mock_provider(get_events_return=PAGE_1_NO_NEXT)
    mock.get_events = AsyncMock(side_effect=[PAGE_1_NO_NEXT])

    paginator = EventsPaginator(mock, changed_at="2026-01-01")
    events = []
    async for event in paginator:
        events.append(event)

    assert events == [{"id": "1"}, {"id": "2"}]
    mock.get_events.assert_awaited_once_with(changed_at="2026-01-01")


@pytest.mark.asyncio
async def test_two_pages():
    from tests.conftest import make_mock_provider

    mock = make_mock_provider(get_events_return=PAGE_1)
    mock.get_events = AsyncMock(side_effect=[PAGE_1, PAGE_2])

    paginator = EventsPaginator(mock, changed_at="2026-01-01")
    events = []
    async for event in paginator:
        events.append(event)

    assert events == [{"id": "1"}, {"id": "2"}, {"id": "3"}]
    assert mock.get_events.await_count == 2
    mock.get_events.assert_any_await(changed_at="2026-01-01")
    mock.get_events.assert_any_await(url="http://host/api/events/?cursor=abc")


@pytest.mark.asyncio
async def test_empty_results():
    from tests.conftest import make_mock_provider

    mock = make_mock_provider(get_events_return=EMPTY_PAGE)
    mock.get_events = AsyncMock(side_effect=[EMPTY_PAGE])

    paginator = EventsPaginator(mock, changed_at="2026-01-01")
    events = []
    async for event in paginator:
        events.append(event)

    assert events == []
    mock.get_events.assert_awaited_once_with(changed_at="2026-01-01")


@pytest.mark.asyncio
async def test_first_call_uses_changed_at():
    from tests.conftest import make_mock_provider

    mock = make_mock_provider(get_events_return=PAGE_1)
    mock.get_events = AsyncMock(side_effect=[PAGE_1])

    paginator = EventsPaginator(mock, changed_at="2000-01-01")
    events = []
    async for event in paginator:
        events.append(event)

    first_call = mock.get_events.call_args_list[0]
    assert first_call.kwargs.get("changed_at") == "2000-01-01"
    assert first_call.kwargs.get("url") is None
