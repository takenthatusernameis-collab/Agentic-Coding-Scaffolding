import time
import unittest

from retry_utils import retry, retry_count, retry_with_backoff


class TestRetryDecorator(unittest.TestCase):
    def test_retry_success_first_try(self):
        """Test that function succeeds on first attempt."""
        attempt_count = 0

        @retry(max_attempts=3, delay=0.01)
        def func():
            nonlocal attempt_count
            attempt_count += 1
            return "success"

        result = func()
        self.assertEqual(result, "success")
        self.assertEqual(attempt_count, 1)

    def test_retry_success_after_retries(self):
        """Test that function succeeds after some retries."""
        attempt_count = 0

        @retry(max_attempts=3, delay=0.01)
        def func():
            nonlocal attempt_count
            attempt_count += 1
            if attempt_count < 3:
                raise ValueError("Try again")
            return "success"

        result = func()
        self.assertEqual(result, "success")
        self.assertEqual(attempt_count, 3)

    def test_retry_fails_after_max_attempts(self):
        """Test that function fails after exceeding max attempts."""
        attempt_count = 0

        @retry(max_attempts=2, delay=0.01)
        def func():
            nonlocal attempt_count
            attempt_count += 1
            raise ValueError("Always fails")

        with self.assertRaises(ValueError):
            func()
        self.assertEqual(attempt_count, 2)

    def test_retry_specific_exceptions(self):
        """Test that only specified exceptions trigger retries."""
        attempt_count = 0

        @retry(max_attempts=3, delay=0.01, exceptions=(ValueError,))
        def func():
            nonlocal attempt_count
            attempt_count += 1
            if attempt_count < 2:
                raise ValueError("Retry on this")
            elif attempt_count == 2:
                raise TypeError("Don't retry on this")
            return "success"

        with self.assertRaises(TypeError):
            func()
        self.assertEqual(attempt_count, 2)

    def test_retry_with_zero_attempts(self):
        """Test behavior with max_attempts=1 (no retries)."""
        attempt_count = 0

        @retry(max_attempts=1, delay=0.01)
        def func():
            nonlocal attempt_count
            attempt_count += 1
            raise ValueError("Fails")

        with self.assertRaises(ValueError):
            func()
        self.assertEqual(attempt_count, 1)


class TestRetryWithBackoffDecorator(unittest.TestCase):
    def test_retry_with_backoff_success_first_try(self):
        """Test that function succeeds on first attempt."""
        attempt_count = 0

        @retry_with_backoff(max_attempts=3, initial_delay=0.01)
        def func():
            nonlocal attempt_count
            attempt_count += 1
            return "success"

        result = func()
        self.assertEqual(result, "success")
        self.assertEqual(attempt_count, 1)

    def test_retry_with_backoff_success_after_retries(self):
        """Test that function succeeds after some retries."""
        attempt_count = 0

        @retry_with_backoff(max_attempts=3, initial_delay=0.01)
        def func():
            nonlocal attempt_count
            attempt_count += 1
            if attempt_count < 3:
                raise ValueError("Try again")
            return "success"

        result = func()
        self.assertEqual(result, "success")
        self.assertEqual(attempt_count, 3)

    def test_retry_with_backoff_fails_after_max_attempts(self):
        """Test that function fails after exceeding max attempts."""
        attempt_count = 0

        @retry_with_backoff(max_attempts=2, initial_delay=0.01)
        def func():
            nonlocal attempt_count
            attempt_count += 1
            raise ValueError("Always fails")

        with self.assertRaises(ValueError):
            func()
        self.assertEqual(attempt_count, 2)

    def test_retry_with_backoff_jitter(self):
        """Test that jitter affects delay (basic test)."""
        delays = []

        @retry_with_backoff(max_attempts=3, initial_delay=0.01, backoff_factor=2.0, jitter=True)
        def func():
            if len(delays) < 2:  # First two attempts
                delays.append(time.time())
                raise ValueError("Try again")
            return "success"

        # Mock time.sleep to capture delays
        original_sleep = time.sleep
        slept_durations = []

        def mock_sleep(duration):
            slept_durations.append(duration)
            # Don't actually sleep in test
            pass

        time.sleep = mock_sleep
        try:
            result = func()
            self.assertEqual(result, "success")
            # Should have slept twice (after first and second attempts)
            self.assertEqual(len(slept_durations), 2)
            # Each sleep duration should be positive
            for duration in slept_durations:
                self.assertGreaterEqual(duration, 0)
        finally:
            time.sleep = original_sleep


class TestRetryCountDecorator(unittest.TestCase):
    def test_retry_count_no_retries(self):
        """Test that retry_count returns 0 when no retries needed."""

        @retry_count(max_attempts=3, delay=0.01)
        def func():
            return "success"

        result, count = func()
        self.assertEqual(result, "success")
        self.assertEqual(count, 0)

    def test_retry_count_with_retries(self):
        """Test that retry_count returns correct retry count."""
        attempt_count = 0

        @retry_count(max_attempts=3, delay=0.01)
        def func():
            nonlocal attempt_count
            attempt_count += 1
            if attempt_count < 3:
                raise ValueError("Try again")
            return "success"

        result, count = func()
        self.assertEqual(result, "success")
        self.assertEqual(count, 2)  # Retried twice

    def test_retry_count_exhausted_attempts(self):
        """Test that retry_count raises exception after max attempts."""
        attempt_count = 0

        @retry_count(max_attempts=2, delay=0.01)
        def func():
            nonlocal attempt_count
            attempt_count += 1
            raise ValueError("Always fails")

        with self.assertRaises(ValueError):
            func()
        # Note: The wrapper re-raises the exception, so we don't get a count return
        # This is expected behavior - when all attempts fail, the exception propagates


if __name__ == "__main__":
    unittest.main()
