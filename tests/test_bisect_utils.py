"""Tests for bisect_utils."""

import unittest

from bisect_utils import (
    bisect_left,
    bisect_right,
    find_leftmost,
    find_rightmost,
    insort_left,
    insort_right,
    is_sorted,
)


class TestBisectLeftRight(unittest.TestCase):
    def test_bisect_left(self) -> None:
        a = [1, 2, 2, 3]
        self.assertEqual(bisect_left(a, 2), 1)
        self.assertEqual(bisect_left(a, 0), 0)
        self.assertEqual(bisect_left(a, 5), 4)

    def test_bisect_right(self) -> None:
        a = [1, 2, 2, 3]
        self.assertEqual(bisect_right(a, 2), 3)
        self.assertEqual(bisect_right(a, 0), 0)
        self.assertEqual(bisect_right(a, 5), 4)

    def test_empty(self) -> None:
        self.assertEqual(bisect_left([], 1), 0)
        self.assertEqual(bisect_right([], 1), 0)

    def test_lo_hi(self) -> None:
        a = [1, 2, 3, 4, 5]
        self.assertEqual(bisect_left(a, 3, 2, 5), 2)
        self.assertEqual(bisect_right(a, 3, 0, 2), 2)

    def test_type_errors(self) -> None:
        with self.assertRaises(TypeError):
            bisect_left(42, 1)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            bisect_right(None, 1)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            bisect_left([1, 2], 1, lo=True)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            bisect_left([1, 2], 1, hi=1.5)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            bisect_right([1, 2], 1, lo=False)  # type: ignore[arg-type]


class TestInsort(unittest.TestCase):
    def test_insort_left(self) -> None:
        a = [1, 3, 5]
        insort_left(a, 2)
        self.assertEqual(a, [1, 2, 3, 5])

    def test_insort_right(self) -> None:
        a = [1, 2, 3, 5]
        insort_right(a, 3)
        self.assertEqual(a, [1, 2, 3, 3, 5])

    def test_insort_empty(self) -> None:
        a: list[int] = []
        insort_left(a, 1)
        self.assertEqual(a, [1])
        insort_right(a, 1)
        self.assertEqual(a, [1, 1])

    def test_insort_lo_hi(self) -> None:
        a = [1, 2, 3, 4]
        insort_left(a, 2, 1, 4)
        self.assertEqual(a, [1, 2, 2, 3, 4])

    def test_type_errors(self) -> None:
        with self.assertRaises(TypeError):
            insort_left((1, 2), 1)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            insort_right("ab", "c")  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            insort_left([1, 2], 1, lo=True)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            insort_right([1, 2], 1, hi=2.0)  # type: ignore[arg-type]


class TestFind(unittest.TestCase):
    def test_find_leftmost(self) -> None:
        a = [1, 2, 2, 3]
        self.assertEqual(find_leftmost(a, 2), 1)
        self.assertIsNone(find_leftmost(a, 9))

    def test_find_rightmost(self) -> None:
        a = [1, 2, 2, 3]
        self.assertEqual(find_rightmost(a, 2), 2)
        self.assertIsNone(find_rightmost(a, 9))

    def test_empty(self) -> None:
        self.assertIsNone(find_leftmost([], 1))
        self.assertIsNone(find_rightmost([], 1))

    def test_type_errors(self) -> None:
        with self.assertRaises(TypeError):
            find_leftmost(42, 1)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            find_rightmost(None, 1)  # type: ignore[arg-type]


class TestIsSorted(unittest.TestCase):
    def test_sorted(self) -> None:
        self.assertTrue(is_sorted([1, 2, 3]))
        self.assertTrue(is_sorted([1, 2, 2, 3]))
        self.assertTrue(is_sorted([]))
        self.assertTrue(is_sorted([5]))
        self.assertFalse(is_sorted([3, 2, 1]))

    def test_reverse(self) -> None:
        self.assertTrue(is_sorted([3, 2, 1], reverse=True))
        self.assertFalse(is_sorted([1, 2, 3], reverse=True))

    def test_type_error(self) -> None:
        with self.assertRaises(TypeError):
            is_sorted(42)  # type: ignore[arg-type]
