"""Unit tests for async_utils module."""

import asyncio
import unittest
from typing import TypeVar

from async_utils import T, async_sleep, gather_with_timeout, retry_async, run_in_thread


class TestRunInThread(unittest.TestCase):
    def test_run_in_thread_basic(self):
        async def run_test():
            result = await run_in_thread(sum, [1, 2, 3, 4])
            self.assertEqual(result, 10)

        asyncio.run(run_test())

    def test_run_in_thread_with_kwargs(self):
        def multiply(a: int, b: int) -> int:
            return a * b

        async def run_test():
            result = await run_in_thread(multiply, a=3, b=4)
            self.assertEqual(result, 12)

        asyncio.run(run_test())


class TestGatherWithTimeout(unittest.TestCase):
    def test_gather_with_timeout_no_timeout(self):
        async def run_test():
            results = await gather_with_timeout(
                asyncio.sleep(0.01, result=1),
                asyncio.sleep(0.01, result=2),
                asyncio.sleep(0.01, result=3),
            )
            self.assertEqual(results, [1, 2, 3])

        asyncio.run(run_test())

    def test_gather_with_timeout_succeeds(self):
        async def run_test():
            results = await gather_with_timeout(
                asyncio.sleep(0.01, result="a"),
                asyncio.sleep(0.01, result="b"),
                timeout=1.0,
            )
            self.assertEqual(results, ["a", "b"])

        asyncio.run(run_test())


class TestAsyncSleep(unittest.TestCase):
    def test_async_sleep_completes(self):
        async def run_test():
            await async_sleep(0.001)
            self.assertTrue(True)

        asyncio.run(run_test())


class TestRetryAsync(unittest.TestCase):
    def test_retry_async_success_first_attempt(self):
        async def always_succeeds():
            return "ok"

        async def run_test():
            result = await retry_async(always_succeeds)
            self.assertEqual(result, "ok")

        asyncio.run(run_test())

    def test_retry_async_succeeds_after_failures(self):
        attempts = []

        async def flaky():
            attempts.append(1)
            if len(attempts) < 2:
                raise ValueError("failed")
            return "success"

        async def run_test():
            result = await retry_async(flaky, max_attempts=3, delay=0.001)
            self.assertEqual(result, "success")
            self.assertEqual(len(attempts), 2)

        asyncio.run(run_test())

    def test_retry_async_fails_all_attempts(self):
        async def always_fails():
            raise ValueError("always fails")

        async def run_test():
            with self.assertRaises(ValueError):
                await retry_async(always_fails, max_attempts=2, delay=0.001)

        asyncio.run(run_test())


class TestRetryAsyncValidation(unittest.IsolatedAsyncioTestCase):
    """retry_async must validate its arguments like retry_utils.retry."""

    async def test_rejects_bool_max_attempts(self):
        async def ok():
            return "ok"

        with self.assertRaises(TypeError):
            await retry_async(ok, max_attempts=True, delay=0)
        with self.assertRaises(TypeError):
            await retry_async(ok, max_attempts=False, delay=0)

    async def test_rejects_non_int_max_attempts(self):
        async def ok():
            return "ok"

        with self.assertRaises(TypeError):
            await retry_async(ok, max_attempts="3", delay=0)  # type: ignore[arg-type]

    async def test_rejects_zero_max_attempts(self):
        async def ok():
            return "ok"

        with self.assertRaises(ValueError):
            await retry_async(ok, max_attempts=0, delay=0)

    async def test_rejects_negative_max_attempts(self):
        async def ok():
            return "ok"

        with self.assertRaises(ValueError):
            await retry_async(ok, max_attempts=-1, delay=0)

    async def test_rejects_bool_delay(self):
        async def ok():
            return "ok"

        with self.assertRaises(TypeError):
            await retry_async(ok, max_attempts=2, delay=True)

    async def test_rejects_non_number_delay(self):
        async def ok():
            return "ok"

        with self.assertRaises(TypeError):
            await retry_async(ok, max_attempts=2, delay="0.1")  # type: ignore[arg-type]

    async def test_rejects_negative_delay(self):
        async def ok():
            return "ok"

        with self.assertRaises(ValueError):
            await retry_async(ok, max_attempts=2, delay=-0.1)

    async def test_rejects_nan_delay(self):
        async def ok():
            return "ok"

        with self.assertRaises(ValueError):
            await retry_async(ok, max_attempts=2, delay=float("nan"))

    async def test_rejects_infinite_delay(self):
        async def ok():
            return "ok"

        with self.assertRaises(ValueError):
            await retry_async(ok, max_attempts=2, delay=float("inf"))
        with self.assertRaises(ValueError):
            await retry_async(ok, max_attempts=2, delay=float("-inf"))


class TestExportedTypeVars(unittest.TestCase):
    def test_typevar_exported(self):
        self.assertIsInstance(T, TypeVar)
        self.assertEqual(T.__name__, "T")


if __name__ == "__main__":
    unittest.main()
