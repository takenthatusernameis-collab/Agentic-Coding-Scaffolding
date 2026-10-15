"""Tests for set_utils module."""

import unittest

from set_utils import (
    cartesian_product,
    difference,
    intersection,
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


class TestIntersection(unittest.TestCase):
    def test_intersection_basic(self) -> None:
        self.assertEqual(intersection([1, 2, 3], [2, 3, 4]), {2, 3})

    def test_intersection_disjoint(self) -> None:
        self.assertEqual(intersection([1, 2], [3, 4]), set())

    def test_intersection_no_overlap(self) -> None:
        self.assertEqual(intersection([], [1, 2]), set())


class TestUnion(unittest.TestCase):
    def test_union_basic(self) -> None:
        self.assertEqual(union([1, 2], [2, 3]), {1, 2, 3})

    def test_union_disjoint(self) -> None:
        self.assertEqual(union([1, 2], [3, 4]), {1, 2, 3, 4})

    def test_union_empty(self) -> None:
        self.assertEqual(union([], []), set())


class TestDifference(unittest.TestCase):
    def test_difference_basic(self) -> None:
        self.assertEqual(difference([1, 2, 3], [2]), {1, 3})

    def test_difference_no_overlap(self) -> None:
        self.assertEqual(difference([1, 2], [3, 4]), {1, 2})

    def test_difference_empty(self) -> None:
        self.assertEqual(difference([], [1, 2]), set())


class TestSymmetricDifference(unittest.TestCase):
    def test_symmetric_difference_basic(self) -> None:
        self.assertEqual(symmetric_difference([1, 2, 3], [2, 3, 4]), {1, 4})

    def test_symmetric_difference_disjoint(self) -> None:
        self.assertEqual(symmetric_difference([1, 2], [3, 4]), {1, 2, 3, 4})

    def test_symmetric_difference_equal(self) -> None:
        self.assertEqual(symmetric_difference([1, 2], [1, 2]), set())


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


if __name__ == "__main__":
    unittest.main()
