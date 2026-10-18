"""Tests for contextlib_utils."""

import io
import os
import tempfile
import unittest

from contextlib_utils import (
    ExitStack,
    chdir,
    closing,
    nullcontext,
    redirect_stderr,
    redirect_stdout,
    suppress,
)


class TestContextlibUtils(unittest.TestCase):
    def test_suppress(self):
        with suppress(ValueError):
            raise ValueError("boom")

    def test_nullcontext(self):
        with nullcontext(42) as v:
            self.assertEqual(v, 42)

    def test_closing(self):
        buf = io.StringIO()
        with closing(buf):
            buf.write("hi")
        self.assertTrue(buf.closed)

    def test_redirect_stdout(self):
        buf = io.StringIO()
        with redirect_stdout(buf):
            print("hello")
        self.assertEqual(buf.getvalue().strip(), "hello")

    def test_redirect_stderr(self):
        buf = io.StringIO()
        with redirect_stderr(buf):
            print("err", file=__import__("sys").stderr)
        self.assertEqual(buf.getvalue().strip(), "err")

    def test_chdir(self):
        here = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            with chdir(tmp):
                self.assertEqual(os.getcwd(), tmp)
        self.assertEqual(os.getcwd(), here)

    def test_chdir_type_error(self):
        with self.assertRaises(TypeError):
            with chdir(123):
                pass

    def test_exitstack(self):
        with ExitStack() as stack:
            buf = io.StringIO()
            stack.callback(buf.close)
        self.assertTrue(buf.closed)


if __name__ == "__main__":
    unittest.main()