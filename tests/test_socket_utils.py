"""Tests for socket_utils module."""

import errno
import socket
import unittest

import socket_utils


class TestCreateSocket(unittest.TestCase):
    """Verify socket creation helpers."""

    def setUp(self):
        self._sockets = []

    def tearDown(self):
        for sock in getattr(self, "_sockets", []):
            sock.close()
        self._sockets = []

    def _track(self, sock):
        self._sockets.append(sock)
        return sock

    def test_create_socket_defaults_to_tcp(self):
        sock = self._track(socket_utils.create_socket())
        self.assertIsInstance(sock, socket.socket)
        self.assertEqual(sock.family, socket.AF_INET)
        self.assertEqual(sock.type, socket.SOCK_STREAM)

    def test_create_socket_with_udp(self):
        sock = self._track(socket_utils.create_socket(socket.AF_INET, socket.SOCK_DGRAM))
        self.assertEqual(sock.type, socket.SOCK_DGRAM)

    def test_create_socket_rejects_non_int_family(self):
        with self.assertRaises(TypeError):
            socket_utils.create_socket("AF_INET")  # type: ignore[arg-type]

    def test_create_socket_rejects_bool_type(self):
        with self.assertRaises(TypeError):
            socket_utils.create_socket(socket.AF_INET, True)  # type: ignore[arg-type]

    def test_create_socket_rejects_non_int_proto(self):
        with self.assertRaises(TypeError):
            socket_utils.create_socket(socket.AF_INET, socket.SOCK_STREAM, "0")  # type: ignore[arg-type]

    def test_create_tcp_socket(self):
        sock = self._track(socket_utils.create_tcp_socket())
        self.assertEqual(sock.type, socket.SOCK_STREAM)

    def test_create_udp_socket(self):
        sock = self._track(socket_utils.create_udp_socket())
        self.assertEqual(sock.type, socket.SOCK_DGRAM)

    def test_create_udp_socket_rejects_bad_family(self):
        with self.assertRaises(TypeError):
            socket_utils.create_udp_socket(1.5)  # type: ignore[arg-type]


class TestAddressHelpers(unittest.TestCase):
    """Verify address construction and resolution."""

    def test_socket_address_returns_tuple(self):
        self.assertEqual(socket_utils.socket_address("127.0.0.1", 8080), ("127.0.0.1", 8080))

    def test_socket_address_rejects_non_string_host(self):
        with self.assertRaises(TypeError):
            socket_utils.socket_address(1234, 80)  # type: ignore[arg-type]

    def test_socket_address_rejects_non_int_port(self):
        with self.assertRaises(TypeError):
            socket_utils.socket_address("127.0.0.1", "80")  # type: ignore[arg-type]

    def test_socket_address_rejects_bool_port(self):
        with self.assertRaises(TypeError):
            socket_utils.socket_address("127.0.0.1", True)  # type: ignore[arg-type]

    def test_socket_address_rejects_out_of_range_port(self):
        with self.assertRaises(ValueError):
            socket_utils.socket_address("127.0.0.1", 70000)

    def test_resolve_address_of_loopback(self):
        results = socket_utils.resolve_address("127.0.0.1", 80)
        self.assertTrue(results)
        self.assertTrue(all(len(item) == 5 for item in results))

    def test_resolve_address_rejects_bad_port(self):
        with self.assertRaises(ValueError):
            socket_utils.resolve_address("127.0.0.1", -1)

    def test_resolve_address_rejects_bad_host(self):
        with self.assertRaises(TypeError):
            socket_utils.resolve_address(None, 80)  # type: ignore[arg-type]

    def test_resolve_address_rejects_unknown_host(self):
        with self.assertRaises(socket.gaierror):
            socket_utils.resolve_address("not a valid host", 80)


class TestConnectionHelpers(unittest.TestCase):
    """Verify connecting, binding and listening."""

    def setUp(self):
        self._sockets = []

    def tearDown(self):
        for sock in self._sockets:
            try:
                sock.close()
            except OSError:
                pass
        self._sockets = []

    def _track(self, sock):
        self._sockets.append(sock)
        return sock

    def _server(self):
        server = self._track(socket_utils.create_tcp_socket())
        socket_utils.set_reuse_address(server)
        socket_utils.bind_socket(server, ("127.0.0.1", 0))
        socket_utils.listen_socket(server)
        return server

    def test_connect_and_accept_over_loopback(self):
        server = self._server()
        host, port = socket_utils.get_socket_name(server)[:2]
        client = self._track(socket_utils.create_tcp_socket())
        socket_utils.connect_socket(client, (host, port))
        accepted, address = socket_utils.accept_connection(server)
        self._track(accepted)
        self.assertIsInstance(address, tuple)
        self.assertEqual(socket_utils.get_peer_name(client)[:2], (host, port))
        self.assertEqual(socket_utils.get_peer_name(accepted)[:2], address[:2])

    def test_connect_socket_requires_socket(self):
        with self.assertRaises(TypeError):
            socket_utils.connect_socket("not a socket", ("127.0.0.1", 80))  # type: ignore[arg-type]

    def test_connect_socket_requires_address_tuple(self):
        sock = self._track(socket_utils.create_tcp_socket())
        with self.assertRaises(TypeError):
            socket_utils.connect_socket(sock, "127.0.0.1:80")  # type: ignore[arg-type]

    def test_connect_socket_rejects_negative_timeout(self):
        sock = self._track(socket_utils.create_tcp_socket())
        with self.assertRaises(ValueError):
            socket_utils.connect_socket(sock, ("127.0.0.1", 80), timeout=-1)

    def test_bind_socket_requires_socket(self):
        with self.assertRaises(TypeError):
            socket_utils.bind_socket(object(), ("127.0.0.1", 0))  # type: ignore[arg-type]

    def test_listen_socket_rejects_negative_backlog(self):
        sock = self._track(socket_utils.create_tcp_socket())
        with self.assertRaises(ValueError):
            socket_utils.listen_socket(sock, backlog=-1)

    def test_listen_socket_rejects_non_int_backlog(self):
        sock = self._track(socket_utils.create_tcp_socket())
        with self.assertRaises(TypeError):
            socket_utils.listen_socket(sock, backlog="5")  # type: ignore[arg-type]

    def test_accept_connection_requires_socket(self):
        with self.assertRaises(TypeError):
            socket_utils.accept_connection(42)  # type: ignore[arg-type]

    def test_create_connection_to_open_port(self):
        server = self._server()
        host, port = socket_utils.get_socket_name(server)[:2]
        client = self._track(socket_utils.create_connection((host, port), timeout=5))
        accepted, _ = socket_utils.accept_connection(server)
        self._track(accepted)
        self.assertIsInstance(client, socket.socket)

    def test_create_connection_rejects_bad_address(self):
        with self.assertRaises(TypeError):
            socket_utils.create_connection(("127.0.0.1",))  # type: ignore[arg-type]


class TestDataTransfer(unittest.TestCase):
    """Verify sending and receiving data."""

    def setUp(self):
        self.left, self.right = socket.socketpair()

    def tearDown(self):
        self.left.close()
        self.right.close()

    def test_send_all_and_receive_bytes(self):
        socket_utils.send_all(self.left, b"ping")
        self.assertEqual(socket_utils.receive_bytes(self.right), b"ping")

    def test_send_all_accepts_bytearray(self):
        socket_utils.send_all(self.left, bytearray(b"pong"))
        self.assertEqual(socket_utils.receive_bytes(self.right), b"pong")

    def test_send_all_requires_bytes(self):
        with self.assertRaises(TypeError):
            socket_utils.send_all(self.left, "text")  # type: ignore[arg-type]

    def test_send_all_requires_socket(self):
        with self.assertRaises(TypeError):
            socket_utils.send_all(None, b"data")  # type: ignore[arg-type]

    def test_receive_bytes_requires_positive_bufsize(self):
        with self.assertRaises(ValueError):
            socket_utils.receive_bytes(self.right, bufsize=0)

    def test_receive_bytes_requires_int_bufsize(self):
        with self.assertRaises(TypeError):
            socket_utils.receive_bytes(self.right, bufsize="10")  # type: ignore[arg-type]

    def test_send_and_receive_datagram(self):
        left = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        right = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            left.bind(("127.0.0.1", 0))
            right.bind(("127.0.0.1", 0))
            sent = socket_utils.send_to(left, b"datagram", socket_utils.get_socket_name(right))
            self.assertEqual(sent, 8)
            data, address = socket_utils.receive_from(right)
            self.assertEqual(data, b"datagram")
            self.assertEqual(address[:2], ("127.0.0.1", socket_utils.get_socket_name(left)[1]))
        finally:
            left.close()
            right.close()

    def test_send_to_requires_address(self):
        with self.assertRaises(TypeError):
            socket_utils.send_to(self.left, b"data", "127.0.0.1:9")  # type: ignore[arg-type]

    def test_receive_from_requires_socket(self):
        with self.assertRaises(TypeError):
            socket_utils.receive_from(None)  # type: ignore[arg-type]


class TestSocketOptions(unittest.TestCase):
    """Verify timeout, blocking and socket option helpers."""

    def setUp(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def tearDown(self):
        self.sock.close()

    def test_set_and_get_timeout(self):
        socket_utils.set_timeout(self.sock, 2.5)
        self.assertEqual(socket_utils.get_timeout(self.sock), 2.5)

    def test_set_timeout_none_restores_blocking_mode(self):
        socket_utils.set_timeout(self.sock, 1.0)
        socket_utils.set_timeout(self.sock, None)
        self.assertIsNone(socket_utils.get_timeout(self.sock))

    def test_set_timeout_rejects_bad_type(self):
        with self.assertRaises(TypeError):
            socket_utils.set_timeout(self.sock, "5")  # type: ignore[arg-type]

    def test_set_timeout_rejects_negative_value(self):
        with self.assertRaises(ValueError):
            socket_utils.set_timeout(self.sock, -0.5)

    def test_set_nonblocking_switches_mode(self):
        socket_utils.set_nonblocking(self.sock)
        self.assertEqual(self.sock.gettimeout(), 0.0)
        socket_utils.set_nonblocking(self.sock, False)
        self.assertIsNone(self.sock.gettimeout())

    def test_set_nonblocking_rejects_non_bool(self):
        with self.assertRaises(TypeError):
            socket_utils.set_nonblocking(self.sock, 1)  # type: ignore[arg-type]

    def test_set_reuse_address(self):
        socket_utils.set_reuse_address(self.sock)
        self.assertEqual(self.sock.getsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR), 1)

    def test_set_reuse_address_rejects_non_bool(self):
        with self.assertRaises(TypeError):
            socket_utils.set_reuse_address(self.sock, "yes")  # type: ignore[arg-type]

    def test_set_keepalive(self):
        socket_utils.set_keepalive(self.sock)
        self.assertEqual(self.sock.getsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE), 1)

    def test_set_keepalive_rejects_non_bool(self):
        with self.assertRaises(TypeError):
            socket_utils.set_keepalive(self.sock, 0)  # type: ignore[arg-type]

    def test_get_socket_name_of_unbound_socket(self):
        name = socket_utils.get_socket_name(self.sock)
        self.assertIsInstance(name, tuple)

    def test_get_peer_name_requires_socket(self):
        with self.assertRaises(TypeError):
            socket_utils.get_peer_name(None)  # type: ignore[arg-type]


class TestShutdownAndClose(unittest.TestCase):
    """Verify shutting down and closing sockets."""

    def test_shutdown_socket(self):
        left, right = socket.socketpair()
        try:
            socket_utils.shutdown_socket(left, socket_utils.SHUT_WR)
            self.assertEqual(right.recv(1), b"")
        finally:
            left.close()
            right.close()

    def test_shutdown_socket_rejects_unknown_mode(self):
        left, right = socket.socketpair()
        try:
            with self.assertRaises(ValueError):
                socket_utils.shutdown_socket(left, 99)
        finally:
            left.close()
            right.close()

    def test_shutdown_socket_requires_socket(self):
        with self.assertRaises(TypeError):
            socket_utils.shutdown_socket(object())  # type: ignore[arg-type]

    def test_close_socket(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket_utils.close_socket(sock)
        self.assertEqual(sock.fileno(), -1)

    def test_close_socket_requires_socket(self):
        with self.assertRaises(TypeError):
            socket_utils.close_socket("not a socket")  # type: ignore[arg-type]


class TestNaming(unittest.TestCase):
    """Verify the naming helpers."""

    def test_socket_family_name(self):
        self.assertEqual(socket_utils.socket_family_name(socket.AF_INET), "AF_INET")
        self.assertEqual(socket_utils.socket_family_name(socket.AF_INET6), "AF_INET6")

    def test_socket_family_name_of_unknown_family(self):
        self.assertEqual(socket_utils.socket_family_name(9999), "UNKNOWN")

    def test_socket_family_name_rejects_non_int(self):
        with self.assertRaises(TypeError):
            socket_utils.socket_family_name("AF_INET")  # type: ignore[arg-type]

    def test_socket_type_name(self):
        self.assertEqual(socket_utils.socket_type_name(socket.SOCK_STREAM), "SOCK_STREAM")
        self.assertEqual(socket_utils.socket_type_name(socket.SOCK_DGRAM), "SOCK_DGRAM")

    def test_socket_type_name_of_unknown_type(self):
        self.assertEqual(socket_utils.socket_type_name(9999), "UNKNOWN")

    def test_socket_type_name_rejects_non_int(self):
        with self.assertRaises(TypeError):
            socket_utils.socket_type_name(None)  # type: ignore[arg-type]

    def test_error_name_of_os_error(self):
        error = OSError(errno.ECONNREFUSED, "Connection refused")
        self.assertEqual(socket_utils.error_name(error), "ECONNREFUSED")

    def test_error_name_of_code(self):
        self.assertEqual(socket_utils.error_name(errno.EAGAIN), "EAGAIN")

    def test_error_name_of_unknown_code(self):
        self.assertEqual(socket_utils.error_name(999999), "UNKNOWN")

    def test_error_name_of_os_error_without_errno(self):
        self.assertEqual(socket_utils.error_name(OSError("boom")), "UNKNOWN")

    def test_error_name_rejects_non_int(self):
        with self.assertRaises(TypeError):
            socket_utils.error_name("ECONNREFUSED")  # type: ignore[arg-type]


class TestHostInformation(unittest.TestCase):
    """Verify host related helpers."""

    def test_get_hostname(self):
        self.assertIsInstance(socket_utils.get_hostname(), str)
        self.assertTrue(socket_utils.get_hostname())

    def test_has_ipv6(self):
        self.assertIsInstance(socket_utils.has_ipv6(), bool)

    def test_is_ipv6_address(self):
        self.assertTrue(socket_utils.is_ipv6_address("::1"))
        self.assertTrue(socket_utils.is_ipv6_address("2001:db8::1"))

    def test_is_ipv6_address_rejects_ipv4(self):
        self.assertFalse(socket_utils.is_ipv6_address("127.0.0.1"))

    def test_is_ipv6_address_rejects_garbage(self):
        self.assertFalse(socket_utils.is_ipv6_address("not-an-address"))

    def test_is_ipv6_address_requires_string(self):
        with self.assertRaises(TypeError):
            socket_utils.is_ipv6_address(None)  # type: ignore[arg-type]


if __name__ == "__main__":
    unittest.main()
