import unittest

from backoff_utils import backoff_delay, constant_backoff, exponential_backoff


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


if __name__ == "__main__":
    unittest.main()
