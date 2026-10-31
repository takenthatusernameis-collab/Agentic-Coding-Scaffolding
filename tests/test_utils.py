"""Tests for utils module."""

import unittest

from utils import (
    chunk,
    compact,
    first,
    flatten,
    is_empty,
    last,
    remove_none,
    second,
    unique,
)


class TestFlatten(unittest.TestCase):
    def test_flatten_basic(self) -> None:
        self.assertEqual(flatten([[1, 2], [3, 4]]), [1, 2, 3, 4])

    def test_flatten_empty(self) -> None:
        self.assertEqual(flatten([]), [])

    def test_flatten_nested_empty(self) -> None:
        self.assertEqual(flatten([[], [1], []]), [1])


class TestChunk(unittest.TestCase):
    def test_chunk_basic(self) -> None:
        self.assertEqual(chunk([1, 2, 3, 4], 2), [[1, 2], [3, 4]])

    def test_chunk_remainder(self) -> None:
        self.assertEqual(chunk([1, 2, 3], 2), [[1, 2], [3]])

    def test_chunk_size_larger(self) -> None:
        self.assertEqual(chunk([1, 2], 5), [[1, 2]])

    def test_chunk_invalid_size(self) -> None:
        with self.assertRaises(ValueError):
            chunk([1, 2, 3], 0)


class TestUnique(unittest.TestCase):
    def test_unique_basic(self) -> None:
        self.assertEqual(unique([1, 2, 2, 3]), [1, 2, 3])

    def test_unique_preserves_order(self) -> None:
        self.assertEqual(unique([3, 1, 2, 1]), [3, 1, 2])

    def test_unique_all_unique(self) -> None:
        self.assertEqual(unique([1, 2, 3]), [1, 2, 3])


class TestIsEmpty(unittest.TestCase):
    def test_is_empty_none(self) -> None:
        self.assertTrue(is_empty(None))

    def test_is_empty_empty_string(self) -> None:
        self.assertTrue(is_empty(""))

    def test_is_empty_empty_list(self) -> None:
        self.assertTrue(is_empty([]))

    def test_is_empty_empty_dict(self) -> None:
        self.assertTrue(is_empty({}))

    def test_is_empty_non_empty(self) -> None:
        self.assertFalse(is_empty("hello"))
        self.assertFalse(is_empty([1]))
        self.assertFalse(is_empty(5))


class TestRemoveNone(unittest.TestCase):
    def test_remove_none_basic(self) -> None:
        self.assertEqual(remove_none([1, None, 2, None, 3]), [1, 2, 3])

    def test_remove_none_no_none(self) -> None:
        self.assertEqual(remove_none([1, 2, 3]), [1, 2, 3])

    def test_remove_none_all_none(self) -> None:
        self.assertEqual(remove_none([None, None]), [])

    def test_remove_none_empty(self) -> None:
        self.assertEqual(remove_none([]), [])


class TestLast(unittest.TestCase):
    def test_last_basic(self) -> None:
        self.assertEqual(last([1, 2, 3]), 3)

    def test_last_single(self) -> None:
        self.assertEqual(last([5]), 5)

    def test_last_empty_raises(self) -> None:
        with self.assertRaises(ValueError):
            last([])


class TestFirst(unittest.TestCase):
    def test_first_basic(self) -> None:
        self.assertEqual(first([1, 2, 3]), 1)

    def test_first_single(self) -> None:
        self.assertEqual(first([5]), 5)

    def test_first_empty_raises(self) -> None:
        with self.assertRaises(ValueError):
            first([])


class TestSecond(unittest.TestCase):
    def test_second_basic(self) -> None:
        self.assertEqual(second([1, 2, 3]), 2)

    def test_second_single_raises(self) -> None:
        with self.assertRaises(ValueError):
            second([5])

    def test_second_empty_raises(self) -> None:
        with self.assertRaises(ValueError):
            second([])


class TestCompact(unittest.TestCase):
    def test_compact_removes_falsy(self) -> None:
        self.assertEqual(compact([0, 1, "", 2, None, 3, [], 4]), [1, 2, 3, 4])

    def test_compact_all_truthy(self) -> None:
        self.assertEqual(compact([1, 2, 3]), [1, 2, 3])

    def test_compact_all_falsy(self) -> None:
        self.assertEqual(compact([0, "", None, [], {}]), [])

    def test_compact_empty(self) -> None:
        self.assertEqual(compact([]), [])
