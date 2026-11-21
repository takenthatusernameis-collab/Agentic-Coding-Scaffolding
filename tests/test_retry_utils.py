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


class TestRetryArgumentValidation(unittest.TestCase):
    """Edge-case validation for retry decorator arguments.

    ``max_attempts=0`` previously let the wrapper loop fall through and raise a
    misleading ``RuntimeError("Unexpected state in retry decorator")`` without
    ever calling the wrapped function. A negative ``delay`` likewise surfaced a
    low-level ``time.sleep`` error. Both are now caught at decoration time.
    """

    def test_retry_rejects_zero_max_attempts(self):
        with self.assertRaises(ValueError):

            @retry(max_attempts=0, delay=0.01)
            def func():  # pragma: no cover - body never runs
                raise ValueError("boom")

    def test_retry_rejects_negative_max_attempts(self):
        with self.assertRaises(ValueError):

            @retry(max_attempts=-1, delay=0.01)
            def func():  # pragma: no cover - body never runs
                raise ValueError("boom")

    def test_retry_rejects_negative_delay(self):
        with self.assertRaises(ValueError):

            @retry(max_attempts=3, delay=-0.01)
            def func():  # pragma: no cover - body never runs
                raise ValueError("boom")

    def test_retry_rejects_non_int_max_attempts(self):
        with self.assertRaises(TypeError):

            @retry(max_attempts=1.5, delay=0.01)  # type: ignore[arg-type]
            def func():  # pragma: no cover - body never runs
                raise ValueError("boom")

    def test_retry_rejects_non_tuple_exceptions(self):
        with self.assertRaises(TypeError):

            @retry(max_attempts=3, delay=0.01, exceptions=ValueError)  # type: ignore[arg-type]
            def func():  # pragma: no cover - body never runs
                raise ValueError("boom")

    def test_retry_with_backoff_rejects_zero_max_attempts(self):
        with self.assertRaises(ValueError):

            @retry_with_backoff(max_attempts=0, initial_delay=0.01)
            def func():  # pragma: no cover - body never runs
                raise ValueError("boom")

    def test_retry_with_backoff_rejects_negative_initial_delay(self):
        with self.assertRaises(ValueError):

            @retry_with_backoff(max_attempts=3, initial_delay=-0.01)
            def func():  # pragma: no cover - body never runs
                raise ValueError("boom")

    def test_retry_count_rejects_zero_max_attempts(self):
        with self.assertRaises(ValueError):

            @retry_count(max_attempts=0, delay=0.01)
            def func():  # pragma: no cover - body never runs
                raise ValueError("boom")

    def test_retry_count_rejects_negative_delay(self):
        with self.assertRaises(ValueError):

            @retry_count(max_attempts=3, delay=-0.01)
            def func():  # pragma: no cover - body never runs
                raise ValueError("boom")

    def test_retry_count_rejects_negative_backoff(self):
        with self.assertRaises(ValueError):

            @retry_count(max_attempts=3, delay=0.01, backoff=-1.0)
            def func():  # pragma: no cover - body never runs
                raise ValueError("boom")

    def test_retry_with_backoff_rejects_non_int_max_attempts(self):
        with self.assertRaises(TypeError):

            @retry_with_backoff(max_attempts=1.5, initial_delay=0.01)  # type: ignore[arg-type]
            def func():  # pragma: no cover - body never runs
                raise ValueError("boom")


class TestRetryBackoffDelaySchedule(unittest.TestCase):
    """Confirm the delay schedule is applied between attempts."""

    def test_retry_uses_backoff_multiplier(self):
        slept: list[float] = []
        original_sleep = time.sleep

        def mock_sleep(duration: float) -> None:
            slept.append(duration)

        time.sleep = mock_sleep
        try:

            @retry(max_attempts=3, delay=0.1, backoff=2.0)
            def func():
                raise ValueError("always")

            with self.assertRaises(ValueError):
                func()
        finally:
            time.sleep = original_sleep

        self.assertEqual(slept, [0.1, 0.2])


class TestRetryArgumentValidationExtended(unittest.TestCase):
    """Contract tests for error branches of ``_validate_retry_args`` that the
    original suite never exercised: non-numeric ``delay``/``backoff`` and
    negative ``backoff``.

    These pin the documented ``TypeError``/``ValueError`` contracts so a
    regression in the validation guards cannot surface a misleading downstream
    error (for example a low-level ``time.sleep`` failure for negative delay).
    """

    def test_retry_rejects_non_number_delay(self):
        with self.assertRaises(TypeError):

            @retry(max_attempts=3, delay="0.1")  # type: ignore[arg-type]
            def func():  # pragma: no cover - body never runs
                raise ValueError("boom")

    def test_retry_rejects_non_number_backoff(self):
        with self.assertRaises(TypeError):

            @retry(max_attempts=3, delay=0.01, backoff="2.0")  # type: ignore[arg-type]
            def func():  # pragma: no cover - body never runs
                raise ValueError("boom")

    def test_retry_rejects_negative_backoff(self):
        with self.assertRaises(ValueError):

            @retry(max_attempts=3, delay=0.01, backoff=-1.0)
            def func():  # pragma: no cover - body never runs
                raise ValueError("boom")

    def test_retry_with_backoff_rejects_non_number_initial_delay(self):
        with self.assertRaises(TypeError):

            @retry_with_backoff(max_attempts=3, initial_delay="0.1")  # type: ignore[arg-type]
            def func():  # pragma: no cover - body never runs
                raise ValueError("boom")

    def test_retry_with_backoff_rejects_non_number_backoff_factor(self):
        with self.assertRaises(TypeError):

            @retry_with_backoff(
                max_attempts=3, initial_delay=0.01, backoff_factor="2.0"
            )  # type: ignore[arg-type]
            def func():  # pragma: no cover - body never runs
                raise ValueError("boom")

    def test_retry_with_backoff_rejects_negative_backoff_factor(self):
        with self.assertRaises(ValueError):

            @retry_with_backoff(max_attempts=3, initial_delay=0.01, backoff_factor=-1.0)
            def func():  # pragma: no cover - body never runs
                raise ValueError("boom")


    def test_retry_with_backoff_rejects_non_bool_jitter(self):
        with self.assertRaises(TypeError):

            @retry_with_backoff(max_attempts=3, initial_delay=0.01, jitter="yes")  # type: ignore[arg-type]
            def func():  # pragma: no cover - body never runs
                raise ValueError("boom")

    def _assert_rejects_non_finite(self, make_decorator, param, values):
        for value in values:
            with self.subTest(param=param, value=value):
                with self.assertRaises(ValueError):
                    # Calling the decorator factory runs _validate_retry_args at
                    # decoration time, so the guard must raise here instead of
                    # letting a non-finite value reach time.sleep downstream.
                    make_decorator(**{param: value})

    def test_retry_rejects_non_finite_delay(self):
        self._assert_rejects_non_finite(
            lambda delay: retry(max_attempts=3, delay=delay),
            "delay",
            (float("nan"), float("inf"), float("-inf")),
        )

    def test_retry_rejects_non_finite_backoff(self):
        self._assert_rejects_non_finite(
            lambda backoff: retry(max_attempts=3, delay=0.01, backoff=backoff),
            "backoff",
            (float("nan"), float("inf"), float("-inf")),
        )

    def test_retry_with_backoff_rejects_non_finite_initial_delay(self):
        self._assert_rejects_non_finite(
            lambda initial_delay: retry_with_backoff(
                max_attempts=3, initial_delay=initial_delay
            ),
            "initial_delay",
            (float("nan"), float("inf"), float("-inf")),
        )

    def test_retry_with_backoff_rejects_non_finite_backoff_factor(self):
        self._assert_rejects_non_finite(
            lambda backoff_factor: retry_with_backoff(
                max_attempts=3, initial_delay=0.01, backoff_factor=backoff_factor
            ),
            "backoff_factor",
            (float("nan"), float("inf"), float("-inf")),
        )

    def test_retry_count_rejects_non_finite_delay(self):
        self._assert_rejects_non_finite(
            lambda delay: retry_count(max_attempts=3, delay=delay),
            "delay",
            (float("nan"), float("inf"), float("-inf")),
        )

    def test_retry_count_rejects_non_finite_backoff(self):
        self._assert_rejects_non_finite(
            lambda backoff: retry_count(max_attempts=3, delay=0.01, backoff=backoff),
            "backoff",
            (float("nan"), float("inf"), float("-inf")),
        )


if __name__ == "__main__":
    unittest.main()
