import threading
import unittest

from threading_utils import (
    active_count,
    create_bounded_semaphore,
    create_condition,
    create_event,
    create_lock,
    create_rlock,
    create_semaphore,
    create_thread,
    create_timer,
    current_thread,
    enumerate_threads,
    synchronized,
)


class TestLocks(unittest.TestCase):
    def test_create_lock(self):
        lock = create_lock()
        self.assertIsInstance(lock, type(threading.Lock()))

    def test_create_rlock(self):
        lock = create_rlock()
        self.assertIsInstance(lock, type(threading.RLock()))


class TestSemaphores(unittest.TestCase):
    def test_create_semaphore_default(self):
        sem = create_semaphore()
        self.assertIsInstance(sem, threading.Semaphore)

    def test_create_semaphore_value(self):
        sem = create_semaphore(3)
        self.assertTrue(sem.acquire())
        self.assertTrue(sem.acquire())
        self.assertTrue(sem.acquire())
        self.assertFalse(sem.acquire(blocking=False))

    def test_create_bounded_semaphore(self):
        sem = create_bounded_semaphore(1)
        self.assertIsInstance(sem, threading.BoundedSemaphore)

    def test_create_semaphore_invalid(self):
        with self.assertRaises(TypeError):
            create_semaphore(-1)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            create_semaphore("1")  # type: ignore[arg-type]


class TestEvent(unittest.TestCase):
    def test_create_event(self):
        event = create_event()
        self.assertIsInstance(event, threading.Event)
        self.assertFalse(event.is_set())
        event.set()
        self.assertTrue(event.is_set())
        event.clear()
        self.assertFalse(event.is_set())


class TestCondition(unittest.TestCase):
    def test_create_condition_default(self):
        cond = create_condition()
        self.assertIsInstance(cond, threading.Condition)

    def test_create_condition_with_lock(self):
        lock = create_lock()
        cond = create_condition(lock)
        self.assertIsInstance(cond, threading.Condition)

    def test_create_condition_invalid_lock(self):
        with self.assertRaises(TypeError):
            create_condition("not a lock")  # type: ignore[arg-type]


class TestTimer(unittest.TestCase):
    def test_create_timer(self):
        called = []

        def callback() -> None:
            called.append(True)

        timer = create_timer(0.01, callback)
        self.assertIsInstance(timer, threading.Timer)
        timer.cancel()

    def test_create_timer_invalid(self):
        with self.assertRaises(TypeError):
            create_timer(-1, lambda: None)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            create_timer(0.01, "not callable")  # type: ignore[arg-type]


class TestThread(unittest.TestCase):
    def test_create_thread(self):
        results = []

        def worker() -> None:
            results.append(1)

        thread = create_thread(worker)
        self.assertIsInstance(thread, threading.Thread)
        thread.start()
        thread.join()
        self.assertEqual(results, [1])

    def test_create_thread_with_args(self):
        results = []

        def worker(a, b=0) -> None:
            results.append(a + b)

        thread = create_thread(worker, args=(2,), kwargs={"b": 3})
        thread.start()
        thread.join()
        self.assertEqual(results, [5])

    def test_create_thread_daemon(self):
        thread = create_thread(lambda: None, daemon=True)
        self.assertTrue(thread.daemon)

    def test_create_thread_invalid(self):
        with self.assertRaises(TypeError):
            create_thread("not callable")  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            create_thread(lambda: None, name=123)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            create_thread(lambda: None, daemon="yes")  # type: ignore[arg-type]


class TestIntrospection(unittest.TestCase):
    def test_current_thread(self):
        thread = current_thread()
        self.assertIsInstance(thread, threading.Thread)

    def test_active_count(self):
        self.assertGreaterEqual(active_count(), 1)

    def test_enumerate_threads(self):
        threads = enumerate_threads()
        self.assertIsInstance(threads, list)
        self.assertGreaterEqual(len(threads), 1)
        self.assertIn(current_thread(), threads)


class TestSynchronized(unittest.TestCase):
    def test_synchronized_serializes(self):
        lock = create_lock()
        results = []

        @synchronized(lock)
        def worker(value: int) -> int:
            results.append(value)
            return value

        threads = [threading.Thread(target=lambda v=i: worker(v)) for i in range(10)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        self.assertEqual(sorted(results), list(range(10)))

    def test_synchronized_default_lock(self):
        @synchronized()
        def worker(value: int) -> int:
            return value

        self.assertEqual(worker(42), 42)

    def test_synchronized_invalid_lock(self):
        with self.assertRaises(TypeError):
            synchronized("not a lock")  # type: ignore[arg-type]


if __name__ == "__main__":
    unittest.main()
