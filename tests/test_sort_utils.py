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


if __name__ == "__main__":
    unittest.main()
