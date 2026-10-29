"""Tests for stats module."""

import math
import unittest

from stats import (
    coefficient_of_variation,
    correlation,
    covariance,
    geometric_mean,
    harmonic_mean,
    kurtosis,
    max_value,
    mean,
    mean_absolute_deviation,
    median,
    median_absolute_deviation,
    midhinge,
    midrange,
    min_value,
    mode,
    multimode,
    moving_average,
    product,
    range,
    root_mean_square,
    skewness,
    standard_error,
    stddev,
    sum_of_cubes,
    sum_of_squares,
    sum_values,
    trimmed_mean,
    variance,
    z_scores,
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


class TestRange(unittest.TestCase):
    def test_basic(self) -> None:
        self.assertEqual(range([1, 2, 3, 4, 5]), 4.0)

    def test_single(self) -> None:
        self.assertEqual(range([5]), 0.0)

    def test_negative(self) -> None:
        self.assertEqual(range([-2, 4]), 6.0)

    def test_unsorted(self) -> None:
        self.assertEqual(range([9, 1, 5]), 8.0)

    def test_empty_raises(self) -> None:
        with self.assertRaises(ValueError):
            range([])

    def test_rejects_non_list(self) -> None:
        with self.assertRaises(TypeError):
            range((1, 2, 3))  # type: ignore[arg-type]

    def test_rejects_non_numeric(self) -> None:
        numbers: list[object] = [1, "a", 3]
        with self.assertRaises(TypeError):
            range(numbers)  # type: ignore[type-var]

    def test_rejects_bool(self) -> None:
        with self.assertRaises(TypeError):
            range([True, 1, 2])  # type: ignore[type-var]


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


class TestMeanAbsoluteDeviation(unittest.TestCase):
    def test_basic(self) -> None:
        self.assertAlmostEqual(mean_absolute_deviation([1, 2, 3, 4, 5]), 1.2)

    def test_constant(self) -> None:
        self.assertEqual(mean_absolute_deviation([2, 2, 2]), 0.0)

    def test_empty_raises(self) -> None:
        with self.assertRaises(ValueError):
            mean_absolute_deviation([])

    def test_rejects_non_list(self) -> None:
        with self.assertRaises(TypeError):
            mean_absolute_deviation((1, 2))  # type: ignore[arg-type]

    def test_rejects_non_numeric(self) -> None:
        with self.assertRaises(TypeError):
            mean_absolute_deviation([1, "a"])  # type: ignore[type-var]

    def test_rejects_bool(self) -> None:
        with self.assertRaises(TypeError):
            mean_absolute_deviation([True, 1])  # type: ignore[list-item]


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


class TestTrimean(unittest.TestCase):
    def test_basic(self) -> None:
        from stats import trimean

        self.assertAlmostEqual(trimean([1, 2, 3, 4, 5]), 3.0)
        self.assertAlmostEqual(trimean([1, 2, 3, 4, 5, 6]), 3.5)

    def test_empty_raises(self) -> None:
        from stats import trimean

        with self.assertRaises(ValueError):
            trimean([])

    def test_rejects_non_list(self) -> None:
        from stats import trimean

        with self.assertRaises(TypeError):
            trimean((1, 2, 3))  # type: ignore[arg-type]

    def test_rejects_non_numeric(self) -> None:
        from stats import trimean

        with self.assertRaises(TypeError):
            trimean([1, 2, "a"])  # type: ignore[type-var]

    def test_rejects_bool(self) -> None:
        from stats import trimean

        with self.assertRaises(TypeError):
            trimean([True, 1, 2])  # type: ignore[type-var]


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


class TestSumValues(unittest.TestCase):
    def test_basic(self) -> None:
        self.assertEqual(sum_values([1, 2, 3, 4, 5]), 15.0)

    def test_single(self) -> None:
        self.assertEqual(sum_values([5]), 5.0)

    def test_negative(self) -> None:
        self.assertEqual(sum_values([-1, 0, 1]), 0.0)

    def test_floats(self) -> None:
        self.assertAlmostEqual(sum_values([0.5, 0.25, 0.25]), 1.0)

    def test_empty_raises(self) -> None:
        with self.assertRaises(ValueError):
            sum_values([])

    def test_rejects_non_list(self) -> None:
        with self.assertRaises(TypeError):
            sum_values((1, 2, 3))  # type: ignore[arg-type]

    def test_rejects_non_numeric(self) -> None:
        numbers: list[object] = [1, "a", 3]
        with self.assertRaises(TypeError):
            sum_values(numbers)  # type: ignore[type-var]

    def test_rejects_bool(self) -> None:
        with self.assertRaises(TypeError):
            sum_values([True, 1, 2])  # type: ignore[type-var]


class TestSumOfCubes(unittest.TestCase):
    def test_basic(self) -> None:
        self.assertEqual(sum_of_cubes([1, 2, 3]), 36.0)

    def test_single(self) -> None:
        self.assertEqual(sum_of_cubes([5]), 125.0)

    def test_negative(self) -> None:
        self.assertEqual(sum_of_cubes([-1, 1]), 0.0)

    def test_zero(self) -> None:
        self.assertEqual(sum_of_cubes([0, 0, 0]), 0.0)

    def test_empty_raises(self) -> None:
        with self.assertRaises(ValueError):
            sum_of_cubes([])

    def test_rejects_non_list(self) -> None:
        with self.assertRaises(TypeError):
            sum_of_cubes((1, 2, 3))  # type: ignore[arg-type]

    def test_rejects_non_numeric(self) -> None:
        numbers: list[object] = [1, "a", 3]
        with self.assertRaises(TypeError):
            sum_of_cubes(numbers)  # type: ignore[type-var]

    def test_rejects_bool(self) -> None:
        with self.assertRaises(TypeError):
            sum_of_cubes([True, 1, 2])  # type: ignore[type-var]


class TestCoefficientOfVariation(unittest.TestCase):
    def test_basic(self) -> None:
        # stddev(2,2,2,2)=0? no, use [1,2,3,4,5]: mean 3, pop std ~1.414
        self.assertAlmostEqual(
            coefficient_of_variation([1, 2, 3, 4, 5]), 1.4142135 / 3.0, places=6
        )

    def test_population_false(self) -> None:
        self.assertAlmostEqual(
            coefficient_of_variation([1, 2, 3, 4, 5], population=False),
            1.5811388 / 3.0,
            places=6,
        )

    def test_constant_mean_zero_raises(self) -> None:
        with self.assertRaises(ValueError):
            coefficient_of_variation([0, 0, 0])

    def test_empty_raises(self) -> None:
        with self.assertRaises(ValueError):
            coefficient_of_variation([])

    def test_rejects_non_list(self) -> None:
        with self.assertRaises(TypeError):
            coefficient_of_variation((1, 2, 3))  # type: ignore[arg-type]

    def test_rejects_non_numeric(self) -> None:
        numbers: list[object] = [1, "a", 3]
        with self.assertRaises(TypeError):
            coefficient_of_variation(numbers)  # type: ignore[type-var]

    def test_rejects_bool(self) -> None:
        with self.assertRaises(TypeError):
            coefficient_of_variation([True, 1, 2])  # type: ignore[type-var]


class TestGeometricMean(unittest.TestCase):
    def test_basic(self) -> None:
        self.assertAlmostEqual(geometric_mean([1, 2, 3, 4, 5]), 2.605171, places=6)

    def test_single(self) -> None:
        self.assertEqual(geometric_mean([5]), 5.0)

    def test_all_ones(self) -> None:
        self.assertEqual(geometric_mean([1, 1, 1]), 1.0)

    def test_empty_raises(self) -> None:
        with self.assertRaises(ValueError):
            geometric_mean([])

    def test_non_positive_raises(self) -> None:
        with self.assertRaises(ValueError):
            geometric_mean([1, -2, 3])
        with self.assertRaises(ValueError):
            geometric_mean([1, 0, 3])

    def test_rejects_non_list(self) -> None:
        with self.assertRaises(TypeError):
            geometric_mean((1, 2, 3))  # type: ignore[arg-type]

    def test_rejects_non_numeric(self) -> None:
        numbers: list[object] = [1, "a", 3]
        with self.assertRaises(TypeError):
            geometric_mean(numbers)  # type: ignore[type-var]

    def test_rejects_bool(self) -> None:
        with self.assertRaises(TypeError):
            geometric_mean([True, 1, 2])  # type: ignore[type-var]


class TestHarmonicMean(unittest.TestCase):
    def test_basic(self) -> None:
        self.assertAlmostEqual(harmonic_mean([1, 2, 3, 4, 5]), 2.189781, places=6)

    def test_single(self) -> None:
        self.assertEqual(harmonic_mean([5]), 5.0)

    def test_all_ones(self) -> None:
        self.assertEqual(harmonic_mean([1, 1, 1]), 1.0)

    def test_empty_raises(self) -> None:
        with self.assertRaises(ValueError):
            harmonic_mean([])

    def test_non_positive_raises(self) -> None:
        with self.assertRaises(ValueError):
            harmonic_mean([1, -2, 3])
        with self.assertRaises(ValueError):
            harmonic_mean([1, 0, 3])

    def test_rejects_non_list(self) -> None:
        with self.assertRaises(TypeError):
            harmonic_mean((1, 2, 3))  # type: ignore[arg-type]

    def test_rejects_non_numeric(self) -> None:
        numbers: list[object] = [1, "a", 3]
        with self.assertRaises(TypeError):
            harmonic_mean(numbers)  # type: ignore[type-var]

    def test_rejects_bool(self) -> None:
        with self.assertRaises(TypeError):
            harmonic_mean([True, 1, 2])  # type: ignore[type-var]


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


class TestTrimmedMean(unittest.TestCase):
    def test_default_is_mean(self) -> None:
        self.assertEqual(trimmed_mean([1, 2, 3, 4, 5]), 3.0)

    def test_trim_one_from_each_end(self) -> None:
        self.assertEqual(trimmed_mean([1, 2, 3, 4, 5], trim_count=1), 3.0)

    def test_trim_even_list(self) -> None:
        self.assertEqual(trimmed_mean([1, 2, 3, 4, 5, 6], trim_count=1), 3.5)

    def test_trim_two_from_each_end(self) -> None:
        self.assertEqual(
            trimmed_mean([1, 2, 3, 4, 5, 6, 7, 8], trim_count=2),
            4.5,
        )

    def test_unsorted_input(self) -> None:
        self.assertEqual(trimmed_mean([9, 1, 5, 2, 8], trim_count=1), 5.0)

    def test_single_element(self) -> None:
        self.assertEqual(trimmed_mean([7]), 7.0)

    def test_negative_values(self) -> None:
        self.assertEqual(trimmed_mean([-3, -1, 0, 1, 3], trim_count=1), 0.0)

    def test_float_values(self) -> None:
        self.assertAlmostEqual(trimmed_mean([1.0, 2.0, 100.0], trim_count=1), 2.0)

    def test_empty_raises(self) -> None:
        with self.assertRaises(ValueError):
            trimmed_mean([])

    def test_negative_trim_count_raises(self) -> None:
        with self.assertRaises(ValueError):
            trimmed_mean([1, 2, 3], trim_count=-1)

    def test_trim_count_too_large_raises(self) -> None:
        with self.assertRaises(ValueError):
            trimmed_mean([1, 2, 3], trim_count=2)
        with self.assertRaises(ValueError):
            trimmed_mean([1, 2, 3, 4], trim_count=2)

    def test_rejects_non_list(self) -> None:
        with self.assertRaises(TypeError):
            trimmed_mean((1, 2, 3))  # type: ignore[arg-type]

    def test_rejects_non_numeric(self) -> None:
        with self.assertRaises(TypeError):
            trimmed_mean([1, 2, "a"])  # type: ignore[type-var]

    def test_rejects_bool(self) -> None:
        with self.assertRaises(TypeError):
            trimmed_mean([True, 1, 2])  # type: ignore[type-var]

    def test_rejects_non_int_trim_count(self) -> None:
        with self.assertRaises(TypeError):
            trimmed_mean([1, 2, 3], 1.5)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            trimmed_mean([1, 2, 3], True)  # type: ignore[arg-type]




class TestRootMeanSquare(unittest.TestCase):
    def test_basic(self) -> None:
        self.assertAlmostEqual(root_mean_square([1, 2, 3]), math.sqrt(14 / 3))

    def test_empty_raises(self) -> None:
        with self.assertRaises(ValueError):
            root_mean_square([])

    def test_rejects_non_list(self) -> None:
        with self.assertRaises(TypeError):
            root_mean_square((1, 2, 3))  # type: ignore[arg-type]

    def test_rejects_non_numeric(self) -> None:
        with self.assertRaises(TypeError):
            root_mean_square([1, 2, "a"])  # type: ignore[type-var]

    def test_rejects_bool(self) -> None:
        with self.assertRaises(TypeError):
            root_mean_square([True, 1, 2])  # type: ignore[type-var]


class TestStandardError(unittest.TestCase):
    def test_basic(self) -> None:
        self.assertAlmostEqual(standard_error([1, 2, 3, 4, 5]), 0.7071067811865476)

    def test_three_values(self) -> None:
        self.assertAlmostEqual(standard_error([1, 2, 3]), 0.5773502691896258)

    def test_negatives(self) -> None:
        self.assertAlmostEqual(standard_error([-2, -1, 0, 1, 2]), 0.7071067811865476)

    def test_floats(self) -> None:
        self.assertAlmostEqual(standard_error([1.5, 2.5, 3.5]), 0.5773502691896258)

    def test_single_raises(self) -> None:
        with self.assertRaises(ValueError):
            standard_error([42])

    def test_empty_raises(self) -> None:
        with self.assertRaises(ValueError):
            standard_error([])

    def test_rejects_non_list(self) -> None:
        with self.assertRaises(TypeError):
            standard_error((1, 2, 3))  # type: ignore[arg-type]

    def test_rejects_non_numeric(self) -> None:
        with self.assertRaises(TypeError):
            standard_error([1, 2, "a"])  # type: ignore[type-var]

    def test_rejects_bool(self) -> None:
        with self.assertRaises(TypeError):
            standard_error([True, 1, 2])  # type: ignore[type-var]


class TestProduct(unittest.TestCase):
    def test_basic(self) -> None:
        self.assertEqual(product([1, 2, 3]), 6.0)

    def test_single(self) -> None:
        self.assertEqual(product([5]), 5.0)

    def test_negatives(self) -> None:
        self.assertEqual(product([2, -3, 4]), -24.0)
        self.assertEqual(product([-1, -2, -3]), -6.0)

    def test_floats(self) -> None:
        self.assertAlmostEqual(product([1.5, 2.0]), 3.0)

    def test_empty_raises(self) -> None:
        with self.assertRaises(ValueError):
            product([])

    def test_rejects_non_list(self) -> None:
        with self.assertRaises(TypeError):
            product((1, 2, 3))  # type: ignore[arg-type]

    def test_rejects_non_numeric(self) -> None:
        with self.assertRaises(TypeError):
            product([1, 2, "a"])  # type: ignore[type-var]

    def test_rejects_bool(self) -> None:
        with self.assertRaises(TypeError):
            product([True, 1, 2])  # type: ignore[type-var]


if __name__ == "__main__":
    unittest.main()


class TestZScores(unittest.TestCase):
    def test_basic(self) -> None:
        result = z_scores([1, 2, 3, 4, 5])
        expected = [
            -1.4142135623730951,
            -0.7071067811865475,
            0.0,
            0.7071067811865475,
            1.4142135623730951,
        ]
        self.assertEqual(len(result), len(expected))
        for a, b in zip(result, expected):
            self.assertAlmostEqual(a, b, places=12)

    def test_constant_raises(self) -> None:
        with self.assertRaises(ValueError):
            z_scores([5, 5, 5])

    def test_empty_raises(self) -> None:
        with self.assertRaises(ValueError):
            z_scores([])

    def test_rejects_non_list(self) -> None:
        with self.assertRaises(TypeError):
            z_scores((1, 2, 3))  # type: ignore[arg-type]

    def test_rejects_non_numeric(self) -> None:
        with self.assertRaises(TypeError):
            z_scores([1, 2, "a"])  # type: ignore[type-var]


class TestMidhinge(unittest.TestCase):
    def test_basic(self) -> None:

        self.assertAlmostEqual(midhinge([1, 2, 3, 4, 5]), 3.0)
        self.assertAlmostEqual(midhinge([1, 2, 3, 4, 5, 6]), 3.5)
        self.assertAlmostEqual(midhinge([6, 2, 9, 1]), 4.25)

    def test_matches_quartile_mean(self) -> None:
        from stats import percentile

        data: list[int | float] = [1, 2, 3, 4, 5, 6, 7, 8]
        expected = (percentile(data, 25) + percentile(data, 75)) / 2.0
        self.assertAlmostEqual(midhinge(data), expected)

    def test_empty_raises(self) -> None:

        with self.assertRaises(ValueError):
            midhinge([])

    def test_single_value(self) -> None:

        self.assertAlmostEqual(midhinge([42]), 42.0)

    def test_negatives_and_floats(self) -> None:

        self.assertAlmostEqual(midhinge([-5, -1, 0, 1, 5]), 0.0)
        self.assertAlmostEqual(midhinge([1.5, 2.5, 3.5, 4.5]), 3.0)

    def test_rejects_non_list(self) -> None:

        with self.assertRaises(TypeError):
            midhinge((1, 2, 3))  # type: ignore[arg-type]

    def test_rejects_non_numeric(self) -> None:

        with self.assertRaises(TypeError):
            midhinge([1, 2, "a"])  # type: ignore[type-var]

    def test_rejects_bool(self) -> None:

        with self.assertRaises(TypeError):
            midhinge([True, 1, 2])  # type: ignore[type-var]


class TestQuartile(unittest.TestCase):
    def test_basic(self) -> None:
        from stats import first_quartile, q1, q3, quartile, third_quartile

        data = [1, 2, 3, 4, 5]
        self.assertAlmostEqual(quartile(data, 1), 2.0)
        self.assertAlmostEqual(quartile(data, 2), 3.0)
        self.assertAlmostEqual(quartile(data, 3), 4.0)
        self.assertAlmostEqual(first_quartile(data), q1(data))
        self.assertAlmostEqual(third_quartile(data), q3(data))

    def test_edges(self) -> None:
        from stats import quartile

        data = [1, 2, 3, 4, 5, 6]
        self.assertAlmostEqual(quartile(data, 0), 1.0)
        self.assertAlmostEqual(quartile(data, 4), 6.0)
        self.assertAlmostEqual(quartile(data, 1), 2.25)
        self.assertAlmostEqual(quartile(data, 3), 4.75)

    def test_empty_raises(self) -> None:
        from stats import quartile

        with self.assertRaises(ValueError):
            quartile([], 1)

    def test_rejects_bad_q(self) -> None:
        from stats import quartile

        with self.assertRaises(ValueError):
            quartile([1, 2, 3], 5)
        with self.assertRaises(ValueError):
            quartile([1, 2, 3], -1)

    def test_rejects_non_int_q(self) -> None:
        from stats import quartile

        with self.assertRaises(TypeError):
            quartile([1, 2, 3], 1.5)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            quartile([1, 2, 3], True)  # type: ignore[arg-type]

    def test_rejects_non_list(self) -> None:
        from stats import quartile

        with self.assertRaises(TypeError):
            quartile((1, 2, 3), 1)  # type: ignore[arg-type]

    def test_rejects_non_numeric(self) -> None:
        from stats import quartile

        with self.assertRaises(TypeError):
            quartile([1, 2, "a"], 1)  # type: ignore[list-item]

    def test_rejects_bool_in_list(self) -> None:
        from stats import quartile

        with self.assertRaises(TypeError):
            quartile([True, 1, 2], 1)  # type: ignore[type-var]


class TestMovingAverage(unittest.TestCase):
    def test_simple_average(self) -> None:
        from stats import moving_average

        self.assertEqual(moving_average([1, 2, 3, 4, 5], 3), [2.0, 3.0, 4.0])

    def test_window_two(self) -> None:
        from stats import moving_average

        self.assertEqual(moving_average([1, 2, 3, 4], 2), [1.5, 2.5, 3.5])

    def test_window_equals_length(self) -> None:
        from stats import moving_average

        self.assertEqual(moving_average([1, 2, 3], 3), [2.0])

    def test_window_one(self) -> None:
        from stats import moving_average

        self.assertEqual(moving_average([1, 2, 3], 1), [1.0, 2.0, 3.0])

    def test_weighted_average(self) -> None:
        from stats import moving_average

        result = moving_average([10, 20, 30], 2, weights=[1, 2])
        self.assertAlmostEqual(result[0], 50 / 3)
        self.assertAlmostEqual(result[1], 80 / 3)

    def test_negative_values(self) -> None:
        from stats import moving_average

        self.assertEqual(moving_average([-1, 0, 1], 2), [-0.5, 0.5])

    def test_floats(self) -> None:
        from stats import moving_average

        self.assertEqual(moving_average([1.5, 2.5, 3.5], 2), [2.0, 3.0])

    def test_empty_raises(self) -> None:
        from stats import moving_average

        with self.assertRaises(ValueError):
            moving_average([], 2)

    def test_window_too_large_raises(self) -> None:
        from stats import moving_average

        with self.assertRaises(ValueError):
            moving_average([1, 2, 3], 4)

    def test_non_positive_window_raises(self) -> None:
        from stats import moving_average

        with self.assertRaises(ValueError):
            moving_average([1, 2, 3], 0)
        with self.assertRaises(ValueError):
            moving_average([1, 2, 3], -1)

    def test_non_int_window_raises(self) -> None:
        from stats import moving_average

        with self.assertRaises(TypeError):
            moving_average([1, 2, 3], 1.5)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            moving_average([1, 2, 3], True)  # type: ignore[arg-type]

    def test_non_list_raises(self) -> None:
        from stats import moving_average

        with self.assertRaises(TypeError):
            moving_average((1, 2, 3), 2)  # type: ignore[arg-type]

    def test_non_numeric_raises(self) -> None:
        from stats import moving_average

        with self.assertRaises(TypeError):
            moving_average([1, 2, "a"], 2)  # type: ignore[list-item]

    def test_bool_in_list_raises(self) -> None:
        from stats import moving_average

        with self.assertRaises(TypeError):
            moving_average([True, 1, 2], 2)  # type: ignore[type-var]

    def test_weights_wrong_length_raises(self) -> None:
        from stats import moving_average

        with self.assertRaises(ValueError):
            moving_average([1, 2, 3], 2, weights=[1, 2, 3])

    def test_weights_non_list_raises(self) -> None:
        from stats import moving_average

        with self.assertRaises(TypeError):
            moving_average([1, 2, 3], 2, weights="ab")  # type: ignore[arg-type]

    def test_weights_non_positive_sum_raises(self) -> None:
        from stats import moving_average

        with self.assertRaises(ValueError):
            moving_average([1, 2, 3], 2, weights=[0, 0])
        with self.assertRaises(ValueError):
            moving_average([1, 2, 3], 2, weights=[-1, 1])
