"""Tests for stats module."""

import unittest

from stats import (
    correlation,
    covariance,
    kurtosis,
    max_value,
    mean,
    median,
    median_absolute_deviation,
    midrange,
    min_value,
    mode,
    multimode,
    skewness,
    stddev,
    sum_of_squares,
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


class TestSkewness(unittest.TestCase):
    def test_symmetric_returns_zero(self) -> None:
        self.assertEqual(skewness([1, 2, 3]), 0.0)

    def test_positive_skew(self) -> None:
        self.assertEqual(skewness([1, 1, 1, 1, 10]), 1.5)

    def test_single_element_raises(self) -> None:
        with self.assertRaises(ValueError):
            skewness([5])

    def test_two_elements_raise(self) -> None:
        with self.assertRaises(ValueError):
            skewness([1, 2])

    def test_empty_raises(self) -> None:
        with self.assertRaises(ValueError):
            skewness([])

    def test_zero_stddev_raises(self) -> None:
        with self.assertRaises(ValueError):
            skewness([7, 7, 7])

    def test_rejects_non_list(self) -> None:
        with self.assertRaises(TypeError):
            skewness((1, 2, 3))  # type: ignore[arg-type]

    def test_rejects_non_numeric(self) -> None:
        numbers: list[object] = [1, "a", 3]
        with self.assertRaises(TypeError):
            skewness(numbers)  # type: ignore[type-var]

    def test_rejects_bool(self) -> None:
        with self.assertRaises(TypeError):
            skewness([True, 1, 2])  # type: ignore[type-var]


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


class TestInterquartileRange(unittest.TestCase):
    def test_basic(self) -> None:
        from stats import interquartile_range

        self.assertAlmostEqual(interquartile_range([1, 2, 3, 4, 5]), 2.0)

    def test_alias_matches_iqr(self) -> None:
        from stats import interquartile_range, iqr

        data = [1, 2, 3, 4, 5, 6]
        self.assertAlmostEqual(interquartile_range(data), iqr(data))  # type: ignore[arg-type]


class TestWeightedMean(unittest.TestCase):
    def test_basic(self) -> None:
        from stats import weighted_mean

        self.assertAlmostEqual(weighted_mean([1, 2, 3], [1, 1, 1]), 2.0)
        self.assertAlmostEqual(weighted_mean([10, 20], [1, 3]), 17.5)

    def test_empty_raises(self) -> None:
        from stats import weighted_mean

        with self.assertRaises(ValueError):
            weighted_mean([], [])

    def test_length_mismatch_raises(self) -> None:
        from stats import weighted_mean

        with self.assertRaises(ValueError):
            weighted_mean([1, 2], [1])

    def test_non_positive_weight_raises(self) -> None:
        from stats import weighted_mean

        with self.assertRaises(ValueError):
            weighted_mean([1, 2], [0, 1])
        with self.assertRaises(ValueError):
            weighted_mean([1, 2], [-1, 1])

    def test_rejects_non_numeric(self) -> None:
        from stats import weighted_mean

        with self.assertRaises(TypeError):
            weighted_mean([1, "a"], [1, 1])  # type: ignore[type-var,misc]
        with self.assertRaises(TypeError):
            weighted_mean([1, 2], [1, "a"])  # type: ignore[type-var,misc]

    def test_rejects_bool(self) -> None:
        from stats import weighted_mean

        with self.assertRaises(TypeError):
            weighted_mean([True, 1], [1, 1])  # type: ignore[type-var]


class TestSumOfSquares(unittest.TestCase):
    def test_basic(self) -> None:
        self.assertEqual(sum_of_squares([1, 2, 3]), 14.0)

    def test_single(self) -> None:
        self.assertEqual(sum_of_squares([5]), 25.0)

    def test_empty_raises(self) -> None:
        with self.assertRaises(ValueError):
            sum_of_squares([])

    def test_rejects_non_list(self) -> None:
        with self.assertRaises(TypeError):
            sum_of_squares((1, 2, 3))  # type: ignore[arg-type]

    def test_rejects_non_numeric(self) -> None:
        numbers: list[object] = [1, "a", 3]
        with self.assertRaises(TypeError):
            sum_of_squares(numbers)  # type: ignore[type-var]

    def test_rejects_bool(self) -> None:
        with self.assertRaises(TypeError):
            sum_of_squares([True, 1, 2])  # type: ignore[type-var]


class TestKurtosis(unittest.TestCase):
    def test_normal_like(self) -> None:
        self.assertAlmostEqual(kurtosis([1, 2, 3, 4, 5, 6, 7, 8]), -1.2, places=1)

    def test_too_few(self) -> None:
        with self.assertRaises(ValueError):
            kurtosis([1, 2, 3])

    def test_zero_std(self) -> None:
        with self.assertRaises(ValueError):
            kurtosis([5, 5, 5, 5])

    def test_non_list(self) -> None:
        with self.assertRaises(TypeError):
            kurtosis("abc")  # type: ignore[arg-type]

    def test_non_number(self) -> None:
        with self.assertRaises(TypeError):
            kurtosis([1, 2, "x", 4])  # type: ignore[list-item, type-var]

    def test_bool(self) -> None:
        from stats import kurtosis

        with self.assertRaises(TypeError):
            kurtosis([True, 1, 2, 3])  # type: ignore[type-var]


class TestCovariance(unittest.TestCase):
    def test_population_positive(self) -> None:
        # x and y increase together -> positive covariance
        self.assertAlmostEqual(covariance([1, 2, 3, 4], [2, 4, 6, 8]), 2.5)

    def test_population_negative(self) -> None:
        # x increases while y decreases -> negative covariance
        self.assertAlmostEqual(covariance([1, 2, 3, 4], [8, 6, 4, 2]), -2.5)

    def test_population_zero(self) -> None:
        # y is constant -> covariance is 0
        self.assertEqual(covariance([1, 2, 3], [5, 5, 5]), 0.0)

    def test_sample_divides_by_n_minus_one(self) -> None:
        self.assertAlmostEqual(covariance([1, 2, 3, 4], [2, 4, 6, 8], population=False), 10.0 / 3)

    def test_single_element_sample_raises(self) -> None:
        with self.assertRaises(ValueError):
            covariance([1], [2], population=False)

    def test_length_mismatch_raises(self) -> None:
        with self.assertRaises(ValueError):
            covariance([1, 2], [1, 2, 3])

    def test_empty_raises(self) -> None:
        with self.assertRaises(ValueError):
            covariance([], [])

    def test_rejects_non_list(self) -> None:
        with self.assertRaises(TypeError):
            covariance((1, 2), [1, 2])  # type: ignore[arg-type]

    def test_rejects_non_numeric(self) -> None:
        with self.assertRaises(TypeError):
            covariance([1, 2], [1, "a"])  # type: ignore[misc]

    def test_rejects_bool(self) -> None:
        with self.assertRaises(TypeError):
            covariance([True, 1], [1, 2])  # type: ignore[type-var]

    def test_rejects_non_bool_population(self) -> None:
        with self.assertRaises(TypeError):
            covariance([1, 2], [1, 2], population="yes")  # type: ignore[arg-type]


class TestCorrelation(unittest.TestCase):
    def test_perfect_positive(self) -> None:
        self.assertAlmostEqual(correlation([1, 2, 3, 4], [2, 4, 6, 8]), 1.0)

    def test_perfect_negative(self) -> None:
        self.assertAlmostEqual(correlation([1, 2, 3, 4], [8, 6, 4, 2]), -1.0)

    def test_no_linear_relationship(self) -> None:
        # y constant -> zero std dev -> ValueError
        with self.assertRaises(ValueError):
            correlation([1, 2, 3], [5, 5, 5])

    def test_zero_std_x_raises(self) -> None:
        with self.assertRaises(ValueError):
            correlation([5, 5, 5], [1, 2, 3])

    def test_moderate_positive(self) -> None:
        # classic example from statistics textbooks
        self.assertAlmostEqual(correlation([1, 2, 3, 4, 5], [2, 4, 5, 4, 5]), 0.8, places=1)

    def test_length_mismatch_raises(self) -> None:
        with self.assertRaises(ValueError):
            correlation([1, 2], [1, 2, 3])

    def test_single_element_raises(self) -> None:
        with self.assertRaises(ValueError):
            correlation([1], [2])

    def test_empty_raises(self) -> None:
        with self.assertRaises(ValueError):
            correlation([], [])

    def test_rejects_non_list(self) -> None:
        with self.assertRaises(TypeError):
            correlation((1, 2), [1, 2])  # type: ignore[arg-type]

    def test_rejects_non_numeric(self) -> None:
        with self.assertRaises(TypeError):
            correlation([1, 2], [1, "a"])  # type: ignore[misc]

    def test_rejects_bool(self) -> None:
        with self.assertRaises(TypeError):
            correlation([True, 1], [1, 2])  # type: ignore[type-var]


class TestMultimode(unittest.TestCase):
    def test_single_mode(self) -> None:
        self.assertEqual(multimode([1, 2, 2, 3]), [2.0])

    def test_multiple_modes(self) -> None:
        self.assertEqual(multimode([1, 1, 2, 2, 3]), [1.0, 2.0])

    def test_all_unique(self) -> None:
        self.assertEqual(multimode([1, 2, 3]), [1.0, 2.0, 3.0])

    def test_order_of_first_appearance(self) -> None:
        self.assertEqual(multimode([3, 1, 3, 2, 2]), [3.0, 2.0])

    def test_single_element(self) -> None:
        self.assertEqual(multimode([5]), [5.0])

    def test_negative_values(self) -> None:
        self.assertEqual(multimode([-1, -1, 0]), [-1.0])

    def test_float_values(self) -> None:
        self.assertEqual(multimode([1.5, 2.5, 1.5]), [1.5])

    def test_empty_raises(self) -> None:
        with self.assertRaises(ValueError):
            multimode([])

    def test_rejects_non_list(self) -> None:
        with self.assertRaises(TypeError):
            multimode((1, 2, 2))  # type: ignore[arg-type]

    def test_rejects_non_numeric(self) -> None:
        with self.assertRaises(TypeError):
            multimode([1, 2, "a"])  # type: ignore[type-var]

    def test_rejects_bool(self) -> None:
        with self.assertRaises(TypeError):
            multimode([True, 1])  # type: ignore[type-var]


if __name__ == "__main__":
    unittest.main()
