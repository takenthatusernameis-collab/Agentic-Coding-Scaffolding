"""Tests for concurrent_utils module."""

import asyncio
import unittest

from concurrent_utils import (
    ProcessPool,
    ThreadPool,
    _dec,
    _double,
    _multiply,
    _square,
    gather,
    run_async,
    to_async,
)


class TestThreadPool(unittest.TestCase):
    def test_threadpool_map(self):
        with ThreadPool(max_workers=2) as pool:
            results = list(pool.map(lambda x: x * 2, [1, 2, 3, 4]))
        self.assertEqual(results, [2, 4, 6, 8])

    def test_threadpool_submit(self):
        def square(x):
            return x * x

        with ThreadPool(max_workers=2) as pool:
            future = pool.submit(square, 5)
            result = future.result()
        self.assertEqual(result, 25)

    def test_threadpool_submit_multiple(self):
        def add(a, b):
            return a + b

        with ThreadPool(max_workers=3) as pool:
            f1 = pool.submit(add, 1, 2)
            f2 = pool.submit(add, 3, 4)
            f3 = pool.submit(add, 5, 6)
            self.assertEqual(f1.result(), 3)
            self.assertEqual(f2.result(), 7)
            self.assertEqual(f3.result(), 11)

    def test_threadpool_default_workers(self):
        with ThreadPool() as pool:
            results = list(pool.map(lambda x: x + 1, [1, 2, 3]))
        self.assertEqual(results, [2, 3, 4])

    def test_threadpool_with_name_prefix(self):
        with ThreadPool(max_workers=2, thread_name_prefix="test") as pool:
            results = list(pool.map(lambda x: x * 3, [1, 2]))
        self.assertEqual(results, [3, 6])

    def test_threadpool_submit_outside_context_raises(self):
        pool = ThreadPool(max_workers=2)
        with self.assertRaises(RuntimeError):
            pool.submit(lambda x: x, 1)

    def test_threadpool_map_outside_context_raises(self):
        pool = ThreadPool(max_workers=2)
        with self.assertRaises(RuntimeError):
            list(pool.map(lambda x: x, [1, 2]))


class TestProcessPool(unittest.TestCase):
    def test_processpool_map(self):
        with ProcessPool(max_workers=2) as pool:
            results = list(pool.map(_double, [1, 2, 3, 4]))
        self.assertEqual(results, [2, 4, 6, 8])

    def test_processpool_submit(self):
        with ProcessPool(max_workers=2) as pool:
            future = pool.submit(_square, 5)
            result = future.result()
        self.assertEqual(result, 25)

    def test_processpool_submit_multiple(self):
        with ProcessPool(max_workers=3) as pool:
            f1 = pool.submit(_multiply, 2, 3)
            f2 = pool.submit(_multiply, 4, 5)
            f3 = pool.submit(_multiply, 6, 7)
            self.assertEqual(f1.result(), 6)
            self.assertEqual(f2.result(), 20)
            self.assertEqual(f3.result(), 42)

    def test_processpool_default_workers(self):
        with ProcessPool() as pool:
            results = list(pool.map(_dec, [5, 6, 7]))
        self.assertEqual(results, [4, 5, 6])

    def test_processpool_submit_outside_context_raises(self):
        pool = ProcessPool(max_workers=2)
        with self.assertRaises(RuntimeError):
            pool.submit(_square, 1)

    def test_processpool_map_outside_context_raises(self):
        pool = ProcessPool(max_workers=2)
        with self.assertRaises(RuntimeError):
            list(pool.map(_square, [1, 2]))


class TestAsyncIOWrappers(unittest.TestCase):
    def test_gather_basic(self):
        async def compute(x):
            await asyncio.sleep(0.001)
            return x * 2

        async def main():
            results = await gather(compute(1), compute(2), compute(3))
            return results

        results = run_async(main())
        self.assertEqual(results, [2, 4, 6])

    def test_gather_with_mixed_values(self):
        async def async_func(x):
            return x + 1

        async def main():
            results = await gather(async_func(1), 10, async_func(3))
            return results

        results = run_async(main())
        self.assertEqual(results, [2, 10, 4])

    def test_gather_empty(self):
        async def main():
            results = await gather()
            return results

        results = run_async(main())
        self.assertEqual(results, [])

    def test_run_async_basic(self):
        async def get_data():
            return "test_data"

        result = run_async(get_data())
        self.assertEqual(result, "test_data")

    def test_run_async_with_exception(self):
        async def fail():
            raise ValueError("test error")

        with self.assertRaises(ValueError):
            run_async(fail())

    def test_to_async_basic(self):
        def compute(x):
            return x * 3

        async def main():
            async_compute = to_async(compute)
            result = await async_compute(4)
            return result

        result = run_async(main())
        self.assertEqual(result, 12)

    def test_to_async_with_multiple_args(self):
        def add(a, b, c):
            return a + b + c

        async def main():
            async_add = to_async(add)
            result = await async_add(1, 2, 3)
            return result

        result = run_async(main())
        self.assertEqual(result, 6)

    def test_to_async_with_kwargs(self):
        def multiply(a, b=1):
            return a * b

        async def main():
            async_multiply = to_async(multiply)
            result = await async_multiply(5, b=3)
            return result

        result = run_async(main())
        self.assertEqual(result, 15)

    def test_to_async_preserves_metadata(self):
        def original_func():
            """Original docstring."""
            return "test"

        async def main():
            wrapped = to_async(original_func)
            self.assertEqual(wrapped.__name__, "original_func")
            self.assertEqual(wrapped.__doc__, "Original docstring.")
            return await wrapped()

        result = run_async(main())
        self.assertEqual(result, "test")


if __name__ == "__main__":
    unittest.main()
