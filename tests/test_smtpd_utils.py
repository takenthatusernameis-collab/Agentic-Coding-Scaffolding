"""Tests for smtpd_utils module."""

import unittest
from unittest import mock

import smtpd_utils
from test.support import smtpd


class TestExports(unittest.TestCase):
    def test_classes_exported(self):
        self.assertIs(smtpd_utils.SMTPServer, smtpd.SMTPServer)
        self.assertIs(smtpd_utils.DebuggingServer, smtpd.DebuggingServer)
        self.assertIs(smtpd_utils.PureProxy, smtpd.PureProxy)
        self.assertIs(smtpd_utils.SMTPChannel, smtpd.SMTPChannel)

    def test_constants_exported(self):
        self.assertIs(smtpd_utils.COMMASPACE, smtpd.COMMASPACE)
        self.assertIs(smtpd_utils.NEWLINE, smtpd.NEWLINE)


class TestCreateSMTPServer(unittest.TestCase):
    def test_create_smtp_server(self):
        with mock.patch("smtpd_utils.SMTPServer") as m:
            m.return_value = mock.sentinel.server
            result = smtpd_utils.create_smtp_server(("localhost", 1025))
            self.assertIs(result, mock.sentinel.server)
            m.assert_called_once()

    def test_create_smtp_server_bad_types(self):
        with self.assertRaises(TypeError):
            smtpd_utils.create_smtp_server(localaddr="bad")  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            smtpd_utils.create_smtp_server(localaddr=("host", "25"))  # type: ignore[arg-type]
        with self.assertRaises(ValueError):
            smtpd_utils.create_smtp_server(localaddr=("host", 70000))
        with self.assertRaises(TypeError):
            smtpd_utils.create_smtp_server(enable_SMTPUTF8="true")  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            smtpd_utils.create_smtp_server(map=[])  # type: ignore[arg-type]


class TestCreateDebuggingServer(unittest.TestCase):
    def test_create_debugging_server(self):
        with mock.patch("smtpd_utils.DebuggingServer") as m:
            m.return_value = mock.sentinel.server
            result = smtpd_utils.create_debugging_server(("localhost", 1025))
            self.assertIs(result, mock.sentinel.server)
            m.assert_called_once()


class TestCreatePureProxy(unittest.TestCase):
    def test_create_pure_proxy(self):
        with mock.patch("smtpd_utils.PureProxy") as m:
            m.return_value = mock.sentinel.server
            result = smtpd_utils.create_pure_proxy(("localhost", 1025))
            self.assertIs(result, mock.sentinel.server)
            m.assert_called_once()


class TestProcessMessage(unittest.TestCase):
    def test_process_message(self):
        server = mock.Mock(spec=smtpd.SMTPServer)
        server.process_message.return_value = "250 Ok"
        result = smtpd_utils.process_message(
            server, ("127.0.0.1", 1234), "from@x", ["to@x"], b"data"
        )
        self.assertEqual(result, "250 Ok")
        server.process_message.assert_called_once()

    def test_process_message_bad_types(self):
        server = mock.Mock(spec=smtpd.SMTPServer)
        with self.assertRaises(TypeError):
            smtpd_utils.process_message("bad", ("127.0.0.1", 1), "f", [], b"x")  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            smtpd_utils.process_message(server, ("127.0.0.1", "1"), "f", [], b"x")  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            smtpd_utils.process_message(server, ("127.0.0.1", 1), "f", "[]", b"x")  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            smtpd_utils.process_message(server, ("127.0.0.1", 1), "f", [], "x")  # type: ignore[arg-type]


if __name__ == "__main__":
    unittest.main()
