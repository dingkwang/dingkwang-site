"""Simple in-memory rate limiter based on client IP address."""

import time
from collections import defaultdict
from typing import NamedTuple

from fastapi import HTTPException, Request

from app.config import RATE_LIMIT_PER_MINUTE

_WINDOW_SECONDS = 60
_CLEANUP_INTERVAL = 300  # clean up stale entries every 5 minutes


class _RateRecord(NamedTuple):
    timestamps: list[float]


_store: dict[str, list[float]] = defaultdict(list)
_last_cleanup: float = time.time()


def _cleanup() -> None:
    """Remove entries whose timestamps are all outside the current window."""
    global _last_cleanup
    now = time.time()
    if now - _last_cleanup < _CLEANUP_INTERVAL:
        return
    _last_cleanup = now
    cutoff = now - _WINDOW_SECONDS
    keys_to_delete = []
    for key, timestamps in _store.items():
        # Remove expired timestamps
        _store[key] = [t for t in timestamps if t > cutoff]
        if not _store[key]:
            keys_to_delete.append(key)
    for key in keys_to_delete:
        del _store[key]


def _get_client_ip(request: Request) -> str:
    """Extract client IP from the request, respecting X-Forwarded-For."""
    forwarded = request.headers.get("x-forwarded-for")
    if forwarded:
        return forwarded.split(",")[0].strip()
    return request.client.host if request.client else "unknown"


async def rate_limit_dependency(request: Request) -> None:
    """FastAPI dependency that enforces per-IP rate limiting.

    Raises HTTPException 429 if the client has exceeded the allowed number
    of requests in the current time window.
    """
    _cleanup()

    client_ip = _get_client_ip(request)
    now = time.time()
    cutoff = now - _WINDOW_SECONDS

    # Prune old timestamps for this client
    timestamps = _store[client_ip]
    _store[client_ip] = [t for t in timestamps if t > cutoff]

    if len(_store[client_ip]) >= RATE_LIMIT_PER_MINUTE:
        raise HTTPException(
            status_code=429,
            detail=(
                f"Rate limit exceeded. Maximum {RATE_LIMIT_PER_MINUTE} "
                f"requests per minute."
            ),
        )

    _store[client_ip].append(now)
