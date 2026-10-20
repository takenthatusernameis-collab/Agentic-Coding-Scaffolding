"""Tests for timeit_utils module."""

import unittest

from timeit_utils import Timer, default_timer, repeat, timeit


class TestDefaultTimer(unittest.TestCase):
    def test_returns_float(self):
        self.assertIsInstance(default_timer(), float)


class TestTimeit(unittest.TestCase):
    def test_basic(self):
        result = timeit("pass", number=10)
        self.assertIsInstance(result, float)
        self.assertGreaterEqual(result, 0.0)

    def test_with_globals(self):
        result = timeit("x + 1", globals={"x": 5}, number=10)
        self.assertIsInstance(result, float)


class TestRepeat(unittest.TestCase):
    def test_basic(self):
        result = repeat("pass", number=10, repeat=3)
        self.assertEqual(len(result), 3)
        for r in result:
            self.assertIsInstance(r, float)


class TestTimer(unittest.TestCase):
    def test_timer_instance(self):
        t = Timer("pass")
        result = t.timeit(number=10)
        self.assertIsInstance(result, float)

    def test_repeat(self):
        t = Timer("pass")
        result = t.repeat(repeat=2, number=10)
        self.assertEqual(len(result), 2)


if __name__ == "__main__":
    unittest.main()
