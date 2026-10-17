"""Unit tests for socketserver_utils."""

import socketserver
import threading
import unittest

from socketserver_utils import (
    close_server,
    create_tcp_server,
    create_udp_server,
    get_server_address,
    handle_one_request,
    is_serving,
    serve_forever,
    shutdown_server,
)


class _Handler(socketserver.BaseRequestHandler):
    def handle(self):
        pass


class TestCreateTcpServer(unittest.TestCase):
    def test_create_tcp_server_valid(self):
        server = create_tcp_server(("127.0.0.1", 0), _Handler)
        try:
            self.assertIsInstance(server, socketserver.TCPServer)
            self.assertTrue(server.allow_reuse_address)
        finally:
            close_server(server)

    def test_create_tcp_server_no_reuse_address(self):
        server = create_tcp_server(("127.0.0.1", 0), _Handler, allow_reuse_address=False)
        try:
            self.assertFalse(server.allow_reuse_address)
        finally:
            close_server(server)

    def test_create_tcp_server_invalid_address_type(self):
        with self.assertRaises(TypeError):
            create_tcp_server("not a tuple", _Handler)  # type: ignore[arg-type]

    def test_create_tcp_server_invalid_address_length(self):
        with self.assertRaises(TypeError):
            create_tcp_server(("127.0.0.1",), _Handler)  # type: ignore[arg-type]

    def test_create_tcp_server_invalid_port_type(self):
        with self.assertRaises(TypeError):
            create_tcp_server(("127.0.0.1", "8080"), _Handler)  # type: ignore[arg-type]

    def test_create_tcp_server_port_bool(self):
        with self.assertRaises(TypeError):
            create_tcp_server(("127.0.0.1", True), _Handler)  # type: ignore[arg-type]

    def test_create_tcp_server_invalid_handler(self):
        with self.assertRaises(TypeError):
            create_tcp_server(("127.0.0.1", 0), object())  # type: ignore[arg-type]


class TestCreateUdpServer(unittest.TestCase):
    def test_create_udp_server_valid(self):
        server = create_udp_server(("127.0.0.1", 0), _Handler)
        try:
            self.assertIsInstance(server, socketserver.UDPServer)
        finally:
            close_server(server)

    def test_create_udp_server_invalid_inputs(self):
        with self.assertRaises(TypeError):
            create_udp_server("not a tuple", _Handler)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            create_udp_server(("127.0.0.1", "8080"), _Handler)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            create_udp_server(("127.0.0.1", 0), object())  # type: ignore[arg-type]


class TestServerInspection(unittest.TestCase):
    def test_get_server_address_and_is_serving(self):
        server = create_tcp_server(("127.0.0.1", 0), _Handler)
        try:
            self.assertEqual(get_server_address(server), server.server_address)
            self.assertTrue(is_serving(server))
        finally:
            close_server(server)

    def test_operations_require_server(self):
        with self.assertRaises(TypeError):
            handle_one_request("not a server")  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            shutdown_server("not a server")  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            close_server("not a server")  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            get_server_address("not a server")  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            is_serving("not a server")  # type: ignore[arg-type]

    def test_serve_forever_validates_poll_interval(self):
        server = create_tcp_server(("127.0.0.1", 0), _Handler)
        try:
            with self.assertRaises(TypeError):
                serve_forever(server, poll_interval="0.5")  # type: ignore[arg-type]
            with self.assertRaises(ValueError):
                serve_forever(server, poll_interval=-1)
        finally:
            close_server(server)

    def test_serve_forever_and_shutdown(self):
        server = create_tcp_server(("127.0.0.1", 0), _Handler)
        try:
            thread = threading.Thread(target=serve_forever, args=(server,), daemon=True)
            thread.start()
            self.assertTrue(is_serving(server))
            shutdown_server(server)
            thread.join(timeout=5)
            self.assertFalse(is_serving(server))
        finally:
            close_server(server)


if __name__ == "__main__":
    unittest.main()
