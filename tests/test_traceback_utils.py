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

            def f1():
                raise IndexError()

            def f2():
                f1()

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


class TestFormatStack(unittest.TestCase):
    def test_format_stack_returns_list(self):
        result = traceback_utils.format_stack()
        self.assertIsInstance(result, list)
        self.assertTrue(all(isinstance(line, str) for line in result))
        self.assertTrue(any("test_traceback_utils" in line for line in result))

    def test_format_stack_with_limit(self):
        def f1():
            return traceback_utils.format_stack(limit=1)

        def f2():
            return f1()

        result = f2()
        self.assertIsInstance(result, list)
        self.assertLessEqual(len(result), 1)

    def test_format_stack_rejects_bad_limit(self):
        with self.assertRaises(TypeError):
            traceback_utils.format_stack(limit="1")  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            traceback_utils.format_stack(limit=True)  # type: ignore[arg-type]


class TestClearFrames(unittest.TestCase):
    def test_clear_frames(self):
        try:
            raise AttributeError("x")
        except AttributeError:
            _, _, tb = sys.exc_info()
            traceback_utils.clear_frames(tb)


class TestExtractStack(unittest.TestCase):
    def test_extract_stack_returns_list(self):
        result = traceback_utils.extract_stack()
        self.assertIsInstance(result, list)
        self.assertTrue(all(hasattr(frame, "filename") for frame in result))
        self.assertTrue(any(frame.filename == __file__ for frame in result))

    def test_extract_stack_with_limit(self):
        def f1():
            traceback_utils.extract_stack(limit=1)

        def f2():
            f1()

        f2()

    def test_extract_stack_rejects_bad_limit(self):
        with self.assertRaises(TypeError):
            traceback_utils.extract_stack(limit="1")  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            traceback_utils.extract_stack(limit=True)  # type: ignore[arg-type]


class TestFormatExc(unittest.TestCase):
    def test_format_exc_empty_when_no_exception(self):
        self.assertEqual(traceback_utils.format_exc(), "")

    def test_format_exc_returns_message(self):
        try:
            raise ValueError("active")
        except ValueError:
            result = traceback_utils.format_exc()
        self.assertIsInstance(result, str)
        self.assertIn("ValueError", result)
        self.assertIn("active", result)

    def test_format_exc_respects_limit(self):
        def f1():
            raise IndexError("deep")

        def f2():
            f1()

        try:
            f2()
        except IndexError:
            result = traceback_utils.format_exc(limit=1)
        self.assertIsInstance(result, str)
        self.assertIn("IndexError", result)

    def test_format_exc_respects_chain(self):
        try:
            try:
                raise ValueError("inner")
            except ValueError:
                raise TypeError("outer")
        except TypeError:
            chained = traceback_utils.format_exc(chain=True)
            unchained = traceback_utils.format_exc(chain=False)
        self.assertIn("TypeError", chained)
        self.assertIn("ValueError", chained)
        self.assertIn("TypeError", unchained)
        self.assertNotIn("ValueError", unchained)

    def test_format_exc_rejects_bad_limit(self):
        with self.assertRaises(TypeError):
            traceback_utils.format_exc(limit="1")  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            traceback_utils.format_exc(limit=True)  # type: ignore[arg-type]

    def test_format_exc_rejects_bad_chain(self):
        with self.assertRaises(TypeError):
            traceback_utils.format_exc(chain="yes")  # type: ignore[arg-type]


if __name__ == "__main__":
    unittest.main()
