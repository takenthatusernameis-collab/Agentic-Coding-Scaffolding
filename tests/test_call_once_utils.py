import threading
import unittest
from typing import TypeVar

from call_once_utils import T, call_once


class TestCallOnce(unittest.TestCase):
    def test_func_called_once(self):
        calls = []

        @call_once
        def get_value(x: int) -> int:
            calls.append(x)
            return x * 2

        self.assertEqual(get_value(5), 10)
        # Later calls return the cached result and ignore new arguments.
        self.assertEqual(get_value(99), 10)
        self.assertEqual(len(calls), 1)

    def test_reset_allows_recall(self):
        calls = []

        @call_once
        def get_value() -> int:
            calls.append(1)
            return len(calls)

        self.assertEqual(get_value(), 1)
        self.assertEqual(get_value(), 1)
        get_value.reset()
        self.assertEqual(get_value(), 2)
        self.assertEqual(len(calls), 2)

    def test_thread_safe_single_invocation(self):
        results = []

        @call_once
        def init() -> str:
            results.append(threading.current_thread().name)
            return "done"

        def worker() -> None:
            results.append(init())

        threads = [threading.Thread(target=worker) for _ in range(10)]
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()
        # Every caller observes the same single result.
        self.assertEqual([r for r in results if r == "done"], ["done"] * 10)

    def test_non_callable_raises(self):
        with self.assertRaises(TypeError):
            call_once(42)  # type: ignore[arg-type]

    def test_exception_is_cached_not_re_invoked(self):
        """A raising first call must not be retried on the next call.

        ``call_once`` guarantees the wrapped body runs at most once, so when the
        single invocation raises, that exception is cached and re-raised to
        later callers without re-invoking ``func``.
        """
        calls = []

        @call_once
        def failing() -> int:
            calls.append(1)
            raise ValueError("boom")

        with self.assertRaises(ValueError):
            failing()
        with self.assertRaises(ValueError):
            failing()
        # The wrapped body was invoked exactly once despite both calls raising.
        self.assertEqual(len(calls), 1)

    def test_reset_allows_fresh_invocation_after_exception(self):
        """``reset`` clears a cached exception so the next call re-invokes."""
        calls = []

        @call_once
        def flaky() -> int:
            calls.append(1)
            if len(calls) == 1:
                raise ValueError("first attempt fails")
            return len(calls)

        with self.assertRaises(ValueError):
            flaky()
        flaky.reset()
        self.assertEqual(flaky(), 2)
        self.assertEqual(len(calls), 2)


class TestExportedTypeVars(unittest.TestCase):
    def test_typevar_exported(self):
        self.assertIsInstance(T, TypeVar)
        self.assertEqual(T.__name__, "T")


if __name__ == "__main__":
    unittest.main()
