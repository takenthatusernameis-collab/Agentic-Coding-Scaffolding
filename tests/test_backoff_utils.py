import unittest

from backoff_utils import backoff_delay, constant_backoff, exponential_backoff, jittered_backoff


class TestBackoffUtils(unittest.TestCase):
    def test_constant_backoff(self):
        self.assertEqual(constant_backoff(1.0), 1.0)
        self.assertEqual(constant_backoff(0.5), 0.5)

    def test_exponential_backoff_uncapped(self):
        self.assertEqual(exponential_backoff(1.0, 2.0, 100.0), 2.0)
        self.assertEqual(exponential_backoff(1.0, 3.0, 100.0), 3.0)

    def test_exponential_backoff_capped(self):
        self.assertEqual(exponential_backoff(10.0, 2.0, 15.0), 15.0)
        self.assertEqual(exponential_backoff(10.0, 100.0, 15.0), 15.0)

    def test_backoff_delay_constant(self):
        self.assertEqual(backoff_delay(strategy="constant", delay=2.5), 2.5)

    def test_backoff_delay_exponential(self):
        self.assertEqual(
            backoff_delay(strategy="exponential", initial=1.0, factor=2.0, max_delay=50.0),
            2.0,
        )

    def test_backoff_delay_default_strategy(self):
        self.assertEqual(backoff_delay(delay=3.0), 3.0)

    def test_backoff_delay_unknown_strategy(self):
        with self.assertRaises(ValueError):
            backoff_delay(strategy="nonexistent", delay=1.0)

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
    def test_constant_backoff(self):
        self.assertEqual(constant_backoff(1.0), 1.0)
        self.assertEqual(constant_backoff(0.5), 0.5)

    def test_exponential_backoff_uncapped(self):
        self.assertEqual(exponential_backoff(1.0, 2.0, 100.0), 2.0)
        self.assertEqual(exponential_backoff(1.0, 3.0, 100.0), 3.0)

    def test_exponential_backoff_capped(self):
        self.assertEqual(exponential_backoff(10.0, 2.0, 15.0), 15.0)
        self.assertEqual(exponential_backoff(10.0, 100.0, 15.0), 15.0)

    def test_backoff_delay_constant(self):
        self.assertEqual(backoff_delay(strategy="constant", delay=2.5), 2.5)

    def test_backoff_delay_exponential(self):
        self.assertEqual(
            backoff_delay(strategy="exponential", initial=1.0, factor=2.0, max_delay=50.0),
            2.0,
        )

    def test_backoff_delay_default_strategy(self):
        self.assertEqual(backoff_delay(delay=3.0), 3.0)

    def test_backoff_delay_unknown_strategy(self):
        with self.assertRaises(ValueError):
            backoff_delay(strategy="nonexistent", delay=1.0)


if __name__ == "__main__":
    unittest.main()
