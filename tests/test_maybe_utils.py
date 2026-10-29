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

    def test_map_or(self) -> None:
        self.assertEqual(Maybe.some(5).map_or(0, lambda x: x * 2), 10)
        self.assertEqual(Maybe.nothing().map_or(0, lambda x: x * 2), 0)

    def test_map_or_default_returned_on_nothing(self) -> None:
        self.assertEqual(Maybe.nothing().map_or(-1, lambda x: x + 1), -1)

    def test_map_or_passes_value_through_fn(self) -> None:
        self.assertEqual(Maybe.some(3).map_or(0, lambda x: x - 1), 2)

    def test_map_or_returns_default_when_fn_returns_none(self) -> None:
        self.assertEqual(Maybe.some(5).map_or(0, lambda x: None), 0)  # type: ignore[arg-type,return-value]

    def test_map_or_returns_default_when_fn_raises(self) -> None:
        def boom(x: int) -> int:
            raise RuntimeError("boom")

        self.assertEqual(Maybe.some(5).map_or(0, boom), 0)

    def test_map_or_default_returned_on_nothing_with_raising_fn(self) -> None:
        def boom(x: int) -> int:
            raise RuntimeError("boom")

        self.assertEqual(Maybe.nothing().map_or(7, boom), 7)

    def test_map_or_floats(self) -> None:
        self.assertAlmostEqual(Maybe.some(2.5).map_or(0.0, lambda x: x * 2.0), 5.0)
        self.assertEqual(Maybe.nothing().map_or(1.5, lambda x: x * 2.0), 1.5)

    def test_map_or_else(self) -> None:
        self.assertEqual(Maybe.some(5).map_or_else(lambda: 0, lambda x: x * 2), 10)
        self.assertEqual(Maybe.nothing().map_or_else(lambda: 7, lambda x: x * 2), 7)

    def test_map_or_else_returns_default_when_fn_returns_none(self) -> None:
        self.assertEqual(Maybe.some(5).map_or_else(lambda: 0, lambda x: None), 0)  # type: ignore[arg-type,return-value]

    def test_map_or_else_calls_default_when_fn_raises(self) -> None:
        def boom(x: int) -> int:
            raise RuntimeError("boom")

        self.assertEqual(Maybe.some(5).map_or_else(lambda: 42, boom), 42)


if __name__ == "__main__":
    unittest.main()
