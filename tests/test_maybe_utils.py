"""Tests for maybe_utils module."""

import unittest

from maybe_utils import Maybe


class TestMaybe(unittest.TestCase):
    def test_some_creation(self) -> None:
        m = Maybe.some(42)
        self.assertTrue(m.is_some())
        self.assertFalse(m.is_nothing())
        self.assertEqual(m.unwrap(), 42)

    def test_nothing_creation(self) -> None:
        m = Maybe.nothing()
        self.assertFalse(m.is_some())
        self.assertTrue(m.is_nothing())

    def test_from_optional(self) -> None:
        self.assertTrue(Maybe.from_optional(5).is_some())
        self.assertTrue(Maybe.from_optional(None).is_nothing())

    def test_unwrap_raises_on_nothing(self) -> None:
        with self.assertRaises(ValueError):
            Maybe.nothing().unwrap()

    def test_unwrap_or(self) -> None:
        self.assertEqual(Maybe.some(10).unwrap_or(0), 10)
        self.assertEqual(Maybe.nothing().unwrap_or(0), 0)

    def test_unwrap_or_else(self) -> None:
        self.assertEqual(Maybe.some(10).unwrap_or_else(lambda: 0), 10)
        self.assertEqual(Maybe.nothing().unwrap_or_else(lambda: 5), 5)

    def test_map(self) -> None:
        m = Maybe.some(5).map(lambda x: x * 2)
        self.assertEqual(m.unwrap(), 10)
        self.assertTrue(Maybe.nothing().map(lambda x: x * 2).is_nothing())

    def test_flat_map(self) -> None:
        m = Maybe.some(5).flat_map(lambda x: Maybe.some(x + 1))
        self.assertEqual(m.unwrap(), 6)

    def test_filter(self) -> None:
        self.assertTrue(Maybe.some(10).filter(lambda x: x > 5).is_some())
        self.assertTrue(Maybe.some(3).filter(lambda x: x > 5).is_nothing())

    def test_or_else(self) -> None:
        self.assertEqual(Maybe.some(1).or_else(Maybe.some(2)).unwrap(), 1)
        self.assertEqual(Maybe.nothing().or_else(Maybe.some(2)).unwrap(), 2)

    def test_bool(self) -> None:
        self.assertTrue(bool(Maybe.some(1)))
        self.assertFalse(bool(Maybe.nothing()))

    def test_eq(self) -> None:
        self.assertEqual(Maybe.some(1), Maybe.some(1))
        self.assertNotEqual(Maybe.some(1), Maybe.some(2))
        self.assertEqual(Maybe.nothing(), Maybe.nothing())


if __name__ == "__main__":
    unittest.main()
