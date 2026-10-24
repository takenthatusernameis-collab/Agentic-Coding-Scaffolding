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


if __name__ == "__main__":
    unittest.main()
