"""Tests for cooldown_utils module."""

import threading
import time
import unittest

from cooldown_utils import Cooldown, cooldown, is_available


class TestIsAvailable(unittest.TestCase):
    def test_is_available(self) -> None:
        self.assertTrue(is_available())


class TestCooldownInit(unittest.TestCase):
    def test_positive_interval(self) -> None:
        cooldown = Cooldown(1.0)
        self.assertIsInstance(cooldown, Cooldown)

    def test_integer_interval(self) -> None:
        cooldown = Cooldown(1)
        self.assertEqual(cooldown._interval, 1.0)

    def test_zero_interval_raises(self) -> None:
        with self.assertRaises(ValueError):
            Cooldown(0)

    def test_negative_interval_raises(self) -> None:
        with self.assertRaises(ValueError):
            Cooldown(-1.0)

    def test_bool_interval_raises(self) -> None:
        with self.assertRaises(TypeError):
            Cooldown(True)

    def test_string_interval_raises(self) -> None:
        with self.assertRaises(TypeError):
            Cooldown("1.0")  # type: ignore[arg-type]


class TestCooldownReady(unittest.TestCase):
    def test_ready_initially(self) -> None:
        cooldown = Cooldown(1.0)
        self.assertTrue(cooldown.ready())

    def test_not_ready_immediately(self) -> None:
        cooldown = Cooldown(1.0)
        cooldown.call(lambda: None)
        self.assertFalse(cooldown.ready())

    def test_ready_after_interval(self) -> None:
        cooldown = Cooldown(0.1)
        cooldown.call(lambda: None)
        time.sleep(0.15)
        self.assertTrue(cooldown.ready())


class TestCooldownRemaining(unittest.TestCase):
    def test_remaining_zero_initially(self) -> None:
        cooldown = Cooldown(1.0)
        self.assertEqual(cooldown.remaining(), 0.0)

    def test_remaining_after_call(self) -> None:
        cooldown = Cooldown(1.0)
        cooldown.call(lambda: None)
        self.assertGreater(cooldown.remaining(), 0.0)
        self.assertLessEqual(cooldown.remaining(), 1.0)

    def test_remaining_zero_after_interval(self) -> None:
        cooldown = Cooldown(0.1)
        cooldown.call(lambda: None)
        time.sleep(0.15)
        self.assertEqual(cooldown.remaining(), 0.0)


class TestCooldownCall(unittest.TestCase):
    def test_call_executes_func(self) -> None:
        cooldown = Cooldown(1.0)
        calls = []

        def func() -> None:
            calls.append(1)

        cooldown.call(func)
        self.assertEqual(calls, [1])

    def test_call_returns_result(self) -> None:
        cooldown = Cooldown(1.0)
        result = cooldown.call(lambda: 42)
        self.assertEqual(result, 42)

    def test_call_passes_arguments(self) -> None:
        cooldown = Cooldown(1.0)
        result = cooldown.call(lambda a, b: a + b, 2, 3)
        self.assertEqual(result, 5)

    def test_call_rejects_before_interval(self) -> None:
        cooldown = Cooldown(1.0)
        cooldown.call(lambda: None)
        with self.assertRaises(TimeoutError):
            cooldown.call(lambda: None)

    def test_call_allows_after_interval(self) -> None:
        cooldown = Cooldown(0.1)
        cooldown.call(lambda: None)
        time.sleep(0.15)
        cooldown.call(lambda: None)

    def test_call_non_callable_raises(self) -> None:
        cooldown = Cooldown(1.0)
        with self.assertRaises(TypeError):
            cooldown.call("not callable")  # type: ignore[arg-type]


class TestCooldownDecorator(unittest.TestCase):
    def test_decorator_wraps_function(self) -> None:
        calls = []

        @cooldown(0.1)
        def func() -> None:
            calls.append(1)

        func()
        func()
        self.assertEqual(len(calls), 1)

    def test_decorator_allows_after_interval(self) -> None:
        calls = []

        @cooldown(0.1)
        def func() -> None:
            calls.append(1)

        func()
        time.sleep(0.15)
        func()
        self.assertEqual(len(calls), 2)

    def test_decorator_raises_before_interval(self) -> None:
        calls = []

        @cooldown(1.0)
        def func() -> None:
            calls.append(1)

        func()
        with self.assertRaises(TimeoutError):
            func()
        self.assertEqual(len(calls), 1)

    def test_decorator_preserves_arguments(self) -> None:
        @cooldown(1.0)
        def add(a: int, b: int) -> int:
            return a + b

        self.assertEqual(add(2, 3), 5)


class TestCooldownThreadSafety(unittest.TestCase):
    def test_concurrent_calls_respect_interval(self) -> None:
        cooldown = Cooldown(0.2)
        results: list[float] = []
        lock = threading.Lock()

        def call() -> None:
            try:
                cooldown.call(lambda: None)
                with lock:
                    results.append(time.monotonic())
            except TimeoutError:
                pass

        threads = [threading.Thread(target=call) for _ in range(10)]
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()

        # At most one call should succeed in quick succession.
        self.assertLessEqual(len(results), 1)


if __name__ == "__main__":
    unittest.main()
