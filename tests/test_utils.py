"""Tests for utils module."""

import unittest

from utils import (
    average,
    chunk,
    compact,
    concat,
    count,
    count_by,
    dedupe,
    difference,
    drop,
    drop_while,
    every,
    filter_list,
    find,
    find_index,
    first,
    flatten,
    for_each,
    from_pairs,
    get,
    group_by,
    has_by,
    has_key,
    head,
    includes,
    index_by,
    initial,
    intersection,
    is_empty,
    is_not_empty,
    items,
    keys,
    last,
    map_list,
    max_list,
    merge,
    min_list,
    omit,
    partition,
    pick,
    pluck,
    product,
    range_list,
    reduce_list,
    remove_none,
    repeat,
    rest,
    reverse,
    sample,
    second,
    shuffle,
    some,
    sum_list,
    tail,
    take,
    take_while,
    to_dict,
    union,
    unique,
    values,
    zip_with,
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


class TestDedupe(unittest.TestCase):
    def test_dedupe_basic(self) -> None:
        self.assertEqual(dedupe([1, 2, 2, 3]), [1, 2, 3])

    def test_dedupe_preserves_order(self) -> None:
        self.assertEqual(dedupe([3, 1, 2, 1]), [3, 1, 2])

    def test_dedupe_matches_unique(self) -> None:
        self.assertEqual(dedupe([1, 2, 2, 3]), unique([1, 2, 2, 3]))


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


class TestCountBy(unittest.TestCase):
    def test_count_by_basic(self) -> None:
        self.assertEqual(count_by([1, 2, 3, 4], lambda x: x % 2 == 0), 2)

    def test_count_by_none(self) -> None:
        self.assertEqual(count_by([1, 3, 5], lambda x: x % 2 == 0), 0)

    def test_count_by_all(self) -> None:
        self.assertEqual(count_by([2, 4, 6], lambda x: x % 2 == 0), 3)

    def test_count_by_empty(self) -> None:
        self.assertEqual(count_by([], lambda x: True), 0)

    def test_count_by_consistency_with_has_by(self) -> None:
        lst = [1, 2, 3, 4, 5]
        predicate = lambda x: x > 2  # noqa: E731
        self.assertEqual(count_by(lst, predicate) > 0, has_by(lst, predicate))

    def test_count_by_non_callable_raises(self) -> None:
        with self.assertRaises(TypeError):
            count_by([1, 2, 3], "not callable")  # type: ignore[arg-type]


class TestHasBy(unittest.TestCase):
    def test_has_by_true(self) -> None:
        self.assertTrue(has_by([1, 2, 3], lambda x: x == 2))

    def test_has_by_false(self) -> None:
        self.assertFalse(has_by([1, 3, 5], lambda x: x % 2 == 0))

    def test_has_by_empty(self) -> None:
        self.assertFalse(has_by([], lambda x: True))

    def test_has_by_consistency_with_count_by(self) -> None:
        lst = [10, 20, 30]
        predicate = lambda x: x > 15  # noqa: E731
        self.assertEqual(has_by(lst, predicate), count_by(lst, predicate) > 0)

    def test_has_by_non_callable_raises(self) -> None:
        with self.assertRaises(TypeError):
            has_by([1, 2, 3], 123)  # type: ignore[arg-type]


class TestIsNotEmpty(unittest.TestCase):
    def test_is_not_empty_none(self) -> None:
        self.assertFalse(is_not_empty(None))

    def test_is_not_empty_empty_values(self) -> None:
        self.assertFalse(is_not_empty(""))
        self.assertFalse(is_not_empty([]))
        self.assertFalse(is_not_empty(()))
        self.assertFalse(is_not_empty(set()))
        self.assertFalse(is_not_empty({}))

    def test_is_not_empty_non_empty(self) -> None:
        self.assertTrue(is_not_empty("hello"))
        self.assertTrue(is_not_empty([1]))
        self.assertTrue(is_not_empty({"a": 1}))
        self.assertTrue(is_not_empty((1,)))

    def test_is_not_empty_numbers_and_bools(self) -> None:
        self.assertTrue(is_not_empty(0))
        self.assertTrue(is_not_empty(False))
        self.assertTrue(is_not_empty(5))

    def test_consistency_with_is_empty(self) -> None:
        for value in [None, "", [], [1], 0, False, "x", {}, {"a": 1}]:
            self.assertEqual(is_not_empty(value), not is_empty(value))


class TestAverage(unittest.TestCase):
    def test_average_basic(self) -> None:
        self.assertEqual(average([1, 2, 3, 4]), 2.5)

    def test_average_single(self) -> None:
        self.assertEqual(average([5]), 5.0)

    def test_average_empty_raises(self) -> None:
        with self.assertRaises(ValueError):
            average([])


class TestConcat(unittest.TestCase):
    def test_concat_basic(self) -> None:
        self.assertEqual(concat([1, 2], [3, 4]), [1, 2, 3, 4])

    def test_concat_single(self) -> None:
        self.assertEqual(concat([1, 2]), [1, 2])

    def test_concat_empty(self) -> None:
        self.assertEqual(concat(), [])

    def test_concat_with_empty(self) -> None:
        self.assertEqual(concat([1], [], [2]), [1, 2])


class TestCount(unittest.TestCase):
    def test_count_basic(self) -> None:
        self.assertEqual(count([1, 2, 2, 3], 2), 2)

    def test_count_absent(self) -> None:
        self.assertEqual(count([1, 2, 3], 5), 0)

    def test_count_empty(self) -> None:
        self.assertEqual(count([], 1), 0)


class TestDifference(unittest.TestCase):
    def test_difference_basic(self) -> None:
        self.assertEqual(difference([1, 2, 3, 4], [2, 4]), [1, 3])

    def test_difference_no_overlap(self) -> None:
        self.assertEqual(difference([1, 2], [3, 4]), [1, 2])

    def test_difference_preserves_order(self) -> None:
        self.assertEqual(difference([3, 1, 2], [2]), [3, 1])


class TestDrop(unittest.TestCase):
    def test_drop_basic(self) -> None:
        self.assertEqual(drop([1, 2, 3, 4], 2), [3, 4])

    def test_drop_zero(self) -> None:
        self.assertEqual(drop([1, 2, 3], 0), [1, 2, 3])

    def test_drop_all(self) -> None:
        self.assertEqual(drop([1, 2], 5), [])

    def test_drop_empty(self) -> None:
        self.assertEqual(drop([], 3), [])


class TestDropWhile(unittest.TestCase):
    def test_drop_while_basic(self) -> None:
        self.assertEqual(drop_while([1, 2, 3, 4], lambda x: x < 3), [3, 4])

    def test_drop_while_none(self) -> None:
        self.assertEqual(drop_while([1, 2, 3], lambda x: x < 0), [1, 2, 3])

    def test_drop_while_all(self) -> None:
        self.assertEqual(drop_while([1, 2, 3], lambda x: True), [])


class TestEvery(unittest.TestCase):
    def test_every_true(self) -> None:
        self.assertTrue(every([2, 4, 6], lambda x: x % 2 == 0))

    def test_every_false(self) -> None:
        self.assertFalse(every([1, 2, 3], lambda x: x % 2 == 0))

    def test_every_empty(self) -> None:
        self.assertTrue(every([], lambda x: True))


class TestFilterList(unittest.TestCase):
    def test_filter_list_basic(self) -> None:
        self.assertEqual(filter_list(lambda x: x % 2 == 0, [1, 2, 3, 4]), [2, 4])

    def test_filter_list_none(self) -> None:
        self.assertEqual(filter_list(lambda x: x < 0, [1, 2, 3]), [])

    def test_filter_list_all(self) -> None:
        self.assertEqual(filter_list(lambda x: x > 0, [1, 2, 3]), [1, 2, 3])


class TestFind(unittest.TestCase):
    def test_find_found(self) -> None:
        self.assertEqual(find([1, 2, 3, 4], lambda x: x > 2), 3)

    def test_find_not_found(self) -> None:
        self.assertIsNone(find([1, 2, 3], lambda x: x > 10))  # type: ignore[operator]

    def test_find_empty(self) -> None:
        self.assertIsNone(find([], lambda x: True))


class TestFindIndex(unittest.TestCase):
    def test_find_index_found(self) -> None:
        self.assertEqual(find_index([1, 2, 3, 4], lambda x: x > 2), 2)

    def test_find_index_not_found(self) -> None:
        self.assertEqual(find_index([1, 2, 3], lambda x: x > 10), -1)

    def test_find_index_empty(self) -> None:
        self.assertEqual(find_index([], lambda x: True), -1)


class TestForEach(unittest.TestCase):
    def test_for_each_applies(self) -> None:
        collected: list[int] = []
        for_each(collected.append, [1, 2, 3])
        self.assertEqual(collected, [1, 2, 3])

    def test_for_each_empty(self) -> None:
        for_each(lambda x: x, [])


class TestFromPairs(unittest.TestCase):
    def test_from_pairs_basic(self) -> None:
        self.assertEqual(from_pairs([("a", 1), ("b", 2)]), {"a": 1, "b": 2})

    def test_from_pairs_empty(self) -> None:
        self.assertEqual(from_pairs([]), {})


class TestGet(unittest.TestCase):
    def test_get_found(self) -> None:
        self.assertEqual(get({"a": 1}, "a"), 1)

    def test_get_missing_default(self) -> None:
        self.assertEqual(get({"a": 1}, "b", 2), 2)

    def test_get_missing_none(self) -> None:
        self.assertIsNone(get({"a": 1}, "b"))

    def test_get_non_dict(self) -> None:
        self.assertEqual(get([1, 2], "a", 0), 0)  # type: ignore[arg-type]


class TestGroupBy(unittest.TestCase):
    def test_group_by_basic(self) -> None:
        self.assertEqual(
            group_by([1, 2, 3, 4], lambda x: x % 2), {0: [2, 4], 1: [1, 3]}
        )

    def test_group_by_empty(self) -> None:
        self.assertEqual(group_by([], lambda x: x), {})


class TestHasKey(unittest.TestCase):
    def test_has_key_true(self) -> None:
        self.assertTrue(has_key({"a": 1}, "a"))

    def test_has_key_false(self) -> None:
        self.assertFalse(has_key({"a": 1}, "b"))

    def test_has_key_non_dict(self) -> None:
        self.assertFalse(has_key([1, 2], "a"))  # type: ignore[arg-type]


class TestHead(unittest.TestCase):
    def test_head_basic(self) -> None:
        self.assertEqual(head([1, 2, 3, 4], 2), [1, 2])

    def test_head_zero(self) -> None:
        self.assertEqual(head([1, 2, 3], 0), [])

    def test_head_alias_take(self) -> None:
        self.assertEqual(head([1, 2, 3], 2), take([1, 2, 3], 2))


class TestIncludes(unittest.TestCase):
    def test_includes_true(self) -> None:
        self.assertTrue(includes([1, 2, 3], 2))

    def test_includes_false(self) -> None:
        self.assertFalse(includes([1, 2, 3], 5))

    def test_includes_empty(self) -> None:
        self.assertFalse(includes([], 1))


class TestIndexBy(unittest.TestCase):
    def test_index_by_basic(self) -> None:
        self.assertEqual(
            index_by([{"id": 1}, {"id": 2}], lambda x: x["id"]), {1: {"id": 1}, 2: {"id": 2}}
        )

    def test_index_by_empty(self) -> None:
        self.assertEqual(index_by([], lambda x: x), {})


class TestInitial(unittest.TestCase):
    def test_initial_basic(self) -> None:
        self.assertEqual(initial([1, 2, 3]), [1, 2])

    def test_initial_single(self) -> None:
        self.assertEqual(initial([5]), [])

    def test_initial_empty(self) -> None:
        self.assertEqual(initial([]), [])


class TestIntersection(unittest.TestCase):
    def test_intersection_basic(self) -> None:
        self.assertEqual(intersection([1, 2, 3], [2, 3, 4]), [2, 3])

    def test_intersection_no_overlap(self) -> None:
        self.assertEqual(intersection([1, 2], [3, 4]), [])

    def test_intersection_preserves_order(self) -> None:
        self.assertEqual(intersection([3, 1, 2], [2, 3]), [3, 2])

    def test_intersection_empty(self) -> None:
        self.assertEqual(intersection([], [1, 2]), [])


class TestItems(unittest.TestCase):
    def test_items_basic(self) -> None:
        self.assertEqual(sorted(items({"a": 1, "b": 2})), [("a", 1), ("b", 2)])

    def test_items_empty(self) -> None:
        self.assertEqual(items({}), [])


class TestKeys(unittest.TestCase):
    def test_keys_basic(self) -> None:
        self.assertEqual(sorted(keys({"b": 1, "a": 2})), ["a", "b"])

    def test_keys_empty(self) -> None:
        self.assertEqual(keys({}), [])


class TestMapList(unittest.TestCase):
    def test_map_list_basic(self) -> None:
        self.assertEqual(map_list(lambda x: x * 2, [1, 2, 3]), [2, 4, 6])

    def test_map_list_empty(self) -> None:
        self.assertEqual(map_list(lambda x: x, []), [])


class TestMaxList(unittest.TestCase):
    def test_max_list_basic(self) -> None:
        self.assertEqual(max_list([1, 5, 3]), 5)

    def test_max_list_empty_raises(self) -> None:
        with self.assertRaises(ValueError):
            max_list([])


class TestMerge(unittest.TestCase):
    def test_merge_basic(self) -> None:
        self.assertEqual(merge({"a": 1}, {"b": 2}), {"a": 1, "b": 2})

    def test_merge_later_wins(self) -> None:
        self.assertEqual(merge({"a": 1}, {"a": 2}), {"a": 2})

    def test_merge_empty(self) -> None:
        self.assertEqual(merge(), {})


class TestMinList(unittest.TestCase):
    def test_min_list_basic(self) -> None:
        self.assertEqual(min_list([1, 5, 3]), 1)

    def test_min_list_empty_raises(self) -> None:
        with self.assertRaises(ValueError):
            min_list([])


class TestOmit(unittest.TestCase):
    def test_omit_basic(self) -> None:
        self.assertEqual(omit({"a": 1, "b": 2, "c": 3}, ["b"]), {"a": 1, "c": 3})

    def test_omit_missing(self) -> None:
        self.assertEqual(omit({"a": 1}, ["b"]), {"a": 1})

    def test_omit_empty(self) -> None:
        self.assertEqual(omit({}, ["a"]), {})


class TestPartition(unittest.TestCase):
    def test_partition_basic(self) -> None:
        self.assertEqual(partition([1, 2, 3, 4], lambda x: x % 2 == 0), [[2, 4], [1, 3]])

    def test_partition_empty(self) -> None:
        self.assertEqual(partition([], lambda x: True), [[], []])


class TestPick(unittest.TestCase):
    def test_pick_basic(self) -> None:
        self.assertEqual(pick({"a": 1, "b": 2, "c": 3}, ["a", "c"]), {"a": 1, "c": 3})

    def test_pick_missing(self) -> None:
        self.assertEqual(pick({"a": 1}, ["b"]), {})

    def test_pick_empty(self) -> None:
        self.assertEqual(pick({}, ["a"]), {})


class TestPluck(unittest.TestCase):
    def test_pluck_basic(self) -> None:
        self.assertEqual(pluck([{"a": 1}, {"a": 2}, {"b": 3}], "a"), [1, 2])

    def test_pluck_empty(self) -> None:
        self.assertEqual(pluck([], "a"), [])


class TestProduct(unittest.TestCase):
    def test_product_basic(self) -> None:
        self.assertEqual(product([1, 2, 3, 4]), 24)

    def test_product_empty_raises(self) -> None:
        with self.assertRaises(ValueError):
            product([])


class TestRangeList(unittest.TestCase):
    def test_range_list_stop(self) -> None:
        self.assertEqual(range_list(5), [0, 1, 2, 3, 4])

    def test_range_list_start_stop(self) -> None:
        self.assertEqual(range_list(2, 5), [2, 3, 4])

    def test_range_list_step(self) -> None:
        self.assertEqual(range_list(0, 6, 2), [0, 2, 4])


class TestReduceList(unittest.TestCase):
    def test_reduce_list_basic(self) -> None:
        self.assertEqual(reduce_list(lambda a, b: a + b, [1, 2, 3, 4], 0), 10)

    def test_reduce_list_empty(self) -> None:
        self.assertEqual(reduce_list(lambda a, b: a + b, [], 5), 5)


class TestRepeat(unittest.TestCase):
    def test_repeat_basic(self) -> None:
        self.assertEqual(repeat("a", 3), ["a", "a", "a"])

    def test_repeat_zero(self) -> None:
        self.assertEqual(repeat("a", 0), [])

    def test_repeat_negative(self) -> None:
        self.assertEqual(repeat("a", -1), [])


class TestRest(unittest.TestCase):
    def test_rest_basic(self) -> None:
        self.assertEqual(rest([1, 2, 3]), [2, 3])

    def test_rest_single(self) -> None:
        self.assertEqual(rest([5]), [])

    def test_rest_empty(self) -> None:
        self.assertEqual(rest([]), [])


class TestReverse(unittest.TestCase):
    def test_reverse_basic(self) -> None:
        self.assertEqual(reverse([1, 2, 3]), [3, 2, 1])

    def test_reverse_empty(self) -> None:
        self.assertEqual(reverse([]), [])


class TestSample(unittest.TestCase):
    def test_sample_basic(self) -> None:
        result = sample([1, 2, 3, 4], 2)
        self.assertEqual(len(result), 2)
        self.assertTrue(all(item in [1, 2, 3, 4] for item in result))

    def test_sample_all(self) -> None:
        result = sample([1, 2, 3], 5)
        self.assertEqual(sorted(result), [1, 2, 3])

    def test_sample_empty(self) -> None:
        self.assertEqual(sample([], 1), [])


class TestShuffle(unittest.TestCase):
    def test_shuffle_is_permutation(self) -> None:
        original = [1, 2, 3, 4]
        result = shuffle(original)
        self.assertEqual(sorted(result), sorted(original))

    def test_shuffle_empty(self) -> None:
        self.assertEqual(shuffle([]), [])


class TestSome(unittest.TestCase):
    def test_some_true(self) -> None:
        self.assertTrue(some([1, 2, 3], lambda x: x == 2))

    def test_some_false(self) -> None:
        self.assertFalse(some([1, 3, 5], lambda x: x % 2 == 0))

    def test_some_empty(self) -> None:
        self.assertFalse(some([], lambda x: True))


class TestSumList(unittest.TestCase):
    def test_sum_list_basic(self) -> None:
        self.assertEqual(sum_list([1, 2, 3, 4]), 10)

    def test_sum_list_empty(self) -> None:
        self.assertEqual(sum_list([]), 0)


class TestTail(unittest.TestCase):
    def test_tail_basic(self) -> None:
        self.assertEqual(tail([1, 2, 3, 4], 2), [3, 4])

    def test_tail_zero(self) -> None:
        self.assertEqual(tail([1, 2, 3], 0), [])

    def test_tail_all(self) -> None:
        self.assertEqual(tail([1, 2], 5), [1, 2])


class TestTake(unittest.TestCase):
    def test_take_basic(self) -> None:
        self.assertEqual(take([1, 2, 3, 4], 2), [1, 2])

    def test_take_zero(self) -> None:
        self.assertEqual(take([1, 2, 3], 0), [])

    def test_take_all(self) -> None:
        self.assertEqual(take([1, 2], 5), [1, 2])


class TestTakeWhile(unittest.TestCase):
    def test_take_while_basic(self) -> None:
        self.assertEqual(take_while([1, 2, 3, 4], lambda x: x < 3), [1, 2])

    def test_take_while_none(self) -> None:
        self.assertEqual(take_while([1, 2, 3], lambda x: x < 0), [])

    def test_take_while_all(self) -> None:
        self.assertEqual(take_while([1, 2, 3], lambda x: True), [1, 2, 3])


class TestToDict(unittest.TestCase):
    def test_to_dict_basic(self) -> None:
        self.assertEqual(to_dict([["a", 1], ["b", 2]]), {"a": 1, "b": 2})

    def test_to_dict_empty(self) -> None:
        self.assertEqual(to_dict([]), {})


class TestUnion(unittest.TestCase):
    def test_union_basic(self) -> None:
        self.assertEqual(union([1, 2], [2, 3]), [1, 2, 3])

    def test_union_preserves_order(self) -> None:
        self.assertEqual(union([3, 1], [1, 2]), [3, 1, 2])


class TestValues(unittest.TestCase):
    def test_values_basic(self) -> None:
        self.assertEqual(sorted(values({"b": 1, "a": 2})), [1, 2])

    def test_values_empty(self) -> None:
        self.assertEqual(values({}), [])


class TestZipWith(unittest.TestCase):
    def test_zip_with_basic(self) -> None:
        self.assertEqual(zip_with([1, 2], [3, 4], lambda a, b: a + b), [4, 6])

    def test_zip_with_empty(self) -> None:
        self.assertEqual(zip_with([], [], lambda a, b: a + b), [])


if __name__ == "__main__":
    unittest.main()
