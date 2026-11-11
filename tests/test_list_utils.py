"""Tests for list_utils module."""

import unittest

from list_utils import (
    all_where,
    chunks,
    contains,
    count_duplicates,
    count_occurrences,
    count_unique,
    count_where,
    drop,
    find,
    find_all,
    find_all_indices,
    find_index,
    find_last,
    find_last_index,
    first_or_default,
    flatten,
    group_by,
    has_all_unique,
    has_duplicates,
    has_occurrences,
    has_where,
    index_of,
    indices_of,
    intersperse,
    is_empty,
    is_sorted,
    last_index_of,
    last_or_default,
    none_where,
    partition,
    safe_get,
    take,
    unique_preserve_order,
)


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


class TestContains(unittest.TestCase):
    def test_contains_present(self) -> None:
        self.assertTrue(contains([1, 2, 3, 4], 3))

    def test_contains_absent(self) -> None:
        self.assertFalse(contains([1, 2, 3], 5))

    def test_contains_empty_list(self) -> None:
        self.assertFalse(contains([], 1))

    def test_contains_strings(self) -> None:
        self.assertTrue(contains(["a", "b", "c"], "b"))

    def test_contains_first_element(self) -> None:
        self.assertTrue(contains([10, 20, 30], 10))

    def test_contains_last_element(self) -> None:
        self.assertTrue(contains([10, 20, 30], 30))

    def test_contains_duplicates_present(self) -> None:
        self.assertTrue(contains([1, 2, 2, 3], 2))

    def test_contains_none_value(self) -> None:
        self.assertTrue(contains([1, None, 3], None))

    def test_contains_non_list_raises(self) -> None:
        with self.assertRaises(TypeError):
            contains("not a list", 1)  # type: ignore[arg-type]


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


class TestFlatten(unittest.TestCase):
    def test_flatten_basic(self) -> None:
        self.assertEqual(flatten([[1, 2], [3, 4], [5]]), [1, 2, 3, 4, 5])

    def test_flatten_with_empty_inner(self) -> None:
        self.assertEqual(flatten([[], [1], [2, 3]]), [1, 2, 3])

    def test_flatten_strings(self) -> None:
        self.assertEqual(flatten([["a", "b"], ["c"]]), ["a", "b", "c"])

    def test_flatten_empty_outer(self) -> None:
        self.assertEqual(flatten([]), [])

    def test_flatten_preserves_order(self) -> None:
        self.assertEqual(flatten([[3], [1, 2], [4]]), [3, 1, 2, 4])

    def test_flatten_non_list_raises(self) -> None:
        with self.assertRaises(TypeError):
            flatten("not a list")  # type: ignore[arg-type]

    def test_flatten_non_list_element_raises(self) -> None:
        with self.assertRaises(TypeError):
            flatten([[1, 2], 3])  # type: ignore[arg-type]


class TestIsEmpty(unittest.TestCase):
    def test_empty(self) -> None:
        self.assertTrue(is_empty([]))

    def test_not_empty(self) -> None:
        self.assertFalse(is_empty([1]))

    def test_non_list_raises(self) -> None:
        with self.assertRaises(TypeError):
            is_empty("x")  # type: ignore[arg-type]


class TestHasDuplicates(unittest.TestCase):
    def test_has_duplicates_true(self) -> None:
        self.assertTrue(has_duplicates([1, 2, 2, 3]))

    def test_has_duplicates_false(self) -> None:
        self.assertFalse(has_duplicates([1, 2, 3]))

    def test_empty(self) -> None:
        self.assertFalse(has_duplicates([]))

    def test_strings(self) -> None:
        self.assertTrue(has_duplicates(["a", "b", "a"]))

    def test_unhashable(self) -> None:
        self.assertTrue(has_duplicates([[1], [2], [1]]))
        self.assertFalse(has_duplicates([[1], [2]]))

    def test_non_list_raises(self) -> None:
        with self.assertRaises(TypeError):
            has_duplicates("aa")  # type: ignore[arg-type]


class TestCountDuplicates(unittest.TestCase):
    def test_count_duplicates_basic(self) -> None:
        self.assertEqual(count_duplicates([1, 2, 2, 3]), 1)

    def test_count_duplicates_none(self) -> None:
        self.assertEqual(count_duplicates([1, 2, 3]), 0)

    def test_count_duplicates_empty(self) -> None:
        self.assertEqual(count_duplicates([]), 0)

    def test_count_duplicates_multiple_same_value(self) -> None:
        self.assertEqual(count_duplicates([1, 2, 2, 2, 3]), 2)

    def test_count_duplicates_multiple_values(self) -> None:
        self.assertEqual(count_duplicates([1, 1, 2, 2]), 2)

    def test_count_duplicates_all_same(self) -> None:
        self.assertEqual(count_duplicates([1, 1, 1]), 2)

    def test_count_duplicates_strings(self) -> None:
        self.assertEqual(count_duplicates(["a", "b", "a"]), 1)

    def test_count_duplicates_unhashable(self) -> None:
        self.assertEqual(count_duplicates([[1], [2], [1]]), 1)
        self.assertEqual(count_duplicates([[1], [2]]), 0)

    def test_count_duplicates_consistency_with_has_duplicates(self) -> None:
        for lst in ([], [1], [1, 2], [1, 1], [1, 2, 2, 3], ["a", "b", "a"]):
            self.assertEqual(count_duplicates(lst) > 0, has_duplicates(lst))  # type: ignore[misc]

    def test_count_duplicates_non_list_raises(self) -> None:
        with self.assertRaises(TypeError):
            count_duplicates("aa")  # type: ignore[arg-type]


class TestIsSorted(unittest.TestCase):
    def test_sorted(self) -> None:
        self.assertTrue(is_sorted([1, 2, 3]))

    def test_unsorted(self) -> None:
        self.assertFalse(is_sorted([3, 2, 1]))

    def test_reverse_sorted(self) -> None:
        self.assertTrue(is_sorted([3, 2, 1], reverse=True))
        self.assertFalse(is_sorted([1, 2, 3], reverse=True))

    def test_empty_and_single(self) -> None:
        self.assertTrue(is_sorted([]))
        self.assertTrue(is_sorted([1]))

    def test_with_equal_elements(self) -> None:
        self.assertTrue(is_sorted([1, 1, 2]))

    def test_non_list_raises(self) -> None:
        with self.assertRaises(TypeError):
            is_sorted("abc")  # type: ignore[arg-type]

    def test_reverse_not_bool_raises(self) -> None:
        with self.assertRaises(TypeError):
            is_sorted([1, 2], reverse=1)  # type: ignore[arg-type]


class TestUniquePreserveOrder(unittest.TestCase):
    def test_unique_preserve_order_basic(self) -> None:
        self.assertEqual(unique_preserve_order([1, 2, 2, 3, 1]), [1, 2, 3])

    def test_unique_preserve_order_strings(self) -> None:
        self.assertEqual(unique_preserve_order(["a", "b", "a"]), ["a", "b"])

    def test_unique_preserve_order_empty(self) -> None:
        self.assertEqual(unique_preserve_order([]), [])

    def test_unique_preserve_order_all_unique(self) -> None:
        self.assertEqual(unique_preserve_order([1, 2, 3]), [1, 2, 3])

    def test_unique_preserve_order_mixed_types(self) -> None:
        self.assertEqual(unique_preserve_order([1, "1", 1]), [1, "1"])

    def test_unique_preserve_order_non_list_raises(self) -> None:
        with self.assertRaises(TypeError):
            unique_preserve_order("not a list")  # type: ignore[arg-type]


class TestFindIndex(unittest.TestCase):
    def test_find_index_basic(self) -> None:
        self.assertEqual(find_index([10, 20, 30], lambda x: x == 20), 1)

    def test_find_index_first(self) -> None:
        self.assertEqual(find_index([1, 2, 3], lambda x: x > 0), 0)

    def test_find_index_last(self) -> None:
        self.assertEqual(find_index([1, 2, 3], lambda x: x == 3), 2)

    def test_find_index_not_found(self) -> None:
        self.assertIsNone(find_index([1, 2, 3], lambda x: x > 10))

    def test_find_index_empty(self) -> None:
        self.assertIsNone(find_index([], lambda x: True))

    def test_find_index_strings(self) -> None:
        self.assertEqual(find_index(["a", "bb", "ccc"], lambda s: len(s) > 1), 1)

    def test_find_index_non_list_raises(self) -> None:
        with self.assertRaises(TypeError):
            find_index("not a list", lambda x: True)  # type: ignore[arg-type]


class TestIndexOf(unittest.TestCase):
    def test_index_of_basic(self) -> None:
        self.assertEqual(index_of([1, 2, 3, 2], 2), 1)

    def test_index_of_first(self) -> None:
        self.assertEqual(index_of([1, 2, 3], 1), 0)

    def test_index_of_last_value(self) -> None:
        self.assertEqual(index_of([1, 2, 3], 3), 2)

    def test_index_of_not_found(self) -> None:
        self.assertIsNone(index_of([1, 2, 3], 9))

    def test_index_of_empty(self) -> None:
        self.assertIsNone(index_of([], 1))

    def test_index_of_strings(self) -> None:
        self.assertEqual(index_of(["a", "bb", "ccc"], "bb"), 1)

    def test_index_of_non_list_raises(self) -> None:
        with self.assertRaises(TypeError):
            index_of("not a list", "a")  # type: ignore[arg-type]

    def test_index_of_consistency_with_find_index(self) -> None:
        lst = [1, 2, 3, 2]
        for v in (1, 2, 3, 9):
            self.assertEqual(index_of(lst, v), find_index(lst, lambda x, val=v: x == val))  # type: ignore[misc]


class TestLastIndexOf(unittest.TestCase):
    def test_last_index_of_basic(self) -> None:
        self.assertEqual(last_index_of([1, 2, 3, 2], 2), 3)

    def test_last_index_of_single(self) -> None:
        self.assertEqual(last_index_of([1, 2, 3], 1), 0)

    def test_last_index_of_not_found(self) -> None:
        self.assertIsNone(last_index_of([1, 2, 3], 9))

    def test_last_index_of_empty(self) -> None:
        self.assertIsNone(last_index_of([], 1))

    def test_last_index_of_strings(self) -> None:
        self.assertEqual(last_index_of(["a", "bb", "a"], "a"), 2)

    def test_last_index_of_non_list_raises(self) -> None:
        with self.assertRaises(TypeError):
            last_index_of("not a list", "a")  # type: ignore[arg-type]


class TestFindLast(unittest.TestCase):
    def test_find_last_basic(self) -> None:
        self.assertEqual(find_last([1, 2, 3, 4], lambda x: x > 2), 4)

    def test_find_last_multiple_matches(self) -> None:
        self.assertEqual(find_last([1, 2, 3, 4], lambda x: x % 2 == 0), 4)

    def test_find_last_no_match(self) -> None:
        self.assertIsNone(find_last([1, 2, 3], lambda x: x > 10))  # type: ignore[operator]

    def test_find_last_empty(self) -> None:
        self.assertIsNone(find_last([], lambda x: True))

    def test_find_last_first_element(self) -> None:
        self.assertEqual(find_last([10, 20, 30], lambda x: x == 10), 10)

    def test_find_last_strings(self) -> None:
        self.assertEqual(find_last(["a", "bb", "ccc"], lambda s: len(s) >= 2), "ccc")

    def test_find_last_non_list_raises(self) -> None:
        with self.assertRaises(TypeError):
            find_last("not a list", lambda x: True)  # type: ignore[arg-type]


class TestFindLastIndex(unittest.TestCase):
    def test_find_last_index_basic(self) -> None:
        self.assertEqual(find_last_index([1, 2, 3, 2], lambda x: x == 2), 3)

    def test_find_last_index_multiple_matches(self) -> None:
        self.assertEqual(find_last_index([1, 2, 3, 4], lambda x: x % 2 == 0), 3)

    def test_find_last_index_no_match(self) -> None:
        self.assertIsNone(find_last_index([1, 2, 3], lambda x: x > 10))

    def test_find_last_index_empty(self) -> None:
        self.assertIsNone(find_last_index([], lambda x: True))

    def test_find_last_index_first_element(self) -> None:
        self.assertEqual(find_last_index([10, 20, 30], lambda x: x == 10), 0)

    def test_find_last_index_strings(self) -> None:
        self.assertEqual(find_last_index(["a", "bb", "ccc", "dd"], lambda s: len(s) == 2), 3)

    def test_find_last_index_non_list_raises(self) -> None:
        with self.assertRaises(TypeError):
            find_last_index("not a list", lambda x: True)  # type: ignore[arg-type]


class TestFindAll(unittest.TestCase):
    def test_find_all_basic(self) -> None:
        self.assertEqual(find_all([1, 2, 3, 4], lambda x: x > 2), [3, 4])

    def test_find_all_none_match(self) -> None:
        self.assertEqual(find_all([1, 2, 3], lambda x: x > 10), [])

    def test_find_all_empty(self) -> None:
        self.assertEqual(find_all([], lambda x: True), [])

    def test_find_all_preserves_order(self) -> None:
        self.assertEqual(find_all([3, 1, 4, 1, 5], lambda x: x % 2 == 1), [3, 1, 1, 5])

    def test_find_all_strings(self) -> None:
        self.assertEqual(find_all(["a", "bb", "ccc"], lambda s: len(s) >= 2), ["bb", "ccc"])

    def test_find_all_non_list_raises(self) -> None:
        with self.assertRaises(TypeError):
            find_all("not a list", lambda x: True)  # type: ignore[arg-type]

    def test_find_all_non_callable_raises(self) -> None:
        with self.assertRaises(TypeError):
            find_all([1, 2, 3], 1)  # type: ignore[arg-type]


class TestFindAllIndices(unittest.TestCase):
    def test_find_all_indices_basic(self) -> None:
        self.assertEqual(find_all_indices([1, 2, 3, 4], lambda x: x > 2), [2, 3])

    def test_find_all_indices_none_match(self) -> None:
        self.assertEqual(find_all_indices([1, 2, 3], lambda x: x > 10), [])

    def test_find_all_indices_empty(self) -> None:
        self.assertEqual(find_all_indices([], lambda x: True), [])

    def test_find_all_indices_all_match(self) -> None:
        self.assertEqual(find_all_indices([2, 4, 6], lambda x: x % 2 == 0), [0, 1, 2])

    def test_find_all_indices_strings(self) -> None:
        self.assertEqual(find_all_indices(["a", "bb", "ccc", "d"], lambda s: len(s) == 1), [0, 3])

    def test_find_all_indices_non_list_raises(self) -> None:
        with self.assertRaises(TypeError):
            find_all_indices("not a list", lambda x: True)  # type: ignore[arg-type]

    def test_find_all_indices_non_callable_raises(self) -> None:
        with self.assertRaises(TypeError):
            find_all_indices([1, 2, 3], 1)  # type: ignore[arg-type]


class TestIndicesOf(unittest.TestCase):
    def test_indices_of_basic(self) -> None:
        self.assertEqual(indices_of([1, 2, 3, 2], 2), [1, 3])

    def test_indices_of_none_match(self) -> None:
        self.assertEqual(indices_of([1, 2, 3], 4), [])

    def test_indices_of_empty(self) -> None:
        self.assertEqual(indices_of([], 1), [])

    def test_indices_of_all_match(self) -> None:
        self.assertEqual(indices_of(["a", "a", "a"], "a"), [0, 1, 2])

    def test_indices_of_single(self) -> None:
        self.assertEqual(indices_of([1, 2, 3], 2), [1])

    def test_indices_of_non_list_raises(self) -> None:
        with self.assertRaises(TypeError):
            indices_of("not a list", "a")  # type: ignore[arg-type]

    def test_indices_of_consistent_with_index_of(self) -> None:
        values = [1, 2, 3, 2, 1]
        for value in (1, 2, 3, 4):
            idxs = indices_of(values, value)
            first = index_of(values, value)
            if first is None:
                self.assertEqual(idxs, [])
            else:
                self.assertEqual(idxs[0], first)



class TestCountUnique(unittest.TestCase):
    def test_basic_counting(self) -> None:
        self.assertEqual(count_unique([1, 2, 2, 3]), 3)
        self.assertEqual(count_unique([1, 1, 2, 2, 3, 3]), 3)

    def test_all_unique(self) -> None:
        self.assertEqual(count_unique([1, 2, 3]), 3)
        self.assertEqual(count_unique(["a", "b", "c"]), 3)

    def test_all_duplicates(self) -> None:
        self.assertEqual(count_unique([1, 1, 1]), 1)

    def test_empty(self) -> None:
        self.assertEqual(count_unique([]), 0)

    def test_single_element(self) -> None:
        self.assertEqual(count_unique([42]), 1)

    def test_unhashable_elements(self) -> None:
        self.assertEqual(count_unique([[1], [2], [1]]), 2)

    def test_consistency_with_has_all_unique(self) -> None:
        for lst in ([1, 2, 3], [1, 2, 2, 3], [], ["a", "b", "a"]):
            self.assertEqual(has_all_unique(lst), count_unique(lst) == len(lst))  # type: ignore[misc]

    def test_non_list_raises(self) -> None:
        with self.assertRaises(TypeError):
            count_unique("abc")  # type: ignore[arg-type]


class TestHasAllUnique(unittest.TestCase):
    def test_all_unique(self) -> None:
        self.assertTrue(has_all_unique([1, 2, 3]))

    def test_duplicates(self) -> None:
        self.assertFalse(has_all_unique([1, 2, 2, 3]))

    def test_empty(self) -> None:
        self.assertTrue(has_all_unique([]))

    def test_single_element(self) -> None:
        self.assertTrue(has_all_unique([42]))

    def test_unhashable_elements(self) -> None:
        self.assertTrue(has_all_unique([[1], [2], [3]]))
        self.assertFalse(has_all_unique([[1], [2], [1]]))

    def test_consistency_with_count_unique(self) -> None:
        lst = [1, 2, 2, 3]
        self.assertEqual(has_all_unique(lst), count_unique(lst) == len(lst))

    def test_non_list_raises(self) -> None:
        with self.assertRaises(TypeError):
            has_all_unique("abc")  # type: ignore[arg-type]

class TestCountOccurrences(unittest.TestCase):
    def test_basic(self) -> None:
        self.assertEqual(count_occurrences([1, 2, 1, 3, 1], 1), 3)

    def test_no_match(self) -> None:
        self.assertEqual(count_occurrences([1, 2, 3], 9), 0)

    def test_empty(self) -> None:
        self.assertEqual(count_occurrences([], 1), 0)

    def test_strings(self) -> None:
        self.assertEqual(count_occurrences(["a", "b", "a"], "a"), 2)

    def test_non_list_raises(self) -> None:
        with self.assertRaises(TypeError):
            count_occurrences("aba", "a")  # type: ignore[arg-type]

    def test_consistency_with_has_occurrences(self) -> None:
        values = [1, 2, 2, 3]
        for value in (1, 2, 9):
            self.assertEqual(has_occurrences(values, value), count_occurrences(values, value) > 0)


class TestCountWhere(unittest.TestCase):
    def test_basic(self) -> None:
        self.assertEqual(count_where([1, 2, 3, 4], lambda x: x % 2 == 0), 2)

    def test_none_match(self) -> None:
        self.assertEqual(count_where([1, 3, 5], lambda x: x % 2 == 0), 0)

    def test_all_match(self) -> None:
        self.assertEqual(count_where([2, 4], lambda x: x % 2 == 0), 2)

    def test_empty(self) -> None:
        self.assertEqual(count_where([], lambda x: True), 0)

    def test_non_list_raises(self) -> None:
        with self.assertRaises(TypeError):
            count_where("abc", lambda x: x == "a")  # type: ignore[arg-type]

    def test_non_callable_raises(self) -> None:
        with self.assertRaises(TypeError):
            count_where([1, 2], 1)  # type: ignore[arg-type]


class TestHasWhere(unittest.TestCase):
    def test_true(self) -> None:
        self.assertTrue(has_where([1, 2, 3], lambda x: x > 2))

    def test_false(self) -> None:
        self.assertFalse(has_where([1, 2, 3], lambda x: x > 10))

    def test_empty(self) -> None:
        self.assertFalse(has_where([], lambda x: True))

    def test_non_list_raises(self) -> None:
        with self.assertRaises(TypeError):
            has_where("abc", lambda x: x == "a")  # type: ignore[arg-type]

    def test_non_callable_raises(self) -> None:
        with self.assertRaises(TypeError):
            has_where([1, 2], 1)  # type: ignore[arg-type]


class TestAllWhere(unittest.TestCase):
    def test_true(self) -> None:
        self.assertTrue(all_where([2, 4, 6], lambda x: x % 2 == 0))

    def test_false(self) -> None:
        self.assertFalse(all_where([2, 3, 6], lambda x: x % 2 == 0))

    def test_empty_vacuous(self) -> None:
        self.assertTrue(all_where([], lambda x: False))

    def test_non_list_raises(self) -> None:
        with self.assertRaises(TypeError):
            all_where("abc", lambda x: True)  # type: ignore[arg-type]

    def test_non_callable_raises(self) -> None:
        with self.assertRaises(TypeError):
            all_where([1, 2], 1)  # type: ignore[arg-type]


class TestNoneWhere(unittest.TestCase):
    def test_true(self) -> None:
        self.assertTrue(none_where([1, 3, 5], lambda x: x % 2 == 0))

    def test_false(self) -> None:
        self.assertFalse(none_where([1, 2, 3], lambda x: x % 2 == 0))

    def test_empty(self) -> None:
        self.assertTrue(none_where([], lambda x: True))

    def test_non_list_raises(self) -> None:
        with self.assertRaises(TypeError):
            none_where("abc", lambda x: True)  # type: ignore[arg-type]

    def test_non_callable_raises(self) -> None:
        with self.assertRaises(TypeError):
            none_where([1, 2], 1)  # type: ignore[arg-type]


class TestHasOccurrences(unittest.TestCase):
    def test_true(self) -> None:
        self.assertTrue(has_occurrences([1, 2, 3], 2))

    def test_false(self) -> None:
        self.assertFalse(has_occurrences([1, 2, 3], 4))

    def test_empty(self) -> None:
        self.assertFalse(has_occurrences([], 1))

    def test_non_list_raises(self) -> None:
        with self.assertRaises(TypeError):
            has_occurrences("aba", "a")  # type: ignore[arg-type]


class TestFirstOrDefault(unittest.TestCase):
    def test_basic(self) -> None:
        self.assertEqual(first_or_default([1, 2, 3]), 1)

    def test_empty_default(self) -> None:
        self.assertEqual(first_or_default([], 0), 0)

    def test_empty_none_default(self) -> None:
        self.assertIsNone(first_or_default([]))

    def test_single_element(self) -> None:
        self.assertEqual(first_or_default([42]), 42)

    def test_default_not_used_when_non_empty(self) -> None:
        self.assertEqual(first_or_default([1, 2, 3], 99), 1)

    def test_non_list_raises(self) -> None:
        with self.assertRaises(TypeError):
            first_or_default("abc")  # type: ignore[arg-type]


class TestLastOrDefault(unittest.TestCase):
    def test_basic(self) -> None:
        self.assertEqual(last_or_default([1, 2, 3]), 3)

    def test_empty_default(self) -> None:
        self.assertEqual(last_or_default([], 0), 0)

    def test_empty_none_default(self) -> None:
        self.assertIsNone(last_or_default([]))

    def test_single_element(self) -> None:
        self.assertEqual(last_or_default([42]), 42)

    def test_default_not_used_when_non_empty(self) -> None:
        self.assertEqual(last_or_default([1, 2, 3], 99), 3)

    def test_non_list_raises(self) -> None:
        with self.assertRaises(TypeError):
            last_or_default("abc")  # type: ignore[arg-type]
