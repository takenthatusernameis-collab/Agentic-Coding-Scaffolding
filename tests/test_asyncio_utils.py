"""Tests for asyncio_utils module."""

import asyncio
import unittest

from asyncio_utils import (
    Event,
    Lock,
    Queue,
    Semaphore,
    all_tasks,
    create_task,
    current_task,
    gather,
    get_event_loop,
    get_running_loop,
    iscoroutine,
    iscoroutinefunction,
    run,
    sleep,
    to_thread,
    wait_for,
)


class TestRun(unittest.TestCase):
    def test_run_coroutine_returns_result(self):
        async def get_value():
            return 42

        self.assertEqual(run(get_value()), 42)


class TestCreateTask(unittest.IsolatedAsyncioTestCase):
    async def test_create_task_returns_result(self):
        async def get_value():
            return 7

        task = create_task(get_value())
        self.assertIsInstance(task, asyncio.Task)
        self.assertEqual(await task, 7)


class TestGather(unittest.IsolatedAsyncioTestCase):
    async def test_gather_returns_results_in_order(self):
        async def value(n):
            return n

        results = await gather(value(1), value(2), value(3))
        self.assertEqual(results, [1, 2, 3])


class TestSleep(unittest.IsolatedAsyncioTestCase):
    async def test_sleep_returns_none(self):
        self.assertIsNone(await sleep(0))


class TestToThread(unittest.IsolatedAsyncioTestCase):
    async def test_to_thread_runs_function(self):
        def add(a, b):
            return a + b

        result = await to_thread(add, 2, 3)
        self.assertEqual(result, 5)


class TestWaitFor(unittest.IsolatedAsyncioTestCase):
    async def test_wait_for_returns_result(self):
        async def get_value():
            return 9

        self.assertEqual(await wait_for(get_value(), timeout=10), 9)

    async def test_wait_for_times_out(self):
        async def never():
            await asyncio.Event().wait()

        with self.assertRaises(asyncio.TimeoutError):
            await wait_for(never(), timeout=0.01)


class TestPrimitives(unittest.TestCase):
    def test_event_lock_queue_semaphore(self):
        self.assertIsInstance(Event(), asyncio.Event)
        self.assertIsInstance(Lock(), asyncio.Lock)
        self.assertIsInstance(Queue(), asyncio.Queue)
        self.assertIsInstance(Semaphore(), asyncio.Semaphore)


class TestIntrospection(unittest.TestCase):
    def test_iscoroutinefunction_and_iscoroutine(self):
        async def foo():
            return 1

        self.assertTrue(iscoroutinefunction(foo))
        self.assertTrue(iscoroutine(foo()))
        self.assertFalse(iscoroutinefunction(len))
        self.assertFalse(iscoroutine(1))


class TestTasks(unittest.IsolatedAsyncioTestCase):
    async def test_current_task(self):
        task = current_task()
        self.assertIsInstance(task, asyncio.Task)

    async def test_all_tasks(self):
        tasks = list(all_tasks())
        self.assertIsInstance(tasks, list)


class TestLoops(unittest.IsolatedAsyncioTestCase):
    async def test_get_running_loop(self):
        loop = get_running_loop()
        self.assertIsInstance(loop, asyncio.AbstractEventLoop)

    def test_get_event_loop(self):
        loop = get_event_loop()
        self.assertIsInstance(loop, asyncio.AbstractEventLoop)


if __name__ == "__main__":
    unittest.main()
