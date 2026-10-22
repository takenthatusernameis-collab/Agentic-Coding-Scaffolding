"""Tests for nntplib_utils."""

import unittest

from nntplib_utils import (
    NNTP_PORT,
    NNTP_SSL_PORT,
    NNTPError,
    create_nntp,
    create_nntp_ssl,
)


class TestNntplibUtils(unittest.TestCase):
    def test_constants(self):
        self.assertIsInstance(NNTP_PORT, int)
        self.assertIsInstance(NNTP_SSL_PORT, int)

    def test_create_nntp_type_error(self):
        with self.assertRaises(TypeError):
            create_nntp(123)  # type: ignore[arg-type]

    def test_create_nntp_ssl_type_error(self):
        with self.assertRaises(TypeError):
            create_nntp_ssl(123)  # type: ignore[arg-type]


if __name__ == "__main__":
    unittest.main()