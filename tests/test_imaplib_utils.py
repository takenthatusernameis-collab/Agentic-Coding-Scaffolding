"""Tests for imaplib_utils module."""

import imaplib
import unittest

import imaplib_utils


class TestImaplibUtils(unittest.TestCase):
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

    def test_create_imap4_defaults(self):
        conn = imaplib_utils.create_imap4()
        self.assertIsInstance(conn, imaplib.IMAP4)
        conn.logout()

    def test_create_imap4_with_params(self):
        conn = imaplib_utils.create_imap4("localhost", imaplib.IMAP4_PORT)
        self.assertIsInstance(conn, imaplib.IMAP4)
        conn.logout()

    def test_create_imap4_bad_host(self):
        with self.assertRaises(TypeError):
            imaplib_utils.create_imap4(123)  # type: ignore[arg-type]

    def test_create_imap4_bad_port(self):
        with self.assertRaises(TypeError):
            imaplib_utils.create_imap4("localhost", "143")  # type: ignore[arg-type]
        with self.assertRaises(ValueError):
            imaplib_utils.create_imap4("localhost", 70000)
        with self.assertRaises(ValueError):
            imaplib_utils.create_imap4("localhost", -1)

    def test_create_imap4_bad_timeout(self):
        with self.assertRaises(TypeError):
            imaplib_utils.create_imap4("localhost", imaplib.IMAP4_PORT, "1")  # type: ignore[arg-type]
        with self.assertRaises(ValueError):
            imaplib_utils.create_imap4("localhost", imaplib.IMAP4_PORT, -1)

    def test_create_imap4_stream(self):
        conn = imaplib_utils.create_imap4_stream("cat")
        self.assertIsInstance(conn, imaplib.IMAP4_stream)
        conn.logout()

    def test_create_imap4_stream_bad_command(self):
        with self.assertRaises(TypeError):
            imaplib_utils.create_imap4_stream(123)  # type: ignore[arg-type]

    def test_is_imap4_error(self):
        try:
            raise imaplib.IMAP4.error("bad")
        except Exception as exc:
            self.assertTrue(imaplib_utils.is_imap4_error(exc))
        self.assertFalse(imaplib_utils.is_imap4_error(ValueError("x")))

    def test_is_imap4_abort(self):
        try:
            raise imaplib.IMAP4.abort("bad")
        except Exception as exc:
            self.assertTrue(imaplib_utils.is_imap4_abort(exc))
        self.assertFalse(imaplib_utils.is_imap4_abort(ValueError("x")))

    def test_is_imap4_readonly(self):
        try:
            raise imaplib.IMAP4.readonly("bad")
        except Exception as exc:
            self.assertTrue(imaplib_utils.is_imap4_readonly(exc))
        self.assertFalse(imaplib_utils.is_imap4_readonly(ValueError("x")))

    def test_create_imap4_ssl_type_errors(self):
        with self.assertRaises(TypeError):
            imaplib_utils.create_imap4_ssl(123)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            imaplib_utils.create_imap4_ssl("localhost", "993")  # type: ignore[arg-type]


if __name__ == "__main__":
    unittest.main()
