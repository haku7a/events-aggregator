from unittest.mock import AsyncMock, MagicMock

import httpx
import pytest

from app.infrastructure.events_client import EventsProviderClient


@pytest.fixture
def mock_settings():
    s = MagicMock()
    s.EVENTS_PROVIDER_BASE_URL = "http://test-host:8000"
    s.EVENTS_PROVIDER_API_KEY.get_secret_value.return_value = "test-api-key"
    return s


@pytest.fixture
def client(mock_settings):
    c = EventsProviderClient(settings=mock_settings)
    c.client = AsyncMock(spec=httpx.AsyncClient)
    return c


def _make_response(status_code=200, json_data=None):
    response = MagicMock(spec=httpx.Response)
    response.status_code = status_code
    response.json.return_value = json_data or {}
    if status_code >= 400:
        request = MagicMock()
        error = httpx.HTTPStatusError(
            message="error", request=request, response=response
        )
        response.raise_for_status.side_effect = error
    else:
        response.raise_for_status = MagicMock()
    return response


@pytest.mark.asyncio
async def test_get_events_with_changed_at(client):
    expected = {"next": None, "results": []}
    client.client.get.return_value = _make_response(json_data=expected)

    result = await client.get_events(changed_at="2026-01-01")

    assert result == expected
    client.client.get.assert_awaited_once()
    call_args = client.client.get.call_args
    assert call_args[0][0] == "http://test-host:8000/api/events/"
    assert call_args[1]["params"] == {"changed_at": "2026-01-01"}


@pytest.mark.asyncio
async def test_get_events_with_url(client):
    expected = {"next": None, "results": [{"id": "1"}]}
    client.client.get.return_value = _make_response(json_data=expected)
    url = "http://test-host:8000/api/events/?changed_at=2026-01-01&cursor=abc"

    result = await client.get_events(url=url)

    assert result == expected
    client.client.get.assert_awaited_once_with(url)


@pytest.mark.asyncio
async def test_get_seats(client):
    expected = {"seats": ["A1", "A2", "B1"]}
    client.client.get.return_value = _make_response(json_data=expected)

    result = await client.get_seats("event-123")

    assert result == expected
    client.client.get.assert_awaited_once_with(
        "http://test-host:8000/api/events/event-123/seats/"
    )


@pytest.mark.asyncio
async def test_register(client):
    expected = {"ticket_id": "ticket-uuid"}
    client.client.post.return_value = _make_response(
        status_code=201, json_data=expected
    )

    result = await client.register(
        event_id="event-123",
        first_name="Ivan",
        last_name="Ivanov",
        email="ivan@example.com",
        seat="A15",
    )

    assert result == expected
    client.client.post.assert_awaited_once_with(
        "http://test-host:8000/api/events/event-123/register/",
        json={
            "first_name": "Ivan",
            "last_name": "Ivanov",
            "email": "ivan@example.com",
            "seat": "A15",
        },
    )


@pytest.mark.asyncio
async def test_unregister(client):
    expected = {"success": True}
    client.client.request.return_value = _make_response(json_data=expected)

    result = await client.unregister(
        event_id="event-123", ticket_id="ticket-uuid"
    )

    assert result == expected
    client.client.request.assert_awaited_once_with(
        "DELETE",
        "http://test-host:8000/api/events/event-123/unregister/",
        json={"ticket_id": "ticket-uuid"},
    )


@pytest.mark.asyncio
async def test_get_events_raises_on_error(client):
    client.client.get.return_value = _make_response(status_code=500)

    with pytest.raises(httpx.HTTPStatusError):
        await client.get_events(changed_at="2026-01-01")


@pytest.mark.asyncio
async def test_close(client):
    await client.close()
    client.client.aclose.assert_awaited_once()
