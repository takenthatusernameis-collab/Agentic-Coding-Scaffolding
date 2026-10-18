"""Socketserver utilities wrapping the standard library socketserver module.

This module provides validated wrappers around the standard library
``socketserver`` module for building network servers: creating TCP/UDP
servers, serving requests forever or handling a single request, shutting
down servers, and inspecting server state. All functions validate their
inputs and raise ``TypeError`` for invalid arguments.
"""

from __future__ import annotations

import socketserver
from typing import Any, Type


def create_tcp_server(
    address: Any,
    handler_class: Type[socketserver.BaseRequestHandler],
    allow_reuse_address: bool = True,
) -> socketserver.TCPServer:
    """Create a TCP server bound to *address*.

    Args:
        address: A (host, port) tuple.
        handler_class: A request handler class.
        allow_reuse_address: Whether to set SO_REUSEADDR.

    Returns:
        A TCPServer instance.
    """
    if not isinstance(address, tuple) or len(address) != 2:
        raise TypeError("address must be a (host, port) tuple")
    host, port = address
    if not isinstance(port, int) or isinstance(port, bool):
        raise TypeError("port must be an integer")
    if not (
        isinstance(handler_class, type)
        and issubclass(handler_class, socketserver.BaseRequestHandler)
    ):
        raise TypeError("handler_class must be a BaseRequestHandler subclass")
    server = socketserver.TCPServer(address, handler_class)
    server.allow_reuse_address = allow_reuse_address
    return server


def create_udp_server(
    address: Any,
    handler_class: Type[socketserver.BaseRequestHandler],
    allow_reuse_address: bool = True,
) -> socketserver.UDPServer:
    """Create a UDP server bound to *address*."""
    if not isinstance(address, tuple) or len(address) != 2:
        raise TypeError("address must be a (host, port) tuple")
    host, port = address
    if not isinstance(port, int) or isinstance(port, bool):
        raise TypeError("port must be an integer")
    if not (
        isinstance(handler_class, type)
        and issubclass(handler_class, socketserver.BaseRequestHandler)
    ):
        raise TypeError("handler_class must be a BaseRequestHandler subclass")
    server = socketserver.UDPServer(address, handler_class)
    server.allow_reuse_address = allow_reuse_address
    return server


def handle_one_request(server: socketserver.BaseServer) -> None:
    """Handle a single request on *server*."""
    if not isinstance(server, socketserver.BaseServer):
        raise TypeError("server must be a BaseServer instance")
    server.handle_request()


def serve_forever(server: socketserver.BaseServer, poll_interval: float = 0.5) -> None:
    """Serve requests forever on *server* (blocks)."""
    if not isinstance(server, socketserver.BaseServer):
        raise TypeError("server must be a BaseServer instance")
    if isinstance(poll_interval, bool) or not isinstance(poll_interval, (int, float)):
        raise TypeError("poll_interval must be a number")
    if poll_interval < 0:
        raise ValueError("poll_interval must be non-negative")
    server.serve_forever(poll_interval=poll_interval)


def shutdown_server(server: socketserver.BaseServer) -> None:
    """Shut down *server*."""
    if not isinstance(server, socketserver.BaseServer):
        raise TypeError("server must be a BaseServer instance")
    server.shutdown()


def close_server(server: socketserver.BaseServer) -> None:
    """Close *server* and release its socket."""
    if not isinstance(server, socketserver.BaseServer):
        raise TypeError("server must be a BaseServer instance")
    server.server_close()


def get_server_address(server: socketserver.BaseServer) -> Any:
    """Return the server's bound address."""
    if not isinstance(server, socketserver.BaseServer):
        raise TypeError("server must be a BaseServer instance")
    return server.server_address


def is_serving(server: socketserver.BaseServer) -> bool:
    """Return True if *server* is currently serving (not shut down)."""
    if not isinstance(server, socketserver.BaseServer):
        raise TypeError("server must be a BaseServer instance")
    flag = getattr(server, "_BaseServer__is_shut_down", None)
    if flag is None:
        return True
    return not flag.is_set()
