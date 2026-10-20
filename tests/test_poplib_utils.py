"""Tests for poplib_utils module."""

import poplib
import unittest
from unittest import mock

import poplib_utils


class TestExports(unittest.TestCase):
    def test_constants(self):
        self.assertIs(poplib_utils.POP3_PORT, poplib.POP3_PORT)
        self.assertIs(poplib_utils.POP3_SSL_PORT, poplib.POP3_SSL_PORT)
        self.assertIs(poplib_utils.POP3, poplib.POP3)
        self.assertIs(poplib_utils.POP3_SSL, poplib.POP3_SSL)
        self.assertIs(poplib_utils.error_proto, poplib.error_proto)


class TestCreatePOP3(unittest.TestCase):
    def test_create_pop3(self):
        with mock.patch.object(poplib, "POP3") as m:
            m.return_value = mock.sentinel.pop
            result = poplib_utils.create_pop3("host")
            self.assertIs(result, mock.sentinel.pop)

    def test_create_pop3_bad_types(self):
        with self.assertRaises(TypeError):
            poplib_utils.create_pop3(host=123)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            poplib_utils.create_pop3(port="110")  # type: ignore[arg-type]
        with self.assertRaises(ValueError):
            poplib_utils.create_pop3(port=70000)
        with self.assertRaises(TypeError):
            poplib_utils.create_pop3(timeout="1")  # type: ignore[arg-type]


class TestCreatePOP3SSL(unittest.TestCase):
    def test_create_pop3_ssl(self):
        with mock.patch.object(poplib, "POP3_SSL") as m:
            m.return_value = mock.sentinel.pop
            result = poplib_utils.create_pop3_ssl("host")
            self.assertIs(result, mock.sentinel.pop)

    def test_create_pop3_ssl_bad_types(self):
        with self.assertRaises(TypeError):
            poplib_utils.create_pop3_ssl(keyfile=123)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            poplib_utils.create_pop3_ssl(certfile=123)  # type: ignore[arg-type]


class TestConnectPOP3(unittest.TestCase):
    def test_connect_pop3(self):
        pop3 = mock.Mock(spec=poplib.POP3)
        poplib_utils.connect_pop3(pop3, "host")
        pop3._shortcmd.assert_called_once()

    def test_connect_pop3_bad_types(self):
        with self.assertRaises(TypeError):
            poplib_utils.connect_pop3("not pop", "host")  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            poplib_utils.connect_pop3(mock.Mock(spec=poplib.POP3), 123)  # type: ignore[arg-type]


if __name__ == "__main__":
    unittest.main()
