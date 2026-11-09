"""Unit tests for seq_utils module."""

import unittest

from seq_utils import (
    adjacent_pairs,
    all_where,
    chunk,
    contains,
    count_occurrences,
    count_unique,
    count_where,
    distinct,
    drop_while,
    find,
    find_all,
    find_all_indices,
    find_index,
    find_last,
    find_last_index,
    first,
    flatten,
    has_all_unique,
    has_duplicates,
    has_occurrences,
    has_where,
    head,
    index_of,
    interleave,
    is_sorted,
    last,
    last_index_of,
    none_where,
    nth,
    nth_or_default,
    partition,
    split_at,
    tail,
    take_while,
    unique,
)


class TestFirst(unittest.TestCase):
    def test_first_non_empty(self):
        self.assertEqual(first([1, 2, 3]), 1)
        self.assertEqual(first(("a", "b")), "a")
        self.assertEqual(first("xyz"), "x")

    def test_first_empty(self):
        self.assertIsNone(first([]))
        self.assertIsNone(first(()))

    def test_first_type_error(self):
        with self.assertRaises(TypeError):
            first(123)  # type: ignore[arg-type]


class TestLast(unittest.TestCase):
    def test_last_non_empty(self):
        self.assertEqual(last([1, 2, 3]), 3)
        self.assertEqual(last(("a", "b")), "b")

    def test_last_empty(self):
        self.assertIsNone(last([]))

    def test_last_type_error(self):
        with self.assertRaises(TypeError):
            last(None)  # type: ignore[arg-type]


class TestNth(unittest.TestCase):
    def test_nth_valid(self):
        self.assertEqual(nth([1, 2, 3], 0), 1)
        self.assertEqual(nth([1, 2, 3], 2), 3)
        self.assertEqual(nth([1, 2, 3], -1), 3)
        self.assertEqual(nth([1, 2, 3], -3), 1)

    def test_nth_out_of_range(self):
        self.assertIsNone(nth([1, 2, 3], 5))
        self.assertIsNone(nth([1, 2, 3], -4))
        self.assertIsNone(nth([], 0))

    def test_nth_type_error(self):
        with self.assertRaises(TypeError):
            nth([1, 2, 3], "1")  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            nth(123, 0)  # type: ignore[arg-type]



class TestNthOrDefault(unittest.TestCase):
    def test_nth_or_default_valid(self):
        self.assertEqual(nth_or_default([1, 2, 3], 0), 1)
        self.assertEqual(nth_or_default([1, 2, 3], 2), 3)
        self.assertEqual(nth_or_default([1, 2, 3], -1), 3)

    def test_nth_or_default_out_of_range(self):
        self.assertEqual(nth_or_default([1, 2, 3], 5, 0), 0)
        self.assertEqual(nth_or_default([1, 2, 3], -4, "x"), "x")
        self.assertIsNone(nth_or_default([], 0))
        self.assertEqual(nth_or_default([], 0, 42), 42)

    def test_nth_or_default_type_error(self):
        with self.assertRaises(TypeError):
            nth_or_default([1, 2, 3], "1")  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            nth_or_default(123, 0)  # type: ignore[arg-type]

class TestHead(unittest.TestCase):
    def test_head(self):
        self.assertEqual(head([1, 2, 3, 4], 2), [1, 2])
        self.assertEqual(head([1, 2, 3]), [1])
        self.assertEqual(head([], 3), [])

    def test_head_zero(self):
        self.assertEqual(head([1, 2, 3], 0), [])

    def test_head_errors(self):
        with self.assertRaises(TypeError):
            head([1, 2, 3], "2")  # type: ignore[arg-type]
        with self.assertRaises(ValueError):
            head([1, 2, 3], -1)
        with self.assertRaises(TypeError):
            head(123, 1)  # type: ignore[arg-type]


class TestTail(unittest.TestCase):
    def test_tail(self):
        self.assertEqual(tail([1, 2, 3, 4], 2), [3, 4])
        self.assertEqual(tail([1, 2, 3]), [3])
        self.assertEqual(tail([], 3), [])

    def test_tail_zero(self):
        self.assertEqual(tail([1, 2, 3], 0), [])

    def test_tail_errors(self):
        with self.assertRaises(TypeError):
            tail([1, 2, 3], "2")  # type: ignore[arg-type]
        with self.assertRaises(ValueError):
            tail([1, 2, 3], -1)
        with self.assertRaises(TypeError):
            tail(123, 1)  # type: ignore[arg-type]


class TestSplitAt(unittest.TestCase):
    def test_split_at(self):
        self.assertEqual(split_at([1, 2, 3, 4], 2), ([1, 2], [3, 4]))
        self.assertEqual(split_at([1, 2, 3], 0), ([], [1, 2, 3]))
        self.assertEqual(split_at([1, 2, 3], 3), ([1, 2, 3], []))
        self.assertEqual(split_at([1, 2, 3], 10), ([1, 2, 3], []))

    def test_split_at_clamped_negative(self):
        self.assertEqual(split_at([1, 2, 3], -5), ([], [1, 2, 3]))

    def test_split_at_type_error(self):
        with self.assertRaises(TypeError):
            split_at([1, 2, 3], "2")  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            split_at(123, 1)  # type: ignore[arg-type]


class TestTakeWhile(unittest.TestCase):
    def test_take_while(self):
        self.assertEqual(take_while([1, 2, 3, 4], lambda x: x < 3), [1, 2])
        self.assertEqual(take_while([], lambda x: True), [])
        self.assertEqual(take_while([5, 6, 7], lambda x: x < 3), [])

    def test_take_while_type_error(self):
        with self.assertRaises(TypeError):
            take_while([1, 2, 3], None)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            take_while(123, lambda x: True)  # type: ignore[arg-type]


class TestDropWhile(unittest.TestCase):
    def test_drop_while(self):
        self.assertEqual(drop_while([1, 2, 3, 4], lambda x: x < 3), [3, 4])
        self.assertEqual(drop_while([], lambda x: True), [])
        self.assertEqual(drop_while([5, 6, 7], lambda x: x < 3), [5, 6, 7])
        self.assertEqual(drop_while([1, 2, 3], lambda x: x < 10), [])

    def test_drop_while_type_error(self):
        with self.assertRaises(TypeError):
            drop_while([1, 2, 3], None)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            drop_while(123, lambda x: True)  # type: ignore[arg-type]


class TestInterleave(unittest.TestCase):
    def test_interleave(self):
        self.assertEqual(interleave([1, 2], [3, 4]), [1, 3, 2, 4])
        self.assertEqual(interleave([1], [2, 3], [4]), [1, 2, 4, 3])
        self.assertEqual(interleave([], []), [])
        self.assertEqual(interleave([1, 2, 3]), [1, 2, 3])

    def test_interleave_type_error(self):
        with self.assertRaises(TypeError):
            interleave([1], 123)  # type: ignore[arg-type]


class TestAdjacentPairs(unittest.TestCase):
    def test_adjacent_pairs(self):
        self.assertEqual(adjacent_pairs([1, 2, 3]), [(1, 2), (2, 3)])
        self.assertEqual(adjacent_pairs([1]), [])
        self.assertEqual(adjacent_pairs([]), [])

    def test_adjacent_pairs_type_error(self):
        with self.assertRaises(TypeError):
            adjacent_pairs(123)  # type: ignore[arg-type]


class TestChunk(unittest.TestCase):
    def test_chunk_basic(self):
        self.assertEqual(chunk([1, 2, 3, 4, 5], 2), [[1, 2], [3, 4], [5]])
        self.assertEqual(chunk([1, 2, 3, 4], 2), [[1, 2], [3, 4]])
        self.assertEqual(chunk([1], 1), [[1]])

    def test_chunk_larger_than_sequence(self):
        self.assertEqual(chunk([1, 2], 5), [[1, 2]])

    def test_chunk_empty(self):
        self.assertEqual(chunk([], 3), [])

    def test_chunk_string(self):
        self.assertEqual(chunk("abcdef", 3), [["a", "b", "c"], ["d", "e", "f"]])

    def test_chunk_tuple(self):
        self.assertEqual(chunk((1, 2, 3, 4), 2), [[1, 2], [3, 4]])

    def test_chunk_size_one(self):
        self.assertEqual(chunk([1, 2, 3], 1), [[1], [2], [3]])

    def test_chunk_type_error(self):
        with self.assertRaises(TypeError):
            chunk(123, 2)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            chunk([1, 2], True)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            chunk([1, 2], "2")  # type: ignore[arg-type]

    def test_chunk_value_error(self):
        with self.assertRaises(ValueError):
            chunk([1, 2], 0)
        with self.assertRaises(ValueError):
            chunk([1, 2], -1)


class TestContains(unittest.TestCase):
    def test_contains_present(self):
        self.assertTrue(contains([1, 2, 3], 2))
        self.assertTrue(contains("abracadabra", "a"))
        self.assertTrue(contains((10, 20, 30), 20))

    def test_contains_absent(self):
        self.assertFalse(contains([1, 2, 3], 4))
        self.assertFalse(contains("hello", "z"))
        self.assertFalse(contains((10, 20, 30), 99))

    def test_contains_empty(self):
        self.assertFalse(contains([], 1))
        self.assertFalse(contains((), 1))
        self.assertFalse(contains("", "a"))

    def test_contains_first_last(self):
        self.assertTrue(contains([1, 2, 3], 1))
        self.assertTrue(contains([1, 2, 3], 3))

    def test_contains_duplicates(self):
        self.assertTrue(contains([1, 1, 1], 1))
        self.assertFalse(contains([1, 1, 1], 2))

    def test_contains_none_value(self):
        self.assertTrue(contains([None, 1, 2], None))
        self.assertFalse(contains([1, 2], None))

    def test_contains_consistency(self):
        seq = [1, 2, 2, 3]
        self.assertEqual(contains(seq, 2), has_occurrences(seq, 2))
        self.assertEqual(contains(seq, 5), has_occurrences(seq, 5))

    def test_contains_type_error(self):
        with self.assertRaises(TypeError):
            contains(123, 1)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            contains(None, 1)  # type: ignore[arg-type]


class TestUnique(unittest.TestCase):
    def test_unique_preserves_order(self):
        self.assertEqual(unique([1, 2, 2, 3, 1]), [1, 2, 3])

    def test_unique_empty(self):
        self.assertEqual(unique([]), [])
        self.assertEqual(unique(()), [])

    def test_unique_strings(self):
        self.assertEqual(unique("aba"), ["a", "b"])
        self.assertEqual(unique("abcb"), ["a", "b", "c"])

    def test_distinct_alias(self):
        self.assertEqual(distinct([1, 1, 2]), [1, 2])

    def test_unique_type_error(self):
        with self.assertRaises(TypeError):
            unique(123)  # type: ignore[arg-type]


class TestFlatten(unittest.TestCase):
    def test_flatten_basic(self):
        self.assertEqual(flatten([[1, 2], [3, 4], [5]]), [1, 2, 3, 4, 5])
        self.assertEqual(flatten([[1], [2], [3]]), [1, 2, 3])

    def test_flatten_mixed(self):
        self.assertEqual(flatten([1, [2, 3], "ab", [4]]), [1, 2, 3, "ab", 4])
        self.assertEqual(flatten(["ab", ["c"]]), ["ab", "c"])
        self.assertEqual(flatten([(1, 2), [3]]), [1, 2, 3])

    def test_flatten_empty(self):
        self.assertEqual(flatten([]), [])
        self.assertEqual(flatten([[]]), [])
        self.assertEqual(flatten([[], []]), [])

    def test_flatten_already_flat(self):
        self.assertEqual(flatten([1, 2, 3]), [1, 2, 3])
        self.assertEqual(flatten("abc"), ["a", "b", "c"])

    def test_flatten_type_error(self):
        with self.assertRaises(TypeError):
            flatten(123)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            flatten(None)  # type: ignore[arg-type]


class TestIsSorted(unittest.TestCase):
    def test_is_sorted(self):
        self.assertTrue(is_sorted([1, 2, 3]))
        self.assertFalse(is_sorted([3, 1, 2]))
        self.assertTrue(is_sorted([3, 2, 1], reverse=True))
        self.assertFalse(is_sorted([1, 3, 2], reverse=True))
        self.assertTrue(is_sorted([]))
        self.assertTrue(is_sorted([5]))

    def test_is_sorted_with_key(self):
        self.assertTrue(is_sorted(["a", "bb", "ccc"], key=len))
        self.assertFalse(is_sorted(["ccc", "bb", "a"], key=len))

    def test_is_sorted_type_error(self):
        with self.assertRaises(TypeError):
            is_sorted(123)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            is_sorted([1, 2], key=123)  # type: ignore[arg-type]


class TestCountOccurrences(unittest.TestCase):
    def test_count_occurrences_basic(self):
        self.assertEqual(count_occurrences([1, 2, 2, 3, 2], 2), 3)
        self.assertEqual(count_occurrences([1, 2, 3], 4), 0)

    def test_count_occurrences_empty(self):
        self.assertEqual(count_occurrences([], 1), 0)
        self.assertEqual(count_occurrences((), 1), 0)

    def test_count_occurrences_string(self):
        self.assertEqual(count_occurrences("abracadabra", "a"), 5)
        self.assertEqual(count_occurrences("hello", "z"), 0)

    def test_count_occurrences_tuple(self):
        self.assertEqual(count_occurrences((1, 1, 2, 1), 1), 3)

    def test_count_occurrences_type_error(self):
        with self.assertRaises(TypeError):
            count_occurrences(123, 1)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            count_occurrences(None, 1)  # type: ignore[arg-type]


class TestHasOccurrences(unittest.TestCase):
    def test_has_occurrences_present(self):
        self.assertTrue(has_occurrences([1, 2, 3], 2))
        self.assertTrue(has_occurrences("abracadabra", "a"))

    def test_has_occurrences_absent(self):
        self.assertFalse(has_occurrences([1, 2, 3], 4))
        self.assertFalse(has_occurrences("hello", "z"))

    def test_has_occurrences_empty(self):
        self.assertFalse(has_occurrences([], 1))
        self.assertFalse(has_occurrences("", "a"))

    def test_has_occurrences_duplicates(self):
        self.assertTrue(has_occurrences([1, 1, 1], 1))

    def test_has_occurrences_consistency(self):
        self.assertEqual(has_occurrences([1, 2, 2, 3], 2), count_occurrences([1, 2, 2, 3], 2) > 0)
        self.assertEqual(has_occurrences([1, 2, 3], 5), count_occurrences([1, 2, 3], 5) > 0)

    def test_has_occurrences_type_error(self):
        with self.assertRaises(TypeError):
            has_occurrences(123, 1)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            has_occurrences(None, 1)  # type: ignore[arg-type]


class TestCountWhere(unittest.TestCase):
    def test_count_where_basic(self):
        self.assertEqual(count_where([1, 2, 3, 4, 5], lambda x: x % 2 == 0), 2)
        self.assertEqual(count_where([1, 2, 3, 4, 5], lambda x: x > 3), 2)

    def test_count_where_no_match(self):
        self.assertEqual(count_where([1, 3, 5], lambda x: x % 2 == 0), 0)
        self.assertEqual(count_where([1, 2, 3], lambda x: x < 0), 0)

    def test_count_where_empty(self):
        self.assertEqual(count_where([], lambda x: True), 0)
        self.assertEqual(count_where((), lambda x: True), 0)

    def test_count_where_string(self):
        self.assertEqual(count_where("abracadabra", lambda c: c == "a"), 5)
        self.assertEqual(count_where("hello", lambda c: c == "z"), 0)

    def test_count_where_tuple(self):
        self.assertEqual(count_where((1, 2, 2, 3), lambda x: x == 2), 2)

    def test_count_where_all_match(self):
        self.assertEqual(count_where([2, 4, 6], lambda x: x % 2 == 0), 3)

    def test_count_where_type_error(self):
        with self.assertRaises(TypeError):
            count_where(123, lambda x: True)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            count_where(None, lambda x: True)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            count_where([1, 2, 3], 1)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            count_where([1, 2, 3], None)  # type: ignore[arg-type]


class TestHasWhere(unittest.TestCase):
    def test_has_where_present(self):
        self.assertTrue(has_where([1, 2, 3], lambda x: x % 2 == 0))
        self.assertTrue(has_where("abracadabra", lambda c: c == "a"))

    def test_has_where_absent(self):
        self.assertFalse(has_where([1, 3, 5], lambda x: x % 2 == 0))
        self.assertFalse(has_where("hello", lambda c: c == "z"))

    def test_has_where_empty(self):
        self.assertFalse(has_where([], lambda x: True))
        self.assertFalse(has_where("", lambda c: True))

    def test_has_where_consistency(self):
        self.assertEqual(
            has_where([1, 2, 3, 4], lambda x: x > 2),
            count_where([1, 2, 3, 4], lambda x: x > 2) > 0,
        )
        self.assertEqual(
            has_where([1, 3, 5], lambda x: x % 2 == 0),
            count_where([1, 3, 5], lambda x: x % 2 == 0) > 0,
        )

    def test_has_where_type_error(self):
        with self.assertRaises(TypeError):
            has_where(123, lambda x: True)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            has_where(None, lambda x: True)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            has_where([1, 2, 3], 1)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            has_where([1, 2, 3], None)  # type: ignore[arg-type]


class TestAllWhere(unittest.TestCase):
    def test_all_where_all_match(self):
        self.assertTrue(all_where([2, 4, 6], lambda x: x % 2 == 0))
        self.assertTrue(all_where([1, 2, 3], lambda x: x > 0))

    def test_all_where_some_fail(self):
        self.assertFalse(all_where([2, 3, 6], lambda x: x % 2 == 0))
        self.assertFalse(all_where([1, -1, 2], lambda x: x > 0))

    def test_all_where_empty_vacuous_true(self):
        self.assertTrue(all_where([], lambda x: False))
        self.assertTrue(all_where((), lambda x: False))
        self.assertTrue(all_where("", lambda c: False))

    def test_all_where_string(self):
        self.assertTrue(all_where("abc", lambda c: c.isalpha()))
        self.assertFalse(all_where("ab1", lambda c: c.isalpha()))

    def test_all_where_tuple(self):
        self.assertTrue(all_where((2, 4), lambda x: x % 2 == 0))

    def test_all_where_consistency_with_count_where(self):
        seq = [1, 2, 3, 4]
        def pred(x):
            return x < 10
        self.assertEqual(all_where(seq, pred), count_where(seq, pred) == len(seq))
        def pred2(x):
            return x % 2 == 0
        self.assertEqual(all_where(seq, pred2), count_where(seq, pred2) == len(seq))

    def test_all_where_type_error(self):
        with self.assertRaises(TypeError):
            all_where(123, lambda x: True)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            all_where(None, lambda x: True)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            all_where([1, 2, 3], 1)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            all_where([1, 2, 3], None)  # type: ignore[arg-type]


class TestNoneWhere(unittest.TestCase):
    def test_none_where_no_match(self):
        self.assertTrue(none_where([1, 3, 5], lambda x: x % 2 == 0))
        self.assertTrue(none_where("hello", lambda c: c == "z"))

    def test_none_where_some_match(self):
        self.assertFalse(none_where([1, 2, 3], lambda x: x % 2 == 0))
        self.assertFalse(none_where("hello", lambda c: c == "l"))

    def test_none_where_empty(self):
        self.assertTrue(none_where([], lambda x: True))
        self.assertTrue(none_where((), lambda x: True))
        self.assertTrue(none_where("", lambda c: True))

    def test_none_where_string(self):
        self.assertTrue(none_where("123", lambda c: c.isalpha()))

    def test_none_where_tuple(self):
        self.assertTrue(none_where((1, 3), lambda x: x % 2 == 0))

    def test_none_where_consistency_with_has_where(self):
        seq = [1, 2, 3, 4]
        def pred(x):
            return x > 10
        self.assertEqual(none_where(seq, pred), not has_where(seq, pred))
        def pred2(x):
            return x % 2 == 0
        self.assertEqual(none_where(seq, pred2), not has_where(seq, pred2))

    def test_none_where_type_error(self):
        with self.assertRaises(TypeError):
            none_where(123, lambda x: True)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            none_where(None, lambda x: True)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            none_where([1, 2, 3], 1)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            none_where([1, 2, 3], None)  # type: ignore[arg-type]


class TestIndexOf(unittest.TestCase):
    def test_index_of_present(self):
        self.assertEqual(index_of([1, 2, 3, 2], 2), 1)
        self.assertEqual(index_of("abracadabra", "c"), 4)
        self.assertEqual(index_of((10, 20, 30), 10), 0)

    def test_index_of_absent(self):
        self.assertIsNone(index_of([1, 2, 3], 4))
        self.assertIsNone(index_of("hello", "z"))

    def test_index_of_empty(self):
        self.assertIsNone(index_of([], 1))
        self.assertIsNone(index_of("", "a"))

    def test_index_of_first_match(self):
        self.assertEqual(index_of([5, 5, 5], 5), 0)

    def test_index_of_consistency(self):
        seq = [1, 2, 2, 3]
        self.assertEqual(index_of(seq, 2) is not None, has_occurrences(seq, 2))
        self.assertEqual(index_of(seq, 5) is not None, has_occurrences(seq, 5))

    def test_index_of_type_error(self):
        with self.assertRaises(TypeError):
            index_of(123, 1)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            index_of(None, 1)  # type: ignore[arg-type]


class TestLastIndexOf(unittest.TestCase):
    def test_last_index_of_present(self):
        self.assertEqual(last_index_of([1, 2, 3, 2], 2), 3)
        self.assertEqual(last_index_of("abracadabra", "a"), 10)
        self.assertEqual(last_index_of((10, 20, 30), 10), 0)

    def test_last_index_of_absent(self):
        self.assertIsNone(last_index_of([1, 2, 3], 4))
        self.assertIsNone(last_index_of("hello", "z"))

    def test_last_index_of_empty(self):
        self.assertIsNone(last_index_of([], 1))
        self.assertIsNone(last_index_of("", "a"))

    def test_last_index_of_single_occurrence(self):
        self.assertEqual(last_index_of([5, 1, 5, 5], 1), 1)

    def test_last_index_of_all_match(self):
        self.assertEqual(last_index_of([5, 5, 5], 5), 2)

    def test_last_index_of_consistency(self):
        seq = [1, 2, 2, 3]
        self.assertEqual(last_index_of(seq, 2) is not None, has_occurrences(seq, 2))
        self.assertEqual(last_index_of(seq, 5) is not None, has_occurrences(seq, 5))
        first_idx = index_of(seq, 2)
        last_idx = last_index_of(seq, 2)
        self.assertIsNotNone(first_idx)
        self.assertIsNotNone(last_idx)
        assert first_idx is not None and last_idx is not None
        self.assertLessEqual(first_idx, last_idx)

    def test_last_index_of_type_error(self):
        with self.assertRaises(TypeError):
            last_index_of(123, 1)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            last_index_of(None, 1)  # type: ignore[arg-type]


if __name__ == "__main__":
    unittest.main()


class TestFind(unittest.TestCase):
    """Test cases for the find function."""

    def test_basic_match(self):
        self.assertEqual(find([1, 2, 3, 4], lambda x: x > 2), 3)

    def test_first_match_returned(self):
        self.assertEqual(find([1, 2, 3, 4], lambda x: x % 2 == 0), 2)

    def test_no_match(self):
        self.assertIsNone(find([1, 2, 3], lambda x: x > 5))

    def test_empty_sequence(self):
        self.assertIsNone(find([], lambda x: True))

    def test_match_at_start(self):
        self.assertEqual(find([10, 20, 30], lambda x: x == 10), 10)

    def test_tuple_and_string(self):
        self.assertEqual(find((5, 6, 7), lambda x: x == 6), 6)
        self.assertEqual(find("hello", lambda c: c == "l"), "l")

    def test_non_sequence_raises_type_error(self):
        with self.assertRaises(TypeError):
            find(123, lambda x: True)
        with self.assertRaises(TypeError):
            find(None, lambda x: True)

    def test_non_callable_predicate_raises_type_error(self):
        with self.assertRaises(TypeError):
            find([1, 2, 3], 1)
        with self.assertRaises(TypeError):
            find([1, 2, 3], None)


class TestFindIndex(unittest.TestCase):
    """Test cases for the find_index function."""

    def test_basic_match(self):
        self.assertEqual(find_index([1, 2, 3, 4], lambda x: x > 2), 2)

    def test_first_match_returned(self):
        self.assertEqual(find_index([1, 2, 3, 4], lambda x: x % 2 == 0), 1)

    def test_no_match(self):
        self.assertIsNone(find_index([1, 2, 3], lambda x: x > 5))

    def test_empty_sequence(self):
        self.assertIsNone(find_index([], lambda x: True))

    def test_match_at_start(self):
        self.assertEqual(find_index([10, 20, 30], lambda x: x == 10), 0)

    def test_match_at_end(self):
        self.assertEqual(find_index([10, 20, 30], lambda x: x == 30), 2)

    def test_tuple_and_string(self):
        self.assertEqual(find_index((5, 6, 7), lambda x: x == 6), 1)
        self.assertEqual(find_index("hello", lambda c: c == "l"), 2)

    def test_non_sequence_raises_type_error(self):
        with self.assertRaises(TypeError):
            find_index(123, lambda x: True)
        with self.assertRaises(TypeError):
            find_index(None, lambda x: True)

    def test_non_callable_predicate_raises_type_error(self):
        with self.assertRaises(TypeError):
            find_index([1, 2, 3], 1)
        with self.assertRaises(TypeError):
            find_index([1, 2, 3], None)


class TestHasDuplicates(unittest.TestCase):
    def test_no_duplicates(self):
        self.assertFalse(has_duplicates([1, 2, 3]))

    def test_duplicates(self):
        self.assertTrue(has_duplicates([1, 2, 2, 3]))

    def test_empty(self):
        self.assertFalse(has_duplicates([]))

    def test_non_sequence_raises(self):
        with self.assertRaises(TypeError):
            has_duplicates(123)


class TestHasAllUnique(unittest.TestCase):
    def test_all_unique(self):
        self.assertTrue(has_all_unique([1, 2, 3]))
        self.assertTrue(has_all_unique("abc"))

    def test_has_duplicates(self):
        self.assertFalse(has_all_unique([1, 2, 2, 3]))
        self.assertFalse(has_all_unique("abca"))

    def test_empty(self):
        self.assertTrue(has_all_unique([]))
        self.assertTrue(has_all_unique(""))
        self.assertTrue(has_all_unique(()))

    def test_single_element(self):
        self.assertTrue(has_all_unique([42]))
        self.assertTrue(has_all_unique(("only",)))

    def test_tuple(self):
        self.assertTrue(has_all_unique((1, 2, 3)))
        self.assertFalse(has_all_unique((1, 2, 1)))

    def test_consistency_with_count_unique(self):
        seq = [1, 2, 3, 2, 1]
        self.assertEqual(has_all_unique(seq), count_unique(seq) == len(seq))
        seq2 = [5, 6, 7]
        self.assertEqual(has_all_unique(seq2), count_unique(seq2) == len(seq2))

    def test_non_sequence_raises(self):
        with self.assertRaises(TypeError):
            has_all_unique(123)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            has_all_unique(None)  # type: ignore[arg-type]


class TestFindLast(unittest.TestCase):
    """Test cases for the find_last function."""

    def test_basic_match(self):
        self.assertEqual(find_last([1, 2, 3, 4], lambda x: x > 2), 4)

    def test_last_match_returned(self):
        self.assertEqual(find_last([1, 2, 3, 4], lambda x: x % 2 == 0), 4)

    def test_no_match(self):
        self.assertIsNone(find_last([1, 2, 3], lambda x: x > 5))

    def test_empty_sequence(self):
        self.assertIsNone(find_last([], lambda x: True))

    def test_match_at_start(self):
        self.assertEqual(find_last([10, 20, 30], lambda x: x == 10), 10)

    def test_tuple_and_string(self):
        self.assertEqual(find_last((5, 6, 7), lambda x: x < 7), 6)
        self.assertEqual(find_last("hello", lambda c: c == "l"), "l")

    def test_consistency_with_find(self):
        seq = [1, 2, 3, 2, 1]
        def pred(x):
            return x == 2
        self.assertEqual(find(seq, pred), 2)
        self.assertEqual(find_last(seq, pred), 2)
        seq2 = [1, 3, 5]
        self.assertIsNone(find(seq2, lambda x: x % 2 == 0))
        self.assertIsNone(find_last(seq2, lambda x: x % 2 == 0))

    def test_non_sequence_raises_type_error(self):
        with self.assertRaises(TypeError):
            find_last(123, lambda x: True)
        with self.assertRaises(TypeError):
            find_last(None, lambda x: True)

    def test_non_callable_predicate_raises_type_error(self):
        with self.assertRaises(TypeError):
            find_last([1, 2, 3], 1)
        with self.assertRaises(TypeError):
            find_last([1, 2, 3], None)


class TestFindLastIndex(unittest.TestCase):
    """Test cases for the find_last_index function."""

    def test_basic_match(self):
        self.assertEqual(find_last_index([1, 2, 3, 4], lambda x: x > 2), 3)

    def test_last_match_returned(self):
        self.assertEqual(find_last_index([1, 2, 3, 4], lambda x: x % 2 == 0), 3)

    def test_no_match(self):
        self.assertIsNone(find_last_index([1, 2, 3], lambda x: x > 5))

    def test_empty_sequence(self):
        self.assertIsNone(find_last_index([], lambda x: True))

    def test_match_at_start(self):
        self.assertEqual(find_last_index([10, 20, 30], lambda x: x == 10), 0)

    def test_match_at_end(self):
        self.assertEqual(find_last_index([10, 20, 30], lambda x: x == 30), 2)

    def test_tuple_and_string(self):
        self.assertEqual(find_last_index((5, 6, 7), lambda x: x < 7), 1)
        self.assertEqual(find_last_index("hello", lambda c: c == "l"), 3)

    def test_consistency_with_find_index(self):
        seq = [1, 2, 3, 2, 1]
        def pred(x):
            return x == 2
        self.assertEqual(find_index(seq, pred), 1)
        self.assertEqual(find_last_index(seq, pred), 3)
        i = find_index(seq, pred)
        j = find_last_index(seq, pred)
        assert i is not None and j is not None
        self.assertLessEqual(i, j)

    def test_non_sequence_raises_type_error(self):
        with self.assertRaises(TypeError):
            find_last_index(123, lambda x: True)
        with self.assertRaises(TypeError):
            find_last_index(None, lambda x: True)

    def test_non_callable_predicate_raises_type_error(self):
        with self.assertRaises(TypeError):
            find_last_index([1, 2, 3], 1)
        with self.assertRaises(TypeError):
            find_last_index([1, 2, 3], None)


class TestFindAll(unittest.TestCase):
    def test_basic(self):
        self.assertEqual(find_all([1, 2, 3, 4], lambda x: x > 2), [3, 4])
        self.assertEqual(find_all_indices([1, 2, 3, 4], lambda x: x > 2), [2, 3])
        self.assertEqual(find_all([], lambda x: True), [])
        self.assertEqual(find_all_indices([], lambda x: True), [])


class TestPartition(unittest.TestCase):
    def test_partition_even_odd(self):
        matching, non_matching = partition([1, 2, 3, 4], lambda x: x % 2 == 0)
        self.assertEqual(matching, [2, 4])
        self.assertEqual(non_matching, [1, 3])

    def test_partition_empty_list(self):
        matching, non_matching = partition([], lambda x: True)
        self.assertEqual(matching, [])
        self.assertEqual(non_matching, [])

    def test_partition_all_match(self):
        matching, non_matching = partition([1, 2, 3], lambda x: True)
        self.assertEqual(matching, [1, 2, 3])
        self.assertEqual(non_matching, [])

    def test_partition_none_match(self):
        matching, non_matching = partition([1, 2, 3], lambda x: False)
        self.assertEqual(matching, [])
        self.assertEqual(non_matching, [1, 2, 3])

    def test_partition_preserves_order(self):
        matching, non_matching = partition([3, 1, 4, 1, 5, 9], lambda x: x % 2 == 0)
        self.assertEqual(matching, [4])
        self.assertEqual(non_matching, [3, 1, 1, 5, 9])

    def test_partition_tuple_and_string(self):
        matching, non_matching = partition(("a", "b", "c"), lambda c: c in "aeiou")
        self.assertEqual(matching, ["a"])
        self.assertEqual(non_matching, ["b", "c"])
        matching, non_matching = partition("hello", lambda c: c == "l")
        self.assertEqual(matching, ["l", "l"])
        self.assertEqual(non_matching, ["h", "e", "o"])

    def test_partition_non_sequence_raises_type_error(self):
        with self.assertRaises(TypeError):
            partition(123, lambda x: True)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            partition(None, lambda x: True)

    def test_partition_non_callable_predicate_raises_type_error(self):
        with self.assertRaises(TypeError):
            partition([1, 2, 3], 1)
        with self.assertRaises(TypeError):
            partition([1, 2, 3], None)
