"""Tests for collections_utils module."""

import unittest
from collections import deque

from collections_utils import (
    chunk,
    compact,
    deep_flatten,
    flatten,
    frequency,
    least_common,
    merge_dicts,
    most_common,
    partition_by,
    pluck,
    to_deque,
    uniq,
    uniq_by,
    windowed,
)


class TestChunk(unittest.TestCase):
    def test_chunk_basic(self):
        result = list(chunk([1, 2, 3, 4, 5], 2))
        self.assertEqual(result, [[1, 2], [3, 4], [5]])

    def test_chunk_exact(self):
        result = list(chunk([1, 2, 3, 4], 2))
        self.assertEqual(result, [[1, 2], [3, 4]])

    def test_chunk_size_one(self):
        result = list(chunk([1, 2, 3], 1))
        self.assertEqual(result, [[1], [2], [3]])

    def test_chunk_errors(self):
        with self.assertRaises(TypeError):
            list(chunk([1, 2, 3], "2"))  # type: ignore

        with self.assertRaises(ValueError):
            list(chunk([1, 2, 3], 0))

        with self.assertRaises(ValueError):
            list(chunk([1, 2, 3], -1))


class TestFlatten(unittest.TestCase):
    def test_flatten_basic(self):
        result = flatten([1, [2, 3], [4], 5])
        self.assertEqual(result, [1, 2, 3, 4, 5])

    def test_flatten_with_tuples(self):
        result = flatten([1, (2, 3), 4])
        self.assertEqual(result, [1, 2, 3, 4])

    def test_flatten_empty(self):
        result = flatten([])
        self.assertEqual(result, [])


class TestDeepFlatten(unittest.TestCase):
    def test_deep_flatten_basic(self):
        result = deep_flatten([1, [2, [3, 4]], 5])
        self.assertEqual(result, [1, 2, 3, 4, 5])

    def test_deep_flatten_multiple_levels(self):
        result = deep_flatten([1, [2, [3, [4]]]])
        self.assertEqual(result, [1, 2, 3, 4])


class TestWindowed(unittest.TestCase):
    def test_windowed_basic(self):
        result = list(windowed([1, 2, 3, 4], 2))
        self.assertEqual(result, [(1, 2), (2, 3), (3, 4)])

    def test_windowed_size_three(self):
        result = list(windowed([1, 2, 3, 4, 5], 3))
        self.assertEqual(result, [(1, 2, 3), (2, 3, 4), (3, 4, 5)])

    def test_windowed_errors(self):
        with self.assertRaises(TypeError):
            list(windowed([1, 2, 3], "1"))  # type: ignore

        with self.assertRaises(ValueError):
            list(windowed([1, 2, 3], 0))


class TestUniq(unittest.TestCase):
    def test_uniq_basic(self):
        result = uniq([1, 2, 2, 3, 1])
        self.assertEqual(result, [1, 2, 3])

    def test_uniq_preserves_order(self):
        result = uniq([3, 1, 2, 1, 3])
        self.assertEqual(result, [3, 1, 2])


class TestUniqBy(unittest.TestCase):
    def test_uniq_by_basic(self):
        result = uniq_by([{"id": 1}, {"id": 2}, {"id": 1}], lambda x: x["id"])
        self.assertEqual(result, [{"id": 1}, {"id": 2}])


class TestFrequency(unittest.TestCase):
    def test_frequency_basic(self):
        result = frequency([1, 2, 2, 3])
        self.assertEqual(result[2], 2)
        self.assertEqual(result[1], 1)


class TestMostLeastCommon(unittest.TestCase):
    def test_most_common(self):
        result = most_common([1, 2, 2, 3, 3, 3])
        self.assertEqual(result[0], (3, 3))

    def test_most_common_n(self):
        result = most_common([1, 2, 2, 3, 3, 3], n=1)
        self.assertEqual(result, [(3, 3)])

    def test_least_common(self):
        result = least_common([1, 2, 2, 3, 3, 3], n=1)
        self.assertEqual(result, [(1, 1)])


class TestMergeDicts(unittest.TestCase):
    def test_merge_dicts_basic(self):
        result = merge_dicts({"a": 1}, {"b": 2}, {"a": 3})
        self.assertEqual(result["a"], 3)
        self.assertEqual(result["b"], 2)


class TestToDeque(unittest.TestCase):
    def test_to_deque_basic(self):
        d = to_deque([1, 2, 3])
        self.assertIsInstance(d, deque)
        self.assertEqual(len(d), 3)

    def test_to_deque_maxlen(self):
        d = to_deque([1, 2, 3], maxlen=2)
        self.assertEqual(len(d), 2)


class TestPluck(unittest.TestCase):
    def test_pluck_basic(self):
        result = pluck([{"a": 1}, {"a": 2}, {"b": 3}], "a")
        self.assertEqual(result, [1, 2])

    def test_pluck_missing_key(self):
        result = pluck([{"a": 1}, {"b": 2}], "a")
        self.assertEqual(result, [1])


class TestCompact(unittest.TestCase):
    def test_compact_basic(self):
        result = compact([0, 1, False, 2, "", 3, None])
        self.assertEqual(result, [1, 2, 3])

    def test_compact_empty_lists(self):
        result = compact([0, [], "", None])
        self.assertEqual(result, [])


class TestPartitionBy(unittest.TestCase):
    def test_partition_by_basic(self):
        result = partition_by([1, 1, 2, 2, 3], lambda x: x)
        self.assertEqual(result, [[1, 1], [2, 2], [3]])

    def test_partition_by_empty(self):
        result = partition_by([], lambda x: x)
        self.assertEqual(result, [])

    def test_partition_by_consecutive_change(self):
        result = partition_by([1, 2, 1], lambda x: x % 2)
        self.assertEqual(result, [[1], [2], [1]])


if __name__ == "__main__":
    unittest.main()
