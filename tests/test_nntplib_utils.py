"""Tests for nntplib_utils."""

import unittest

import nntplib_utils


class TestExports(unittest.TestCase):
    def test_exports(self) -> None:
        for name in [
            "NNTP",
            "NNTP_SSL",
            "NNTPError",
            "NNTPReplyError",
            "NNTPTemporaryError",
            "NNTPPermanentError",
            "NNTPProtocolError",
            "NNTPDataError",
            "GroupInfo",
            "ArticleInfo",
            "create_nntp",
            "create_nntp_ssl",
            "is_available",
        ]:
            self.assertTrue(hasattr(nntplib_utils, name), name)

    def test_is_available_returns_bool(self) -> None:
        self.assertIsInstance(nntplib_utils.is_available(), bool)


@unittest.skipUnless(nntplib_utils.is_available(), "nntplib not available")
class TestValidation(unittest.TestCase):
    """Exercise argument validation without opening a network connection.

    Every check below raises before the underlying NNTP object is constructed,
    so no socket is created.
    """

    def test_create_nntp_host_must_be_str(self) -> None:
        with self.assertRaises(TypeError):
            nntplib_utils.create_nntp(123)  # type: ignore[arg-type]

    def test_create_nntp_port_must_be_int(self) -> None:
        with self.assertRaises(TypeError):
            nntplib_utils.create_nntp("host", "119")  # type: ignore[arg-type]

    def test_create_nntp_port_rejects_bool(self) -> None:
        with self.assertRaises(TypeError):
            nntplib_utils.create_nntp("host", True)  # type: ignore[arg-type]

    def test_create_nntp_port_range(self) -> None:
        with self.assertRaises(ValueError):
            nntplib_utils.create_nntp("host", 70000)
        with self.assertRaises(ValueError):
            nntplib_utils.create_nntp("host", -1)

    def test_create_nntp_user_must_be_str(self) -> None:
        with self.assertRaises(TypeError):
            nntplib_utils.create_nntp("host", 119, 5)  # type: ignore[arg-type]

    def test_create_nntp_password_must_be_str(self) -> None:
        with self.assertRaises(TypeError):
            nntplib_utils.create_nntp("host", 119, None, 5)  # type: ignore[arg-type]

    def test_create_nntp_timeout_must_be_number(self) -> None:
        with self.assertRaises(TypeError):
            nntplib_utils.create_nntp("host", timeout="soon")  # type: ignore[arg-type]

    def test_create_nntp_ssl_host_must_be_str(self) -> None:
        with self.assertRaises(TypeError):
            nntplib_utils.create_nntp_ssl(123)  # type: ignore[arg-type]

    def test_create_nntp_ssl_port_range(self) -> None:
        with self.assertRaises(ValueError):
            nntplib_utils.create_nntp_ssl("host", 70000)

    def test_create_nntp_ssl_timeout_must_be_number(self) -> None:
        with self.assertRaises(TypeError):
            nntplib_utils.create_nntp_ssl("host", timeout="soon")  # type: ignore[arg-type]


@unittest.skipUnless(nntplib_utils.is_available(), "nntplib not available")
class TestExceptionHierarchy(unittest.TestCase):
    def test_reply_error_is_nntp_error(self) -> None:
        self.assertTrue(issubclass(nntplib_utils.NNTPReplyError, nntplib_utils.NNTPError))

    def test_temporary_error_is_nntp_error(self) -> None:
        self.assertTrue(issubclass(nntplib_utils.NNTPTemporaryError, nntplib_utils.NNTPError))

    def test_permanent_error_is_nntp_error(self) -> None:
        self.assertTrue(issubclass(nntplib_utils.NNTPPermanentError, nntplib_utils.NNTPError))

    def test_protocol_error_is_nntp_error(self) -> None:
        self.assertTrue(issubclass(nntplib_utils.NNTPProtocolError, nntplib_utils.NNTPError))

    def test_data_error_is_nntp_error(self) -> None:
        self.assertTrue(issubclass(nntplib_utils.NNTPDataError, nntplib_utils.NNTPError))


if __name__ == "__main__":
    unittest.main()
