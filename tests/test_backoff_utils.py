"""Tests for the backoff strategy utilities."""

import unittest

from backoff_utils import backoff_delay, constant_backoff, exponential_backoff, jittered_backoff


class TestBackoffUtils(unittest.TestCase):
    def test_constant_backoff(self):
        self.assertEqual(constant_backoff(1.0), 1.0)
        self.assertEqual(constant_backoff(0.5), 0.5)
        self.assertEqual(constant_backoff(1.0, attempt=1), 1.0)
        self.assertEqual(constant_backoff(1.0, attempt=5), 1.0)

    def test_constant_backoff_validation(self):
        with self.assertRaises(ValueError):
            constant_backoff(-1.0)
        with self.assertRaises(TypeError):
            constant_backoff("x")

    def test_exponential_backoff_uncapped(self):
        self.assertEqual(exponential_backoff(1.0, 2.0, 100.0, attempt=1), 2.0)
        self.assertEqual(exponential_backoff(1.0, 3.0, 100.0, attempt=1), 3.0)
        self.assertEqual(exponential_backoff(1.0, 2.0, 100.0, attempt=2), 4.0)
        self.assertEqual(exponential_backoff(1.0, 2.0, 100.0, attempt=3), 8.0)

    def test_exponential_backoff_capped(self):
        self.assertEqual(exponential_backoff(10.0, 2.0, 15.0, attempt=1), 15.0)
        self.assertEqual(exponential_backoff(10.0, 100.0, 15.0, attempt=1), 15.0)

    def test_exponential_backoff_validation(self):
        with self.assertRaises(ValueError):
            exponential_backoff(-1.0, 2.0, 100.0)
        with self.assertRaises(ValueError):
            exponential_backoff(1.0, 0.5, 100.0)
        with self.assertRaises(ValueError):
            exponential_backoff(1.0, 2.0, -1.0)
        with self.assertRaises(TypeError):
            exponential_backoff("x", 2.0, 100.0)
        with self.assertRaises(ValueError):
            exponential_backoff(1.0, 2.0, 100.0, attempt=0)

    def test_backoff_delay_constant(self):
        self.assertEqual(backoff_delay(strategy="constant", delay=2.5), 2.5)
        self.assertEqual(backoff_delay(strategy="constant", delay=2.5, attempt=3), 2.5)

    def test_backoff_delay_exponential(self):
        call = dict(initial=1.0, factor=2.0, max_delay=50.0, attempt=1)
        self.assertEqual(backoff_delay(strategy="exponential", **call), 2.0)
        call = dict(initial=1.0, factor=2.0, max_delay=50.0, attempt=2)
        self.assertEqual(backoff_delay(strategy="exponential", **call), 4.0)
        call = dict(initial=1.0, factor=2.0, max_delay=50.0, attempt=3)
        self.assertEqual(backoff_delay(strategy="exponential", **call), 8.0)

    def test_backoff_delay_default_strategy(self):
        self.assertEqual(backoff_delay(delay=3.0), 3.0)

    def test_backoff_delay_unknown_strategy(self):
        with self.assertRaises(ValueError):
            backoff_delay(strategy="nonexistent", delay=1.0)

    def test_backoff_delay_validation(self):
        with self.assertRaises(TypeError):
            backoff_delay(strategy="constant", delay=1.0, attempt="x")
        with self.assertRaises(ValueError):
            backoff_delay(strategy="constant", delay=1.0, attempt=0)

    def test_jittered_backoff_bounds(self):
        for _ in range(100):
            value = jittered_backoff(10.0, 0.2)
            self.assertGreaterEqual(value, 8.0)
            self.assertLessEqual(value, 12.0)

    def test_jittered_backoff_zero_jitter(self):
        self.assertEqual(jittered_backoff(5.0, 0.0), 5.0)

    def test_jittered_backoff_negative_delay_raises(self):
        with self.assertRaises(ValueError):
            jittered_backoff(-1.0)

    def test_jittered_backoff_bad_jitter_raises(self):
        with self.assertRaises(ValueError):
            jittered_backoff(1.0, 1.5)
        with self.assertRaises(ValueError):
            jittered_backoff(1.0, -0.1)

    def test_jittered_backoff_type_errors(self):
        with self.assertRaises(TypeError):
            jittered_backoff("x")
        with self.assertRaises(TypeError):
            jittered_backoff(1.0, "x")


if __name__ == "__main__":
    unittest.main()
