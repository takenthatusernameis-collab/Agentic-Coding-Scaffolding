import unittest

from itertools_utils import (
    accumulate_values,
    all_equal,
    chain_iterables,
    chunk_iterable,
    combinations_of,
    combinations_with_replacement_of,
    count_duplicates,
    count_from,
    count_if,
    count_none,
    cycle_take,
    drop,
    drop_while_pred,
    first_or_default,
    flatten_once,
    group_by_key,
    grouper,
    has_all,
    has_any,
    has_duplicates,
    has_none,
    is_empty_iterable,
    last_or_default,
    pairwise_iterable,
    partition,
    product_of,
    repeat_value,
    sliding_window,
    take,
    take_while_pred,
    unique_everseen,
    unique_justseen,
    window,
    zip_longest_iterables,
    zip_strict_iterables,
)


class TestIterToolsUtils(unittest.TestCase):
    def test_chain_iterables(self):
        self.assertEqual(chain_iterables([1, 2], [3, 4]), [1, 2, 3, 4])

    def test_chunk_iterable(self):
        self.assertEqual(chunk_iterable(range(10), 3), [[0, 1, 2], [3, 4, 5], [6, 7, 8], [9]])

    def test_combinations(self):
        self.assertEqual(combinations_of([1, 2, 3], 2), [(1, 2), (1, 3), (2, 3)])

    def test_combinations_with_replacement(self):
        self.assertEqual(
            combinations_with_replacement_of([1, 2, 3], 2),
            [(1, 1), (1, 2), (1, 3), (2, 2), (2, 3), (3, 3)],
        )


class TestPairwiseIterable(unittest.TestCase):
    def test_basic(self):
        self.assertEqual(pairwise_iterable([1, 2, 3, 4]), [(1, 2), (2, 3), (3, 4)])

    def test_two_elements(self):
        self.assertEqual(pairwise_iterable([1, 2]), [(1, 2)])

    def test_single_element(self):
        self.assertEqual(pairwise_iterable([1]), [])

    def test_empty(self):
        self.assertEqual(pairwise_iterable([]), [])

    def test_non_iterable_raises_type_error(self):
        with self.assertRaises(TypeError):
            pairwise_iterable(123)

    def test_product(self):
        self.assertEqual(product_of([[1, 2], [3, 4]]), [(1, 3), (1, 4), (2, 3), (2, 4)])

    def test_group_by_key(self):
        res = group_by_key([1, 2, 3, 4], lambda x: x % 2)
        self.assertEqual(res[0], [2, 4])
        self.assertEqual(res[1], [1, 3])

    def test_invalid_types(self):
        with self.assertRaises(ValueError):
            chunk_iterable([1, 2, 3], 0)
        with self.assertRaises(ValueError):
            chunk_iterable([1, 2, 3], -1)
        with self.assertRaises(TypeError):
            chunk_iterable([1, 2, 3], "x")


class TestFlattenOnce(unittest.TestCase):
    def test_flatten_once(self):
        self.assertEqual(flatten_once([[1, 2], [3, 4], [5]]), [1, 2, 3, 4, 5])

    def test_empty(self):
        self.assertEqual(flatten_once([]), [])

    def test_nested_iterables(self):
        self.assertEqual(flatten_once([(1, 2), {3, 4}]), [1, 2, 3, 4])

    def test_non_iterable_raises_type_error(self):
        with self.assertRaises(TypeError):
            flatten_once(42)

    def test_non_iterable_inner_element_raises_type_error(self):
        with self.assertRaises(TypeError):
            flatten_once([1, 2, 3])


class TestTakeWhilePred(unittest.TestCase):
    def test_take_while_pred(self):
        self.assertEqual(take_while_pred([1, 2, 3, 4, 5], lambda x: x < 4), [1, 2, 3])

    def test_empty(self):
        self.assertEqual(take_while_pred([], lambda x: True), [])

    def test_all_taken(self):
        self.assertEqual(take_while_pred([1, 2, 3], lambda x: x < 10), [1, 2, 3])

    def test_none_taken(self):
        self.assertEqual(take_while_pred([1, 2, 3], lambda x: x > 10), [])

    def test_non_iterable_raises_type_error(self):
        with self.assertRaises(TypeError):
            take_while_pred(42, lambda x: True)

    def test_non_callable_predicate_raises_type_error(self):
        with self.assertRaises(TypeError):
            take_while_pred([1, 2, 3], "not callable")


class TestAccumulateValues(unittest.TestCase):
    def test_default_sum(self):
        self.assertEqual(accumulate_values([1, 2, 3, 4]), [1, 3, 6, 10])

    def test_empty(self):
        self.assertEqual(accumulate_values([]), [])

    def test_single(self):
        self.assertEqual(accumulate_values([5]), [5])

    def test_with_func(self):
        self.assertEqual(accumulate_values([1, 2, 3, 4], lambda a, b: a * b), [1, 2, 6, 24])

    def test_non_iterable_raises_type_error(self):
        with self.assertRaises(TypeError):
            accumulate_values(42)

    def test_non_callable_func_raises_type_error(self):
        with self.assertRaises(TypeError):
            accumulate_values([1, 2, 3], "not callable")


class TestRepeatValue(unittest.TestCase):
    def test_default_times(self):
        self.assertEqual(repeat_value("x"), ["x", "x", "x"])

    def test_explicit_times(self):
        self.assertEqual(repeat_value(0, 4), [0, 0, 0, 0])

    def test_zero_times(self):
        self.assertEqual(repeat_value("x", 0), [])

    def test_non_int_times_raises_type_error(self):
        with self.assertRaises(TypeError):
            repeat_value("x", "three")

    def test_negative_times_raises_value_error(self):
        with self.assertRaises(ValueError):
            repeat_value("x", -1)


class TestCycleTake(unittest.TestCase):
    def test_cycle_take(self):
        self.assertEqual(cycle_take([1, 2, 3], 7), [1, 2, 3, 1, 2, 3, 1])

    def test_empty(self):
        self.assertEqual(cycle_take([], 5), [])

    def test_zero(self):
        self.assertEqual(cycle_take([1, 2, 3], 0), [])

    def test_non_iterable_raises_type_error(self):
        with self.assertRaises(TypeError):
            cycle_take(42, 5)

    def test_non_int_n_raises_type_error(self):
        with self.assertRaises(TypeError):
            cycle_take([1, 2, 3], "5")

    def test_negative_n_raises_value_error(self):
        with self.assertRaises(ValueError):
            cycle_take([1, 2, 3], -1)


class TestPartition(unittest.TestCase):
    def test_partition_even_odd(self):
        self.assertEqual(partition([1, 2, 3, 4, 5], lambda x: x % 2 == 0), ([2, 4], [1, 3, 5]))

    def test_empty_iterable(self):
        self.assertEqual(partition([], bool), ([], []))

    def test_all_true(self):
        self.assertEqual(partition([1, 2, 3], bool), ([1, 2, 3], []))

    def test_all_false(self):
        self.assertEqual(partition([0, "", None], bool), ([], [0, "", None]))

    def test_preserves_order(self):
        self.assertEqual(
            partition(["a", "ab", "b", "bc"], lambda x: len(x) == 2),
            (["ab", "bc"], ["a", "b"]),
        )

    def test_non_iterable_raises_type_error(self):
        with self.assertRaises(TypeError):
            partition(42, bool)

    def test_non_callable_predicate_raises_type_error(self):
        with self.assertRaises(TypeError):
            partition([1, 2, 3], "not callable")


class TestZipLongestIterables(unittest.TestCase):
    def test_equal_length(self):
        self.assertEqual(zip_longest_iterables([1, 2], [3, 4]), [(1, 3), (2, 4)])

    def test_fill_default_none(self):
        self.assertEqual(
            zip_longest_iterables([1, 2, 3], ["a", "b"]),
            [(1, "a"), (2, "b"), (3, None)],
        )

    def test_fill_value(self):
        self.assertEqual(
            zip_longest_iterables([1, 2], [3, 4, 5], fillvalue=-1),
            [(1, 3), (2, 4), (-1, 5)],
        )

    def test_single_iterable(self):
        self.assertEqual(zip_longest_iterables([1, 2, 3]), [(1,), (2,), (3,)])

    def test_no_iterables(self):
        self.assertEqual(zip_longest_iterables(), [])

    def test_empty_iterables(self):
        self.assertEqual(zip_longest_iterables([], []), [])

    def test_one_empty(self):
        self.assertEqual(
            zip_longest_iterables([1, 2], [], fillvalue=0),
            [(1, 0), (2, 0)],
        )

    def test_three_iterables(self):
        self.assertEqual(
            zip_longest_iterables([1, 2], [3, 4, 5], ["a"], fillvalue=-1),
            [(1, 3, "a"), (2, 4, -1), (-1, 5, -1)],
        )

    def test_preserves_order(self):
        self.assertEqual(
            zip_longest_iterables(["a", "b"], [1, 2, 3]),
            [("a", 1), ("b", 2), (None, 3)],
        )

    def test_non_iterable_raises_type_error(self):
        with self.assertRaises(TypeError):
            zip_longest_iterables([1, 2], 42)

    def test_non_iterable_first_raises_type_error(self):
        with self.assertRaises(TypeError):
            zip_longest_iterables(42, [1, 2])

    def test_fillvalue_not_required_to_be_iterable(self):
        self.assertEqual(
            zip_longest_iterables([1, 2], [3], fillvalue=0),
            [(1, 3), (2, 0)],
        )


class TestZipStrictIterables(unittest.TestCase):
    def test_equal_length(self):
        self.assertEqual(
            zip_strict_iterables([1, 2, 3], ["a", "b", "c"]),
            [(1, "a"), (2, "b"), (3, "c")],
        )

    def test_single_iterable(self):
        self.assertEqual(zip_strict_iterables([1, 2, 3]), [(1,), (2,), (3,)])

    def test_no_iterables(self):
        self.assertEqual(zip_strict_iterables(), [])

    def test_empty_iterables(self):
        self.assertEqual(zip_strict_iterables([], []), [])

    def test_three_iterables(self):
        self.assertEqual(
            zip_strict_iterables([1, 2], [3, 4], ["a", "b"]),
            [(1, 3, "a"), (2, 4, "b")],
        )

    def test_unequal_length_raises_value_error(self):
        with self.assertRaises(ValueError):
            zip_strict_iterables([1, 2, 3], ["a", "b"])

    def test_one_empty_raises_value_error(self):
        with self.assertRaises(ValueError):
            zip_strict_iterables([1, 2], [])

    def test_non_iterable_raises_type_error(self):
        with self.assertRaises(TypeError):
            zip_strict_iterables([1, 2], 42)


class TestDropWhilePred(unittest.TestCase):
    def test_basic(self):
        self.assertEqual(drop_while_pred([1, 2, 3, 4], lambda x: x < 3), [3, 4])

    def test_none_dropped(self):
        self.assertEqual(drop_while_pred([5, 6, 7], lambda x: x < 3), [5, 6, 7])

    def test_all_dropped(self):
        self.assertEqual(drop_while_pred([1, 2, 3], lambda x: x < 10), [])

    def test_empty(self):
        self.assertEqual(drop_while_pred([], lambda x: True), [])

    def test_non_iterable_raises_type_error(self):
        with self.assertRaises(TypeError):
            drop_while_pred(42, lambda x: True)

    def test_non_callable_predicate_raises_type_error(self):
        with self.assertRaises(TypeError):
            drop_while_pred([1, 2, 3], 42)


class TestUniqueEverseen(unittest.TestCase):
    def test_basic(self):
        self.assertEqual(
            unique_everseen("AAAABBBCCDAABBB"),
            ["A", "B", "C", "D"],
        )

    def test_with_key(self):
        self.assertEqual(
            unique_everseen("ABbACa", key=str.lower),
            ["A", "B", "C"],
        )

    def test_numbers(self):
        self.assertEqual(unique_everseen([1, 2, 1, 3, 2]), [1, 2, 3])

    def test_empty(self):
        self.assertEqual(unique_everseen([]), [])

    def test_non_iterable_raises_type_error(self):
        with self.assertRaises(TypeError):
            unique_everseen(42)

    def test_non_callable_key_raises_type_error(self):
        with self.assertRaises(TypeError):
            unique_everseen([1, 2, 3], key=123)


class TestUniqueJustseen(unittest.TestCase):
    def test_unique_justseen_consecutive(self):
        self.assertEqual(
            unique_justseen("AAAABBBCCDAABBB"),
            list("ABCDAB"),
        )

    def test_unique_justseen_key(self):
        self.assertEqual(
            unique_justseen("ABbACa", key=str.lower),
            list("ABACa"),
        )

    def test_unique_justseen_empty(self):
        self.assertEqual(unique_justseen([]), [])

    def test_unique_justseen_rejects_non_iterable(self):
        with self.assertRaises(TypeError):
            unique_justseen(42)

    def test_unique_justseen_rejects_bad_key(self):
        with self.assertRaises(TypeError):
            unique_justseen([1, 2, 3], key=123)


class TestSlidingWindow(unittest.TestCase):
    def test_sliding_window_basic(self):
        self.assertEqual(sliding_window([1, 2, 3, 4], 2), [(1, 2), (2, 3), (3, 4)])

    def test_sliding_window_exact_length(self):
        self.assertEqual(sliding_window([1, 2, 3], 3), [(1, 2, 3)])

    def test_sliding_window_larger_than_iterable(self):
        self.assertEqual(sliding_window([1, 2, 3], 5), [])

    def test_sliding_window_length_one(self):
        self.assertEqual(sliding_window([1, 2, 3], 1), [(1,), (2,), (3,)])

    def test_sliding_window_empty(self):
        self.assertEqual(sliding_window([], 3), [])

    def test_sliding_window_zero(self):
        self.assertEqual(sliding_window([1, 2, 3], 0), [])

    def test_sliding_window_rejects_negative(self):
        with self.assertRaises(ValueError):
            sliding_window([1, 2, 3], -1)

    def test_sliding_window_rejects_non_iterable(self):
        with self.assertRaises(TypeError):
            sliding_window(123, 2)

    def test_sliding_window_rejects_bad_n(self):
        with self.assertRaises(TypeError):
            sliding_window([1, 2, 3], 2.5)
        with self.assertRaises(TypeError):
            sliding_window([1, 2, 3], True)

    def test_window_alias(self):
        self.assertEqual(window("abc", 2), [("a", "b"), ("b", "c")])


class TestGrouper(unittest.TestCase):
    def test_grouper_exact_multiple(self):
        self.assertEqual(grouper([1, 2, 3, 4], 2), [(1, 2), (3, 4)])

    def test_grouper_pads_with_none_default(self):
        self.assertEqual(grouper([1, 2, 3, 4, 5], 2), [(1, 2), (3, 4), (5, None)])

    def test_grouper_pads_with_custom_fillvalue(self):
        self.assertEqual(
            grouper([1, 2, 3, 4, 5], 2, fillvalue=-1),
            [(1, 2), (3, 4), (5, -1)],
        )

    def test_grouper_pads_short_chunk_to_full_size(self):
        self.assertEqual(grouper([1], 3, fillvalue=0), [(1, 0, 0)])

    def test_grouper_size_one(self):
        self.assertEqual(grouper([1, 2, 3], 1), [(1,), (2,), (3,)])

    def test_grouper_empty_iterable(self):
        self.assertEqual(grouper([], 3), [])
        self.assertEqual(grouper([], 3, fillvalue=0), [])

    def test_grouper_strings(self):
        self.assertEqual(grouper("abcde", 2), [("a", "b"), ("c", "d"), ("e", None)])

    def test_grouper_each_chunk_has_n_elements(self):
        for n in (1, 2, 3, 5, 7):
            for data in ([], [1], [1, 2], list(range(11))):
                chunks = grouper(data, n)
                for chunk in chunks:
                    self.assertEqual(len(chunk), n)

    def test_grouper_preserves_order_and_concatenation(self):
        data = list(range(7))
        chunks = grouper(data, 3)
        flat = [item for chunk in chunks for item in chunk if item is not None]
        self.assertEqual(flat, data)

    def test_grouper_rejects_non_iterable(self):
        with self.assertRaises(TypeError):
            grouper(123, 2)

    def test_grouper_rejects_bad_n_type(self):
        with self.assertRaises(TypeError):
            grouper([1, 2, 3], 2.5)
        with self.assertRaises(TypeError):
            grouper([1, 2, 3], True)

    def test_grouper_rejects_non_positive_n(self):
        with self.assertRaises(ValueError):
            grouper([1, 2, 3], 0)
        with self.assertRaises(ValueError):
            grouper([1, 2, 3], -1)


    def test_count_from_default(self):
        self.assertEqual(count_from(), list(range(1000)))

    def test_count_from_start_step(self):
        self.assertEqual(count_from(5, 2)[:5], [5, 7, 9, 11, 13])

    def test_count_from_bad_start_type(self):
        with self.assertRaises(TypeError):
            count_from(True)

    def test_count_from_bad_step_type(self):
        with self.assertRaises(TypeError):
            count_from(0, True)


class TestIsEmptyIterable(unittest.TestCase):
    def test_empty_list(self):
        self.assertTrue(is_empty_iterable([]))

    def test_non_empty_list(self):
        self.assertFalse(is_empty_iterable([1, 2, 3]))

    def test_empty_string(self):
        self.assertTrue(is_empty_iterable(""))

    def test_non_empty_string(self):
        self.assertFalse(is_empty_iterable("abc"))

    def test_empty_tuple(self):
        self.assertTrue(is_empty_iterable(()))

    def test_generator_empty(self):
        self.assertTrue(is_empty_iterable(iter(())))

    def test_generator_non_empty(self):
        self.assertFalse(is_empty_iterable(x for x in range(3)))

    def test_rejects_non_iterable(self):
        with self.assertRaises(TypeError):
            is_empty_iterable(42)

    def test_rejects_none(self):
        with self.assertRaises(TypeError):
            is_empty_iterable(None)


class TestTake(unittest.TestCase):
    def test_basic(self):
        self.assertEqual(take([1, 2, 3, 4], 2), [1, 2])

    def test_more_than_available(self):
        self.assertEqual(take([1, 2], 5), [1, 2])

    def test_zero(self):
        self.assertEqual(take(range(10), 0), [])

    def test_empty(self):
        self.assertEqual(take([], 3), [])

    def test_generator(self):
        self.assertEqual(take((x for x in range(10)), 3), [0, 1, 2])

    def test_rejects_non_iterable(self):
        with self.assertRaises(TypeError):
            take(42, 1)

    def test_rejects_bool_n(self):
        with self.assertRaises(TypeError):
            take([1, 2, 3], True)

    def test_rejects_non_int_n(self):
        with self.assertRaises(TypeError):
            take([1, 2, 3], "2")

    def test_rejects_negative_n(self):
        with self.assertRaises(ValueError):
            take([1, 2, 3], -1)


class TestDrop(unittest.TestCase):
    def test_basic(self):
        self.assertEqual(drop([1, 2, 3, 4], 2), [3, 4])

    def test_more_than_available(self):
        self.assertEqual(drop([1, 2], 5), [])

    def test_zero(self):
        self.assertEqual(drop([1, 2, 3], 0), [1, 2, 3])

    def test_empty(self):
        self.assertEqual(drop([], 3), [])

    def test_generator(self):
        self.assertEqual(drop((x for x in range(5)), 2), [2, 3, 4])

    def test_rejects_non_iterable(self):
        with self.assertRaises(TypeError):
            drop(42, 1)

    def test_rejects_bool_n(self):
        with self.assertRaises(TypeError):
            drop([1, 2, 3], False)

    def test_rejects_non_int_n(self):
        with self.assertRaises(TypeError):
            drop([1, 2, 3], 2.0)

    def test_rejects_negative_n(self):
        with self.assertRaises(ValueError):
            drop([1, 2, 3], -1)


class TestFirstOrDefault(unittest.TestCase):
    def test_first_element(self):
        self.assertEqual(first_or_default([1, 2, 3]), 1)

    def test_empty_list(self):
        self.assertIsNone(first_or_default([]))

    def test_empty_with_default(self):
        self.assertEqual(first_or_default([], default="none"), "none")

    def test_generator(self):
        self.assertEqual(first_or_default(x for x in range(5)), 0)

    def test_rejects_non_iterable(self):
        with self.assertRaises(TypeError):
            first_or_default(42)

    def test_rejects_none(self):
        with self.assertRaises(TypeError):
            first_or_default(None)


class TestLastOrDefault(unittest.TestCase):
    def test_last_element(self):
        self.assertEqual(last_or_default([1, 2, 3]), 3)

    def test_empty_list(self):
        self.assertIsNone(last_or_default([]))

    def test_empty_with_default(self):
        self.assertEqual(last_or_default([], default="none"), "none")

    def test_generator(self):
        self.assertEqual(last_or_default(x for x in range(5)), 4)

    def test_rejects_non_iterable(self):
        with self.assertRaises(TypeError):
            last_or_default(42)

    def test_rejects_none(self):
        with self.assertRaises(TypeError):
            last_or_default(None)


class TestCountIf(unittest.TestCase):
    def test_basic(self):
        self.assertEqual(count_if([1, 2, 3, 4, 5], lambda x: x % 2 == 0), 2)

    def test_empty(self):
        self.assertEqual(count_if([], bool), 0)

    def test_none_match(self):
        self.assertEqual(count_if([1, 3, 5], lambda x: x % 2 == 0), 0)

    def test_all_match(self):
        self.assertEqual(count_if([2, 4, 6], lambda x: x % 2 == 0), 3)

    def test_generator(self):
        self.assertEqual(count_if((x for x in range(5)), lambda x: x > 2), 2)

    def test_truthiness(self):
        self.assertEqual(count_if([0, 1, "", "a", None, []], bool), 2)

    def test_rejects_non_iterable(self):
        with self.assertRaises(TypeError):
            count_if(42, bool)

    def test_rejects_non_callable(self):
        with self.assertRaises(TypeError):
            count_if([1, 2, 3], 123)


class TestCountNone(unittest.TestCase):
    def test_basic(self):
        self.assertEqual(count_none([1, 2, 3, 4, 5], lambda x: x % 2 == 0), 3)

    def test_empty(self):
        self.assertEqual(count_none([], bool), 0)

    def test_all_match(self):
        self.assertEqual(count_none([2, 4, 6], lambda x: x % 2 == 0), 0)

    def test_none_match(self):
        self.assertEqual(count_none([1, 3, 5], lambda x: x % 2 == 0), 3)

    def test_generator(self):
        self.assertEqual(count_none((x for x in range(5)), lambda x: x > 2), 3)

    def test_truthiness(self):
        self.assertEqual(count_none([0, 1, "", "a", None, []], bool), 4)

    def test_rejects_non_iterable(self):
        with self.assertRaises(TypeError):
            count_none(42, bool)

    def test_rejects_non_callable(self):
        with self.assertRaises(TypeError):
            count_none([1, 2, 3], 123)


class TestHasAny(unittest.TestCase):
    def test_match(self):
        self.assertTrue(has_any([1, 2, 3], lambda x: x > 2))

    def test_no_match(self):
        self.assertFalse(has_any([1, 2, 3], lambda x: x > 5))

    def test_empty(self):
        self.assertFalse(has_any([], bool))

    def test_short_circuits(self):
        seen = []

        def pred(x):
            seen.append(x)
            return x == 2

        self.assertTrue(has_any([1, 2, 3, 4], pred))
        self.assertEqual(seen, [1, 2])

    def test_generator(self):
        self.assertTrue(has_any((x for x in range(10)), lambda x: x == 7))

    def test_rejects_non_iterable(self):
        with self.assertRaises(TypeError):
            has_any(42, bool)

    def test_rejects_non_callable(self):
        with self.assertRaises(TypeError):
            has_any([1, 2, 3], "x")

class TestHasAll(unittest.TestCase):
    def test_all_match(self):
        self.assertTrue(has_all([1, 2, 3], lambda x: x > 0))

    def test_not_all_match(self):
        self.assertFalse(has_all([1, 2, 3], lambda x: x > 2))

    def test_empty(self):
        self.assertTrue(has_all([], bool))

    def test_short_circuits(self):
        seen = []

        def pred(x):
            seen.append(x)
            return x > 2

        self.assertFalse(has_all([1, 2, 3, 4], pred))
        self.assertEqual(seen, [1])

    def test_rejects_non_iterable(self):
        with self.assertRaises(TypeError):
            has_all(42, bool)

    def test_rejects_non_callable(self):
        with self.assertRaises(TypeError):
            has_all([1, 2, 3], "x")


class TestHasNone(unittest.TestCase):
    def test_none_match(self):
        self.assertTrue(has_none([1, 2, 3], lambda x: x > 5))

    def test_some_match(self):
        self.assertFalse(has_none([1, 2, 3], lambda x: x > 2))

    def test_empty(self):
        self.assertTrue(has_none([], bool))

    def test_short_circuits(self):
        seen = []

        def pred(x):
            seen.append(x)
            return x > 2

        self.assertFalse(has_none([1, 2, 3, 4], pred))
        self.assertEqual(seen, [1, 2, 3])

    def test_rejects_non_iterable(self):
        with self.assertRaises(TypeError):
            has_none(42, bool)

    def test_rejects_non_callable(self):
        with self.assertRaises(TypeError):
            has_none([1, 2, 3], "x")


class TestCountDuplicates(unittest.TestCase):
    def test_basic(self):
        self.assertEqual(count_duplicates([1, 2, 2, 3, 1]), 2)

    def test_empty(self):
        self.assertEqual(count_duplicates([]), 0)

    def test_all_distinct(self):
        self.assertEqual(count_duplicates([1, 2, 3]), 0)

    def test_rejects_non_iterable(self):
        with self.assertRaises(TypeError):
            count_duplicates(42)


class TestHasDuplicates(unittest.TestCase):
    def test_true(self):
        self.assertTrue(has_duplicates([1, 2, 2, 3]))

    def test_false(self):
        self.assertFalse(has_duplicates([1, 2, 3]))

    def test_empty(self):
        self.assertFalse(has_duplicates([]))

    def test_rejects_non_iterable(self):
        with self.assertRaises(TypeError):
            has_duplicates(42)




class TestAllEqual(unittest.TestCase):
    def test_empty(self):
        self.assertTrue(all_equal([]))

    def test_all_same(self):
        self.assertTrue(all_equal([1, 1, 1]))

    def test_different(self):
        self.assertFalse(all_equal([1, 2, 3]))

    def test_single(self):
        self.assertTrue(all_equal([42]))

    def test_rejects_non_iterable(self):
        with self.assertRaises(TypeError):
            all_equal(42)


if __name__ == "__main__":
    unittest.main()
