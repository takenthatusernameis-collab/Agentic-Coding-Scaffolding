"""Tests for traceback_utils module."""

import sys
import unittest

import traceback_utils


class TestFormatException(unittest.TestCase):
    def test_format_exception(self):
        try:
            raise ValueError("test error")
        except ValueError:
            etype, value, tb = sys.exc_info()
            result = traceback_utils.format_exception(etype, value, tb)
            self.assertIsInstance(result, list)
            self.assertTrue(any("ValueError" in line for line in result))

    def test_format_exception_type_error(self):
        with self.assertRaises(TypeError):
            traceback_utils.format_exception("bad", ValueError("x"), None)

    def test_format_exception_only(self):
        result = traceback_utils.format_exception_only(ValueError, ValueError("test"))
        self.assertIsInstance(result, list)
        self.assertTrue(any("ValueError" in line for line in result))


class TestFormatTb(unittest.TestCase):
    def test_format_tb(self):
        try:
            raise RuntimeError("oops")
        except RuntimeError:
            _, _, tb = sys.exc_info()
            result = traceback_utils.format_tb(tb)
            self.assertIsInstance(result, list)


class TestExtractTb(unittest.TestCase):
    def test_extract_tb(self):
        try:
            raise KeyError("missing")
        except KeyError:
            _, _, tb = sys.exc_info()
            result = traceback_utils.extract_tb(tb)
            self.assertIsInstance(result, list)

    def test_extract_tb_with_limit(self):
        try:
            def f1(): raise IndexError()
            def f2(): f1()
            f2()
        except IndexError:
            _, _, tb = sys.exc_info()
            result = traceback_utils.extract_tb(tb, limit=1)
            self.assertIsInstance(result, list)


class TestPrintFunctions(unittest.TestCase):
    def test_print_tb(self):
        try:
            raise OSError("fail")
        except OSError:
            _, _, tb = sys.exc_info()
            traceback_utils.print_tb(tb)

    def test_print_stack(self):
        traceback_utils.print_stack()

    def test_print_exception(self):
        try:
            raise TypeError("bad")
        except TypeError:
            etype, value, tb = sys.exc_info()
            traceback_utils.print_exception(etype, value, tb)


class TestClearFrames(unittest.TestCase):
    def test_clear_frames(self):
        try:
            raise AttributeError("x")
        except AttributeError:
            _, _, tb = sys.exc_info()
            traceback_utils.clear_frames(tb)


if __name__ == "__main__":
    unittest.main()
