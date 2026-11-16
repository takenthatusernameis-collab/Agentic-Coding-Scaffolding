"""Tests for rate_limiter_utils module."""

import time
import unittest
from typing import TypeVar

import rate_limiter_utils
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
        limiter = RateLimiter(rate=10.0, capacity=1.0)
        # Should be able to acquire immediately
        self.assertTrue(limiter.acquire(1.0))
        # Now bucket is empty
        self.assertFalse(limiter.acquire(1.0))
        # Wait for one token to refill (1 token per 0.1s at rate=10.0)
        time.sleep(0.2)
        self.assertTrue(limiter.acquire(1.0))

    def test_acquire_blocking(self):
        limiter = RateLimiter(rate=10.0, capacity=1.0)
        # Start with full bucket
        start = time.monotonic()
        limiter.acquire_blocking(1.0)  # Should return immediately
        elapsed = time.monotonic() - start
        self.assertLess(elapsed, 0.1)  # Should be very quick

        # Now bucket is empty, next acquire should block for about 0.1s
        start = time.monotonic()
        limiter.acquire_blocking(1.0)
        elapsed = time.monotonic() - start
        self.assertGreaterEqual(elapsed, 0.05)
        self.assertLess(elapsed, 0.3)

    def test_token_bucket_context_manager(self):
        limiter = RateLimiter(rate=10.0, capacity=1.0)
        # Acquire one token immediately
        with token_bucket(limiter, 1.0):
            pass  # Should not block
        # Now bucket is empty, entering context should block
        start = time.monotonic()
        with token_bucket(limiter, 1.0):
            pass
        elapsed = time.monotonic() - start
        self.assertGreaterEqual(elapsed, 0.05)
        self.assertLess(elapsed, 0.3)

    def test_acquire_more_than_capacity(self):
        limiter = RateLimiter(rate=10.0, capacity=1.0)
        # A request larger than the bucket can never be satisfied and must not
        # be reported as acquired.
        self.assertFalse(limiter.acquire(2.0))
        # The rejected request must not consume tokens.
        self.assertTrue(limiter.acquire(1.0))

    def test_acquire_negative_tokens_rejected(self):
        limiter = RateLimiter(rate=1.0, capacity=1.0)
        limiter.tokens = 0.0
        with self.assertRaises(ValueError):
            limiter.acquire(-1.0)
        # The failed request must not mint tokens.
        self.assertAlmostEqual(limiter.tokens, 0.0, places=6)

    def test_acquire_blocking_raises_when_tokens_exceed_capacity(self):
        limiter = RateLimiter(rate=10.0, capacity=1.0)
        # This used to spin forever because acquire() can never succeed.
        start = time.monotonic()
        with self.assertRaises(ValueError):
            limiter.acquire_blocking(2.0)
        self.assertLess(time.monotonic() - start, 0.1)

    def test_token_bucket_raises_when_tokens_exceed_capacity(self):
        limiter = RateLimiter(rate=10.0, capacity=1.0)
        with self.assertRaises(ValueError):
            with token_bucket(limiter, 2.0):
                pass

    def test_non_positive_capacity_rejected(self):
        with self.assertRaises(ValueError):
            RateLimiter(rate=1.0, capacity=0.0)

    def test_rate_limit_preserves_metadata(self):
        @rate_limit(rate=1000.0)
        def documented() -> str:
            """A documented callable."""
            return "ok"

        self.assertEqual(documented.__name__, "documented")
        self.assertEqual(documented.__doc__, "A documented callable.")
        self.assertEqual(documented(), "ok")

    def test_rate_limit_decorator(self):
        calls = []

        @rate_limit(rate=20.0, capacity=2.0)  # 20 calls per second, burst of 2
        def limited_function():
            calls.append(time.monotonic())

        # Call function 5 times
        start = time.monotonic()
        for i in range(5):
            limited_function()
        elapsed = time.monotonic() - start

        # With rate 20 per second and capacity=2, the first two calls are immediate.
        # Then each additional call requires 0.05 seconds to regenerate one token.
        # For 5 calls: 2 immediate + 3 * 0.05 = 0.15 seconds minimum.
        self.assertGreaterEqual(elapsed, 0.1)
        self.assertLess(elapsed, 0.5)  # Allow slack above 0.15

        # Check that the calls are spaced appropriately after the bucket is depleted
        # We expect intervals of about 0.05 seconds after the first two calls.
        if len(calls) >= 3:
            # Intervals between call2-call3, call3-call4, call4-call5 should be ~0.05
            intervals = [calls[i + 1] - calls[i] for i in range(1, len(calls) - 1)]
            for interval in intervals:
                self.assertAlmostEqual(interval, 0.05, places=1)


class TestExportedTypeVars(unittest.TestCase):
    def test_typevar_exported(self):
        self.assertIsInstance(rate_limiter_utils.F, TypeVar)
        self.assertEqual(rate_limiter_utils.F.__name__, "F")


if __name__ == "__main__":
    unittest.main()
