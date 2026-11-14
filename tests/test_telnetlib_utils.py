"""Tests for telnetlib_utils."""

from __future__ import annotations

import telnetlib
import unittest
from unittest import mock

import telnetlib_utils

TELNETLIB_AVAILABLE = telnetlib_utils.is_available()


class _FakeTelnet:
    """A stand-in for :class:`telnetlib.Telnet` that records every call."""

    def __init__(self) -> None:
        self.read_until_args: list[tuple] = []
        self.read_all_calls = 0
        self.written: list[bytes] = []
        self.expect_args: list[tuple] = []
        self.closed = False
        self.opened_with: list[tuple] = []

    def open(self, host, port=23, timeout=None):
        self.opened_with.append((host, port, timeout))

    def read_until(self, expected, timeout=None):
        self.read_until_args.append((expected, timeout))
        return b"prefix-" + expected

    def read_all(self):
        self.read_all_calls += 1
        return b"all"

    def read_some(self):
        return b"some"

    def read_eager(self):
        return b"eager"

    def read_very_eager(self):
        return b"very-eager"

    def read_lazy(self):
        return b"lazy"

    def read_very_lazy(self):
        return b"very-lazy"

    def read_sb_data(self):
        return b"sb-data"

    def write(self, buffer):
        self.written.append(buffer)
        return len(buffer)

    def expect(self, list_patterns, timeout=None):
        self.expect_args.append((list_patterns, timeout))
        return (0, b"match", b"text")

    def close(self):
        self.closed = True


class TestExports(unittest.TestCase):
    def test_all_exports_are_present(self):
        for name in telnetlib_utils.__all__:
            self.assertTrue(hasattr(telnetlib_utils, name), name)

    def test_is_available_returns_bool(self):
        self.assertIsInstance(telnetlib_utils.is_available(), bool)

    @unittest.skipUnless(TELNETLIB_AVAILABLE, "telnetlib is not available")
    def test_constants_match_the_standard_library(self):
        self.assertEqual(telnetlib_utils.IAC, telnetlib.IAC)
        self.assertEqual(telnetlib_utils.DO, telnetlib.DO)
        self.assertEqual(telnetlib_utils.DONT, telnetlib.DONT)
        self.assertEqual(telnetlib_utils.WILL, telnetlib.WILL)
        self.assertEqual(telnetlib_utils.WONT, telnetlib.WONT)
        self.assertEqual(telnetlib_utils.SE, telnetlib.SE)
        self.assertEqual(telnetlib_utils.NOP, telnetlib.NOP)
        self.assertEqual(telnetlib_utils.SB, telnetlib.SB)
        self.assertEqual(telnetlib_utils.theNULL, telnetlib.theNULL)

    @unittest.skipUnless(TELNETLIB_AVAILABLE, "telnetlib is not available")
    def test_telnet_class_is_reexported(self):
        self.assertIs(telnetlib_utils.Telnet, telnetlib.Telnet)


class TestCreateTelnet(unittest.TestCase):
    def test_no_host_builds_a_bare_client(self):
        with mock.patch.object(telnetlib_utils, "Telnet") as fake:
            client = telnetlib_utils.create_telnet()
        self.assertIs(client, fake.return_value)
        fake.assert_called_once_with()

    def test_host_and_port_are_forwarded(self):
        with mock.patch.object(telnetlib_utils, "Telnet") as fake:
            telnetlib_utils.create_telnet("example.com", 2323)
        fake.assert_called_once_with("example.com", 2323)

    def test_timeout_is_forwarded_as_a_float(self):
        with mock.patch.object(telnetlib_utils, "Telnet") as fake:
            telnetlib_utils.create_telnet("example.com", 23, timeout=5)
        fake.assert_called_once_with("example.com", 23, 5.0)

    def test_bad_host_type(self):
        with self.assertRaises(TypeError):
            telnetlib_utils.create_telnet(123)  # type: ignore[arg-type]

    def test_bad_port_type(self):
        with self.assertRaises(TypeError):
            telnetlib_utils.create_telnet("example.com", "23")  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            telnetlib_utils.create_telnet("example.com", True)  # type: ignore[arg-type]

    def test_bad_timeout_type(self):
        with self.assertRaises(TypeError):
            telnetlib_utils.create_telnet("example.com", 23, timeout="5")  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            telnetlib_utils.create_telnet("example.com", 23, timeout=True)  # type: ignore[arg-type]


class TestConnectTelnet(unittest.TestCase):
    def test_open_is_called_without_timeout(self):
        fake = _FakeTelnet()
        with mock.patch.object(telnetlib_utils, "Telnet", return_value=fake):
            client = telnetlib_utils.connect_telnet("example.com", 2323)
        self.assertIs(client, fake)
        self.assertEqual(fake.opened_with, [("example.com", 2323, None)])

    def test_open_is_called_with_timeout(self):
        fake = _FakeTelnet()
        with mock.patch.object(telnetlib_utils, "Telnet", return_value=fake):
            telnetlib_utils.connect_telnet("example.com", 23, timeout=3)
        self.assertEqual(fake.opened_with, [("example.com", 23, 3.0)])


class TestReadWrappers(unittest.TestCase):
    def setUp(self):
        self.tn = _FakeTelnet()

    def test_read_until(self):
        self.assertEqual(
            telnetlib_utils.read_until(self.tn, b"x", timeout=2),
            b"prefix-x",
        )
        self.assertEqual(self.tn.read_until_args, [(b"x", 2)])

    def test_read_until_accepts_bytearray(self):
        telnetlib_utils.read_until(self.tn, bytearray(b"y"))
        self.assertEqual(self.tn.read_until_args, [(b"y", None)])

    def test_read_until_bad_type(self):
        with self.assertRaises(TypeError):
            telnetlib_utils.read_until(self.tn, "x")  # type: ignore[arg-type]

    def test_read_until_text(self):
        self.assertEqual(
            telnetlib_utils.read_until_text(self.tn, "done", timeout=1),
            "prefix-done",
        )
        self.assertEqual(self.tn.read_until_args, [(b"done", 1)])

    def test_read_until_text_uses_the_given_encoding(self):
        self.tn.read_until = lambda expected, timeout=None: "héllo".encode("latin-1")
        self.assertEqual(
            telnetlib_utils.read_until_text(self.tn, "x", encoding="latin-1"),
            "héllo",
        )

    def test_read_until_text_bad_type(self):
        with self.assertRaises(TypeError):
            telnetlib_utils.read_until_text(self.tn, b"done")  # type: ignore[arg-type]

    def test_simple_read_wrappers(self):
        self.assertEqual(telnetlib_utils.read_all(self.tn), b"all")
        self.assertEqual(telnetlib_utils.read_some(self.tn), b"some")
        self.assertEqual(telnetlib_utils.read_eager(self.tn), b"eager")
        self.assertEqual(telnetlib_utils.read_very_eager(self.tn), b"very-eager")
        self.assertEqual(telnetlib_utils.read_lazy(self.tn), b"lazy")
        self.assertEqual(telnetlib_utils.read_very_lazy(self.tn), b"very-lazy")
        self.assertEqual(telnetlib_utils.read_sb_data(self.tn), b"sb-data")


class TestWriteWrappers(unittest.TestCase):
    def setUp(self):
        self.tn = _FakeTelnet()

    def test_write_returns_the_length(self):
        self.assertEqual(telnetlib_utils.write(self.tn, b"hello"), 5)
        self.assertEqual(self.tn.written, [b"hello"])

    def test_write_accepts_bytearray(self):
        telnetlib_utils.write(self.tn, bytearray(b"hi"))
        self.assertEqual(self.tn.written, [b"hi"])

    def test_write_bad_type(self):
        with self.assertRaises(TypeError):
            telnetlib_utils.write(self.tn, "hi")  # type: ignore[arg-type]

    def test_send_line_with_str(self):
        self.assertEqual(telnetlib_utils.send_line(self.tn, "hello"), 7)
        self.assertEqual(self.tn.written, [b"hello\r\n"])

    def test_send_line_with_bytes(self):
        self.assertEqual(telnetlib_utils.send_line(self.tn, b"hello"), 7)
        self.assertEqual(self.tn.written, [b"hello\r\n"])

    def test_send_line_uses_the_given_encoding(self):
        telnetlib_utils.send_line(self.tn, "héllo", encoding="latin-1")
        self.assertEqual(self.tn.written, ["héllo\r\n".encode("latin-1")])

    def test_send_line_bad_type(self):
        with self.assertRaises(TypeError):
            telnetlib_utils.send_line(self.tn, 5)  # type: ignore[arg-type]


class TestExpectWrappers(unittest.TestCase):
    def setUp(self):
        self.tn = _FakeTelnet()

    def test_expect_delegates(self):
        result = telnetlib_utils.expect(self.tn, [b"a", b"b"], timeout=2)
        self.assertEqual(result, (0, b"match", b"text"))
        self.assertEqual(self.tn.expect_args, [([b"a", b"b"], 2)])

    def test_expect_text_encodes_str_patterns(self):
        telnetlib_utils.expect_text(self.tn, ["one", b"two"], timeout=1)
        self.assertEqual(self.tn.expect_args, [([b"one", b"two"], 1)])

    def test_expect_text_uses_the_given_encoding(self):
        telnetlib_utils.expect_text(self.tn, ["héllo"], encoding="latin-1")
        self.assertEqual(self.tn.expect_args, [([b"h\xe9llo"], None)])


class TestClose(unittest.TestCase):
    def test_close_delegates(self):
        tn = _FakeTelnet()
        telnetlib_utils.close(tn)
        self.assertTrue(tn.closed)


class TestEscapeIac(unittest.TestCase):
    def test_escapes_the_iac_byte(self):
        iac = telnetlib_utils.IAC
        self.assertEqual(telnetlib_utils.escape_iac(b"a" + iac + b"b"), b"a" + iac + iac + b"b")

    def test_plain_data_is_unchanged(self):
        self.assertEqual(telnetlib_utils.escape_iac(b"plain"), b"plain")

    def test_accepts_bytearray(self):
        iac = telnetlib_utils.IAC
        self.assertEqual(telnetlib_utils.escape_iac(bytearray(iac)), iac + iac)

    def test_bad_type(self):
        with self.assertRaises(TypeError):
            telnetlib_utils.escape_iac("data")  # type: ignore[arg-type]


class TestStripIac(unittest.TestCase):
    def test_escaped_iac_is_unescaped(self):
        iac = telnetlib_utils.IAC
        self.assertEqual(telnetlib_utils.strip_iac(iac + iac), iac)

    def test_negotiation_commands_are_dropped(self):
        do = telnetlib_utils.DO
        will = telnetlib_utils.WILL
        iac = telnetlib_utils.IAC
        data = b"before" + iac + do + b"\x01" + iac + will + b"\x03" + b"after"
        self.assertEqual(telnetlib_utils.strip_iac(data), b"beforeafter")

    def test_subnegotiation_payload_is_dropped(self):
        sb = telnetlib_utils.SB
        se = telnetlib_utils.SE
        iac = telnetlib_utils.IAC
        data = b"a" + iac + sb + b"\x01payload" + iac + se + b"b"
        self.assertEqual(telnetlib_utils.strip_iac(data), b"ab")

    def test_bare_iac_is_kept(self):
        iac = telnetlib_utils.IAC
        self.assertEqual(telnetlib_utils.strip_iac(b"a" + iac), b"a" + iac)

    def test_plain_data_is_unchanged(self):
        self.assertEqual(telnetlib_utils.strip_iac(b"plain"), b"plain")

    def test_accepts_bytearray(self):
        iac = telnetlib_utils.IAC
        self.assertEqual(telnetlib_utils.strip_iac(bytearray(iac + iac)), iac)

    def test_bad_type(self):
        with self.assertRaises(TypeError):
            telnetlib_utils.strip_iac("data")  # type: ignore[arg-type]


class TestCommandName(unittest.TestCase):
    def test_known_command(self):
        self.assertEqual(telnetlib_utils.command_name(telnetlib_utils.IAC[0]), "IAC")

    def test_unknown_command_falls_back_to_the_number(self):
        self.assertEqual(telnetlib_utils.command_name(200), "200")

    def test_bad_type(self):
        with self.assertRaises(TypeError):
            telnetlib_utils.command_name("IAC")  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            telnetlib_utils.command_name(True)  # type: ignore[arg-type]


class TestOptionName(unittest.TestCase):
    def test_unknown_option_falls_back_to_the_number(self):
        self.assertEqual(telnetlib_utils.option_name(42), "42")

    def test_bad_type(self):
        with self.assertRaises(TypeError):
            telnetlib_utils.option_name("x")  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            telnetlib_utils.option_name(True)  # type: ignore[arg-type]


class TestUnavailableModule(unittest.TestCase):
    """The wrappers raise a clear error when telnetlib itself is missing."""

    def test_create_telnet_raises_when_unavailable(self):
        with mock.patch.object(telnetlib_utils, "_TELNETLIB_AVAILABLE", False):
            with self.assertRaises(RuntimeError):
                telnetlib_utils.create_telnet()


if __name__ == "__main__":
    unittest.main()
