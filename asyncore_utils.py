"""Asynchronous socket services utilities wrapping the standard library :mod:`asyncore`."""

from __future__ import annotations

from typing import Any

try:
    import asyncore as _asyncore

    _ASYNCHORE_AVAILABLE = True
except Exception:  # pragma: no cover - module removed on Python 3.12+
    _asyncore = None  # type: ignore[assignment]
    _ASYNCHORE_AVAILABLE = False

__all__: list[str] = [
    "dispatcher",
    "dispatcher_with_send",
    "file_dispatcher",
    "file_wrapper",
    "loop",
    "poll",
    "read",
    "write",
    "close_all",
    "select",
    "poll2",
    "poll3",
    "socket_map",
    "ExitNow",
    "errorcode",
    "create_dispatcher",
]


if _ASYNCHORE_AVAILABLE:
    dispatcher = _asyncore.dispatcher
    dispatcher_with_send = _asyncore.dispatcher_with_send
    file_dispatcher = _asyncore.file_dispatcher
    file_wrapper = _asyncore.file_wrapper
    loop = _asyncore.loop
    poll = _asyncore.poll
    read = _asyncore.read
    write = _asyncore.write
    close_all = _asyncore.close_all
    select = _asyncore.select
    poll2 = getattr(_asyncore, "poll2", None)
    poll3 = getattr(_asyncore, "poll3", None)
    socket_map = _asyncore.socket_map
    ExitNow = _asyncore.ExitNow
    errorcode = _asyncore.errorcode
else:  # pragma: no cover - exercised only on interpreters that ship the module

    def dispatcher(*args, **kwargs):  # type: ignore[no-untyped-def]
        """Raise RuntimeError because the standard library module is unavailable."""
        raise RuntimeError("asyncore module is not available")

    dispatcher_with_send = dispatcher
    file_dispatcher = dispatcher
    file_wrapper = dispatcher
    loop = dispatcher
    poll = dispatcher
    read = dispatcher
    write = dispatcher
    close_all = dispatcher
    select = dispatcher
    poll2 = dispatcher
    poll3 = dispatcher
    socket_map = {}
    ExitNow = RuntimeError
    errorcode = {}


def create_dispatcher(map: dict[Any, Any] | None = None) -> Any:
    """Create a dispatcher with an optional map.

    Args:
        map: Optional mapping of file descriptor to dispatcher. Must be a
            ``dict`` when provided.

    Returns:
        A new dispatcher instance.

    Raises:
        TypeError: When *map* is not a dict or ``None``.

    Examples:
        >>> create_dispatcher()  # doctest: +SKIP
        <...dispatcher...>
    """
    if map is not None and not isinstance(map, dict):
        raise TypeError("map must be a dict or None")
    return dispatcher(map=map)