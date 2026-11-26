"""Tests for cooldown_utils module."""

import threading
import time
import unittest
from typing import ParamSpec, TypeVar

from cooldown_utils import Cooldown, P, T, cooldown, format_remaining, is_available


class TestIsAvailable(unittest.TestCase):
    def test_is_available(self) -> None:
        self.assertTrue(is_available())


class TestCooldownInit(unittest.TestCase):
    def test_positive_interval(self) -> None:
        cd = Cooldown(1.0)
        self.assertIsInstance(cd, Cooldown)

    def test_integer_interval(self) -> None:
        cd = Cooldown(1)
        self.assertEqual(cd._interval, 1.0)

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

    def test_nan_interval_raises(self) -> None:
        with self.assertRaises(ValueError):
            Cooldown(float("nan"))

    def test_infinite_interval_raises(self) -> None:
        with self.assertRaises(ValueError):
            Cooldown(float("inf"))
        with self.assertRaises(ValueError):
            Cooldown(float("-inf"))


class TestCooldownReady(unittest.TestCase):
    def test_ready_initially(self) -> None:
        cd = Cooldown(1.0)
        self.assertTrue(cd.ready())

    def test_not_ready_immediately(self) -> None:
        cd = Cooldown(1.0)
        cd.call(lambda: None)
        self.assertFalse(cd.ready())

    def test_ready_after_interval(self) -> None:
        cd = Cooldown(0.01)
        cd.call(lambda: None)
        time.sleep(0.015)
        self.assertTrue(cd.ready())


class TestCooldownReset(unittest.TestCase):
    def test_reset_clears_last_call(self) -> None:
        cd = Cooldown(1.0)
        cd.call(lambda: None)
        self.assertFalse(cd.ready())
        cd.reset()
        self.assertTrue(cd.ready())
        self.assertEqual(cd.remaining(), 0.0)


class TestCooldownRemaining(unittest.TestCase):
    def test_remaining_zero_initially(self) -> None:
        cd = Cooldown(1.0)
        self.assertEqual(cd.remaining(), 0.0)

    def test_remaining_after_call(self) -> None:
        cd = Cooldown(1.0)
        cd.call(lambda: None)
        self.assertGreater(cd.remaining(), 0.0)
        self.assertLessEqual(cd.remaining(), 1.0)

    def test_remaining_zero_after_interval(self) -> None:
        cd = Cooldown(0.01)
        cd.call(lambda: None)
        time.sleep(0.015)
        self.assertEqual(cd.remaining(), 0.0)


class TestCooldownCall(unittest.TestCase):
    def test_call_executes_func(self) -> None:
        cd = Cooldown(1.0)
        calls = []

        def func() -> None:
            calls.append(1)

        cd.call(func)
        self.assertEqual(calls, [1])

    def test_call_returns_result(self) -> None:
        cd = Cooldown(1.0)
        result = cd.call(lambda: 42)
        self.assertEqual(result, 42)

    def test_call_passes_arguments(self) -> None:
        cd = Cooldown(1.0)
        result = cd.call(lambda a, b: a + b, 2, 3)
        self.assertEqual(result, 5)

    def test_call_rejects_before_interval(self) -> None:
        cd = Cooldown(1.0)
        cd.call(lambda: None)
        with self.assertRaises(TimeoutError):
            cd.call(lambda: None)

    def test_call_allows_after_interval(self) -> None:
        cd = Cooldown(0.01)
        cd.call(lambda: None)
        time.sleep(0.015)
        cd.call(lambda: None)

    def test_call_non_callable_raises(self) -> None:
        cd = Cooldown(1.0)
        with self.assertRaises(TypeError):
            cd.call("not callable")  # type: ignore[arg-type]


class TestCooldownDecorator(unittest.TestCase):
    def test_decorator_wraps_function(self) -> None:
        calls = []

        @cooldown(0.1)
        def func() -> None:
            calls.append(1)

        func()
        with self.assertRaises(TimeoutError):
            func()
        self.assertEqual(len(calls), 1)

    def test_decorator_allows_after_interval(self) -> None:
        calls = []

        @cooldown(0.01)
        def func() -> None:
            calls.append(1)

        func()
        time.sleep(0.015)
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

    def test_decorator_rejects_non_callable_at_decoration_time(self) -> None:
        with self.assertRaises(TypeError):
            cooldown(1.0)(42)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            cooldown(1.0)("not callable")  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            cooldown(1.0)([])  # type: ignore[arg-type]


class TestCooldownThreadSafety(unittest.TestCase):
    def test_concurrent_calls_respect_interval(self) -> None:
        cd = Cooldown(0.2)
        results: list[float] = []
        lock = threading.Lock()

        def call() -> None:
            try:
                cd.call(lambda: None)
                with lock:
                    results.append(time.monotonic())
            except TimeoutError:
                pass

        threads = [threading.Thread(target=call) for _ in range(10)]
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()

        self.assertLessEqual(len(results), 1)


class TestFormatRemaining(unittest.TestCase):
    def test_zero(self) -> None:
        self.assertEqual(format_remaining(0), "0.000s")

    def test_rounding(self) -> None:
        self.assertEqual(format_remaining(1.2345), "1.234s")

    def test_int(self) -> None:
        self.assertEqual(format_remaining(5), "5.000s")

    def test_type_error(self) -> None:
        with self.assertRaises(TypeError):
            format_remaining("1")  # type: ignore[arg-type]

    def test_bool_type_error(self) -> None:
        with self.assertRaises(TypeError):
            format_remaining(True)  # type: ignore[arg-type]

    def test_negative_value_error(self) -> None:
        with self.assertRaises(ValueError):
            format_remaining(-1.0)

    def test_nan_value_error(self) -> None:
        with self.assertRaises(ValueError):
            format_remaining(float("nan"))

    def test_infinite_value_error(self) -> None:
        with self.assertRaises(ValueError):
            format_remaining(float("inf"))
        with self.assertRaises(ValueError):
            format_remaining(float("-inf"))


class TestExportedTypeVars(unittest.TestCase):
    def test_typevars_exported(self):
        self.assertIsInstance(T, TypeVar)
        self.assertEqual(T.__name__, "T")
        self.assertIsInstance(P, ParamSpec)
        self.assertEqual(P.__name__, "P")


if __name__ == "__main__":
    unittest.main()
