import socket
import unittest

from networking_utils import (
    find_free_port,
    get_local_ip,
    is_port_open,
    is_valid_port,
    resolve_hostname,
    tcp_ping,
)


class TestIsValidPort(unittest.TestCase):
    def test_valid_ports(self):
        self.assertTrue(is_valid_port(1))
        self.assertTrue(is_valid_port(80))
        self.assertTrue(is_valid_port(443))
        self.assertTrue(is_valid_port(65535))

    def test_invalid_ports(self):
        self.assertFalse(is_valid_port(0))
        self.assertFalse(is_valid_port(-1))
        self.assertFalse(is_valid_port(65536))
        self.assertFalse(is_valid_port(100000))

    def test_type_errors(self):
        with self.assertRaises(TypeError):
            is_valid_port("80")
        with self.assertRaises(TypeError):
            is_valid_port(80.0)
        with self.assertRaises(TypeError):
            is_valid_port(True)


class TestIsPortOpen(unittest.TestCase):
    def setUp(self):
        self.server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_sock.bind(("127.0.0.1", 0))
        self.server_sock.listen(1)
        self.port = self.server_sock.getsockname()[1]

    def tearDown(self):
        self.server_sock.close()

    def test_open_port(self):
        self.assertTrue(is_port_open("127.0.0.1", self.port))

    def test_closed_port(self):
        port = find_free_port()
        self.assertFalse(is_port_open("127.0.0.1", port, timeout=0.1))

    def test_type_errors(self):
        with self.assertRaises(TypeError):
            is_port_open(127, 80)
        with self.assertRaises(TypeError):
            is_port_open("127.0.0.1", "80")
        with self.assertRaises(TypeError):
            is_port_open("127.0.0.1", 80, timeout="1")

    def test_value_errors(self):
        with self.assertRaises(ValueError):
            is_port_open("127.0.0.1", 0)
        with self.assertRaises(ValueError):
            is_port_open("127.0.0.1", 65536)
        with self.assertRaises(ValueError):
            is_port_open("127.0.0.1", 80, timeout=-1)


class TestFindFreePort(unittest.TestCase):
    def test_returns_valid_port(self):
        port = find_free_port()
        self.assertTrue(is_valid_port(port))

    def test_returns_different_ports(self):
        ports = {find_free_port() for _ in range(5)}
        self.assertEqual(len(ports), 5)

    def test_range_validation(self):
        with self.assertRaises(ValueError):
            find_free_port(0, 100)
        with self.assertRaises(ValueError):
            find_free_port(100, 65536)
        with self.assertRaises(ValueError):
            find_free_port(5000, 1000)

    def test_type_errors(self):
        with self.assertRaises(TypeError):
            find_free_port("1024", 65535)
        with self.assertRaises(TypeError):
            find_free_port(1024, "65535")


class TestResolveHostname(unittest.TestCase):
    def test_resolves_localhost(self):
        self.assertEqual(resolve_hostname("localhost"), "127.0.0.1")

    def test_type_error(self):
        with self.assertRaises(TypeError):
            resolve_hostname(127)

    def test_value_errors(self):
        with self.assertRaises(ValueError):
            resolve_hostname("")
        with self.assertRaises(ValueError):
            resolve_hostname("   ")
        with self.assertRaises(ValueError):
            resolve_hostname("this-hostname-does-not-exist.example.invalid")


class TestGetLocalIp(unittest.TestCase):
    def test_returns_string(self):
        ip = get_local_ip()
        self.assertIsInstance(ip, str)
        self.assertTrue(ip)


class TestTcpPing(unittest.TestCase):
    def setUp(self):
        self.server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_sock.bind(("127.0.0.1", 0))
        self.server_sock.listen(1)
        self.port = self.server_sock.getsockname()[1]

    def tearDown(self):
        self.server_sock.close()

    def test_open_port_returns_float(self):
        result = tcp_ping("127.0.0.1", self.port)
        self.assertIsInstance(result, float)
        self.assertGreaterEqual(result, 0.0)

    def test_closed_port_returns_none(self):
        port = find_free_port()
        self.assertIsNone(tcp_ping("127.0.0.1", port, timeout=0.1))

    def test_type_errors(self):
        with self.assertRaises(TypeError):
            tcp_ping(127, 80)
        with self.assertRaises(TypeError):
            tcp_ping("127.0.0.1", "80")
        with self.assertRaises(TypeError):
            tcp_ping("127.0.0.1", 80, timeout="1")

    def test_value_errors(self):
        with self.assertRaises(ValueError):
            tcp_ping("127.0.0.1", 0)
        with self.assertRaises(ValueError):
            tcp_ping("127.0.0.1", 65536)
        with self.assertRaises(ValueError):
            tcp_ping("127.0.0.1", 80, timeout=-1)


if __name__ == "__main__":
    unittest.main()
