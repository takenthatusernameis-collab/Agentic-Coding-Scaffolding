"""Tests for ip_utils module."""

import unittest

from ip_utils import (
    get_ip_version,
    in_subnet,
    int_to_ip,
    ip_to_int,
    is_link_local_ip,
    is_loopback_ip,
    is_multicast_ip,
    is_private_ip,
    is_reserved_ip,
    is_valid_ip,
    is_valid_ipv4,
    is_valid_ipv6,
    normalize_ip,
)


class TestIsValidIP(unittest.TestCase):
    def test_valid_ipv4(self) -> None:
        self.assertTrue(is_valid_ip("192.168.1.1"))
        self.assertTrue(is_valid_ip("8.8.8.8"))
        self.assertTrue(is_valid_ip("127.0.0.1"))

    def test_valid_ipv6(self) -> None:
        self.assertTrue(is_valid_ip("2001:db8::1"))
        self.assertTrue(is_valid_ip("::1"))
        self.assertTrue(is_valid_ip("2001:4860:4860::8888"))

    def test_invalid_ip(self) -> None:
        self.assertFalse(is_valid_ip("256.256.256.256"))
        self.assertFalse(is_valid_ip("not an ip"))
        self.assertFalse(is_valid_ip("192.168.1"))
        self.assertFalse(is_valid_ip(""))
        self.assertFalse(is_valid_ip(None))  # type: ignore


class TestIsValidIPv4(unittest.TestCase):
    def test_valid_ipv4(self) -> None:
        self.assertTrue(is_valid_ipv4("192.168.1.1"))
        self.assertTrue(is_valid_ipv4("10.0.0.1"))

    def test_invalid_ipv4(self) -> None:
        self.assertFalse(is_valid_ipv4("2001:db8::1"))
        self.assertFalse(is_valid_ipv4("256.1.1.1"))
        self.assertFalse(is_valid_ipv4("invalid"))


class TestIsValidIPv6(unittest.TestCase):
    def test_valid_ipv6(self) -> None:
        self.assertTrue(is_valid_ipv6("2001:db8::1"))
        self.assertTrue(is_valid_ipv6("::1"))

    def test_invalid_ipv6(self) -> None:
        self.assertFalse(is_valid_ipv6("192.168.1.1"))
        self.assertFalse(is_valid_ipv6("invalid"))


class TestGetIPVersion(unittest.TestCase):
    def test_ipv4_version(self) -> None:
        self.assertEqual(get_ip_version("192.168.1.1"), 4)

    def test_ipv6_version(self) -> None:
        self.assertEqual(get_ip_version("2001:db8::1"), 6)

    def test_invalid_raises(self) -> None:
        with self.assertRaises(ValueError):
            get_ip_version("invalid")


class TestIPConversion(unittest.TestCase):
    def test_ipv4_to_int(self) -> None:
        self.assertEqual(ip_to_int("192.168.1.1"), 3232235777)
        self.assertEqual(ip_to_int("0.0.0.0"), 0)

    def test_ipv6_to_int(self) -> None:
        result = ip_to_int("::1")
        self.assertIsInstance(result, int)

    def test_int_to_ipv4(self) -> None:
        self.assertEqual(int_to_ip(3232235777), "192.168.1.1")
        self.assertEqual(int_to_ip(0), "0.0.0.0")

    def test_int_to_ipv6(self) -> None:
        self.assertEqual(int_to_ip(1, version=6), "::1")

    def test_invalid_conversion(self) -> None:
        with self.assertRaises(ValueError):
            ip_to_int("invalid")
        with self.assertRaises(ValueError):
            int_to_ip(-1)
        with self.assertRaises(ValueError):
            int_to_ip(1, version=5)


class TestIPProperties(unittest.TestCase):
    def test_is_private(self) -> None:
        self.assertTrue(is_private_ip("192.168.1.1"))
        self.assertTrue(is_private_ip("10.0.0.1"))
        self.assertTrue(is_private_ip("172.16.0.1"))
        self.assertFalse(is_private_ip("8.8.8.8"))

    def test_is_loopback(self) -> None:
        self.assertTrue(is_loopback_ip("127.0.0.1"))
        self.assertTrue(is_loopback_ip("::1"))
        self.assertFalse(is_loopback_ip("8.8.8.8"))

    def test_is_multicast(self) -> None:
        self.assertTrue(is_multicast_ip("224.0.0.1"))
        self.assertFalse(is_multicast_ip("192.168.1.1"))

    def test_is_link_local(self) -> None:
        self.assertTrue(is_link_local_ip("169.254.1.1"))
        self.assertTrue(is_link_local_ip("fe80::1"))
        self.assertFalse(is_link_local_ip("192.168.1.1"))

    def test_is_reserved(self) -> None:
        self.assertTrue(is_reserved_ip("240.0.0.1"))
        self.assertFalse(is_reserved_ip("192.168.1.1"))

    def test_invalid_properties(self) -> None:
        with self.assertRaises(ValueError):
            is_private_ip("invalid")
        with self.assertRaises(ValueError):
            is_loopback_ip("invalid")


class TestNormalizeIP(unittest.TestCase):
    def test_normalize_ipv4(self) -> None:
        self.assertEqual(normalize_ip("192.168.001.001"), "192.168.1.1")

    def test_normalize_ipv6(self) -> None:
        self.assertEqual(normalize_ip("::ffff:192.0.2.1"), "192.0.2.1")  # may be compressed form

    def test_invalid_normalize(self) -> None:
        with self.assertRaises(ValueError):
            normalize_ip("invalid")


class TestInSubnet(unittest.TestCase):
    def test_ipv4_in_subnet(self) -> None:
        self.assertTrue(in_subnet("192.168.1.10", "192.168.1.0/24"))
        self.assertTrue(in_subnet("10.0.0.5", "10.0.0.0/8"))
        self.assertFalse(in_subnet("192.168.2.10", "192.168.1.0/24"))

    def test_ipv6_in_subnet(self) -> None:
        self.assertTrue(in_subnet("2001:db8::1", "2001:db8::/32"))
        self.assertFalse(in_subnet("2001:db9::1", "2001:db8::/32"))

    def test_invalid_in_subnet(self) -> None:
        with self.assertRaises(ValueError):
            in_subnet("invalid", "192.168.1.0/24")
        with self.assertRaises(ValueError):
            in_subnet("192.168.1.1", "invalid")


if __name__ == "__main__":
    unittest.main()
