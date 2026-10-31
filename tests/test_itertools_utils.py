import unittest

from itertools_utils import (
    accumulate_values,
    chain_iterables,
    chunk_iterable,
    combinations_of,
    combinations_with_replacement_of,
    cycle_take,
    drop_while_pred,
    flatten_once,
    group_by_key,
    pairwise_iterable,
    partition,
    product_of,
    repeat_value,
    take_while_pred,
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
        self.assertEqual(
            partition([1, 2, 3, 4, 5], lambda x: x % 2 == 0), ([2, 4], [1, 3, 5])
        )

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
        self.assertEqual(
            zip_longest_iterables([1, 2], [3, 4]), [(1, 3), (2, 4)]
        )

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


if __name__ == "__main__":
    unittest.main()
