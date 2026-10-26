"""Asynchronous socket services utilities (wrapping :mod:`asyncore` from test support)."""

from __future__ import annotations

from typing import Any, Optional, Tuple

try:
    from test.support import asyncore as _asyncore
except Exception:  # pragma: no cover
    import asyncore as _asyncore  # type: ignore


__all__ = [
    "dispatcher",
    "dispatcher_with_send",
    "file_dispatcher",
    "file_wrapper",
    "loop",
    "socket_map",
    "read",
    "write",
    "readwrite",
    "close_all",
    "compact_traceback",
    "poll",
    "poll2",
    "poll3",
    "ExitNow",
    "errorcode",
    "create_dispatcher",
]


dispatcher = _asyncore.dispatcher
dispatcher_with_send = _asyncore.dispatcher_with_send
file_dispatcher = _asyncore.file_dispatcher
file_wrapper = _asyncore.file_wrapper
loop = _asyncore.loop
socket_map = _asyncore.socket_map
read = _asyncore.read
write = _asyncore.write
readwrite = _asyncore.readwrite
close_all = _asyncore.close_all
compact_traceback = _asyncore.compact_traceback
poll = _asyncore.poll
poll2 = _asyncore.poll2
poll3 = _asyncore.poll3
ExitNow = _asyncore.ExitNow
errorcode = _asyncore.errorcode


def _require_tuple_pair(value: Any, name: str) -> Tuple[Any, Any]:
    if not isinstance(value, tuple) or len(value) != 2:
        raise TypeError(f"{name} must be a (host, port) tuple")
    return value


def _require_str(value: Any, name: str) -> str:
    if not isinstance(value, str):
        raise TypeError(f"{name} must be a str, got {type(value).__name__}")
    return value


def _require_int(value: Any, name: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int):
        raise TypeError(f"{name} must be an int, got {type(value).__name__}")
    return value


def create_dispatcher(sock=None, map: Optional[dict] = None) -> dispatcher:
    if map is not None and not isinstance(map, dict):
        raise TypeError("map must be a dict or None")
    try:
        return dispatcher(sock=sock, map=map)
    except TypeError:
        return dispatcher(sock)
