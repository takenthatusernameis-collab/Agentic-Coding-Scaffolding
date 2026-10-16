"""Tests for heapq_utils module."""

from __future__ import annotations

import unittest

from heapq_utils import (
    heapify,
    heappop,
    heappush,
    heappushpop,
    heapreplace,
    merge,
    nlargest,
    nsmallest,
)


class TestHeapify(unittest.TestCase):
    def test_heapify_in_place(self) -> None:
        items = [3, 1, 4, 1, 5, 9, 2, 6]
        heapify(items)
        self.assertEqual(items[0], min(items))

    def test_heapify_empty(self) -> None:
        items: list[int] = []
        heapify(items)
        self.assertEqual(items, [])

    def test_heapify_type_error(self) -> None:
        with self.assertRaises(TypeError):
            heapify("not a list")  # type: ignore[arg-type]


class TestHeappush(unittest.TestCase):
    def test_push_pop_order(self) -> None:
        items: list[int] = []
        for value in [5, 1, 3, 2, 4]:
            heappush(items, value)
        self.assertEqual([heappop(items) for _ in range(len(items))], [1, 2, 3, 4, 5])

    def test_push_type_error(self) -> None:
        with self.assertRaises(TypeError):
            heappush("not a list", 1)  # type: ignore[arg-type]


class TestHeappop(unittest.TestCase):
    def test_heappop(self) -> None:
        items = [5, 1, 3]
        heapify(items)
        self.assertEqual(heappop(items), 1)

    def test_heappop_empty(self) -> None:
        items: list[int] = []
        with self.assertRaises(IndexError):
            heappop(items)

    def test_heappop_type_error(self) -> None:
        with self.assertRaises(TypeError):
            heappop("not a list")  # type: ignore[arg-type]


class TestHeapreplace(unittest.TestCase):
    def test_heapreplace(self) -> None:
        items = [1, 3, 5]
        heapify(items)
        self.assertEqual(heapreplace(items, 2), 1)
        self.assertEqual(items[0], 2)

    def test_heapreplace_empty(self) -> None:
        items: list[int] = []
        with self.assertRaises(IndexError):
            heapreplace(items, 1)


class TestHeappushpop(unittest.TestCase):
    def test_heappushpop(self) -> None:
        items = [1, 3, 5]
        heapify(items)
        self.assertEqual(heappushpop(items, 2), 1)

    def test_heappushpop_type_error(self) -> None:
        with self.assertRaises(TypeError):
            heappushpop("not a list", 1)  # type: ignore[arg-type]


class TestMerge(unittest.TestCase):
    def test_merge_sorted(self) -> None:
        result = list(merge([1, 3, 5], [2, 4, 6]))
        self.assertEqual(result, [1, 2, 3, 4, 5, 6])

    def test_merge_reverse(self) -> None:
        result = list(merge([5, 3, 1], [6, 4, 2], reverse=True))
        self.assertEqual(result, [6, 5, 4, 3, 2, 1])

    def test_merge_type_error(self) -> None:
        with self.assertRaises(TypeError):
            merge(123)  # type: ignore[arg-type]


class TestNlargest(unittest.TestCase):
    def test_nlargest(self) -> None:
        self.assertEqual(nlargest(2, [1, 5, 3, 4, 2]), [5, 4])

    def test_nlargest_zero(self) -> None:
        self.assertEqual(nlargest(0, [1, 2, 3]), [])

    def test_nlargest_key(self) -> None:
        self.assertEqual(nlargest(1, ["a", "bb", "ccc"], key=len), ["ccc"])

    def test_nlargest_type_errors(self) -> None:
        with self.assertRaises(TypeError):
            nlargest(1, 123)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            nlargest("one", [1, 2, 3])  # type: ignore[arg-type]

    def test_nlargest_value_error(self) -> None:
        with self.assertRaises(ValueError):
            nlargest(-1, [1, 2, 3])


class TestNsmallest(unittest.TestCase):
    def test_nsmallest(self) -> None:
        self.assertEqual(nsmallest(2, [1, 5, 3, 4, 2]), [1, 2])

    def test_nsmallest_zero(self) -> None:
        self.assertEqual(nsmallest(0, [1, 2, 3]), [])

    def test_nsmallest_key(self) -> None:
        self.assertEqual(nsmallest(1, ["ccc", "bb", "a"], key=len), ["a"])

    def test_nsmallest_type_errors(self) -> None:
        with self.assertRaises(TypeError):
            nsmallest(1, 123)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            nsmallest("one", [1, 2, 3])  # type: ignore[arg-type]

    def test_nsmallest_value_error(self) -> None:
        with self.assertRaises(ValueError):
            nsmallest(-1, [1, 2, 3])


if __name__ == "__main__":
    unittest.main()
