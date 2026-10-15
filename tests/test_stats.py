"""Tests for stats module."""

import unittest

from stats import mean, median, mode, stddev, variance


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


if __name__ == "__main__":
    unittest.main()
