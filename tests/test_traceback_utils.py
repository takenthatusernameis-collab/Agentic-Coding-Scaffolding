import unittest

from traceback_utils import (
    extract_stack,
    format_exc,
    format_exception,
    format_exception_only,
    format_stack,
)


class TestTracebackUtils(unittest.TestCase):
    def test_format_exception_only(self):
        result = format_exception_only(ValueError, ValueError("something went wrong"))
        self.assertIsInstance(result, list)
        self.assertTrue(all(isinstance(line, str) for line in result))
        self.assertTrue(any("something went wrong" in line for line in result))

    def test_format_exception(self):
        try:
            raise ValueError("boom")
        except ValueError as exc:
            result = format_exception(exc)
        self.assertIsInstance(result, list)
        self.assertTrue(any("boom" in line for line in result))

    def test_extract_stack(self):
        result = extract_stack()
        self.assertIsInstance(result, list)
        self.assertGreaterEqual(len(result), 1)

    def test_format_stack(self):
        result = format_stack()
        self.assertIsInstance(result, list)
        self.assertGreaterEqual(len(result), 1)
        self.assertTrue(all(isinstance(line, str) for line in result))

    def test_format_exc_no_exception(self):
        result = format_exc()
        self.assertIsInstance(result, str)
        self.assertEqual(result, "")

    def test_format_exc_with_exception(self):
        try:
            raise RuntimeError("traceback test")
        except RuntimeError:
            result = format_exc()
        self.assertIsInstance(result, str)
        self.assertIn("RuntimeError", result)
        self.assertIn("traceback test", result)


if __name__ == "__main__":
    unittest.main()
