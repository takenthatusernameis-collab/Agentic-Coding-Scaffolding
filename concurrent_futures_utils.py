"""Utilities for asynchronous execution (wrapping :mod:`concurrent.futures`).

This module provides a small, validated layer over the standard library
``concurrent.futures`` module for submitting work and managing executors.
All functions validate their inputs and raise ``TypeError`` or ``ValueError``
on invalid arguments.
"""

from concurrent.futures import (
    FIRST_COMPLETED,
    FIRST_EXCEPTION,
    Future,
    ProcessPoolExecutor,
    ThreadPoolExecutor,
    as_completed,
    wait,
)
from typing import Any, Callable, Iterable, Sequence, cast


def thread_pool_executor(max_workers: int | None = None, **kwargs: Any) -> ThreadPoolExecutor:
    """Return a :class:`~concurrent.futures.ThreadPoolExecutor`.

    Args:
        max_workers: Maximum number of worker threads.
        **kwargs: Additional arguments passed to the executor.

    Returns:
        A new ``ThreadPoolExecutor`` instance.

    Raises:
        TypeError: If ``max_workers`` is not an int or ``None``.
        ValueError: If ``max_workers`` is not positive (when provided).
    """
    if max_workers is not None and not isinstance(max_workers, int):
        raise TypeError("max_workers must be an int or None")
    if max_workers is not None and max_workers <= 0:
        raise ValueError("max_workers must be positive")
    return ThreadPoolExecutor(max_workers=max_workers, **kwargs)


def process_pool_executor(max_workers: int | None = None, **kwargs: Any) -> ProcessPoolExecutor:
    """Return a :class:`~concurrent.futures.ProcessPoolExecutor`.

    Args:
        max_workers: Maximum number of worker processes.
        **kwargs: Additional arguments passed to the executor.

    Returns:
        A new ``ProcessPoolExecutor`` instance.

    Raises:
        TypeError: If ``max_workers`` is not an int or ``None``.
        ValueError: If ``max_workers`` is not positive (when provided).
    """
    if max_workers is not None and not isinstance(max_workers, int):
        raise TypeError("max_workers must be an int or None")
    if max_workers is not None and max_workers <= 0:
        raise ValueError("max_workers must be positive")
    return ProcessPoolExecutor(max_workers=max_workers, **kwargs)


def submit(executor: Any, fn: Callable[..., Any], *args: Any, **kwargs: Any) -> Future[Any]:
    """Submit ``fn`` to ``executor`` and return a :class:`~concurrent.futures.Future`.

    Args:
        executor: An executor instance.
        fn: The function to execute.
        *args: Positional arguments for ``fn``.
        **kwargs: Keyword arguments for ``fn``.

    Returns:
        A ``Future`` representing the execution of ``fn``.

    Raises:
        TypeError: If ``fn`` is not callable.
    """
    if not callable(fn):
        raise TypeError("fn must be callable")
    return cast(Future[Any], executor.submit(fn, *args, **kwargs))


def as_completed_iter(
    fs: Iterable[Future[Any]], timeout: float | None = None
) -> Iterable[Future[Any]]:
    """Return an iterator over ``fs`` as they complete (alias to :func:`as_completed`).

    Args:
        fs: Iterable of ``Future`` objects.
        timeout: Maximum number of seconds to wait.

    Returns:
        An iterator of completed futures.

    Raises:
        TypeError: If ``timeout`` is not a float/int or ``None``.
        ValueError: If ``timeout`` is negative.
    """
    if timeout is not None:
        if not isinstance(timeout, (int, float)):
            raise TypeError("timeout must be a float, int, or None")
        if timeout < 0:
            raise ValueError("timeout must be non-negative")
    return as_completed(fs, timeout=timeout)


def wait_futures(
    fs: Sequence[Future[Any]], timeout: float | None = None, return_when: str = "ALL_COMPLETED"
) -> tuple[set[Future[Any]], set[Future[Any]]]:
    """Wait for ``fs`` to complete and return (done, not_done).

    Args:
        fs: Sequence of ``Future`` objects.
        timeout: Maximum number of seconds to wait.
        return_when: Condition to return; one of ``ALL_COMPLETED``,
            ``FIRST_COMPLETED``, ``FIRST_EXCEPTION``.

    Returns:
        A tuple ``(done, not_done)``.

    Raises:
        TypeError: If ``timeout`` is not a float/int or ``None``.
        ValueError: If ``timeout`` is negative or ``return_when`` is invalid.
    """
    if timeout is not None:
        if not isinstance(timeout, (int, float)):
            raise TypeError("timeout must be a float, int, or None")
        if timeout < 0:
            raise ValueError("timeout must be non-negative")
    if return_when not in {"ALL_COMPLETED", "FIRST_COMPLETED", "FIRST_EXCEPTION"}:
        raise ValueError(
            "return_when must be one of ALL_COMPLETED, FIRST_COMPLETED, FIRST_EXCEPTION"
        )
    return wait(fs, timeout=timeout, return_when=return_when)


__all__ = [
    "ThreadPoolExecutor",
    "ProcessPoolExecutor",
    "Future",
    "as_completed",
    "wait",
    "FIRST_COMPLETED",
    "FIRST_EXCEPTION",
    "thread_pool_executor",
    "process_pool_executor",
    "submit",
    "as_completed_iter",
    "wait_futures",
]
