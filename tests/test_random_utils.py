"""Tests for random_utils module."""

import unittest

from random_utils import (
    random_choice,
    random_gaussian,
    random_int,
    random_sample,
    random_shuffle,
    random_uniform,
    weighted_choice,
)


class TestRandomInt(unittest.TestCase):
    def test_in_range(self) -> None:
        for _ in range(100):
            value = random_int(1, 10)
            self.assertTrue(1 <= value <= 10)

    def test_single_value_range(self) -> None:
        self.assertEqual(random_int(5, 5), 5)

    def test_negative_range(self) -> None:
        for _ in range(100):
            value = random_int(-10, -1)
            self.assertTrue(-10 <= value <= -1)

    def test_invalid_range_raises(self) -> None:
        with self.assertRaises(ValueError):
            random_int(10, 1)

    def test_seeded_is_reproducible(self) -> None:
        self.assertEqual(random_int(1, 100, seed=42), random_int(1, 100, seed=42))

    def test_different_seeds_differ(self) -> None:
        # Over a large enough range, two distinct seeds should not always match.
        a = [random_int(1, 1_000_000, seed=i) for i in range(10)]
        self.assertEqual(len(set(a)), len(a))


class TestRandomChoice(unittest.TestCase):
    def test_returns_member(self) -> None:
        items = ["apple", "banana", "cherry"]
        self.assertIn(random_choice(items), items)

    def test_empty_raises(self) -> None:
        with self.assertRaises(ValueError):
            random_choice([])

    def test_seeded_is_reproducible(self) -> None:
        self.assertEqual(
            random_choice(["a", "b", "c"], seed=0),
            random_choice(["a", "b", "c"], seed=0),
        )


class TestRandomSample(unittest.TestCase):
    def test_size(self) -> None:
        sample = random_sample([1, 2, 3, 4, 5], 3)
        self.assertEqual(len(sample), 3)

    def test_unique_without_replacement(self) -> None:
        sample = random_sample([1, 2, 3, 4], 2)
        self.assertEqual(len(set(sample)), 2)

    def test_sample_all(self) -> None:
        sample = random_sample([1, 2, 3], 3)
        self.assertEqual(sorted(sample), [1, 2, 3])

    def test_zero_sample(self) -> None:
        self.assertEqual(random_sample([1, 2, 3], 0), [])

    def test_empty_raises(self) -> None:
        with self.assertRaises(ValueError):
            random_sample([], 1)

    def test_negative_n_raises(self) -> None:
        with self.assertRaises(ValueError):
            random_sample([1, 2, 3], -1)

    def test_n_too_large_raises(self) -> None:
        with self.assertRaises(ValueError):
            random_sample([1, 2, 3], 4)

    def test_seeded_is_reproducible(self) -> None:
        self.assertEqual(
            random_sample([1, 2, 3, 4, 5], 2, seed=7),
            random_sample([1, 2, 3, 4, 5], 2, seed=7),
        )


class TestRandomShuffle(unittest.TestCase):
    def test_returns_permutation(self) -> None:
        items = [1, 2, 3, 4, 5]
        shuffled = random_shuffle(items)
        self.assertEqual(sorted(shuffled), sorted(items))
        self.assertEqual(items, [1, 2, 3, 4, 5])  # original unchanged

    def test_empty_raises(self) -> None:
        with self.assertRaises(ValueError):
            random_shuffle([])

    def test_seeded_is_reproducible(self) -> None:
        self.assertEqual(
            random_shuffle([1, 2, 3, 4, 5], seed=99),
            random_shuffle([1, 2, 3, 4, 5], seed=99),
        )

    def test_single_element(self) -> None:
        self.assertEqual(random_shuffle([42]), [42])


class TestWeightedChoice(unittest.TestCase):
    def test_returns_member(self) -> None:
        items = ["a", "b", "c"]
        self.assertIn(weighted_choice(items, [1, 1, 1], seed=1), items)

    def test_zero_weight_is_excluded(self) -> None:
        # With only "b" having positive weight, it should always be chosen.
        self.assertEqual(weighted_choice(["a", "b"], [0, 1], seed=5), "b")

    def test_empty_raises(self) -> None:
        with self.assertRaises(ValueError):
            weighted_choice([], [])

    def test_mismatched_lengths_raises(self) -> None:
        with self.assertRaises(ValueError):
            weighted_choice(["a", "b"], [1])

    def test_negative_weight_raises(self) -> None:
        with self.assertRaises(ValueError):
            weighted_choice(["a", "b"], [1, -1])

    def test_all_zero_weights_raises(self) -> None:
        with self.assertRaises(ValueError):
            weighted_choice(["a", "b"], [0, 0])

    def test_seeded_is_reproducible(self) -> None:
        self.assertEqual(
            weighted_choice(["a", "b", "c"], [1, 2, 3], seed=42),
            weighted_choice(["a", "b", "c"], [1, 2, 3], seed=42),
        )


class TestRandomUniform(unittest.TestCase):
    def test_in_range(self) -> None:
        for _ in range(100):
            value = random_uniform(0, 1)
            self.assertTrue(0 <= value <= 1)

    def test_invalid_range_raises(self) -> None:
        with self.assertRaises(ValueError):
            random_uniform(10, 1)

    def test_seeded_is_reproducible(self) -> None:
        self.assertAlmostEqual(random_uniform(0, 1, seed=13), random_uniform(0, 1, seed=13))


class TestRandomGaussian(unittest.TestCase):
    def test_returns_float(self) -> None:
        self.assertIsInstance(random_gaussian(seed=3), float)

    def test_negative_sigma_raises(self) -> None:
        with self.assertRaises(ValueError):
            random_gaussian(sigma=-1)

    def test_seeded_is_reproducible(self) -> None:
        self.assertAlmostEqual(random_gaussian(0, 1, seed=17), random_gaussian(0, 1, seed=17))


if __name__ == "__main__":
    unittest.main()
