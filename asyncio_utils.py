"""Utilities wrapping the standard library ``asyncio`` module.

This module provides convenient helpers for running and composing
asynchronous programs using :mod:`asyncio`, including :func:`run`,
:func:`create_task`, :func:`gather`, :func:`sleep`, :func:`to_thread`,
and :func:`wait_for`, together with re-exports of the :class:`Event`,
:class:`Lock`, :class:`Queue`, and :class:`Semaphore` primitives.
"""

from __future__ import annotations

import asyncio as _asyncio
from typing import Any, Callable, Coroutine, Iterable, Optional, TypeVar

__all__: list[str] = [
    "all_tasks",
    "create_task",
    "current_task",
    "Event",
    "gather",
    "get_event_loop",
    "get_running_loop",
    "iscoroutine",
    "iscoroutinefunction",
    "Lock",
    "Queue",
    "run",
    "Semaphore",
    "sleep",
    "to_thread",
    "wait_for",
]

T = TypeVar("T")


def run(coro: Coroutine[Any, Any, T]) -> T:
    """Run *coro* and return its result.

    Args:
        coro: The coroutine to run.

    Returns:
        The result returned by *coro*.
    """
    return _asyncio.run(coro)


def create_task(coro: Coroutine[Any, Any, T]) -> _asyncio.Task:
    """Schedule *coro* as a :class:`~asyncio.Task`.

    Args:
        coro: The coroutine to schedule.

    Returns:
        The scheduled :class:`~asyncio.Task`.
    """
    return _asyncio.create_task(coro)


async def gather(*coros: Coroutine[Any, Any, Any]) -> list[Any]:
    """Run *coros* concurrently and return their results in order.

    Args:
        *coros: Coroutines to run concurrently.

    Returns:
        List of results in the same order as *coros*.
    """
    return await _asyncio.gather(*coros)


async def sleep(seconds: float) -> None:
    """Sleep for *seconds* without blocking the event loop.

    Args:
        seconds: Number of seconds to sleep.
    """
    await _asyncio.sleep(seconds)


async def to_thread(
    func: Callable[..., T], /, *args: Any, **kwargs: Any
) -> T:
    """Run *func* in a worker thread and return its result.

    Args:
        func: The blocking function to run.
        *args: Positional arguments for *func*.
        **kwargs: Keyword arguments for *func*.

    Returns:
        The result returned by *func*.
    """
    return await _asyncio.to_thread(func, *args, **kwargs)


async def wait_for(
    coro: Coroutine[Any, Any, T], timeout: Optional[float] = None
) -> T:
    """Wait for *coro* with an optional *timeout*.

    Args:
        coro: The coroutine to wait for.
        timeout: Maximum seconds to wait, or ``None`` to wait forever.

    Returns:
        The result returned by *coro*.

    Raises:
        asyncio.TimeoutError: If *timeout* is reached.
    """
    return await _asyncio.wait_for(coro, timeout=timeout)


def current_task() -> Optional[_asyncio.Task]:
    """Return the currently running :class:`~asyncio.Task`, or ``None``."""
    return _asyncio.current_task()


def all_tasks() -> Iterable[_asyncio.Task]:
    """Return all :class:`~asyncio.Task` instances known to the loop."""
    return _asyncio.all_tasks()


def iscoroutinefunction(obj: Any) -> bool:
    """Return ``True`` if *obj* is a coroutine function."""
    return _asyncio.iscoroutinefunction(obj)


def iscoroutine(obj: Any) -> bool:
    """Return ``True`` if *obj* is a coroutine."""
    return _asyncio.iscoroutine(obj)


Event = _asyncio.Event
Lock = _asyncio.Lock
Queue = _asyncio.Queue
Semaphore = _asyncio.Semaphore


def get_event_loop() -> _asyncio.AbstractEventLoop:
    """Return the running event loop, creating one if none is running.

    Returns:
        The running event loop, or a newly created event loop.
    """
    try:
        return _asyncio.get_running_loop()
    except RuntimeError:
        return _asyncio.new_event_loop()


def get_running_loop() -> _asyncio.AbstractEventLoop:
    """Return the running event loop.

    Returns:
        The currently running event loop.

    Raises:
        RuntimeError: If there is no running event loop.
    """
    return _asyncio.get_running_loop()
