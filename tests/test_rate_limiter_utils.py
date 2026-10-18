"""Tests for rate_limiter_utils module."""

import time
import unittest

from rate_limiter_utils import RateLimiter, rate_limit, token_bucket


class TestRateLimiter(unittest.TestCase):
    def test_initialization(self):
        limiter = RateLimiter(rate=1.0)
        self.assertEqual(limiter.rate, 1.0)
        self.assertEqual(limiter.capacity, 1.0)
        self.assertEqual(limiter.tokens, 1.0)

        limiter = RateLimiter(rate=2.0, capacity=4.0)
        self.assertEqual(limiter.rate, 2.0)
        self.assertEqual(limiter.capacity, 4.0)
        self.assertEqual(limiter.tokens, 4.0)

    def test_acquire_immediate(self):
        limiter = RateLimiter(rate=1.0, capacity=1.0)
        # Should be able to acquire immediately
        self.assertTrue(limiter.acquire(1.0))
        # Now bucket is empty
        self.assertFalse(limiter.acquire(1.0))
        # Wait a bit and try again
        time.sleep(1.1)
        self.assertTrue(limiter.acquire(1.0))

    def test_acquire_blocking(self):
        limiter = RateLimiter(rate=1.0, capacity=1.0)
        # Start with full bucket
        start = time.monotonic()
        limiter.acquire_blocking(1.0)  # Should return immediately
        elapsed = time.monotonic() - start
        self.assertLess(elapsed, 0.1)  # Should be very quick

        # Now bucket is empty, next acquire should block for about 1 second
        start = time.monotonic()
        limiter.acquire_blocking(1.0)
        elapsed = time.monotonic() - start
        self.assertGreaterEqual(elapsed, 0.9)
        self.assertLess(elapsed, 1.1)

    def test_token_bucket_context_manager(self):
        limiter = RateLimiter(rate=1.0, capacity=1.0)
        # Acquire one token immediately
        with token_bucket(limiter, 1.0):
            pass  # Should not block
        # Now bucket is empty, entering context should block
        start = time.monotonic()
        with token_bucket(limiter, 1.0):
            pass
        elapsed = time.monotonic() - start
        self.assertGreaterEqual(elapsed, 0.9)
        self.assertLess(elapsed, 1.1)

    def test_rate_limit_decorator(self):
        calls = []

        @rate_limit(rate=2.0)  # 2 calls per second
        def limited_function():
            calls.append(time.monotonic())

        # Call function 5 times
        start = time.monotonic()
        for i in range(5):
            limited_function()
        elapsed = time.monotonic() - start

        # With rate 2 per second and capacity=2 (default), the first two calls are immediate.
        # Then each additional call requires 0.5 seconds to regenerate one token.
        # For 5 calls: 2 immediate + 3 * 0.5 = 1.5 seconds minimum.
        self.assertGreaterEqual(elapsed, 1.4)
        self.assertLess(elapsed, 2.0)  # Allow a little slack above 1.5

        # Check that the calls are spaced appropriately after the bucket is depleted
        # We expect intervals of about 0.5 seconds after the first two calls.
        if len(calls) >= 3:
            # Intervals between call2-call3, call3-call4, call4-call5 should be ~0.5
            intervals = [calls[i + 1] - calls[i] for i in range(1, len(calls) - 1)]
            for interval in intervals:
                self.assertAlmostEqual(interval, 0.5, places=1)


if __name__ == "__main__":
    unittest.main()
