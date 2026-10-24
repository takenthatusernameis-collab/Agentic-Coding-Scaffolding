"""Tests for either_utils module."""

import unittest

from either_utils import Either


class TestEither(unittest.TestCase):
    def test_right_creation(self) -> None:
        e = Either.right(42)
        self.assertTrue(e.is_right())
        self.assertFalse(e.is_left())
        self.assertTrue(e.is_ok())
        self.assertFalse(e.is_err())
        self.assertEqual(e.unwrap(), 42)

    def test_left_creation(self) -> None:
        e = Either.left("error")
        self.assertFalse(e.is_right())
        self.assertTrue(e.is_left())
        self.assertFalse(e.is_ok())
        self.assertTrue(e.is_err())

    def test_ok_err_aliases(self) -> None:
        self.assertTrue(Either.ok(5).is_ok())
        self.assertTrue(Either.err("bad").is_err())

    def test_from_optional(self) -> None:
        self.assertTrue(Either.from_optional(5, "missing").is_right())
        self.assertTrue(Either.from_optional(None, "missing").is_left())

    def test_unwrap_raises_on_left(self) -> None:
        with self.assertRaises(ValueError):
            Either.left("error").unwrap()

    def test_unwrap_left_raises_on_right(self) -> None:
        with self.assertRaises(ValueError):
            Either.right(42).unwrap_left()

    def test_unwrap_or(self) -> None:
        self.assertEqual(Either.right(10).unwrap_or(0), 10)
        self.assertEqual(Either.left("err").unwrap_or(0), 0)

    def test_unwrap_or_else(self) -> None:
        self.assertEqual(Either.right(10).unwrap_or_else(lambda e: 0), 10)
        self.assertEqual(Either.left("err").unwrap_or_else(lambda e: len(e)), 3)

    def test_map(self) -> None:
        e = Either.right(5).map(lambda x: x * 2)
        self.assertEqual(e.unwrap(), 10)
        self.assertTrue(Either.left("err").map(lambda x: x * 2).is_left())

    def test_map_left(self) -> None:
        e = Either.left("err").map_left(lambda e: e.upper())
        self.assertEqual(e.unwrap_left(), "ERR")
        self.assertTrue(Either.right(5).map_left(lambda e: e).is_right())

    def test_flat_map(self) -> None:
        e = Either.right(5).flat_map(lambda x: Either.right(x + 1))
        self.assertEqual(e.unwrap(), 6)
        self.assertTrue(Either.left("err").flat_map(lambda x: Either.right(x)).is_left())

    def test_or_else(self) -> None:
        self.assertEqual(Either.right(1).or_else(Either.right(2)).unwrap(), 1)
        self.assertEqual(Either.left("a").or_else(Either.right(2)).unwrap(), 2)

    def test_fold(self) -> None:
        self.assertEqual(Either.right(5).fold(lambda e: -1, lambda x: x * 2), 10)
        self.assertEqual(Either.left("err").fold(lambda e: len(e), lambda x: x), 3)

    def test_swap(self) -> None:
        e = Either.left("err").swap()
        self.assertTrue(e.is_right())
        e2 = Either.right(5).swap()
        self.assertTrue(e2.is_left())

    def test_bool(self) -> None:
        self.assertTrue(bool(Either.right(1)))
        self.assertFalse(bool(Either.left("err")))

    def test_eq(self) -> None:
        self.assertEqual(Either.right(1), Either.right(1))
        self.assertNotEqual(Either.right(1), Either.right(2))
        self.assertEqual(Either.left("a"), Either.left("a"))
        self.assertNotEqual(Either.right(1), Either.left(1))


if __name__ == "__main__":
    unittest.main()
