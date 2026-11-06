"""Tests for sort_utils."""

import unittest

import sort_utils


class TestSortUtils(unittest.TestCase):
    def test_is_sorted(self):
        self.assertTrue(sort_utils.is_sorted([1, 2, 3]))
        self.assertFalse(sort_utils.is_sorted([3, 1, 2]))

    def test_bubble_sort(self):
        self.assertEqual(sort_utils.bubble_sort([3, 1, 2]), [1, 2, 3])

    def test_merge_sort(self):
        self.assertEqual(sort_utils.merge_sort([3, 1, 2]), [1, 2, 3])

    def test_reverse(self):
        self.assertEqual(sort_utils.merge_sort([1, 2, 3], reverse=True), [3, 2, 1])

    def test_key(self):
        self.assertEqual(sort_utils.top_n([("a", 2), ("b", 1)], 1, key=lambda x: x[1]), [("a", 2)])

    def test_nth_largest(self):
        self.assertEqual(sort_utils.nth_largest([1, 2, 3], 2), 2)


class TestInsertionSort(unittest.TestCase):
    def test_basic(self):
        self.assertEqual(sort_utils.insertion_sort([3, 1, 2]), [1, 2, 3])

    def test_reverse(self):
        self.assertEqual(sort_utils.insertion_sort([1, 2, 3], reverse=True), [3, 2, 1])

    def test_key(self):
        self.assertEqual(
            sort_utils.insertion_sort([("a", 2), ("b", 1)], key=lambda x: x[1]),
            [("b", 1), ("a", 2)],
        )

    def test_empty(self):
        self.assertEqual(sort_utils.insertion_sort([]), [])

    def test_single(self):
        self.assertEqual(sort_utils.insertion_sort([5]), [5])

    def test_already_sorted(self):
        self.assertEqual(sort_utils.insertion_sort([1, 2, 3]), [1, 2, 3])

    def test_duplicates(self):
        self.assertEqual(sort_utils.insertion_sort([2, 1, 2, 1]), [1, 1, 2, 2])

    def test_stability(self):
        items = [("a", 1), ("b", 1), ("c", 1)]
        self.assertEqual(sort_utils.insertion_sort(items, key=lambda x: x[1]), items)


class TestSelectionSort(unittest.TestCase):
    def test_basic(self):
        self.assertEqual(sort_utils.selection_sort([3, 1, 2]), [1, 2, 3])

    def test_reverse(self):
        self.assertEqual(sort_utils.selection_sort([1, 2, 3], reverse=True), [3, 2, 1])

    def test_key(self):
        self.assertEqual(
            sort_utils.selection_sort([("a", 2), ("b", 1)], key=lambda x: x[1]),
            [("b", 1), ("a", 2)],
        )

    def test_empty(self):
        self.assertEqual(sort_utils.selection_sort([]), [])

    def test_single(self):
        self.assertEqual(sort_utils.selection_sort([5]), [5])

    def test_already_sorted(self):
        self.assertEqual(sort_utils.selection_sort([1, 2, 3]), [1, 2, 3])

    def test_duplicates(self):
        self.assertEqual(sort_utils.selection_sort([2, 1, 2, 1]), [1, 1, 2, 2])

    def test_matches_reference(self):
        import random

        for _ in range(50):
            items = [random.randint(-100, 100) for _ in range(random.randint(0, 30))]
            self.assertEqual(sort_utils.selection_sort(items), sorted(items))
            self.assertEqual(
                sort_utils.selection_sort(items, reverse=True),
                sorted(items, reverse=True),
            )

    def test_does_not_mutate_input(self):
        items = [3, 1, 2]
        result = sort_utils.selection_sort(items)
        self.assertEqual(items, [3, 1, 2])
        self.assertEqual(result, [1, 2, 3])

    def test_string_items(self):
        self.assertEqual(
            sort_utils.selection_sort(["banana", "apple", "cherry"]),
            ["apple", "banana", "cherry"],
        )


if __name__ == "__main__":
    unittest.main()
