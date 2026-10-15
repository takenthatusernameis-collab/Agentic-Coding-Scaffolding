"""Concurrent execution utilities for parallel and asynchronous processing.

This module provides helpers for concurrent execution using threads, processes,
and asyncio, including ThreadPool, ProcessPool wrappers and asyncio utilities.
"""

import asyncio
import concurrent.futures
import functools
from typing import Any, Awaitable, Callable, Iterable, List, Optional, TypeVar, Union

T = TypeVar("T")
R = TypeVar("R")


class ThreadPool:
    """Context manager wrapper around ThreadPoolExecutor.

    Provides a simple interface for executing tasks in parallel using threads.

    Args:
        max_workers: The maximum number of worker threads to use.
        thread_name_prefix: An optional name prefix for worker threads.

    Examples:
        >>> with ThreadPool(max_workers=4) as pool:
        ...     results = pool.map(lambda x: x * 2, [1, 2, 3, 4])
        ...     print(list(results))
        [2, 4, 6, 8]

        >>> def square(x):
        ...     return x * x
        >>> with ThreadPool(max_workers=2) as pool:
        ...     future = pool.submit(square, 5)
        ...     print(future.result())
        25
    """

    def __init__(
        self,
        max_workers: Optional[int] = None,
        thread_name_prefix: str = "",
    ) -> None:
        self._max_workers = max_workers
        self._thread_name_prefix = thread_name_prefix
        self._executor: Optional[concurrent.futures.ThreadPoolExecutor] = None

    def __enter__(self) -> "ThreadPool":
        self._executor = concurrent.futures.ThreadPoolExecutor(
            max_workers=self._max_workers,
            thread_name_prefix=self._thread_name_prefix or "ThreadPool",
        )
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        if self._executor is not None:
            self._executor.shutdown(wait=True)

    def submit(
        self,
        fn: Callable[..., R],
        *args: Any,
        **kwargs: Any,
    ) -> concurrent.futures.Future[R]:
        """Submit a task to be executed asynchronously."""
        if self._executor is None:
            raise RuntimeError("ThreadPool must be used as a context manager")
        return self._executor.submit(fn, *args, **kwargs)

    def map(
        self,
        fn: Callable[[T], R],
        iterable: Iterable[T],
        timeout: Optional[float] = None,
    ) -> Iterable[R]:
        """Map a function over an iterable, executing in parallel."""
        if self._executor is None:
            raise RuntimeError("ThreadPool must be used as a context manager")
        return self._executor.map(fn, iterable, timeout=timeout)


class ProcessPool:
    """Context manager wrapper around ProcessPoolExecutor."""

    def __init__(
        self,
        max_workers: Optional[int] = None,
        mp_context: Any = None,
    ) -> None:
        self._max_workers = max_workers
        self._mp_context = mp_context
        self._executor: Optional[concurrent.futures.ProcessPoolExecutor] = None

    def __enter__(self) -> "ProcessPool":
        kwargs: Any = {}
        if self._max_workers is not None:
            kwargs["max_workers"] = self._max_workers
        if self._mp_context is not None:
            kwargs["mp_context"] = self._mp_context
        self._executor = concurrent.futures.ProcessPoolExecutor(**kwargs)
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        if self._executor is not None:
            self._executor.shutdown(wait=True)

    def submit(
        self,
        fn: Callable[..., R],
        *args: Any,
        **kwargs: Any,
    ) -> concurrent.futures.Future[R]:
        """Submit a task to be executed asynchronously."""
        if self._executor is None:
            raise RuntimeError("ProcessPool must be used as a context manager")
        return self._executor.submit(fn, *args, **kwargs)

    def map(
        self,
        fn: Callable[[T], R],
        iterable: Iterable[T],
        timeout: Optional[float] = None,
    ) -> Iterable[R]:
        """Map a function over an iterable, executing in parallel."""
        if self._executor is None:
            raise RuntimeError("ProcessPool must be used as a context manager")
        return self._executor.map(fn, iterable, timeout=timeout)


async def gather(*coroutines_or_futures: Union[Awaitable[R], R]) -> List[R]:
    """Run awaitable objects in the given sequence concurrently."""

    async def _ensure_awaitable(obj: Union[Awaitable[R], R]) -> R:
        if asyncio.iscoroutine(obj) or hasattr(obj, "__await__"):
            return await obj  # type: ignore[misc]
        return obj  # type: ignore[return-value]

    results = await asyncio.gather(*[_ensure_awaitable(obj) for obj in coroutines_or_futures])
    return list(results)


def run_async(coro: Awaitable[R]) -> R:
    """Run an async coroutine from synchronous code."""
    return asyncio.run(coro)  # type: ignore[arg-type]


def to_async(fn: Callable[..., Any]) -> Callable[..., Awaitable[Any]]:
    """Convert a synchronous function to an async function."""

    @functools.wraps(fn)
    async def async_wrapper(*args: Any, **kwargs: Any) -> Any:
        loop = asyncio.get_running_loop()
        # run_in_executor doesn't take kwargs directly; need to use partial
        return await loop.run_in_executor(None, functools.partial(fn, *args, **kwargs))

    return async_wrapper


# Module-level helper functions for ProcessPool examples/tests
def _square(x: int) -> int:
    return x * x


def _double(x: int) -> int:
    return x * 2


def _add(a: int, b: int) -> int:
    return a + b


def _multiply(a: int, b: int) -> int:
    return a * b


def _inc(x: int) -> int:
    return x + 1


def _dec(x: int) -> int:
    return x - 1


def _triple(x: int) -> int:
    return x * 3
