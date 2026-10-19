"""Low-level socket utilities wrapping the standard library socket module.

The :mod:`socket` module is the foundation of all network communication in
Python. This wrapper exposes a small, validated surface over it so callers can
create sockets, resolve addresses, move data over connections, and translate
numeric error codes into readable names without repeating the usual type
checks.
"""

from __future__ import annotations

import errno
import socket
from typing import Any, List, Optional, Tuple

__all__ = [
    "AF_INET",
    "AF_INET6",
    "AF_UNIX",
    "SOCK_STREAM",
    "SOCK_DGRAM",
    "SHUT_RD",
    "SHUT_WR",
    "SHUT_RDWR",
    "create_socket",
    "create_tcp_socket",
    "create_udp_socket",
    "socket_address",
    "resolve_address",
    "connect_socket",
    "create_connection",
    "bind_socket",
    "listen_socket",
    "accept_connection",
    "send_all",
    "send_to",
    "receive_bytes",
    "receive_from",
    "set_timeout",
    "get_timeout",
    "set_nonblocking",
    "set_reuse_address",
    "set_keepalive",
    "shutdown_socket",
    "close_socket",
    "get_socket_name",
    "get_peer_name",
    "socket_family_name",
    "socket_type_name",
    "error_name",
    "get_hostname",
    "has_ipv6",
    "is_ipv6_address",
]

# Address families re-exported for convenience.
AF_INET = socket.AF_INET
AF_INET6 = socket.AF_INET6
AF_UNIX = socket.AF_UNIX

# Socket types re-exported for convenience.
SOCK_STREAM = socket.SOCK_STREAM
SOCK_DGRAM = socket.SOCK_DGRAM

# Shutdown modes re-exported for convenience.
SHUT_RD = socket.SHUT_RD
SHUT_WR = socket.SHUT_WR
SHUT_RDWR = socket.SHUT_RDWR

# The default buffer size used by the receive helpers.
DEFAULT_BUFFER_SIZE = 4096

# The largest valid TCP/UDP port number.
MAX_PORT = 65535


def _require_socket(sock: Any, name: str = "sock") -> socket.socket:
    """Return *sock* when it is a socket, otherwise raise ``TypeError``."""
    if not isinstance(sock, socket.socket):
        raise TypeError(f"{name} must be a socket, got {type(sock).__name__}")
    return sock


def _require_int(value: Any, name: str) -> int:
    """Return *value* when it is a plain integer, otherwise raise ``TypeError``."""
    if isinstance(value, bool) or not isinstance(value, int):
        raise TypeError(f"{name} must be an int, got {type(value).__name__}")
    return value


def _require_host(value: Any, name: str = "host") -> str:
    """Return *value* when it is a string, otherwise raise ``TypeError``."""
    if not isinstance(value, str):
        raise TypeError(f"{name} must be a string, got {type(value).__name__}")
    return value


def _require_port(value: Any, name: str = "port") -> int:
    """Return *value* when it is a valid port number, otherwise raise."""
    port = _require_int(value, name)
    if not 0 <= port <= MAX_PORT:
        raise ValueError(f"{name} must be between 0 and {MAX_PORT}, got {port}")
    return port


def _require_address(value: Any, name: str = "address") -> Any:
    """Return *value* when it is a ``(host, port)`` pair, otherwise raise."""
    if not isinstance(value, (tuple, list)) or len(value) != 2:
        raise TypeError(f"{name} must be a (host, port) tuple")
    host = _require_host(value[0], f"{name}[0]")
    port = _require_port(value[1], f"{name}[1]")
    return (host, port)


def _require_data(value: Any, name: str = "data") -> bytes:
    """Return *value* as immutable bytes, otherwise raise ``TypeError``."""
    if isinstance(value, (bytes, bytearray, memoryview)):
        return bytes(value)
    raise TypeError(f"{name} must be bytes-like, got {type(value).__name__}")


def _require_timeout(value: Any, name: str = "timeout") -> Optional[float]:
    """Return *value* when it is ``None`` or a non-negative number."""
    if value is None:
        return None
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise TypeError(f"{name} must be a number or None, got {type(value).__name__}")
    if value < 0:
        raise ValueError(f"{name} must be non-negative, got {value}")
    return float(value)


def create_socket(
    family: int = socket.AF_INET,
    sock_type: int = socket.SOCK_STREAM,
    proto: int = 0,
) -> socket.socket:
    """Create a new socket.

    Args:
        family: Address family, such as ``AF_INET`` or ``AF_INET6``.
        sock_type: Socket type, such as ``SOCK_STREAM`` or ``SOCK_DGRAM``.
        proto: Protocol number, ``0`` for the default protocol.

    Returns:
        The newly created socket.

    Raises:
        TypeError: If an argument has the wrong type.
        OSError: If the socket cannot be created.
    """
    _require_int(family, "family")
    _require_int(sock_type, "sock_type")
    _require_int(proto, "proto")
    return socket.socket(family, sock_type, proto)


def create_tcp_socket(family: int = socket.AF_INET) -> socket.socket:
    """Create a stream (TCP) socket.

    Args:
        family: Address family of the socket.

    Returns:
        The newly created TCP socket.

    Raises:
        TypeError: If *family* is not an integer.
    """
    return create_socket(family, socket.SOCK_STREAM)


def create_udp_socket(family: int = socket.AF_INET) -> socket.socket:
    """Create a datagram (UDP) socket.

    Args:
        family: Address family of the socket.

    Returns:
        The newly created UDP socket.

    Raises:
        TypeError: If *family* is not an integer.
    """
    return create_socket(family, socket.SOCK_DGRAM)


def socket_address(host: str, port: int) -> Tuple[str, int]:
    """Build a validated ``(host, port)`` address pair.

    Args:
        host: Hostname or IP address.
        port: Port number.

    Returns:
        The validated address tuple.

    Raises:
        TypeError: If *host* is not a string or *port* is not an integer.
        ValueError: If *port* is outside the valid range.
    """
    return (_require_host(host), _require_port(port))


def resolve_address(
    host: str,
    port: int,
    family: int = socket.AF_UNSPEC,
    sock_type: int = socket.SOCK_STREAM,
) -> List[Tuple[Any, ...]]:
    """Resolve *host* and *port* into a list of candidate addresses.

    Args:
        host: Hostname or IP address to resolve.
        port: Port number to resolve.
        family: Address family filter, ``AF_UNSPEC`` for every family.
        sock_type: Socket type filter.

    Returns:
        The list of ``(family, type, proto, canonname, sockaddr)`` tuples
        produced by :func:`socket.getaddrinfo`.

    Raises:
        TypeError: If an argument has the wrong type.
        ValueError: If *port* is outside the valid range.
        socket.gaierror: If the address cannot be resolved.
    """
    text = _require_host(host)
    number = _require_port(port)
    _require_int(family, "family")
    _require_int(sock_type, "sock_type")
    return list(socket.getaddrinfo(text, number, family, sock_type))


def connect_socket(
    sock: socket.socket,
    address: Any,
    timeout: Optional[float] = None,
) -> socket.socket:
    """Connect *sock* to *address*.

    Args:
        sock: The socket to connect.
        address: A ``(host, port)`` tuple.
        timeout: Optional timeout applied before connecting.

    Returns:
        The connected socket.

    Raises:
        TypeError: If an argument has the wrong type.
        ValueError: If *timeout* is negative.
        OSError: If the connection fails.
    """
    connection = _require_socket(sock)
    target = _require_address(address)
    wait = _require_timeout(timeout)
    if wait is not None:
        connection.settimeout(wait)
    connection.connect(target)
    return connection


def create_connection(address: Any, timeout: Optional[float] = None) -> socket.socket:
    """Create a socket connected to *address*.

    Args:
        address: A ``(host, port)`` tuple.
        timeout: Optional timeout applied to the new socket.

    Returns:
        The connected socket.

    Raises:
        TypeError: If an argument has the wrong type.
        ValueError: If *timeout* is negative.
        OSError: If the connection fails.
    """
    target = _require_address(address)
    wait = _require_timeout(timeout)
    return socket.create_connection(target, timeout=wait)


def bind_socket(sock: socket.socket, address: Any) -> socket.socket:
    """Bind *sock* to *address*.

    Args:
        sock: The socket to bind.
        address: A ``(host, port)`` tuple.

    Returns:
        The bound socket.

    Raises:
        TypeError: If an argument has the wrong type.
        OSError: If the bind fails.
    """
    connection = _require_socket(sock)
    target = _require_address(address)
    connection.bind(target)
    return connection


def listen_socket(sock: socket.socket, backlog: int = socket.SOMAXCONN) -> socket.socket:
    """Mark *sock* as a listening socket.

    Args:
        sock: The socket to listen on.
        backlog: Maximum number of pending connections.

    Returns:
        The listening socket.

    Raises:
        TypeError: If an argument has the wrong type.
        ValueError: If *backlog* is negative.
        OSError: If the socket cannot listen.
    """
    connection = _require_socket(sock)
    size = _require_int(backlog, "backlog")
    if size < 0:
        raise ValueError(f"backlog must be non-negative, got {size}")
    connection.listen(size)
    return connection


def accept_connection(sock: socket.socket) -> Tuple[socket.socket, Any]:
    """Accept a pending connection on *sock*.

    Args:
        sock: The listening socket.

    Returns:
        A tuple of the accepted socket and the peer address.

    Raises:
        TypeError: If *sock* is not a socket.
        OSError: If no connection can be accepted.
    """
    connection = _require_socket(sock)
    client, address = connection.accept()
    return client, address


def send_all(sock: socket.socket, data: Any) -> int:
    """Send *data* over *sock*.

    Args:
        sock: The connected socket.
        data: The bytes to send.

    Returns:
        The number of bytes sent.

    Raises:
        TypeError: If an argument has the wrong type.
        OSError: If the data cannot be sent.
    """
    connection = _require_socket(sock)
    payload = _require_data(data)
    connection.sendall(payload)
    return len(payload)


def send_to(sock: socket.socket, data: Any, address: Any) -> int:
    """Send *data* to *address* using *sock*.

    Args:
        sock: The socket to send from.
        data: The bytes to send.
        address: A ``(host, port)`` tuple.

    Returns:
        The number of bytes sent.

    Raises:
        TypeError: If an argument has the wrong type.
        OSError: If the data cannot be sent.
    """
    connection = _require_socket(sock)
    payload = _require_data(data)
    target = _require_address(address)
    return int(connection.sendto(payload, target))


def receive_bytes(sock: socket.socket, bufsize: int = DEFAULT_BUFFER_SIZE) -> bytes:
    """Receive up to *bufsize* bytes from *sock*.

    Args:
        sock: The connected socket.
        bufsize: Maximum number of bytes to read.

    Returns:
        The bytes that were received.

    Raises:
        TypeError: If an argument has the wrong type.
        ValueError: If *bufsize* is not positive.
        OSError: If the data cannot be received.
    """
    connection = _require_socket(sock)
    size = _require_int(bufsize, "bufsize")
    if size <= 0:
        raise ValueError(f"bufsize must be positive, got {size}")
    return bytes(connection.recv(size))


def receive_from(sock: socket.socket, bufsize: int = DEFAULT_BUFFER_SIZE) -> Tuple[bytes, Any]:
    """Receive a datagram from *sock* along with its sender address.

    Args:
        sock: The bound socket.
        bufsize: Maximum number of bytes to read.

    Returns:
        A tuple of the received bytes and the sender address.

    Raises:
        TypeError: If an argument has the wrong type.
        ValueError: If *bufsize* is not positive.
        OSError: If the datagram cannot be received.
    """
    connection = _require_socket(sock)
    size = _require_int(bufsize, "bufsize")
    if size <= 0:
        raise ValueError(f"bufsize must be positive, got {size}")
    data, address = connection.recvfrom(size)
    return bytes(data), address


def set_timeout(sock: socket.socket, timeout: Optional[float]) -> socket.socket:
    """Set the timeout of *sock*.

    Args:
        sock: The socket to configure.
        timeout: Timeout in seconds, or ``None`` for a blocking socket.

    Returns:
        The configured socket.

    Raises:
        TypeError: If an argument has the wrong type.
        ValueError: If *timeout* is negative.
    """
    connection = _require_socket(sock)
    wait = _require_timeout(timeout)
    connection.settimeout(wait)
    return connection


def get_timeout(sock: socket.socket) -> Optional[float]:
    """Return the timeout of *sock*.

    Args:
        sock: The socket to inspect.

    Returns:
        The timeout in seconds, or ``None`` when the socket is blocking.

    Raises:
        TypeError: If *sock* is not a socket.
    """
    connection = _require_socket(sock)
    timeout = connection.gettimeout()
    if timeout is None:
        return None
    return float(timeout)


def set_nonblocking(sock: socket.socket, flag: bool = True) -> socket.socket:
    """Put *sock* in non-blocking mode, or back into blocking mode.

    Args:
        sock: The socket to configure.
        flag: ``True`` for non-blocking mode, ``False`` for blocking mode.

    Returns:
        The configured socket.

    Raises:
        TypeError: If an argument has the wrong type.
    """
    connection = _require_socket(sock)
    if not isinstance(flag, bool):
        raise TypeError(f"flag must be a bool, got {type(flag).__name__}")
    connection.setblocking(not flag)
    return connection


def set_reuse_address(sock: socket.socket, flag: bool = True) -> socket.socket:
    """Enable or disable address reuse on *sock*.

    Args:
        sock: The socket to configure.
        flag: ``True`` to allow the address to be reused.

    Returns:
        The configured socket.

    Raises:
        TypeError: If an argument has the wrong type.
        OSError: If the option cannot be set.
    """
    connection = _require_socket(sock)
    if not isinstance(flag, bool):
        raise TypeError(f"flag must be a bool, got {type(flag).__name__}")
    connection.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1 if flag else 0)
    return connection


def set_keepalive(sock: socket.socket, flag: bool = True) -> socket.socket:
    """Enable or disable TCP keepalive on *sock*.

    Args:
        sock: The socket to configure.
        flag: ``True`` to enable keepalive probes.

    Returns:
        The configured socket.

    Raises:
        TypeError: If an argument has the wrong type.
        OSError: If the option cannot be set.
    """
    connection = _require_socket(sock)
    if not isinstance(flag, bool):
        raise TypeError(f"flag must be a bool, got {type(flag).__name__}")
    connection.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1 if flag else 0)
    return connection


def shutdown_socket(sock: socket.socket, how: int = socket.SHUT_RDWR) -> socket.socket:
    """Shut down one or both directions of *sock*.

    Args:
        sock: The socket to shut down.
        how: Shutdown mode, one of ``SHUT_RD``, ``SHUT_WR`` or ``SHUT_RDWR``.

    Returns:
        The socket that was shut down.

    Raises:
        TypeError: If an argument has the wrong type.
        OSError: If the shutdown fails.
    """
    connection = _require_socket(sock)
    mode = _require_int(how, "how")
    if mode not in (socket.SHUT_RD, socket.SHUT_WR, socket.SHUT_RDWR):
        raise ValueError(f"how must be one of SHUT_RD, SHUT_WR or SHUT_RDWR, got {mode}")
    connection.shutdown(mode)
    return connection


def close_socket(sock: socket.socket) -> None:
    """Close *sock*.

    Closing an already closed socket is not an error.

    Args:
        sock: The socket to close.

    Raises:
        TypeError: If *sock* is not a socket.
    """
    connection = _require_socket(sock)
    connection.close()


def get_socket_name(sock: socket.socket) -> Any:
    """Return the local address *sock* is bound to.

    Args:
        sock: The socket to inspect.

    Returns:
        The bound address of the socket.

    Raises:
        TypeError: If *sock* is not a socket.
        OSError: If the address cannot be read.
    """
    connection = _require_socket(sock)
    return connection.getsockname()


def get_peer_name(sock: socket.socket) -> Any:
    """Return the address of the peer *sock* is connected to.

    Args:
        sock: The connected socket.

    Returns:
        The peer address of the socket.

    Raises:
        TypeError: If *sock* is not a socket.
        OSError: If the peer address cannot be read.
    """
    connection = _require_socket(sock)
    return connection.getpeername()


def socket_family_name(family: int) -> str:
    """Return the readable name of an address family.

    Args:
        family: The numeric address family.

    Returns:
        The family name, or ``"UNKNOWN"`` when the family is not registered.

    Raises:
        TypeError: If *family* is not an integer.
    """
    number = _require_int(family, "family")
    try:
        return socket.AddressFamily(number).name
    except ValueError:
        return "UNKNOWN"


def socket_type_name(sock_type: int) -> str:
    """Return the readable name of a socket type.

    Args:
        sock_type: The numeric socket type.

    Returns:
        The socket type name, or ``"UNKNOWN"`` when the type is not registered.

    Raises:
        TypeError: If *sock_type* is not an integer.
    """
    number = _require_int(sock_type, "sock_type")
    try:
        return socket.SocketKind(number).name
    except ValueError:
        return "UNKNOWN"


def error_name(error: Any) -> str:
    """Return the symbolic name of an operating system error code.

    Args:
        error: An :class:`OSError` instance or a numeric error code.

    Returns:
        The error name, such as ``"ECONNREFUSED"``, or ``"UNKNOWN"`` when the
        code is not registered.

    Raises:
        TypeError: If *error* is neither an ``OSError`` nor an integer.
    """
    if isinstance(error, OSError):
        code = error.errno
    else:
        code = _require_int(error, "error")
    if code is None:
        return "UNKNOWN"
    return errno.errorcode.get(code, "UNKNOWN")


def get_hostname() -> str:
    """Return the hostname of the local machine."""
    return socket.gethostname()


def has_ipv6() -> bool:
    """Return ``True`` when the platform supports IPv6."""
    return bool(socket.has_ipv6)


def is_ipv6_address(host: str) -> bool:
    """Return ``True`` when *host* is a valid IPv6 address.

    Args:
        host: The address to inspect.

    Returns:
        ``True`` when *host* is a valid IPv6 address.

    Raises:
        TypeError: If *host* is not a string.
    """
    text = _require_host(host)
    try:
        socket.inet_pton(socket.AF_INET6, text)
    except (OSError, ValueError):
        return False
    return True
