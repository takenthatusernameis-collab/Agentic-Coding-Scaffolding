"""Tests for stats module."""

import unittest

from stats import (
    max_value,
    mean,
    median,
    median_absolute_deviation,
    midrange,
    min_value,
    mode,
    stddev,
    variance,
)


class TestMinValue(unittest.TestCase):
    def test_min_basic(self) -> None:
        self.assertEqual(min_value([3, 1, 2]), 1)

    def test_min_negative(self) -> None:
        self.assertEqual(min_value([-1, 0, 1]), -1)

    def test_min_single(self) -> None:
        self.assertEqual(min_value([5]), 5)

    def test_min_empty_raises(self) -> None:
        with self.assertRaises(ValueError):
            min_value([])


class TestMaxValue(unittest.TestCase):
    def test_max_basic(self) -> None:
        self.assertEqual(max_value([1, 3, 2]), 3)

    def test_max_negative(self) -> None:
        self.assertEqual(max_value([-1, 0, 1]), 1)

    def test_max_single(self) -> None:
        self.assertEqual(max_value([5]), 5)

    def test_max_empty_raises(self) -> None:
        with self.assertRaises(ValueError):
            max_value([])


class TestMidrange(unittest.TestCase):
    def test_midrange_basic(self) -> None:
        self.assertEqual(midrange([1, 2, 3, 4, 5]), 3.0)

    def test_midrange_even(self) -> None:
        self.assertEqual(midrange([1, 9]), 5.0)

    def test_midrange_single(self) -> None:
        self.assertEqual(midrange([5]), 5.0)

    def test_midrange_negative(self) -> None:
        self.assertEqual(midrange([-2, 4]), 1.0)

    def test_midrange_unsorted(self) -> None:
        self.assertEqual(midrange([9, 1, 5]), 5.0)

    def test_midrange_empty_raises(self) -> None:
        with self.assertRaises(ValueError):
            midrange([])

    def test_midrange_rejects_non_list(self) -> None:
        with self.assertRaises(TypeError):
            midrange((1, 2, 3))  # type: ignore[arg-type]

    def test_midrange_rejects_non_numeric(self) -> None:
        numbers: list[object] = [1, "a", 3]
        with self.assertRaises(TypeError):
            midrange(numbers)  # type: ignore[type-var]

    def test_midrange_rejects_bool(self) -> None:
        with self.assertRaises(TypeError):
            midrange([True, 1, 2])  # type: ignore[type-var]


class TestMean(unittest.TestCase):
    def test_mean_basic(self) -> None:
        self.assertEqual(mean([1, 2, 3, 4, 5]), 3.0)

    def test_mean_even(self) -> None:
        self.assertEqual(mean([1, 3]), 2.0)

    def test_mean_single(self) -> None:
        self.assertEqual(mean([5]), 5.0)

    def test_mean_negative(self) -> None:
        self.assertEqual(mean([-1, 0, 1]), 0.0)

    def test_mean_empty_raises(self) -> None:
        with self.assertRaises(ValueError):
            mean([])


class TestMedian(unittest.TestCase):
    def test_median_odd(self) -> None:
        self.assertEqual(median([1, 2, 3, 4, 5]), 3.0)

    def test_median_even(self) -> None:
        self.assertEqual(median([1, 2, 3, 4]), 2.5)

    def test_median_single(self) -> None:
        self.assertEqual(median([5]), 5.0)

    def test_median_unsorted(self) -> None:
        self.assertEqual(median([5, 1, 3]), 3.0)

    def test_median_empty_raises(self) -> None:
        with self.assertRaises(ValueError):
            median([])


class TestMode(unittest.TestCase):
    def test_mode_basic(self) -> None:
        self.assertEqual(mode([1, 2, 2, 3, 4]), 2)

    def test_mode_all_same(self) -> None:
        self.assertEqual(mode([7, 7, 7]), 7)

    def test_mode_bimodal_returns_first_in_sorted_order(self) -> None:
        self.assertEqual(mode([1, 1, 2, 2]), 1)

    def test_mode_single(self) -> None:
        self.assertEqual(mode([5]), 5)

    def test_mode_empty_raises(self) -> None:
        with self.assertRaises(ValueError):
            mode([])


class TestVariance(unittest.TestCase):
    def test_variance_population_basic(self) -> None:
        result = variance([1, 2, 3, 4, 5])
        self.assertAlmostEqual(result, 2.0, places=5)

    def test_variance_population_single(self) -> None:
        self.assertAlmostEqual(variance([5]), 0.0, places=5)

    def test_variance_sample(self) -> None:
        result = variance([1, 2, 3, 4, 5], population=False)
        self.assertAlmostEqual(result, 2.5, places=5)

    def test_variance_sample_requires_two_elements(self) -> None:
        with self.assertRaises(ValueError):
            variance([5], population=False)

    def test_variance_empty_raises(self) -> None:
        with self.assertRaises(ValueError):
            variance([])


class TestStddev(unittest.TestCase):
    def test_stddev_population_basic(self) -> None:
        result = stddev([1, 2, 3, 4, 5])
        self.assertAlmostEqual(result, 1.4142135623730951, places=5)

    def test_stddev_population_single(self) -> None:
        self.assertAlmostEqual(stddev([5]), 0.0, places=5)

    def test_stddev_sample(self) -> None:
        result = stddev([1, 2, 3, 4, 5], population=False)
        self.assertAlmostEqual(result, 1.5811388300841898, places=5)

    def test_stddev_empty_raises(self) -> None:
        with self.assertRaises(ValueError):
            stddev([])


class TestMedianAbsoluteDeviation(unittest.TestCase):
    def test_mad_basic(self) -> None:
        self.assertEqual(median_absolute_deviation([1, 2, 3]), 1.0)

    def test_mad_all_equal(self) -> None:
        self.assertEqual(median_absolute_deviation([2, 2, 2, 2]), 0.0)

    def test_mad_single_element(self) -> None:
        self.assertEqual(median_absolute_deviation([5]), 0.0)

    def test_mad_negative_values(self) -> None:
        self.assertEqual(median_absolute_deviation([-3, -1, 0, 1, 3]), 1.0)

    def test_mad_mixed_int_float(self) -> None:
        self.assertEqual(median_absolute_deviation([1, 2.5, 4]), 1.5)

    def test_mad_empty_raises(self) -> None:
        with self.assertRaises(ValueError):
            median_absolute_deviation([])

    def test_mad_rejects_non_list(self) -> None:
        with self.assertRaises(TypeError):
            median_absolute_deviation((1, 2, 3))  # type: ignore[arg-type]

    def test_mad_rejects_non_numeric(self) -> None:
        numbers: list[object] = [1, "a", 3]
        with self.assertRaises(TypeError):
            median_absolute_deviation(numbers)  # type: ignore[type-var]

    def test_mad_rejects_bool(self) -> None:
        with self.assertRaises(TypeError):
            median_absolute_deviation([True, 1, 2])  # type: ignore[type-var]


if __name__ == "__main__":
    unittest.main()
