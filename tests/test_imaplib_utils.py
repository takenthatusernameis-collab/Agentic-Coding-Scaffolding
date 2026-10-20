"""Tests for imaplib_utils module."""

import imaplib
import time
import unittest
from datetime import datetime, timezone
from unittest import mock

import imaplib_utils


class TestExports(unittest.TestCase):
    def test_constants(self):
        self.assertIs(imaplib_utils.CRLF, imaplib.CRLF)
        self.assertEqual(imaplib_utils.IMAP4_PORT, imaplib.IMAP4_PORT)
        self.assertEqual(imaplib_utils.IMAP4_SSL_PORT, imaplib.IMAP4_SSL_PORT)

    def test_classes_exported(self):
        self.assertIs(imaplib_utils.IMAP4, imaplib.IMAP4)
        self.assertIs(imaplib_utils.IMAP4_SSL, imaplib.IMAP4_SSL)
        self.assertIs(imaplib_utils.IMAP4_stream, imaplib.IMAP4_stream)

    def test_error_classes_exported(self):
        self.assertIs(imaplib_utils.IMAP4Error, imaplib.IMAP4.error)
        self.assertIs(imaplib_utils.IMAP4AbortError, imaplib.IMAP4.abort)
        self.assertIs(imaplib_utils.IMAP4ReadOnlyError, imaplib.IMAP4.readonly)


class TestCreateImap4(unittest.TestCase):
    def test_create_imap4_passes_arguments(self):
        with mock.patch.object(imaplib, "IMAP4") as fake:
            client = imaplib_utils.create_imap4("example.org", 1143, timeout=5)
        fake.assert_called_once_with("example.org", 1143, timeout=5)
        self.assertIs(client, fake.return_value)

    def test_create_imap4_defaults(self):
        with mock.patch.object(imaplib, "IMAP4") as fake:
            imaplib_utils.create_imap4()
        fake.assert_called_once_with("", imaplib.IMAP4_PORT, timeout=None)

    def test_create_imap4_bad_host(self):
        with self.assertRaises(TypeError):
            imaplib_utils.create_imap4(123)  # type: ignore[arg-type]

    def test_create_imap4_bad_port(self):
        with self.assertRaises(TypeError):
            imaplib_utils.create_imap4("localhost", "143")  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            imaplib_utils.create_imap4("localhost", True)  # type: ignore[arg-type]

    def test_create_imap4_port_out_of_range(self):
        with self.assertRaises(ValueError):
            imaplib_utils.create_imap4("localhost", 70000)
        with self.assertRaises(ValueError):
            imaplib_utils.create_imap4("localhost", -1)

    def test_create_imap4_bad_timeout(self):
        with self.assertRaises(TypeError):
            imaplib_utils.create_imap4("localhost", imaplib.IMAP4_PORT, "1")  # type: ignore[arg-type]
        with self.assertRaises(ValueError):
            imaplib_utils.create_imap4("localhost", imaplib.IMAP4_PORT, -1)

    def test_create_imap4_timeout_is_coerced_to_float(self):
        with mock.patch.object(imaplib, "IMAP4") as fake:
            imaplib_utils.create_imap4("localhost", 143, timeout=2)
        fake.assert_called_once_with("localhost", 143, timeout=2.0)


class TestCreateImap4Ssl(unittest.TestCase):
    def test_create_imap4_ssl_passes_arguments(self):
        with mock.patch.object(imaplib, "IMAP4_SSL") as fake:
            client = imaplib_utils.create_imap4_ssl(
                "example.org",
                993,
                keyfile="key.pem",
                certfile="cert.pem",
                timeout=3,
            )
        fake.assert_called_once_with(
            "example.org",
            993,
            keyfile="key.pem",
            certfile="cert.pem",
            ssl_context=None,
            timeout=3.0,
        )
        self.assertIs(client, fake.return_value)

    def test_create_imap4_ssl_bad_arguments(self):
        with self.assertRaises(TypeError):
            imaplib_utils.create_imap4_ssl(123)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            imaplib_utils.create_imap4_ssl("localhost", "993")  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            imaplib_utils.create_imap4_ssl("localhost", 993, keyfile=5)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            imaplib_utils.create_imap4_ssl("localhost", 993, certfile=5)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            imaplib_utils.create_imap4_ssl("localhost", 993, timeout="1")  # type: ignore[arg-type]

    def test_create_imap4_ssl_port_out_of_range(self):
        with self.assertRaises(ValueError):
            imaplib_utils.create_imap4_ssl("localhost", 70000)


class TestCreateImap4Stream(unittest.TestCase):
    def test_create_imap4_stream_passes_command(self):
        with mock.patch.object(imaplib, "IMAP4_stream") as fake:
            client = imaplib_utils.create_imap4_stream("cat")
        fake.assert_called_once_with("cat")
        self.assertIs(client, fake.return_value)

    def test_create_imap4_stream_bad_command(self):
        with self.assertRaises(TypeError):
            imaplib_utils.create_imap4_stream(123)  # type: ignore[arg-type]


class TestErrorHelpers(unittest.TestCase):
    def test_is_imap4_error(self):
        self.assertTrue(imaplib_utils.is_imap4_error(imaplib.IMAP4.error("bad")))
        self.assertFalse(imaplib_utils.is_imap4_error(ValueError("x")))

    def test_is_imap4_abort(self):
        self.assertTrue(imaplib_utils.is_imap4_abort(imaplib.IMAP4.abort("bad")))
        self.assertFalse(imaplib_utils.is_imap4_abort(ValueError("x")))

    def test_is_imap4_readonly(self):
        self.assertTrue(imaplib_utils.is_imap4_readonly(imaplib.IMAP4.readonly("bad")))
        self.assertFalse(imaplib_utils.is_imap4_readonly(ValueError("x")))


class TestParseCapabilities(unittest.TestCase):
    def test_parse_untagged_capability_response(self):
        parsed = imaplib_utils.parse_capabilities("* CAPABILITY IMAP4rev1 STARTTLS")
        self.assertEqual(parsed, ["IMAP4rev1", "STARTTLS"])

    def test_parse_bracketed_capability_greeting(self):
        parsed = imaplib_utils.parse_capabilities(
            "* OK [CAPABILITY IMAP4rev1 AUTH=PLAIN] Ready"
        )
        self.assertEqual(parsed, ["IMAP4rev1", "AUTH=PLAIN"])

    def test_parse_plain_capability_string(self):
        parsed = imaplib_utils.parse_capabilities("IMAP4rev1 STARTTLS")
        self.assertEqual(parsed, ["IMAP4rev1", "STARTTLS"])

    def test_parse_capabilities_without_capability_section(self):
        self.assertEqual(imaplib_utils.parse_capabilities("* OK Ready"), [])

    def test_parse_capabilities_bad_type(self):
        with self.assertRaises(TypeError):
            imaplib_utils.parse_capabilities(None)  # type: ignore[arg-type]


class TestHasCapability(unittest.TestCase):
    def test_has_capability_with_string(self):
        self.assertTrue(imaplib_utils.has_capability("IMAP4rev1 STARTTLS", "STARTTLS"))

    def test_has_capability_ignores_case(self):
        self.assertTrue(imaplib_utils.has_capability("IMAP4rev1", "imap4rev1"))

    def test_has_capability_missing(self):
        self.assertFalse(imaplib_utils.has_capability("IMAP4rev1", "STARTTLS"))

    def test_has_capability_with_sequence(self):
        self.assertTrue(imaplib_utils.has_capability(["IMAP4rev1", "IDLE"], "IDLE"))
        self.assertFalse(imaplib_utils.has_capability(["IMAP4rev1"], "IDLE"))

    def test_has_capability_bad_arguments(self):
        with self.assertRaises(TypeError):
            imaplib_utils.has_capability(42, "IMAP4rev1")  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            imaplib_utils.has_capability(["IMAP4rev1", 5], "IMAP4rev1")  # type: ignore[list-item]
        with self.assertRaises(TypeError):
            imaplib_utils.has_capability("IMAP4rev1", 5)  # type: ignore[arg-type]


class TestFlags(unittest.TestCase):
    def test_parse_flags_from_fetch_response(self):
        parsed = imaplib_utils.parse_flags(b"* 1 FETCH (FLAGS (\\Seen \\Deleted))")
        self.assertEqual(parsed, (b"\\Seen", b"\\Deleted"))

    def test_parse_flags_without_flags_section(self):
        self.assertEqual(imaplib_utils.parse_flags(b"* 1 FETCH (UID 12)"), ())

    def test_parse_flags_bad_type(self):
        with self.assertRaises(TypeError):
            imaplib_utils.parse_flags("(\\Seen)")  # type: ignore[arg-type]

    def test_parse_fetch_flags_from_fetch_response(self):
        parsed = imaplib_utils.parse_fetch_flags(
            "* 1 FETCH (UID 12 FLAGS (\\Seen \\Deleted))"
        )
        self.assertEqual(parsed, ["\\Seen", "\\Deleted"])

    def test_parse_fetch_flags_without_flags_section(self):
        self.assertEqual(imaplib_utils.parse_fetch_flags("* 1 FETCH (UID 12)"), [])

    def test_parse_fetch_flags_bad_type(self):
        with self.assertRaises(TypeError):
            imaplib_utils.parse_fetch_flags(None)  # type: ignore[arg-type]

    def test_format_flags_from_sequence(self):
        self.assertEqual(
            imaplib_utils.format_flags(["\\Seen", "\\Draft"]), "(\\Seen \\Draft)"
        )

    def test_format_flags_from_string(self):
        self.assertEqual(imaplib_utils.format_flags("  \\Seen   \\Draft "), "(\\Seen \\Draft)")

    def test_format_flags_removes_duplicates(self):
        self.assertEqual(imaplib_utils.format_flags("\\Seen \\Seen"), "(\\Seen)")

    def test_format_flags_bad_arguments(self):
        with self.assertRaises(TypeError):
            imaplib_utils.format_flags([1])  # type: ignore[list-item]
        with self.assertRaises(TypeError):
            imaplib_utils.format_flags(42)  # type: ignore[arg-type]


class TestInternalDate(unittest.TestCase):
    def test_parse_internaldate(self):
        parsed = imaplib_utils.parse_internaldate(
            b'INTERNALDATE "05-Feb-2024 10:20:30 +0100"'
        )
        self.assertIsNotNone(parsed)
        assert parsed is not None
        self.assertEqual(parsed.tm_year, 2024)
        self.assertEqual(parsed.tm_mon, 2)
        self.assertEqual(parsed.tm_mday, 5)

    def test_parse_internaldate_invalid_value(self):
        self.assertIsNone(imaplib_utils.parse_internaldate(b"not a date"))

    def test_parse_internaldate_bad_type(self):
        with self.assertRaises(TypeError):
            imaplib_utils.parse_internaldate("05-Feb-2024")  # type: ignore[arg-type]

    def test_format_internaldate_from_timestamp(self):
        formatted = imaplib_utils.format_internaldate(1707121200.0)
        self.assertTrue(formatted.startswith('"05-Feb-2024'))

    def test_format_internaldate_from_struct_time(self):
        formatted = imaplib_utils.format_internaldate(time.localtime(1707121200))
        self.assertTrue(formatted.startswith('"05-Feb-2024'))

    def test_format_internaldate_from_datetime(self):
        moment = datetime(2024, 2, 5, 10, 20, 30, tzinfo=timezone.utc)
        formatted = imaplib_utils.format_internaldate(moment)
        self.assertTrue(formatted.startswith('"05-Feb-2024'))

    def test_format_internaldate_from_quoted_string(self):
        formatted = imaplib_utils.format_internaldate('"05-Feb-2024 10:20:30 +0100"')
        self.assertEqual(formatted, '"05-Feb-2024 10:20:30 +0100"')

    def test_format_internaldate_bad_type(self):
        with self.assertRaises(TypeError):
            imaplib_utils.format_internaldate(object())


class TestIntToAp(unittest.TestCase):
    def test_int_to_ap(self):
        self.assertEqual(imaplib_utils.int_to_ap(26), b"BK")
        self.assertEqual(imaplib_utils.int_to_ap(255), b"PP")

    def test_int_to_ap_zero(self):
        self.assertEqual(imaplib_utils.int_to_ap(0), b"")

    def test_int_to_ap_bad_type(self):
        with self.assertRaises(TypeError):
            imaplib_utils.int_to_ap("26")  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            imaplib_utils.int_to_ap(True)  # type: ignore[arg-type]


if __name__ == "__main__":
    unittest.main()
