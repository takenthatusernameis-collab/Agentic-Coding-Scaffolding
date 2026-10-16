"""Networking utilities for TCP port and host operations.

This module provides helpers for validating TCP ports, checking whether a port
is open on a host, finding a free local port, resolving hostnames to IP
addresses, detecting the local IP address, and measuring TCP connect latency.
All functions validate their inputs and raise ``TypeError`` or ``ValueError``
on invalid arguments.
"""

from __future__ import annotations

import socket
import time
from typing import Optional

__all__: list[str] = [
    "is_valid_port",
    "is_port_open",
    "find_free_port",
    "resolve_hostname",
    "get_local_ip",
    "tcp_ping",
]


def is_valid_port(port: int) -> bool:
    """Return ``True`` if *port* is a valid TCP/UDP port number (1-65535).

    Args:
        port: The port number to validate.

    Returns:
        ``True`` if *port`` is within the valid range, otherwise ``False``.

    Raises:
        TypeError: If *port`` is not an integer.

    Examples:
        >>> is_valid_port(80)
        True
        >>> is_valid_port(0)
        False
        >>> is_valid_port(65536)
        False
    """
    if isinstance(port, bool) or not isinstance(port, int):
        raise TypeError(f"port must be an integer, got {type(port).__name__}")
    return 1 <= port <= 65535


def is_port_open(host: str, port: int, timeout: float = 1.0) -> bool:
    """Return ``True`` if a TCP connection to *host*:*port* can be established.

    Args:
        host: The hostname or IP address to connect to.
        port: The port number to connect to.
        timeout: The connection timeout in seconds (default: 1.0).

    Returns:
        ``True`` if the port is open and reachable, otherwise ``False``.

    Raises:
        TypeError: If *host`` is not a string, *port`` is not an integer, or
            *timeout`` is not a number.
        ValueError: If *port`` is not a valid port number or *timeout`` is
            negative.

    Examples:
        >>> is_port_open("127.0.0.1", 1)  # doctest: +SKIP
        False
    """
    if not isinstance(host, str):
        raise TypeError(f"host must be a string, got {type(host).__name__}")
    if isinstance(port, bool) or not isinstance(port, int):
        raise TypeError(f"port must be an integer, got {type(port).__name__}")
    if not 1 <= port <= 65535:
        raise ValueError(f"port {port} is not a valid port number (1-65535)")
    if isinstance(timeout, bool) or not isinstance(timeout, (int, float)):
        raise TypeError(f"timeout must be a number, got {type(timeout).__name__}")
    if timeout < 0:
        raise ValueError("timeout must not be negative")

    try:
        with socket.create_connection((host, port), timeout=timeout):
            return True
    except OSError:
        return False


def find_free_port(start: int = 1024, end: int = 65535) -> int:
    """Return a free local TCP port by binding a temporary listener.

    The function binds to port 0 to let the OS assign an unused port, then
    returns that port number. The *start* and *end* bounds are validated but
    the OS-assigned port is returned regardless of the range.

    Args:
        start: The inclusive lower bound of the acceptable port range.
        end: The inclusive upper bound of the acceptable port range.

    Returns:
        A free local TCP port number.

    Raises:
        TypeError: If *start`` or *end`` is not an integer.
        ValueError: If either bound is not a valid port number, or
            *start`` is greater than *end``.

    Examples:
        >>> port = find_free_port()
        >>> is_valid_port(port)
        True
    """
    if isinstance(start, bool) or not isinstance(start, int):
        raise TypeError(f"start must be an integer, got {type(start).__name__}")
    if isinstance(end, bool) or not isinstance(end, int):
        raise TypeError(f"end must be an integer, got {type(end).__name__}")
    if not 1 <= start <= 65535:
        raise ValueError(f"start {start} is not a valid port number (1-65535)")
    if not 1 <= end <= 65535:
        raise ValueError(f"end {end} is not a valid port number (1-65535)")
    if start > end:
        raise ValueError(f"start {start} must be <= end {end}")

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind(("127.0.0.1", 0))
        port = sock.getsockname()[1]
    return port


def resolve_hostname(hostname: str) -> str:
    """Resolve *hostname* to its IPv4 address.

    Args:
        hostname: The hostname to resolve.

    Returns:
        The IPv4 address as a string.

    Raises:
        TypeError: If *hostname`` is not a string.
        ValueError: If *hostname`` is empty or cannot be resolved.

    Examples:
        >>> resolve_hostname("localhost")  # doctest: +SKIP
        '127.0.0.1'
    """
    if not isinstance(hostname, str):
        raise TypeError(f"hostname must be a string, got {type(hostname).__name__}")
    if not hostname.strip():
        raise ValueError("hostname must not be empty")

    try:
        return socket.gethostbyname(hostname)
    except OSError as exc:
        raise ValueError(f"could not resolve hostname {hostname!r}: {exc}") from exc


def get_local_ip() -> str:
    """Return the local machine's IPv4 address used for outbound connections.

    Returns:
        The local IPv4 address as a string, or ``"127.0.0.1"`` if it cannot
        be determined.
    """
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
            sock.connect(("8.8.8.8", 80))
            return sock.getsockname()[0]
    except OSError:
        return "127.0.0.1"


def tcp_ping(host: str, port: int, timeout: float = 1.0) -> Optional[float]:
    """Measure the time in seconds to establish a TCP connection to *host*:*port*.

    Args:
        host: The hostname or IP address to connect to.
        port: The port number to connect to.
        timeout: The connection timeout in seconds (default: 1.0).

    Returns:
        The connection time in seconds, or ``None`` if the connection could
        not be established within *timeout``.

    Raises:
        TypeError: If *host`` is not a string, *port`` is not an integer, or
            *timeout`` is not a number.
        ValueError: If *port`` is not a valid port number or *timeout`` is
            negative.

    Examples:
        >>> tcp_ping("127.0.0.1", 1)  # doctest: +SKIP
        None
    """
    if not isinstance(host, str):
        raise TypeError(f"host must be a string, got {type(host).__name__}")
    if isinstance(port, bool) or not isinstance(port, int):
        raise TypeError(f"port must be an integer, got {type(port).__name__}")
    if not 1 <= port <= 65535:
        raise ValueError(f"port {port} is not a valid port number (1-65535)")
    if isinstance(timeout, bool) or not isinstance(timeout, (int, float)):
        raise TypeError(f"timeout must be a number, got {type(timeout).__name__}")
    if timeout < 0:
        raise ValueError("timeout must not be negative")

    start = time.perf_counter()
    try:
        with socket.create_connection((host, port), timeout=timeout):
            return time.perf_counter() - start
    except OSError:
        return None
