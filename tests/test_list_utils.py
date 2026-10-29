"""Tests for list_utils module."""

import unittest

from list_utils import chunks, drop, find, group_by, intersperse, partition, safe_get, take


class TestPartition(unittest.TestCase):
    def test_partition_even_odd(self) -> None:
        matching, non_matching = partition([1, 2, 3, 4], lambda x: x % 2 == 0)
        self.assertEqual(matching, [2, 4])
        self.assertEqual(non_matching, [1, 3])

    def test_partition_empty_list(self) -> None:
        matching: list[int] = []
        non_matching: list[int] = []
        matching, non_matching = partition([], lambda x: True)
        self.assertEqual(matching, [])
        self.assertEqual(non_matching, [])

    def test_partition_all_match(self) -> None:
        matching, non_matching = partition([1, 2, 3], lambda x: True)
        self.assertEqual(matching, [1, 2, 3])
        self.assertEqual(non_matching, [])

    def test_partition_none_match(self) -> None:
        matching, non_matching = partition([1, 2, 3], lambda x: False)
        self.assertEqual(matching, [])
        self.assertEqual(non_matching, [1, 2, 3])

    def test_partition_preserves_order(self) -> None:
        matching, non_matching = partition([3, 1, 4, 1, 5, 9], lambda x: x % 2 == 0)
        self.assertEqual(matching, [4])
        self.assertEqual(non_matching, [3, 1, 1, 5, 9])

    def test_partition_non_list_raises(self) -> None:
        with self.assertRaises(TypeError):
            partition("not a list", lambda x: True)  # type: ignore[arg-type]


class TestGroupBy(unittest.TestCase):
    def test_group_by_length(self) -> None:
        result = group_by(["a", "bb", "c", "ddd"], lambda s: len(s))
        self.assertEqual(result[1], ["a", "c"])
        self.assertEqual(result[2], ["bb"])
        self.assertEqual(result[3], ["ddd"])

    def test_group_by_preserves_insertion_order(self) -> None:
        result = group_by(["x", "y", "z"], lambda s: s)
        self.assertEqual(result["x"], ["x"])
        self.assertEqual(result["y"], ["y"])
        self.assertEqual(result["z"], ["z"])

    def test_group_by_empty_list(self) -> None:
        result = group_by([], lambda x: x)
        self.assertEqual(result, {})

    def test_group_by_all_same_key(self) -> None:
        result = group_by([1, 2, 3], lambda x: "same")
        self.assertEqual(result["same"], [1, 2, 3])

    def test_group_by_non_list_raises(self) -> None:
        with self.assertRaises(TypeError):
            group_by("not a list", lambda x: x)  # type: ignore[arg-type]


class TestSafeGet(unittest.TestCase):
    def test_safe_get_valid_index(self) -> None:
        self.assertEqual(safe_get([1, 2, 3], 0), 1)
        self.assertEqual(safe_get([1, 2, 3], 2), 3)

    def test_safe_get_negative_index(self) -> None:
        self.assertEqual(safe_get([1, 2, 3], -1), 3)

    def test_safe_get_out_of_range_returns_default(self) -> None:
        self.assertIsNone(safe_get([1, 2, 3], 5))

    def test_safe_get_out_of_range_custom_default(self) -> None:
        self.assertEqual(safe_get([1, 2, 3], 10, default=0), 0)

    def test_safe_get_empty_list(self) -> None:
        self.assertIsNone(safe_get([], 0))
        self.assertEqual(safe_get([], 0, default="fallback"), "fallback")

    def test_safe_get_non_list_raises(self) -> None:
        with self.assertRaises(TypeError):
            safe_get("not a list", 0)  # type: ignore[arg-type]


class TestFind(unittest.TestCase):
    def test_find_first_match(self) -> None:
        result = find([1, 2, 3, 4], lambda x: x > 2)
        self.assertEqual(result, 3)

    def test_find_no_match_returns_none(self) -> None:
        result = find([1, 2, 3], lambda x: x > 10)
        self.assertIsNone(result)

    def test_find_empty_list_returns_none(self) -> None:
        result = find([], lambda x: True)
        self.assertIsNone(result)

    def test_find_first_of_multiple_matches(self) -> None:
        result = find([1, 2, 4, 6], lambda x: x % 2 == 0)
        self.assertEqual(result, 2)

    def test_find_non_list_raises(self) -> None:
        with self.assertRaises(TypeError):
            find("not a list", lambda x: True)  # type: ignore[arg-type]


class TestDrop(unittest.TestCase):
    def test_drop_basic(self) -> None:
        self.assertEqual(drop([1, 2, 3, 4, 5], 2), [3, 4, 5])

    def test_drop_zero(self) -> None:
        self.assertEqual(drop([1, 2, 3], 0), [1, 2, 3])

    def test_drop_all_elements(self) -> None:
        self.assertEqual(drop([1, 2, 3], 3), [])

    def test_drop_more_than_length(self) -> None:
        self.assertEqual(drop([1, 2, 3], 10), [])

    def test_drop_negative_raises(self) -> None:
        with self.assertRaises(ValueError):
            drop([1, 2, 3], -1)

    def test_drop_boolean_n_raises(self) -> None:
        with self.assertRaises(TypeError):
            drop([1, 2, 3], True)  # type: ignore[arg-type]

    def test_drop_non_list_raises(self) -> None:
        with self.assertRaises(TypeError):
            drop("not a list", 1)  # type: ignore[arg-type]


class TestTake(unittest.TestCase):
    def test_take_basic(self) -> None:
        self.assertEqual(take([1, 2, 3, 4, 5], 3), [1, 2, 3])

    def test_take_zero(self) -> None:
        self.assertEqual(take([1, 2, 3], 0), [])

    def test_take_more_than_length(self) -> None:
        self.assertEqual(take([1, 2, 3], 10), [1, 2, 3])

    def test_take_exact_length(self) -> None:
        self.assertEqual(take([1, 2, 3], 3), [1, 2, 3])

    def test_take_negative_raises(self) -> None:
        with self.assertRaises(ValueError):
            take([1, 2, 3], -1)

    def test_take_boolean_n_raises(self) -> None:
        with self.assertRaises(TypeError):
            take([1, 2, 3], True)  # type: ignore[arg-type]

    def test_take_non_list_raises(self) -> None:
        with self.assertRaises(TypeError):
            take("not a list", 1)  # type: ignore[arg-type]


class TestIntersperse(unittest.TestCase):
    def test_intersperse_ints(self) -> None:
        self.assertEqual(intersperse([1, 2, 3], 0), [1, 0, 2, 0, 3])

    def test_intersperse_strings(self) -> None:
        self.assertEqual(intersperse(["a", "b"], "-"), ["a", "-", "b"])

    def test_intersperse_single_element(self) -> None:
        self.assertEqual(intersperse([1], 0), [1])

    def test_intersperse_empty_list(self) -> None:
        self.assertEqual(intersperse([], "-"), [])

    def test_intersperse_preserves_original(self) -> None:
        original = [1, 2, 3]
        intersperse(original, 0)
        self.assertEqual(original, [1, 2, 3])

    def test_intersperse_non_list_raises(self) -> None:
        with self.assertRaises(TypeError):
            intersperse("not a list", "-")  # type: ignore[arg-type]


class TestChunks(unittest.TestCase):
    def test_chunks_basic(self) -> None:
        self.assertEqual(chunks([1, 2, 3, 4, 5], 2), [[1, 2], [3, 4], [5]])

    def test_chunks_equal_chunks(self) -> None:
        self.assertEqual(chunks([1, 2, 3, 4], 2), [[1, 2], [3, 4]])

    def test_chunks_size_one(self) -> None:
        self.assertEqual(chunks([1, 2, 3], 1), [[1], [2], [3]])

    def test_chunks_empty_list(self) -> None:
        self.assertEqual(chunks([], 3), [])

    def test_chunks_preserves_original(self) -> None:
        original = [1, 2, 3, 4]
        chunks(original, 2)
        self.assertEqual(original, [1, 2, 3, 4])

    def test_chunks_size_zero_raises(self) -> None:
        with self.assertRaises(ValueError):
            chunks([1, 2, 3], 0)

    def test_chunks_size_negative_raises(self) -> None:
        with self.assertRaises(ValueError):
            chunks([1, 2, 3], -1)

    def test_chunks_boolean_size_raises(self) -> None:
        with self.assertRaises(TypeError):
            chunks([1, 2, 3], True)  # type: ignore[arg-type]

    def test_chunks_non_list_raises(self) -> None:
        with self.assertRaises(TypeError):
            chunks("not a list", 2)  # type: ignore[arg-type]

    def test_chunks_size_not_int_raises(self) -> None:
        with self.assertRaises(TypeError):
            chunks([1, 2, 3], 2.0)  # type: ignore[arg-type]


if __name__ == "__main__":
    unittest.main()
