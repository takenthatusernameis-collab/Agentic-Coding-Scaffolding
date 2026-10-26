"""Asynchronous chat utilities (wrapping :mod:`asynchat` from test support)."""

from __future__ import annotations

from typing import Any

try:
    from test.support import asynchat as _asynchat
except Exception:  # pragma: no cover
    import asynchat as _asynchat  # type: ignore


__all__ = [
    "async_chat",
    "find_prefix_at_end",
    "simple_producer",
    "deque",
]


async_chat = _asynchat.async_chat
find_prefix_at_end = _asynchat.find_prefix_at_end
simple_producer = _asynchat.simple_producer
deque = _asynchat.deque
