"""POP3 utility functions wrapping the standard library :mod:`poplib`."""

from __future__ import annotations

import poplib
from typing import Any

__all__: list[str] = [
    "POP3",
    "POP3_SSL",
    "error_proto",
    "POP3_PORT",
    "POP3_SSL_PORT",
    "create_pop3",
    "create_pop3_ssl",
    "connect_pop3",
]

POP3_PORT = poplib.POP3_PORT
POP3_SSL_PORT = poplib.POP3_SSL_PORT

POP3 = poplib.POP3
POP3_SSL = poplib.POP3_SSL
error_proto = poplib.error_proto


def create_pop3(host: str = "", port: int = POP3_PORT, timeout: float | None = None) -> poplib.POP3:
    if not isinstance(host, str):
        raise TypeError("host must be a str")
    if not isinstance(port, int) or isinstance(port, bool):
        raise TypeError("port must be an int")
    if port < 0 or port > 65535:
        raise ValueError("port must be between 0 and 65535")
    if timeout is not None and (not isinstance(timeout, (int, float)) or isinstance(timeout, bool)):
        raise TypeError("timeout must be a number or None")
    to = timeout if timeout is not None else None
    return POP3(host, port, to)  # type: ignore[arg-type]


def create_pop3_ssl(
    host: str = "",
    port: int = POP3_SSL_PORT,
    keyfile: str | None = None,
    certfile: str | None = None,
    context: Any = None,
    timeout: float | None = None,
) -> poplib.POP3_SSL:
    if not isinstance(host, str):
        raise TypeError("host must be a str")
    if not isinstance(port, int) or isinstance(port, bool):
        raise TypeError("port must be an int")
    if port < 0 or port > 65535:
        raise ValueError("port must be between 0 and 65535")
    if keyfile is not None and not isinstance(keyfile, str):
        raise TypeError("keyfile must be a str or None")
    if certfile is not None and not isinstance(certfile, str):
        raise TypeError("certfile must be a str or None")
    if timeout is not None and (not isinstance(timeout, (int, float)) or isinstance(timeout, bool)):
        raise TypeError("timeout must be a number or None")
    # keyfile/certfile are accepted for compatibility; Python 3.12 uses context
    to = timeout if timeout is not None else None
    return POP3_SSL(host, port, context=context, timeout=to)  # type: ignore[arg-type]


def connect_pop3(
    pop3: poplib.POP3,
    host: str,
    port: int = POP3_PORT,
    timeout: float | None = None,
) -> None:
    if not isinstance(pop3, poplib.POP3) and not isinstance(pop3, poplib.POP3_SSL):
        raise TypeError("pop3 must be a POP3 instance")
    if not isinstance(host, str):
        raise TypeError("host must be a str")
    if not isinstance(port, int) or isinstance(port, bool):
        raise TypeError("port must be an int")
    if port < 0 or port > 65535:
        raise ValueError("port must be between 0 and 65535")
    if timeout is not None and (not isinstance(timeout, (int, float)) or isinstance(timeout, bool)):
        raise TypeError("timeout must be a number or None")
    getattr(pop3, "_shortcmd")(f"connect {host} {port}")
