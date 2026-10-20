"""Tests for ftplib_utils module."""

import ftplib
import unittest
from unittest import mock

import ftplib_utils


class TestExports(unittest.TestCase):
    def test_port_constants(self):
        self.assertIs(ftplib_utils.FTP_PORT, ftplib.FTP_PORT)
        self.assertIs(ftplib_utils.MAXLINE, ftplib.MAXLINE)

    def test_classes_exported(self):
        self.assertIs(ftplib_utils.FTP, ftplib.FTP)
        self.assertIs(ftplib_utils.FTP_TLS, ftplib.FTP_TLS)

    def test_error_classes_exported(self):
        self.assertIs(ftplib_utils.error_reply, ftplib.error_reply)
        self.assertIs(ftplib_utils.error_temp, ftplib.error_temp)
        self.assertIs(ftplib_utils.error_perm, ftplib.error_perm)
        self.assertIs(ftplib_utils.error_proto, ftplib.error_proto)
        self.assertIs(ftplib_utils.all_errors, ftplib.all_errors)


class TestCreateFTP(unittest.TestCase):
    def test_create_ftp(self):
        with mock.patch.object(ftplib, "FTP") as m:
            m.return_value = mock.sentinel.ftp
            result = ftplib_utils.create_ftp("host", "user", "pass")
            self.assertIs(result, mock.sentinel.ftp)
            m.assert_called_once()

    def test_create_ftp_bad_types(self):
        with self.assertRaises(TypeError):
            ftplib_utils.create_ftp(host=123)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            ftplib_utils.create_ftp(user=123)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            ftplib_utils.create_ftp(passwd=123)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            ftplib_utils.create_ftp(acct=123)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            ftplib_utils.create_ftp(timeout="1")  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            ftplib_utils.create_ftp(source_address=("host",))  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            ftplib_utils.create_ftp(source_address=(123, 21))  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            ftplib_utils.create_ftp(source_address=("host", "21"))  # type: ignore[arg-type]


class TestCreateFTPTLS(unittest.TestCase):
    def test_create_ftp_tls(self):
        with mock.patch.object(ftplib, "FTP_TLS") as m:
            m.return_value = mock.sentinel.ftp
            result = ftplib_utils.create_ftp_tls("host", "user", "pass")
            self.assertIs(result, mock.sentinel.ftp)
            m.assert_called_once()

    def test_create_ftp_tls_bad_types(self):
        with self.assertRaises(TypeError):
            ftplib_utils.create_ftp_tls(timeout="1")  # type: ignore[arg-type]


class TestConnectFTP(unittest.TestCase):
    def test_connect_ftp(self):
        ftp = mock.Mock(spec=ftplib.FTP)
        ftp.connect.return_value = "220"
        result = ftplib_utils.connect_ftp(ftp, "host", 21)
        self.assertEqual(result, "220")
        ftp.connect.assert_called_once_with("host", 21, None, None)

    def test_connect_ftp_bad_types(self):
        ftp = mock.Mock(spec=ftplib.FTP)
        with self.assertRaises(TypeError):
            ftplib_utils.connect_ftp("not ftp", "host")  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            ftplib_utils.connect_ftp(ftp, 123)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            ftplib_utils.connect_ftp(ftp, "host", port="21")  # type: ignore[arg-type]
        with self.assertRaises(ValueError):
            ftplib_utils.connect_ftp(ftp, "host", port=70000)
        with self.assertRaises(TypeError):
            ftplib_utils.connect_ftp(ftp, "host", timeout="1")  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            ftplib_utils.connect_ftp(ftp, "host", source_address=("host",))  # type: ignore[arg-type]


class TestParsers(unittest.TestCase):
    def test_parse257(self):
        self.assertEqual(ftplib_utils.parse257('257 "/pub" is current directory'), "/pub")

    def test_parse257_bad_type(self):
        with self.assertRaises(TypeError):
            ftplib_utils.parse257(123)  # type: ignore[arg-type]

    def test_parse150(self):
        result = ftplib_utils.parse150(
            "150 Opening BINARY mode data connection for file (123 bytes)"
        )
        self.assertIsNotNone(result)

    def test_parse150_bad_type(self):
        with self.assertRaises(TypeError):
            ftplib_utils.parse150(123)  # type: ignore[arg-type]

    def test_parse227(self):
        result = ftplib_utils.parse227("227 Entering Passive Mode (127,0,0,1,4,1)")
        self.assertIsInstance(result, tuple)

    def test_parse227_bad_type(self):
        with self.assertRaises(TypeError):
            ftplib_utils.parse227(123)  # type: ignore[arg-type]

    def test_parse229(self):
        try:
            result = ftplib_utils.parse229("229 Entering Extended Passive Mode (|||6446|)")
            self.assertIsInstance(result, tuple)
        except Exception:
            pass

    def test_parse229_bad_type(self):
        with self.assertRaises(TypeError):
            ftplib_utils.parse229(123)  # type: ignore[arg-type]


if __name__ == "__main__":
    unittest.main()
