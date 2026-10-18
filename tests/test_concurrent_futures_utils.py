import unittest
from concurrent.futures import Future, ThreadPoolExecutor

from concurrent_futures_utils import (
    FIRST_COMPLETED,
    FIRST_EXCEPTION,
    as_completed_iter,
    process_pool_executor,
    submit,
    thread_pool_executor,
    wait_futures,
)


def square(x: int) -> int:
    return x * x


class TestConcurrentFuturesUtils(unittest.TestCase):
    def test_thread_pool_executor(self):
        with thread_pool_executor(max_workers=2) as ex:
            f = submit(ex, square, 4)
            self.assertIsInstance(f, Future)
            self.assertEqual(f.result(), 16)

    def test_process_pool_executor(self):
        with process_pool_executor(max_workers=2) as ex:
            f = submit(ex, square, 5)
            self.assertEqual(f.result(), 25)

    def test_as_completed_iter(self):
        with thread_pool_executor(max_workers=2) as ex:
            fs = [submit(ex, square, i) for i in range(3)]
            results = []
            for f in as_completed_iter(fs):
                results.append(f.result())
            self.assertEqual(sorted(results), [0, 1, 4])

    def test_wait_futures(self):
        with thread_pool_executor(max_workers=2) as ex:
            fs = [submit(ex, square, i) for i in range(3)]
            done, not_done = wait_futures(fs)
            self.assertTrue(all(f.done() for f in done))
            self.assertEqual(len(not_done), 0)

    def test_constants_and_type_errors(self):
        self.assertEqual(FIRST_COMPLETED, "FIRST_COMPLETED")
        self.assertEqual(FIRST_EXCEPTION, "FIRST_EXCEPTION")
        with self.assertRaises(TypeError):
            thread_pool_executor(max_workers="2")  # type: ignore[arg-type]
        with self.assertRaises(ValueError):
            thread_pool_executor(max_workers=0)
        with self.assertRaises(TypeError):
            submit(ThreadPoolExecutor(), 123)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            as_completed_iter([], timeout="bad")  # type: ignore[arg-type]
        with self.assertRaises(ValueError):
            as_completed_iter([], timeout=-1)
        with self.assertRaises(ValueError):
            wait_futures([], return_when="BAD")


if __name__ == "__main__":
    unittest.main()
