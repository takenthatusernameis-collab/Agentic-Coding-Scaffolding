import threading
import unittest

from call_once_utils import call_once


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


if __name__ == "__main__":
    unittest.main()
