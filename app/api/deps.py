from fastapi import Request

from app.infrastructure.events_client import EventsProviderClient


def get_client(request: Request) -> EventsProviderClient:
    return request.app.state.client
