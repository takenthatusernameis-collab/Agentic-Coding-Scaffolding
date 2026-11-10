"""Tests for set_utils module."""

import unittest

from set_utils import (
    cartesian_product,
    count_difference,
    count_intersection,
    count_symmetric_difference,
    count_union,
    difference,
    has_intersection,
    intersection,
    is_disjoint,
    is_equal,
    is_not_equal,
    is_not_subset,
    is_not_superset,
    is_proper_subset,
    is_proper_superset,
    is_subset,
    is_superset,
    power_set,
    symmetric_difference,
    union,
)


class TestIsSubset(unittest.TestCase):
    def test_is_subset_true(self) -> None:
        self.assertTrue(is_subset([1, 2], [1, 2, 3]))

    def test_is_subset_false(self) -> None:
        self.assertFalse(is_subset([1, 4], [1, 2, 3]))

    def test_is_subset_equal(self) -> None:
        self.assertTrue(is_subset([1, 2], [1, 2]))

    def test_is_subset_empty(self) -> None:
        self.assertTrue(is_subset([], [1, 2, 3]))


class TestIsSuperset(unittest.TestCase):
    def test_is_superset_true(self) -> None:
        self.assertTrue(is_superset([1, 2, 3], [2]))

    def test_is_superset_false(self) -> None:
        self.assertFalse(is_superset([1, 2], [2, 3]))

    def test_is_superset_equal(self) -> None:
        self.assertTrue(is_superset([1, 2], [1, 2]))


class TestIsNotSubset(unittest.TestCase):
    def test_not_subset_true(self) -> None:
        self.assertTrue(is_not_subset([1, 4], [1, 2, 3]))

    def test_not_subset_false_subset(self) -> None:
        self.assertFalse(is_not_subset([1, 2], [1, 2, 3]))

    def test_not_subset_equal(self) -> None:
        self.assertFalse(is_not_subset([1, 2], [1, 2]))

    def test_not_subset_empty(self) -> None:
        self.assertFalse(is_not_subset([], [1, 2, 3]))

    def test_not_subset_duplicates_ignored(self) -> None:
        self.assertTrue(is_not_subset([1, 1, 4], [1, 2, 3]))
        self.assertFalse(is_not_subset([1, 1, 2], [1, 2, 3]))

    def test_not_subset_strings(self) -> None:
        self.assertTrue(is_not_subset("ad", "abc"))
        self.assertFalse(is_not_subset("ab", "abc"))

    def test_not_subset_consistency_with_is_subset(self) -> None:
        cases = [
            ([1, 2], [1, 2, 3]),
            ([1, 4], [1, 2, 3]),
            ([1, 2], [1, 2]),
            ([], [1, 2, 3]),
            ("ab", "abc"),
        ]
        for a, b in cases:
            self.assertEqual(is_not_subset(a, b), not is_subset(a, b))

    def test_not_subset_type_error(self) -> None:
        with self.assertRaises(TypeError):
            is_not_subset(123, [1, 2])  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            is_not_subset([1, 2], 123)  # type: ignore[arg-type]


class TestIsNotSuperset(unittest.TestCase):
    def test_not_superset_true(self) -> None:
        self.assertTrue(is_not_superset([1, 2], [2, 3]))

    def test_not_superset_false_superset(self) -> None:
        self.assertFalse(is_not_superset([1, 2, 3], [2]))

    def test_not_superset_equal(self) -> None:
        self.assertFalse(is_not_superset([1, 2], [1, 2]))

    def test_not_superset_empty_subset(self) -> None:
        self.assertFalse(is_not_superset([1, 2, 3], []))

    def test_not_superset_duplicates_ignored(self) -> None:
        self.assertTrue(is_not_superset([1, 1, 2], [2, 3]))
        self.assertFalse(is_not_superset([1, 1, 2, 3], [2, 3]))

    def test_not_superset_strings(self) -> None:
        self.assertTrue(is_not_superset("ab", "bc"))
        self.assertFalse(is_not_superset("abc", "ab"))

    def test_not_superset_consistency_with_is_superset(self) -> None:
        cases = [
            ([1, 2, 3], [2]),
            ([1, 2], [2, 3]),
            ([1, 2], [1, 2]),
            ([1, 2, 3], []),
            ("abc", "ab"),
        ]
        for a, b in cases:
            self.assertEqual(is_not_superset(a, b), not is_superset(a, b))

    def test_not_superset_type_error(self) -> None:
        with self.assertRaises(TypeError):
            is_not_superset(123, [1, 2])  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            is_not_superset([1, 2], 123)  # type: ignore[arg-type]


class TestIsDisjoint(unittest.TestCase):
    def test_disjoint_true(self):
        self.assertTrue(is_disjoint([1, 2], [3, 4]))

    def test_disjoint_false(self):
        self.assertFalse(is_disjoint([1, 2], [2, 3]))

    def test_disjoint_equal(self):
        self.assertFalse(is_disjoint([1, 2], [1, 2]))

    def test_disjoint_empty(self):
        self.assertTrue(is_disjoint([], [1, 2, 3]))
        self.assertTrue(is_disjoint([1, 2, 3], []))
        self.assertTrue(is_disjoint([], []))

    def test_disjoint_overlap_single(self):
        self.assertFalse(is_disjoint([1, 2, 3], [3, 4, 5]))

    def test_disjoint_type_error(self):
        with self.assertRaises(TypeError):
            is_disjoint(123, [1, 2])  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            is_disjoint([1, 2], 123)  # type: ignore[arg-type]


class TestHasIntersection(unittest.TestCase):
    def test_has_intersection_true(self) -> None:
        self.assertTrue(has_intersection([1, 2], [2, 3]))

    def test_has_intersection_false(self) -> None:
        self.assertFalse(has_intersection([1, 2], [3, 4]))

    def test_has_intersection_empty(self) -> None:
        self.assertFalse(has_intersection([], [1, 2]))
        self.assertFalse(has_intersection([1, 2], []))
        self.assertFalse(has_intersection([], []))

    def test_has_intersection_duplicates(self) -> None:
        self.assertTrue(has_intersection([1, 1, 2], [2, 2]))

    def test_has_intersection_strings(self) -> None:
        self.assertTrue(has_intersection("abc", "cd"))
        self.assertFalse(has_intersection("abc", "de"))

    def test_has_intersection_consistency_with_is_disjoint(self) -> None:
        cases = [
            ([1, 2], [3, 4]),
            ([1, 2], [2, 3]),
            ([], [1]),
            ([1, 1], [1]),
        ]
        for a, b in cases:
            self.assertEqual(has_intersection(a, b), not is_disjoint(a, b))

    def test_has_intersection_type_error(self) -> None:
        with self.assertRaises(TypeError):
            has_intersection(123, [1, 2])  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            has_intersection([1, 2], 123)  # type: ignore[arg-type]


class TestIsEqual(unittest.TestCase):
    def test_is_equal_same_order(self):
        self.assertTrue(is_equal([1, 2, 3], [1, 2, 3]))

    def test_is_equal_different_order(self):
        self.assertTrue(is_equal([1, 2, 3], [3, 2, 1]))

    def test_is_equal_duplicates_ignored(self):
        self.assertTrue(is_equal([1, 2, 2, 3], [1, 2, 3]))

    def test_is_equal_not_equal(self):
        self.assertFalse(is_equal([1, 2], [1, 2, 3]))

    def test_is_equal_empty(self):
        self.assertTrue(is_equal([], []))

    def test_is_equal_one_empty(self):
        self.assertFalse(is_equal([1, 2], []))

    def test_is_equal_disjoint(self):
        self.assertFalse(is_equal([1, 2], [3, 4]))

    def test_is_equal_strings(self):
        self.assertTrue(is_equal("abc", "cba"))

    def test_is_equal_tuples(self):
        self.assertTrue(is_equal((1, 2), [2, 1]))

    def test_is_equal_type_error(self):
        with self.assertRaises(TypeError):
            is_equal(123, [1, 2])  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            is_equal([1, 2], 123)  # type: ignore[arg-type]


class TestIsNotEqual(unittest.TestCase):
    def test_is_not_equal_different(self):
        self.assertTrue(is_not_equal([1, 2], [1, 2, 3]))

    def test_is_not_equal_same_order(self):
        self.assertFalse(is_not_equal([1, 2, 3], [1, 2, 3]))

    def test_is_not_equal_different_order(self):
        self.assertFalse(is_not_equal([1, 2, 3], [3, 2, 1]))

    def test_is_not_equal_duplicates_ignored(self):
        self.assertFalse(is_not_equal([1, 2, 2, 3], [1, 2, 3]))

    def test_is_not_equal_empty(self):
        self.assertFalse(is_not_equal([], []))

    def test_is_not_equal_one_empty(self):
        self.assertTrue(is_not_equal([1, 2], []))
        self.assertTrue(is_not_equal([], [1, 2]))

    def test_is_not_equal_disjoint(self):
        self.assertTrue(is_not_equal([1, 2], [3, 4]))

    def test_is_not_equal_strings(self):
        self.assertFalse(is_not_equal("abc", "cba"))
        self.assertTrue(is_not_equal("abc", "ab"))

    def test_is_not_equal_consistency_with_is_equal(self):
        cases = [
            ([1, 2, 3], [1, 2, 3]),
            ([1, 2, 3], [3, 2, 1]),
            ([1, 2, 2, 3], [1, 2, 3]),
            ([1, 2], [1, 2, 3]),
            ([], []),
            ([1, 2], []),
            ([1, 2], [3, 4]),
            ("abc", "cba"),
        ]
        for a, b in cases:
            self.assertEqual(is_not_equal(a, b), not is_equal(a, b))

    def test_is_not_equal_type_error(self):
        with self.assertRaises(TypeError):
            is_not_equal(123, [1, 2])  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            is_not_equal([1, 2], 123)  # type: ignore[arg-type]


class TestIntersection(unittest.TestCase):
    def test_intersection_basic(self) -> None:
        self.assertEqual(intersection([1, 2, 3], [2, 3, 4]), {2, 3})

    def test_intersection_disjoint(self) -> None:
        self.assertEqual(intersection([1, 2], [3, 4]), set())

    def test_intersection_no_overlap(self) -> None:
        self.assertEqual(intersection([], [1, 2]), set())


class TestCountIntersection(unittest.TestCase):
    def test_count_intersection_basic(self) -> None:
        self.assertEqual(count_intersection([1, 2, 3], [2, 3, 4]), 2)

    def test_count_intersection_disjoint(self) -> None:
        self.assertEqual(count_intersection([1, 2], [3, 4]), 0)

    def test_count_intersection_no_overlap(self) -> None:
        self.assertEqual(count_intersection([], [1, 2]), 0)
        self.assertEqual(count_intersection([1, 2], []), 0)
        self.assertEqual(count_intersection([], []), 0)

    def test_count_intersection_duplicates_ignored(self) -> None:
        # Distinct elements only: duplicates in either input count once.
        self.assertEqual(count_intersection([1, 1, 2], [2, 2]), 1)
        self.assertEqual(count_intersection([1, 1, 1], [1, 1]), 1)

    def test_count_intersection_strings(self) -> None:
        self.assertEqual(count_intersection("abc", "cd"), 1)
        self.assertEqual(count_intersection("abc", "de"), 0)

    def test_count_intersection_single(self) -> None:
        self.assertEqual(count_intersection([1], [1]), 1)
        self.assertEqual(count_intersection([1], [2]), 0)

    def test_count_intersection_consistency_with_intersection(self) -> None:
        cases = [
            ([1, 2, 3], [2, 3, 4]),
            ([1, 2], [3, 4]),
            ([], [1, 2]),
            ([1, 1, 2], [2, 2]),
            ("abc", "cd"),
            ([1, 2, 3, 4], [4, 3, 2, 1]),
        ]
        for a, b in cases:
            self.assertEqual(count_intersection(a, b), len(intersection(a, b)))

    def test_count_intersection_consistency_with_has_intersection(self) -> None:
        cases = [
            ([1, 2], [2, 3]),
            ([1, 2], [3, 4]),
            ([], [1, 2]),
            ([1, 1, 2], [2, 2]),
        ]
        for a, b in cases:
            self.assertEqual(has_intersection(a, b), count_intersection(a, b) > 0)

    def test_count_intersection_type_error(self) -> None:
        with self.assertRaises(TypeError):
            count_intersection(123, [1, 2])  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            count_intersection([1, 2], 123)  # type: ignore[arg-type]


class TestUnion(unittest.TestCase):
    def test_union_basic(self) -> None:
        self.assertEqual(union([1, 2], [2, 3]), {1, 2, 3})

    def test_union_disjoint(self) -> None:
        self.assertEqual(union([1, 2], [3, 4]), {1, 2, 3, 4})

    def test_union_empty(self) -> None:
        self.assertEqual(union([], []), set())


class TestCountUnion(unittest.TestCase):
    def test_count_union_basic(self) -> None:
        self.assertEqual(count_union([1, 2], [2, 3]), 3)

    def test_count_union_disjoint(self) -> None:
        self.assertEqual(count_union([1, 2], [3, 4]), 4)

    def test_count_union_empty(self) -> None:
        self.assertEqual(count_union([], []), 0)
        self.assertEqual(count_union([], [1, 2]), 2)
        self.assertEqual(count_union([1, 2], []), 2)

    def test_count_union_duplicates_ignored(self) -> None:
        self.assertEqual(count_union([1, 1, 2], [2, 2]), 2)
        self.assertEqual(count_union([1, 1, 1], [1, 1]), 1)

    def test_count_union_strings(self) -> None:
        self.assertEqual(count_union("abc", "cd"), 4)
        self.assertEqual(count_union("abc", "abc"), 3)

    def test_count_union_consistency_with_union(self) -> None:
        cases = [
            ([1, 2], [2, 3]),
            ([1, 2], [3, 4]),
            ([], [1, 2]),
            ([1, 1, 2], [2, 2]),
            ("abc", "cd"),
            ([1, 2, 3], [3, 2, 1]),
        ]
        for a, b in cases:
            self.assertEqual(count_union(a, b), len(union(a, b)))

    def test_count_union_type_error(self) -> None:
        with self.assertRaises(TypeError):
            count_union(123, [1, 2])  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            count_union([1, 2], 123)  # type: ignore[arg-type]


class TestDifference(unittest.TestCase):
    def test_difference_basic(self) -> None:
        self.assertEqual(difference([1, 2, 3], [2]), {1, 3})

    def test_difference_no_overlap(self) -> None:
        self.assertEqual(difference([1, 2], [3, 4]), {1, 2})

    def test_difference_empty(self) -> None:
        self.assertEqual(difference([], [1, 2]), set())


class TestCountDifference(unittest.TestCase):
    def test_count_difference_basic(self) -> None:
        self.assertEqual(count_difference([1, 2, 3], [2]), 2)

    def test_count_difference_no_overlap(self) -> None:
        self.assertEqual(count_difference([1, 2], [3, 4]), 2)

    def test_count_difference_empty(self) -> None:
        self.assertEqual(count_difference([], [1, 2]), 0)
        self.assertEqual(count_difference([1, 2], []), 2)
        self.assertEqual(count_difference([], []), 0)

    def test_count_difference_duplicates_ignored(self) -> None:
        self.assertEqual(count_difference([1, 1, 2], [2]), 1)
        self.assertEqual(count_difference([1, 1, 1], [1]), 0)

    def test_count_difference_strings(self) -> None:
        self.assertEqual(count_difference("abc", "cd"), 2)
        self.assertEqual(count_difference("abc", "abc"), 0)

    def test_count_difference_all_removed(self) -> None:
        self.assertEqual(count_difference([1, 2], [1, 2, 3]), 0)

    def test_count_difference_consistency_with_difference(self) -> None:
        cases = [
            ([1, 2, 3], [2]),
            ([1, 2], [3, 4]),
            ([], [1, 2]),
            ([1, 1, 2], [2]),
            ("abc", "cd"),
            ([1, 2], [1, 2, 3]),
        ]
        for a, b in cases:
            self.assertEqual(count_difference(a, b), len(difference(a, b)))

    def test_count_difference_type_error(self) -> None:
        with self.assertRaises(TypeError):
            count_difference(123, [1, 2])  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            count_difference([1, 2], 123)  # type: ignore[arg-type]


class TestSymmetricDifference(unittest.TestCase):
    def test_symmetric_difference_basic(self) -> None:
        self.assertEqual(symmetric_difference([1, 2, 3], [2, 3, 4]), {1, 4})

    def test_symmetric_difference_disjoint(self) -> None:
        self.assertEqual(symmetric_difference([1, 2], [3, 4]), {1, 2, 3, 4})

    def test_symmetric_difference_equal(self) -> None:
        self.assertEqual(symmetric_difference([1, 2], [1, 2]), set())


class TestCountSymmetricDifference(unittest.TestCase):
    def test_count_symmetric_difference_basic(self) -> None:
        self.assertEqual(count_symmetric_difference([1, 2, 3], [2, 3, 4]), 2)

    def test_count_symmetric_difference_disjoint(self) -> None:
        self.assertEqual(count_symmetric_difference([1, 2], [3, 4]), 4)

    def test_count_symmetric_difference_equal(self) -> None:
        self.assertEqual(count_symmetric_difference([1, 2], [1, 2]), 0)

    def test_count_symmetric_difference_empty(self) -> None:
        self.assertEqual(count_symmetric_difference([], []), 0)
        self.assertEqual(count_symmetric_difference([], [1, 2]), 2)
        self.assertEqual(count_symmetric_difference([1, 2], []), 2)

    def test_count_symmetric_difference_duplicates_ignored(self) -> None:
        self.assertEqual(count_symmetric_difference([1, 1, 2], [2, 2]), 1)
        self.assertEqual(count_symmetric_difference([1, 1, 1], [1, 1]), 0)

    def test_count_symmetric_difference_strings(self) -> None:
        self.assertEqual(count_symmetric_difference("abc", "cd"), 3)
        self.assertEqual(count_symmetric_difference("abc", "abc"), 0)

    def test_count_symmetric_difference_consistency(self) -> None:
        cases = [
            ([1, 2, 3], [2, 3, 4]),
            ([1, 2], [3, 4]),
            ([1, 2], [1, 2]),
            ([], [1, 2]),
            ([1, 1, 2], [2, 2]),
            ("abc", "cd"),
        ]
        for a, b in cases:
            self.assertEqual(
                count_symmetric_difference(a, b),
                len(symmetric_difference(a, b)),
            )

    def test_count_symmetric_difference_type_error(self) -> None:
        with self.assertRaises(TypeError):
            count_symmetric_difference(123, [1, 2])  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            count_symmetric_difference([1, 2], 123)  # type: ignore[arg-type]


class TestCartesianProduct(unittest.TestCase):
    def test_cartesian_product_basic(self) -> None:
        result = list(cartesian_product([1, 2], ["a", "b"]))
        self.assertEqual(result, [(1, "a"), (1, "b"), (2, "a"), (2, "b")])

    def test_cartesian_product_empty(self) -> None:
        self.assertEqual(list(cartesian_product([], [1, 2])), [])
        self.assertEqual(list(cartesian_product([1, 2], [])), [])

    def test_cartesian_product_single(self) -> None:
        self.assertEqual(list(cartesian_product([1], ["x"])), [(1, "x")])


class TestPowerSet(unittest.TestCase):
    def test_power_set_empty(self) -> None:
        result: list = list(power_set([]))
        self.assertEqual(result, [()])

    def test_power_set_single(self) -> None:
        result = list(power_set([1]))
        self.assertEqual(result, [(), (1,)])

    def test_power_set_two(self) -> None:
        result = list(power_set([1, 2]))
        self.assertEqual(len(result), 4)
        self.assertIn((), result)
        self.assertIn((1,), result)
        self.assertIn((2,), result)
        self.assertIn((1, 2), result)

    def test_power_set_three(self) -> None:
        result = list(power_set([1, 2, 3]))
        self.assertEqual(len(result), 8)

    def test_power_set_preserves_order(self) -> None:
        result = list(power_set(["a", "b"]))
        self.assertEqual(result, [(), ("a",), ("b",), ("a", "b")])


class TestIsProperSubset(unittest.TestCase):
    def test_proper_subset_true(self) -> None:
        self.assertTrue(is_proper_subset([1, 2], [1, 2, 3]))

    def test_proper_subset_false_equal(self) -> None:
        self.assertFalse(is_proper_subset([1, 2], [1, 2]))

    def test_proper_subset_false_not_subset(self) -> None:
        self.assertFalse(is_proper_subset([1, 4], [1, 2, 3]))

    def test_proper_subset_empty(self) -> None:
        self.assertTrue(is_proper_subset([], [1, 2, 3]))
        self.assertFalse(is_proper_subset([], []))

    def test_proper_subset_duplicates_ignored(self) -> None:
        self.assertTrue(is_proper_subset([1, 1, 2], [1, 2, 3]))

    def test_proper_subset_strings(self) -> None:
        self.assertTrue(is_proper_subset("ab", "abc"))
        self.assertFalse(is_proper_subset("abc", "abc"))

    def test_proper_subset_consistency_with_is_subset(self) -> None:
        cases = [
            ([1, 2], [1, 2, 3]),
            ([1, 2], [1, 2]),
            ([1, 4], [1, 2, 3]),
            ([], [1, 2, 3]),
            ([], []),
        ]
        for a, b in cases:
            self.assertEqual(is_proper_subset(a, b), is_subset(a, b) and not is_equal(a, b))

    def test_proper_subset_type_error(self) -> None:
        with self.assertRaises(TypeError):
            is_proper_subset(123, [1, 2])  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            is_proper_subset([1, 2], 123)  # type: ignore[arg-type]


class TestIsProperSuperset(unittest.TestCase):
    def test_proper_superset_true(self) -> None:
        self.assertTrue(is_proper_superset([1, 2, 3], [1, 2]))

    def test_proper_superset_false_equal(self) -> None:
        self.assertFalse(is_proper_superset([1, 2], [1, 2]))

    def test_proper_superset_false_not_superset(self) -> None:
        self.assertFalse(is_proper_superset([1, 2], [2, 3]))

    def test_proper_superset_empty(self) -> None:
        self.assertTrue(is_proper_superset([1, 2, 3], []))
        self.assertFalse(is_proper_superset([], []))

    def test_proper_superset_duplicates_ignored(self) -> None:
        self.assertTrue(is_proper_superset([1, 2, 2, 3], [1, 2]))

    def test_proper_superset_strings(self) -> None:
        self.assertTrue(is_proper_superset("abc", "ab"))
        self.assertFalse(is_proper_superset("abc", "abc"))

    def test_proper_superset_consistency_with_is_superset(self) -> None:
        cases = [
            ([1, 2, 3], [1, 2]),
            ([1, 2], [1, 2]),
            ([1, 2], [2, 3]),
            ([1, 2, 3], []),
            ([], []),
        ]
        for a, b in cases:
            self.assertEqual(
                is_proper_superset(a, b),
                is_superset(a, b) and not is_equal(a, b),
            )

    def test_proper_superset_type_error(self) -> None:
        with self.assertRaises(TypeError):
            is_proper_superset(123, [1, 2])  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            is_proper_superset([1, 2], 123)  # type: ignore[arg-type]


if __name__ == "__main__":
    unittest.main()
