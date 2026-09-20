"""Tiny TTL cache for search responses (starter)."""
import time

_store: dict[str, tuple[float, dict]] = {}
TTL = 300

def get(key: str) -> dict | None:
    hit = _store.get(key)
    if hit and time.time() - hit[0] < TTL:
        return hit[1]
    return None

def set(key: str, value: dict) -> None:
    _store[key] = (time.time(), value)
