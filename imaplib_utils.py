"""IMAP4 client utilities (wrapping :mod:`imaplib`).

The :mod:`imaplib` module defines three classes, ``IMAP4``, ``IMAP4_SSL`` and
``IMAP4_stream``, which encapsulate a connection to an IMAP4 server and
implement a large subset of the IMAP4rev1 client commands. This wrapper
exposes validated constructors and helpers plus common constants for
working with IMAP4 connections.
"""

from __future__ import annotations

import imaplib as _imaplib
from typing import Any, Optional, Tuple

__all__ = [
    "CRLF",
    "IMAP4",
    "IMAP4_SSL",
    "IMAP4_SSL_PORT",
    "IMAP4_PORT",
    "IMAP4_stream",
    "IMAP4Error",
    "IMAP4AbortError",
    "IMAP4ReadOnlyError",
    "create_imap4",
    "create_imap4_ssl",
    "create_imap4_stream",
    "is_imap4_error",
    "is_imap4_abort",
    "is_imap4_readonly",
]

CRLF = _imaplib.CRLF
IMAP4_PORT = _imaplib.IMAP4_PORT
IMAP4_SSL_PORT = _imaplib.IMAP4_SSL_PORT

IMAP4 = _imaplib.IMAP4
IMAP4_SSL = _imaplib.IMAP4_SSL
IMAP4_stream = _imaplib.IMAP4_stream

IMAP4Error = _imaplib.IMAP4.error
IMAP4AbortError = _imaplib.IMAP4.abort
IMAP4ReadOnlyError = _imaplib.IMAP4.readonly


def _require_str(value: Any, name: str) -> str:
    if not isinstance(value, str):
        raise TypeError(f"{name} must be a str, got {type(value).__name__}")
    return value


def _require_optional_str(value: Any, name: str) -> Optional[str]:
    if value is None:
        return None
    if not isinstance(value, str):
        raise TypeError(f"{name} must be a str or None, got {type(value).__name__}")
    return value


def _require_int(value: Any, name: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int):
        raise TypeError(f"{name} must be an int, got {type(value).__name__}")
    return value


def _require_optional_int(value: Any, name: str) -> Optional[int]:
    if value is None:
        return None
    if isinstance(value, bool) or not isinstance(value, int):
        raise TypeError(f"{name} must be an int or None, got {type(value).__name__}")
    return value


def _require_optional_float(value: Any, name: str) -> Optional[float]:
    if value is None:
        return None
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise TypeError(f"{name} must be a number or None, got {type(value).__name__}")
    return float(value)


def create_imap4(
    host: str = "",
    port: int = IMAP4_PORT,
    timeout: Optional[float] = None,
) -> _imaplib.IMAP4:
    """Create an IMAP4 connection."""
    _require_str(host, "host")
    port_value = _require_int(port, "port")
    if port_value < 0 or port_value > 65535:
        raise ValueError("port must be between 0 and 65535")
    timeout_value = _require_optional_float(timeout, "timeout")
    if timeout_value is not None and timeout_value < 0:
        raise ValueError("timeout must be non-negative")
    return _imaplib.IMAP4(host, port_value, timeout=timeout_value)


def create_imap4_ssl(
    host: str = "",
    port: int = IMAP4_SSL_PORT,
    keyfile: Optional[str] = None,
    certfile: Optional[str] = None,
    ssl_context: Any = None,
    timeout: Optional[float] = None,
) -> _imaplib.IMAP4_SSL:
    """Create an IMAP4_SSL connection."""
    _require_str(host, "host")
    port_value = _require_int(port, "port")
    if port_value < 0 or port_value > 65535:
        raise ValueError("port must be between 0 and 65535")
    keyfile_value = _require_optional_str(keyfile, "keyfile")
    certfile_value = _require_optional_str(certfile, "certfile")
    timeout_value = _require_optional_float(timeout, "timeout")
    if timeout_value is not None and timeout_value < 0:
        raise ValueError("timeout must be non-negative")
    try:
        return _imaplib.IMAP4_SSL(
            host,
            port_value,
            keyfile=keyfile_value,
            certfile=certfile_value,
            ssl_context=ssl_context,
            timeout=timeout_value,
        )
    except TypeError:
        return _imaplib.IMAP4_SSL(host, port_value, keyfile_value, certfile_value)


def create_imap4_stream(command: str) -> _imaplib.IMAP4_stream:
    """Create an IMAP4_stream connection."""
    _require_str(command, "command")
    return _imaplib.IMAP4_stream(command)


def is_imap4_error(exc: Any) -> bool:
    """Return True if exc is an IMAP4 error."""
    return isinstance(exc, _imaplib.IMAP4.error)


def is_imap4_abort(exc: Any) -> bool:
    """Return True if exc is an IMAP4 abort error."""
    return isinstance(exc, _imaplib.IMAP4.abort)


def is_imap4_readonly(exc: Any) -> bool:
    """Return True if exc is an IMAP4 readonly error."""
    return isinstance(exc, _imaplib.IMAP4.readonly)
