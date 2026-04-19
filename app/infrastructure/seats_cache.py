import time


_seats_cache: dict[str, tuple[list[str], float]] = {}
TTL_SECONDS = 30


def get_cached_seats(event_id: str) -> list[str] | None:
    if event_id in _seats_cache:
        seats, timestamp = _seats_cache[event_id]
        if time.time() - timestamp < TTL_SECONDS:
            return seats
        del _seats_cache[event_id]
    return None


def set_cached_seats(event_id: str, seats: list[str]) -> None:
    _seats_cache[event_id] = (seats, time.time())
