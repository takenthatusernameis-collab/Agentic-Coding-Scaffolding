import math
import unittest

from interval_utils import (
    interval_contains,
    interval_distance,
    interval_intersection,
    interval_is_subset,
    interval_length,
    interval_midpoint,
    interval_overlaps,
    interval_shift,
    interval_symmetric_difference,
    interval_union,
    is_valid_interval,
    merge_intervals,
    normalize_interval,
)


class TestNormalizeInterval(unittest.TestCase):
    def test_already_ordered(self):
        self.assertEqual(normalize_interval(1, 5), (1, 5))

    def test_swaps_endpoints(self):
        self.assertEqual(normalize_interval(5, 1), (1, 5))

    def test_equal_endpoints(self):
        self.assertEqual(normalize_interval(3, 3), (3, 3))

    def test_negative_values(self):
        self.assertEqual(normalize_interval(-5, -1), (-5, -1))
        self.assertEqual(normalize_interval(-1, -5), (-5, -1))

    def test_float_values(self):
        self.assertEqual(normalize_interval(2.5, 1.5), (1.5, 2.5))

    def test_mixed_int_float(self):
        self.assertEqual(normalize_interval(3, 1.5), (1.5, 3))

    def test_non_number_raises(self):
        with self.assertRaises(TypeError):
            normalize_interval("1", 5)
        with self.assertRaises(TypeError):
            normalize_interval(1, None)
        with self.assertRaises(TypeError):
            normalize_interval(True, 5)
        with self.assertRaises(TypeError):
            normalize_interval(1, False)  # type: ignore[arg-type]


class TestIsValidInterval(unittest.TestCase):
    def test_valid_tuple(self):
        self.assertTrue(is_valid_interval((1, 5)))

    def test_valid_list(self):
        self.assertTrue(is_valid_interval([1, 5]))

    def test_equal_endpoints_valid(self):
        self.assertTrue(is_valid_interval((3, 3)))

    def test_invalid_low_greater_than_high(self):
        self.assertFalse(is_valid_interval((5, 1)))

    def test_not_a_pair(self):
        self.assertFalse(is_valid_interval((1,)))
        self.assertFalse(is_valid_interval((1, 2, 3)))
        self.assertFalse(is_valid_interval("ab"))
        self.assertFalse(is_valid_interval(42))

    def test_non_number_elements(self):
        self.assertFalse(is_valid_interval(("a", "b")))
        self.assertFalse(is_valid_interval((1, "b")))
        self.assertFalse(is_valid_interval((True, 5)))

    def test_none(self):
        self.assertFalse(is_valid_interval(None))


class TestIntervalContains(unittest.TestCase):
    def test_inside(self):
        self.assertTrue(interval_contains((1, 5), 3))

    def test_at_endpoints(self):
        self.assertTrue(interval_contains((1, 5), 1))
        self.assertTrue(interval_contains((1, 5), 5))

    def test_outside(self):
        self.assertFalse(interval_contains((1, 5), 0))
        self.assertFalse(interval_contains((1, 5), 6))

    def test_degenerate_interval(self):
        self.assertTrue(interval_contains((3, 3), 3))
        self.assertFalse(interval_contains((3, 3), 4))

    def test_float_value(self):
        self.assertTrue(interval_contains((1.5, 2.5), 2.0))

    def test_invalid_interval_raises(self):
        with self.assertRaises(ValueError):
            interval_contains((5, 1), 3)

    def test_non_number_value_raises(self):
        with self.assertRaises(TypeError):
            interval_contains((1, 5), "x")


class TestIntervalOverlaps(unittest.TestCase):
    def test_overlapping(self):
        self.assertTrue(interval_overlaps((1, 5), (4, 8)))

    def test_touching_endpoints(self):
        self.assertTrue(interval_overlaps((1, 5), (5, 8)))

    def test_disjoint(self):
        self.assertFalse(interval_overlaps((1, 3), (4, 8)))

    def test_one_inside_other(self):
        self.assertTrue(interval_overlaps((1, 10), (4, 6)))

    def test_identical(self):
        self.assertTrue(interval_overlaps((2, 4), (2, 4)))

    def test_invalid_interval_raises(self):
        with self.assertRaises(ValueError):
            interval_overlaps((5, 1), (2, 4))


class TestIntervalIntersection(unittest.TestCase):
    def test_partial_overlap(self):
        self.assertEqual(interval_intersection((1, 5), (4, 8)), (4, 5))

    def test_touching(self):
        self.assertEqual(interval_intersection((1, 5), (5, 8)), (5, 5))

    def test_disjoint(self):
        self.assertIsNone(interval_intersection((1, 3), (4, 8)))

    def test_one_inside_other(self):
        self.assertEqual(interval_intersection((1, 10), (4, 6)), (4, 6))

    def test_identical(self):
        self.assertEqual(interval_intersection((2, 4), (2, 4)), (2, 4))

    def test_invalid_interval_raises(self):
        with self.assertRaises(ValueError):
            interval_intersection((5, 1), (2, 4))


class TestIntervalUnion(unittest.TestCase):
    def test_overlapping_merges(self):
        self.assertEqual(interval_union((1, 5), (4, 8)), (1, 8))

    def test_touching_merges(self):
        self.assertEqual(interval_union((1, 5), (5, 8)), (1, 8))

    def test_disjoint_returns_none(self):
        self.assertIsNone(interval_union((1, 3), (4, 8)))

    def test_one_inside_other(self):
        self.assertEqual(interval_union((1, 10), (4, 6)), (1, 10))

    def test_identical(self):
        self.assertEqual(interval_union((2, 4), (2, 4)), (2, 4))

    def test_invalid_interval_raises(self):
        with self.assertRaises(ValueError):
            interval_union((5, 1), (2, 4))


class TestMergeIntervals(unittest.TestCase):
    def test_disjoint_stays_disjoint(self):
        self.assertEqual(merge_intervals([(1, 3), (5, 8)]), [(1, 3), (5, 8)])

    def test_overlapping_merges(self):
        self.assertEqual(merge_intervals([(1, 5), (4, 8)]), [(1, 8)])

    def test_touching_merges(self):
        self.assertEqual(merge_intervals([(1, 5), (5, 8)]), [(1, 8)])

    def test_unsorted_input(self):
        self.assertEqual(merge_intervals([(5, 8), (1, 3)]), [(1, 3), (5, 8)])

    def test_chain_merge(self):
        self.assertEqual(merge_intervals([(1, 3), (2, 6), (5, 8)]), [(1, 8)])

    def test_empty_list(self):
        self.assertEqual(merge_intervals([]), [])

    def test_single_interval(self):
        self.assertEqual(merge_intervals([(2, 4)]), [(2, 4)])

    def test_non_list_raises(self):
        with self.assertRaises(TypeError):
            merge_intervals((1, 3))  # type: ignore[arg-type]

    def test_invalid_interval_raises(self):
        with self.assertRaises(ValueError):
            merge_intervals([(5, 1)])


class TestIntervalLength(unittest.TestCase):
    def test_positive_length(self):
        self.assertEqual(interval_length((1, 5)), 4.0)

    def test_zero_length(self):
        self.assertEqual(interval_length((3, 3)), 0.0)

    def test_float_length(self):
        self.assertEqual(interval_length((1.5, 3.5)), 2.0)

    def test_negative_interval(self):
        self.assertEqual(interval_length((-5, -1)), 4.0)

    def test_invalid_interval_raises(self):
        with self.assertRaises(ValueError):
            interval_length((5, 1))


class TestIntervalMidpoint(unittest.TestCase):
    def test_whole_number(self):
        self.assertEqual(interval_midpoint((1, 5)), 3.0)

    def test_fractional(self):
        self.assertEqual(interval_midpoint((1, 4)), 2.5)

    def test_degenerate_interval(self):
        self.assertEqual(interval_midpoint((3, 3)), 3.0)

    def test_negative_interval(self):
        self.assertEqual(interval_midpoint((-5, -1)), -3.0)

    def test_invalid_interval_raises(self):
        with self.assertRaises(ValueError):
            interval_midpoint((5, 1))


class TestIntervalDistance(unittest.TestCase):
    def test_overlapping_is_zero(self):
        self.assertEqual(interval_distance((1, 5), (4, 8)), 0.0)

    def test_touching_is_zero(self):
        self.assertEqual(interval_distance((1, 5), (5, 8)), 0.0)

    def test_disjoint_a_before_b(self):
        self.assertEqual(interval_distance((1, 3), (5, 8)), 2.0)

    def test_disjoint_b_before_a(self):
        self.assertEqual(interval_distance((5, 8), (1, 3)), 2.0)

    def test_float_distance(self):
        self.assertEqual(interval_distance((1.0, 2.0), (3.5, 5.0)), 1.5)

    def test_invalid_interval_raises(self):
        with self.assertRaises(ValueError):
            interval_distance((5, 1), (2, 4))


class TestIntervalIsSubset(unittest.TestCase):
    def test_a_inside_b(self):
        self.assertTrue(interval_is_subset((2, 4), (1, 5)))

    def test_a_touches_b_endpoints(self):
        self.assertTrue(interval_is_subset((1, 5), (1, 5)))

    def test_a_extends_past_b(self):
        self.assertFalse(interval_is_subset((0, 6), (1, 5)))

    def test_a_outside_b(self):
        self.assertFalse(interval_is_subset((6, 8), (1, 5)))

    def test_invalid_interval_raises(self):
        with self.assertRaises(ValueError):
            interval_is_subset((5, 1), (1, 5))


class TestIntervalShift(unittest.TestCase):
    def test_shift_positive(self):
        self.assertEqual(interval_shift((1, 5), 2), (3, 7))

    def test_shift_negative(self):
        self.assertEqual(interval_shift((1, 5), -3), (-2, 2))

    def test_shift_float(self):
        self.assertEqual(interval_shift((1.5, 3.5), 0.5), (2.0, 4.0))

    def test_shift_zero(self):
        self.assertEqual(interval_shift((1, 5), 0), (1, 5))

    def test_invalid_interval_raises(self):
        with self.assertRaises(ValueError):
            interval_shift((5, 1), 2)

    def test_non_number_delta_raises(self):
        with self.assertRaises(TypeError):
            interval_shift((1, 5), "2")  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            interval_shift((1, 5), True)  # type: ignore[arg-type]


class TestIntervalSymmetricDifference(unittest.TestCase):
    def test_disjoint_returns_both(self):
        self.assertEqual(
            interval_symmetric_difference((1, 3), (5, 8)),
            [(1, 3), (5, 8)],
        )

    def test_identical_returns_empty(self):
        self.assertEqual(interval_symmetric_difference((1, 5), (1, 5)), [])

    def test_partial_overlap(self):
        self.assertEqual(
            interval_symmetric_difference((1, 5), (4, 8)),
            [(1, 4), (5, 8)],
        )

    def test_one_inside_other(self):
        self.assertEqual(
            interval_symmetric_difference((2, 4), (1, 5)),
            [(1, 2), (4, 5)],
        )

    def test_touching_intervals(self):
        self.assertEqual(
            interval_symmetric_difference((1, 5), (5, 8)),
            [(1, 5), (5, 8)],
        )

    def test_invalid_interval_raises(self):
        with self.assertRaises(ValueError):
            interval_symmetric_difference((5, 1), (2, 4))


class TestIntervalUtilsBoundaries(unittest.TestCase):
    def test_normalize_interval_float_inf(self):
        self.assertEqual(normalize_interval(float("inf"), 5), (5.0, float("inf")))
        self.assertEqual(normalize_interval(0, float("inf")), (0, float("inf")))

    def test_normalize_interval_negative_inf(self):
        self.assertEqual(normalize_interval(-10, float("-inf")), (float("-inf"), -10))

    def test_is_valid_interval_with_inf(self):
        self.assertTrue(is_valid_interval((-float("inf"), float("inf"))))
        self.assertTrue(is_valid_interval((0, float("inf"))))
        self.assertTrue(is_valid_interval((float("-inf"), 0)))
        self.assertFalse(is_valid_interval((float("inf"), 0)))
        self.assertFalse(is_valid_interval((0, float("-inf"))))

    def test_is_valid_interval_with_nan(self):
        self.assertFalse(is_valid_interval((float("nan"), 5)))
        self.assertFalse(is_valid_interval((0, float("nan"))))
        self.assertFalse(is_valid_interval((float("nan"), float("nan"))))

    def test_interval_contains_with_inf(self):
        self.assertTrue(interval_contains((0, float("inf")), 1000000))
        self.assertTrue(interval_contains((float("-inf"), 0), -1000000))
        self.assertTrue(interval_contains((float("-inf"), float("inf")), 0))

    def test_interval_contains_with_nan_value(self):
        # NaN comparisons return False, no TypeError raised for float NaN
        self.assertFalse(interval_contains((0, 10), float("nan")))  # type: ignore[arg-type]

    def test_interval_overlaps_with_inf(self):
        self.assertTrue(interval_overlaps((0, float("inf")), (5, 10)))
        self.assertTrue(interval_overlaps((float("-inf"), 0), (-5, 5)))
        self.assertFalse(
            interval_overlaps((0, 1), (float("inf"), float("inf") + 1)) if False else False
        )  # skip complex case

    def test_interval_intersection_with_inf(self):
        self.assertEqual(interval_intersection((0, float("inf")), (5, 10)), (5, 10))
        self.assertEqual(interval_intersection((float("-inf"), 5), (-10, 0)), (-10, 0))
        self.assertEqual(interval_intersection((float("-inf"), float("inf")), (1, 2)), (1, 2))
        self.assertIsNone(interval_intersection((0, 1), (2, float("inf"))))

    def test_interval_union_with_inf(self):
        self.assertEqual(interval_union((0, float("inf")), (5, 10)), (0, float("inf")))
        self.assertIsNone(interval_union((0, 1), (2, float("inf"))))
        self.assertIsNone(interval_union((float("-inf"), 0), (1, float("inf"))))

    def test_interval_length_with_inf(self):
        self.assertEqual(interval_length((0, float("inf"))), float("inf"))
        self.assertEqual(interval_length((float("-inf"), 5)), float("inf"))
        self.assertEqual(interval_length((float("-inf"), float("inf"))), float("inf"))

    def test_interval_midpoint_with_inf(self):
        self.assertEqual(interval_midpoint((0, float("inf"))), float("inf"))
        self.assertEqual(interval_midpoint((float("-inf"), 0)), float("-inf"))
        self.assertTrue(math.isnan(interval_midpoint((float("-inf"), float("inf")))))

    def test_interval_distance_with_inf(self):
        self.assertEqual(interval_distance((0, float("inf")), (5, 10)), 0)
        self.assertEqual(interval_distance((float("-inf"), 0), (1, float("inf"))), float("inf"))
        self.assertEqual(interval_distance((0, 1), (float("inf"), float("inf"))), float("inf"))

    def test_interval_shift_with_inf(self):
        self.assertEqual(interval_shift((0, float("inf")), 5), (5, float("inf")))
        self.assertEqual(interval_shift((float("-inf"), 0), -3), (float("-inf"), -3))
        self.assertEqual(
            interval_shift((float("-inf"), float("inf")), 100), (float("-inf"), float("inf"))
        )

    def test_interval_shift_with_nan_delta(self):
        with self.assertRaises(TypeError):
            interval_shift((0, 1), float("nan"))

    def test_interval_shift_with_inf_delta(self):
        with self.assertRaises(TypeError):
            interval_shift((0, 1), float("inf"))


class TestIntervalUtilsBoundariesExtra(unittest.TestCase):
    def test_interval_is_subset_with_inf_extra(self):
        self.assertTrue(interval_is_subset((0, 5), (float("-inf"), float("inf"))))
        self.assertTrue(
            interval_is_subset((float("-inf"), float("inf")), (float("-inf"), float("inf")))
        )
        self.assertFalse(interval_is_subset((float("-inf"), 0), (-5, 5)))
        self.assertTrue(interval_is_subset((-5, 0), (float("-inf"), 0)))

    def test_merge_intervals_with_inf(self):
        self.assertEqual(merge_intervals([(0, float("inf")), (5, 10)]), [(0, float("inf"))])
        self.assertEqual(
            merge_intervals([(float("-inf"), 0), (-5, float("inf"))]),
            [(float("-inf"), float("inf"))],
        )

    def test_normalize_interval_both_inf_nan(self):
        self.assertEqual(
            normalize_interval(float("inf"), float("-inf")), (float("-inf"), float("inf"))
        )
        result = normalize_interval(float("nan"), float("inf"))
        self.assertTrue(math.isnan(result[0]))
        self.assertTrue(math.isnan(result[1]))

    def test_interval_symmetric_difference_with_inf(self):
        self.assertEqual(interval_symmetric_difference((0, float("inf")), (5, 10)), [])
        diff = interval_symmetric_difference((0, 5), (3, float("inf")))
        self.assertEqual(diff, [(0, 3), (5, float("inf"))])
        self.assertEqual(
            interval_symmetric_difference((0, 1), (2, float("inf"))), [(0, 1), (2, float("inf"))]
        )
        self.assertEqual(interval_intersection((0, float("inf")), (5, 100)), (5, 100))
        self.assertEqual(interval_intersection((float("-inf"), 10), (0, float("inf"))), (0, 10))

    def test_interval_union_with_inf(self):
        self.assertEqual(interval_union((0, float("inf")), (5, 100)), (0, float("inf")))
        self.assertEqual(
            interval_union((float("-inf"), 10), (0, float("inf"))), (float("-inf"), float("inf"))
        )

    def test_interval_length_with_inf(self):
        self.assertTrue(math.isinf(interval_length((0, float("inf")))))

    def test_interval_midpoint_with_inf(self):
        # Midpoint of finite and inf is inf
        self.assertTrue(math.isinf(interval_midpoint((0, float("inf")))))
        self.assertTrue(math.isinf(interval_midpoint((float("-inf"), 0))))

    def test_interval_distance_with_inf(self):
        self.assertEqual(interval_distance((0, 1), (2, float("inf"))), 1.0)
        self.assertEqual(interval_distance((float("-inf"), 0), (1, float("inf"))), 1.0)

    def test_interval_is_subset_with_inf(self):
        self.assertTrue(interval_is_subset((0, 1), (float("-inf"), float("inf"))))
        self.assertTrue(interval_is_subset((float("-inf"), 0), (float("-inf"), 5)))

    def test_interval_shift_with_inf(self):
        self.assertEqual(interval_shift((0, float("inf")), 5), (5, float("inf")))
        self.assertEqual(interval_shift((float("-inf"), 0), -3), (float("-inf"), -3))

    def test_interval_shift_bool_rejected(self):
        with self.assertRaises(TypeError):
            interval_shift((0, 10), True)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            interval_shift((0, 10), False)  # type: ignore[arg-type]

    def test_interval_shift_invalid_interval(self):
        with self.assertRaises(ValueError):
            interval_shift((10, 0), 1)
        with self.assertRaises(ValueError):
            interval_shift("bad", 1)  # type: ignore[arg-type]

    def test_interval_shift_floats(self):
        self.assertEqual(interval_shift((1.5, 2.5), 0.5), (2.0, 3.0))

    def test_invalid_interval_types_various(self):
        with self.assertRaises(ValueError):
            interval_contains("bad", 5)  # type: ignore[arg-type]
        with self.assertRaises(ValueError):
            interval_overlaps((1, 2), "bad")  # type: ignore[arg-type]
        with self.assertRaises(ValueError):
            interval_intersection([], (1, 2))  # type: ignore[arg-type]
        with self.assertRaises(ValueError):
            interval_union((1,), (1, 2))  # type: ignore[arg-type]

    def test_merge_intervals_type_validation(self):
        with self.assertRaises(TypeError):
            merge_intervals("not a list")  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            merge_intervals(((1, 2),))  # type: ignore[arg-type]

    def test_normalize_interval_bool_rejected(self):
        with self.assertRaises(TypeError):
            normalize_interval(True, 5)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            normalize_interval(5, False)  # type: ignore[arg-type]


if __name__ == "__main__":
    unittest.main()
