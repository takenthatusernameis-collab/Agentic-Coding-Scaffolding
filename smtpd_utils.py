"""SMTP server utilities (wrapping :mod:`smtpd` from test support).

The :mod:`smtpd` module provides simple SMTP server classes for testing and
development. This wrapper re-exports the standard classes and helpers and
adds validated convenience constructors and helpers.
"""

from __future__ import annotations

import socket
from typing import Any, Optional, Tuple

try:
    from test.support import smtpd as _smtpd
except Exception:  # pragma: no cover
    import smtpd as _smtpd  # type: ignore


__all__ = [
    "COMMASPACE",
    "DATA_SIZE_DEFAULT",
    "DEBUGSTREAM",
    "NEWLINE",
    "Devnull",
    "Options",
    "PureProxy",
    "SMTPChannel",
    "SMTPServer",
    "DebuggingServer",
    "create_smtp_server",
    "create_debugging_server",
    "create_pure_proxy",
    "process_message",
]


COMMASPACE = _smtpd.COMMASPACE
DATA_SIZE_DEFAULT = _smtpd.DATA_SIZE_DEFAULT
DEBUGSTREAM = _smtpd.DEBUGSTREAM
NEWLINE = _smtpd.NEWLINE
Devnull = _smtpd.Devnull
Options = _smtpd.Options

SMTPChannel = _smtpd.SMTPChannel
SMTPServer = _smtpd.SMTPServer
DebuggingServer = _smtpd.DebuggingServer
PureProxy = _smtpd.PureProxy

_process_message = getattr(_smtpd.SMTPServer, "process_message", None)


def _require_str(value: Any, name: str) -> str:
    if not isinstance(value, str):
        raise TypeError(f"{name} must be a str, got {type(value).__name__}")
    return value


def _require_int(value: Any, name: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int):
        raise TypeError(f"{name} must be an int, got {type(value).__name__}")
    return value


def _require_tuple_pair(value: Any, name: str) -> Tuple[Any, Any]:
    if not isinstance(value, tuple) or len(value) != 2:
        raise TypeError(f"{name} must be a (host, port) tuple")
    return value


def create_smtp_server(
    localaddr: Tuple[str, int] = ("localhost", 1025),
    remoteaddr: Optional[Tuple[str, int]] = None,
    data_size_limit: int = DATA_SIZE_DEFAULT,
    map: Optional[dict] = None,
    enable_SMTPUTF8: bool = False,
    decode_data: bool = False,
) -> SMTPServer:
    _require_tuple_pair(localaddr, "localaddr")
    _require_str(localaddr[0], "localaddr[0]")
    _require_int(localaddr[1], "localaddr[1]")
    if localaddr[1] < 0 or localaddr[1] > 65535:
        raise ValueError("localaddr[1] must be between 0 and 65535")
    if remoteaddr is not None:
        _require_tuple_pair(remoteaddr, "remoteaddr")
        _require_str(remoteaddr[0], "remoteaddr[0]")
        _require_int(remoteaddr[1], "remoteaddr[1]")
        if remoteaddr[1] < 0 or remoteaddr[1] > 65535:
            raise ValueError("remoteaddr[1] must be between 0 and 65535")
    _require_int(data_size_limit, "data_size_limit")
    if isinstance(enable_SMTPUTF8, bool) is False or not isinstance(enable_SMTPUTF8, bool):
        raise TypeError("enable_SMTPUTF8 must be a bool")
    if not isinstance(decode_data, bool):
        raise TypeError("decode_data must be a bool")
    if map is not None and not isinstance(map, dict):
        raise TypeError("map must be a dict or None")
    try:
        return SMTPServer(
            localaddr,
            remoteaddr,
            data_size_limit=data_size_limit,
            map=map,
            enable_SMTPUTF8=enable_SMTPUTF8,
            decode_data=decode_data,
        )
    except TypeError:
        # Fallback for older signatures
        return SMTPServer(localaddr, remoteaddr)


def create_debugging_server(
    localaddr: Tuple[str, int] = ("localhost", 1025),
    remoteaddr: Optional[Tuple[str, int]] = None,
) -> DebuggingServer:
    _require_tuple_pair(localaddr, "localaddr")
    _require_str(localaddr[0], "localaddr[0]")
    _require_int(localaddr[1], "localaddr[1]")
    if localaddr[1] < 0 or localaddr[1] > 65535:
        raise ValueError("localaddr[1] must be between 0 and 65535")
    if remoteaddr is not None:
        _require_tuple_pair(remoteaddr, "remoteaddr")
        _require_str(remoteaddr[0], "remoteaddr[0]")
        _require_int(remoteaddr[1], "remoteaddr[1]")
        if remoteaddr[1] < 0 or remoteaddr[1] > 65535:
            raise ValueError("remoteaddr[1] must be between 0 and 65535")
    return DebuggingServer(localaddr, remoteaddr)


def create_pure_proxy(
    localaddr: Tuple[str, int] = ("localhost", 1025),
    remoteaddr: Optional[Tuple[str, int]] = None,
) -> PureProxy:
    _require_tuple_pair(localaddr, "localaddr")
    _require_str(localaddr[0], "localaddr[0]")
    _require_int(localaddr[1], "localaddr[1]")
    if localaddr[1] < 0 or localaddr[1] > 65535:
        raise ValueError("localaddr[1] must be between 0 and 65535")
    if remoteaddr is not None:
        _require_tuple_pair(remoteaddr, "remoteaddr")
        _require_str(remoteaddr[0], "remoteaddr[0]")
        _require_int(remoteaddr[1], "remoteaddr[1]")
        if remoteaddr[1] < 0 or remoteaddr[1] > 65535:
            raise ValueError("remoteaddr[1] must be between 0 and 65535")
    return PureProxy(localaddr, remoteaddr)


def process_message(
    server: SMTPServer,
    peer: Tuple[str, int],
    mailfrom: str,
    rcpttos: list,
    data: bytes,
    **kwargs: Any,
) -> Optional[str]:
    if not isinstance(server, SMTPServer):
        raise TypeError("server must be an SMTPServer instance")
    _require_tuple_pair(peer, "peer")
    _require_str(peer[0], "peer[0]")
    _require_int(peer[1], "peer[1]")
    if peer[1] < 0 or peer[1] > 65535:
        raise ValueError("peer[1] must be between 0 and 65535")
    _require_str(mailfrom, "mailfrom")
    if not isinstance(rcpttos, list):
        raise TypeError("rcpttos must be a list")
    if not isinstance(data, (bytes, bytearray)):
        raise TypeError("data must be bytes or bytearray")
    if hasattr(server, "process_message"):
        try:
            return server.process_message(peer, mailfrom, rcpttos, bytes(data), **kwargs)
        except Exception:
            pass
    # Fallback to module function if available
    if _process_message is not None:
        try:
            return _process_message(server, peer, mailfrom, rcpttos, bytes(data), **kwargs)
        except Exception:
            pass
    return None
