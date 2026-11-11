"""Asynchronous chat utilities wrapping the standard library :mod:`asynchat`."""

from __future__ import annotations

from collections import deque as _deque

try:
    import asynchat as _asynchat

    _ASYNCHAT_AVAILABLE = True
except Exception:  # pragma: no cover - module removed on Python 3.12+
    _asynchat = None  # type: ignore[assignment]
    _ASYNCHAT_AVAILABLE = False

__all__: list[str] = [
    "async_chat",
    "find_prefix_at_end",
    "simple_producer",
    "deque",
]


if _ASYNCHAT_AVAILABLE:
    async_chat = _asynchat.async_chat
    find_prefix_at_end = _asynchat.find_prefix_at_end
    simple_producer = _asynchat.simple_producer
    deque = _deque
else:  # pragma: no cover - exercised only on interpreters that ship the module

    def async_chat(*args, **kwargs):  # type: ignore[no-untyped-def]
        """Raise RuntimeError because the standard library module is unavailable."""
        raise RuntimeError("asynchat module is not available")

    def find_prefix_at_end(*args, **kwargs):  # type: ignore[no-untyped-def]
        """Raise RuntimeError because the standard library module is unavailable."""
        raise RuntimeError("asynchat module is not available")

    def simple_producer(*args, **kwargs):  # type: ignore[no-untyped-def]
        """Raise RuntimeError because the standard library module is unavailable."""
        raise RuntimeError("asynchat module is not available")

    deque = None  # type: ignore[assignment]