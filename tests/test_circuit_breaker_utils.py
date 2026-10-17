import threading
import time
import unittest

from circuit_breaker_utils import CircuitBreaker, CircuitOpenError


class TestCircuitBreaker(unittest.TestCase):
    def test_closed_executes_normally(self):
        breaker = CircuitBreaker(failure_threshold=3)
        calls = []

        def get_value() -> int:
            calls.append(1)
            return 42

        self.assertEqual(breaker.call(get_value), 42)
        self.assertEqual(calls, [1])
        self.assertEqual(breaker.state, CircuitBreaker.CLOSED)
        self.assertEqual(breaker.failures, 0)

    def test_opens_after_threshold(self):
        breaker = CircuitBreaker(failure_threshold=3)

        def fail() -> None:
            raise ValueError("boom")

        for _ in range(2):
            with self.assertRaises(ValueError):
                breaker.call(fail)
        self.assertEqual(breaker.state, CircuitBreaker.CLOSED)
        self.assertEqual(breaker.failures, 2)
        # Third failure opens the circuit.
        with self.assertRaises(ValueError):
            breaker.call(fail)
        self.assertEqual(breaker.state, CircuitBreaker.OPEN)
        self.assertEqual(breaker.failures, 3)

    def test_open_rejects_calls(self):
        breaker = CircuitBreaker(failure_threshold=1, recovery_timeout=60.0)

        def always_fail() -> None:
            raise ValueError("boom")

        with self.assertRaises(ValueError):
            breaker.call(always_fail)
        self.assertEqual(breaker.state, CircuitBreaker.OPEN)
        # Open circuit short-circuits without invoking func.
        called = []

        def guarded() -> str:
            called.append(1)
            return "ok"

        with self.assertRaises(CircuitOpenError):
            breaker.call(guarded)
        self.assertEqual(called, [])

    def test_can_execute_reflects_open_state(self):
        breaker = CircuitBreaker(failure_threshold=1, recovery_timeout=60.0)

        def fail() -> None:
            raise ValueError("boom")

        with self.assertRaises(ValueError):
            breaker.call(fail)
        self.assertFalse(breaker.can_execute())

    def test_half_open_allows_trial_call(self):
        breaker = CircuitBreaker(failure_threshold=1, recovery_timeout=0.05)

        def fail() -> None:
            raise ValueError("boom")

        with self.assertRaises(ValueError):
            breaker.call(fail)
        self.assertEqual(breaker.state, CircuitBreaker.OPEN)
        time.sleep(0.1)
        self.assertEqual(breaker.state, CircuitBreaker.HALF_OPEN)
        # A successful trial call closes the circuit.
        self.assertEqual(breaker.call(lambda: "ok"), "ok")
        self.assertEqual(breaker.state, CircuitBreaker.CLOSED)

    def test_half_open_failed_trial_reopens(self):
        breaker = CircuitBreaker(failure_threshold=1, recovery_timeout=0.05)

        def fail() -> None:
            raise ValueError("boom")

        with self.assertRaises(ValueError):
            breaker.call(fail)
        self.assertEqual(breaker.state, CircuitBreaker.OPEN)
        time.sleep(0.1)
        self.assertEqual(breaker.state, CircuitBreaker.HALF_OPEN)
        with self.assertRaises(ValueError):
            breaker.call(fail)
        self.assertEqual(breaker.state, CircuitBreaker.OPEN)

    def test_half_open_only_one_trial_at_a_time(self):
        breaker = CircuitBreaker(failure_threshold=1, recovery_timeout=0.05)

        with self.assertRaises(ValueError):
            breaker.call(lambda: (_ for _ in ()).throw(ValueError("boom")))
        time.sleep(0.1)
        self.assertEqual(breaker.state, CircuitBreaker.HALF_OPEN)

        trial_started = threading.Event()
        trial_release = threading.Event()

        def blocking_trial() -> str:
            trial_started.set()
            trial_release.wait()
            return "ok"

        trial_thread = threading.Thread(target=lambda: breaker.call(blocking_trial))
        trial_thread.start()
        self.assertTrue(trial_started.wait(timeout=5))
        # While a trial call is in progress, a second call is rejected.
        with self.assertRaises(CircuitOpenError):
            breaker.call(lambda: "ok")
        trial_release.set()
        trial_thread.join()
        self.assertEqual(breaker.state, CircuitBreaker.CLOSED)

    def test_expected_exception_only(self):
        breaker = CircuitBreaker(failure_threshold=1, expected_exception=ValueError)

        def type_error() -> None:
            raise TypeError("wrong type")

        # TypeError is not expected, so it propagates and does not open.
        with self.assertRaises(TypeError):
            breaker.call(type_error)
        self.assertEqual(breaker.state, CircuitBreaker.CLOSED)
        self.assertEqual(breaker.failures, 0)

    def test_reset_closes_circuit(self):
        breaker = CircuitBreaker(failure_threshold=1, recovery_timeout=60.0)

        def fail() -> None:
            raise ValueError("boom")

        with self.assertRaises(ValueError):
            breaker.call(fail)
        self.assertEqual(breaker.state, CircuitBreaker.OPEN)
        breaker.reset()
        self.assertEqual(breaker.state, CircuitBreaker.CLOSED)
        self.assertEqual(breaker.failures, 0)
        self.assertTrue(breaker.can_execute())
        self.assertEqual(breaker.call(lambda: 1), 1)

    def test_non_callable_raises(self):
        breaker = CircuitBreaker()
        with self.assertRaises(TypeError):
            breaker.call(42)  # type: ignore[arg-type]

    def test_invalid_threshold_raises(self):
        with self.assertRaises(TypeError):
            CircuitBreaker(failure_threshold="3")  # type: ignore[arg-type]
        with self.assertRaises(ValueError):
            CircuitBreaker(failure_threshold=0)

    def test_invalid_timeout_raises(self):
        with self.assertRaises(TypeError):
            CircuitBreaker(recovery_timeout="30")  # type: ignore[arg-type]
        with self.assertRaises(ValueError):
            CircuitBreaker(recovery_timeout=0)

    def test_invalid_expected_exception_raises(self):
        with self.assertRaises(TypeError):
            CircuitBreaker(expected_exception="ValueError")  # type: ignore[arg-type]

    def test_thread_safe_concurrent_failures(self):
        breaker = CircuitBreaker(failure_threshold=50)
        errors: list[BaseException] = []

        def worker() -> None:
            try:
                breaker.call(lambda: (_ for _ in ()).throw(ValueError("boom")))
            except ValueError as exc:
                errors.append(exc)

        threads = [threading.Thread(target=worker) for _ in range(50)]
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()
        self.assertEqual(len(errors), 50)
        self.assertEqual(breaker.state, CircuitBreaker.OPEN)
        self.assertEqual(breaker.failures, 50)


class TestCircuitOpenError(unittest.TestCase):
    def test_is_runtime_error(self):
        self.assertTrue(issubclass(CircuitOpenError, RuntimeError))
        err = CircuitOpenError("circuit open")
        self.assertEqual(str(err), "circuit open")


if __name__ == "__main__":
    unittest.main()
