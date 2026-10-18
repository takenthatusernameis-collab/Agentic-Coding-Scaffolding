"""Utilities for working with Python's multiprocessing module.

This module provides convenient wrappers around stdlib `multiprocessing` functions
for creating pools, managing processes, and sharing data safely.
"""

from __future__ import annotations

import multiprocessing as mp
from multiprocessing import Queue as MPQueue
from typing import Any, Callable, Iterable, Sequence


def get_context(method: str | None = None) -> Any:
    """Get a multiprocessing context.

    Args:
        method: The start method ('spawn', 'fork', 'forkserver') or None for default.

    Returns:
        A multiprocessing context.

    Raises:
        TypeError: If method is not a string or None.
        ValueError: If method is not a valid start method.
    """
    if method is not None and not isinstance(method, str):
        raise TypeError("method must be a string or None")
    return mp.get_context(method)  # type: ignore[call-overload]


def cpu_count() -> int:
    """Get the number of CPUs available.

    Returns:
        Number of CPUs.
    """
    return mp.cpu_count()


def active_children() -> list[Any]:
    """Get list of active child processes.

    Returns:
        List of Process objects.
    """
    return mp.active_children()


def current_process() -> Any:
    """Get the current process object.

    Returns:
        Current Process object.
    """
    return mp.current_process()


def freeze_support() -> None:
    """Call freeze_support for Windows executables."""
    mp.freeze_support()


# Pool utilities
def create_pool(processes: int | None = None, context: str | None = None) -> mp.pool.Pool:
    """Create a process pool.

    Args:
        processes: Number of worker processes (None for cpu_count()).
        context: Start method context name.

    Returns:
        A Pool instance.

    Raises:
        TypeError: If inputs are not of expected types.
    """
    if processes is not None and not isinstance(processes, int):
        raise TypeError("processes must be an int or None")
    if context is not None and not isinstance(context, str):
        raise TypeError("context must be a string or None")
    ctx = get_context(context) if context else mp.get_context()
    return ctx.Pool(processes=processes)


def pool_map(
    func: Callable[..., Any],
    iterable: Iterable[Any],
    chunksize: int | None = None,
    processes: int | None = None,
) -> list[Any]:
    """Map a function over an iterable using a process pool.

    Args:
        func: Function to apply.
        iterable: Iterable of arguments.
        chunksize: Size of chunks for each process.
        processes: Number of processes.

    Returns:
        List of results.

    Raises:
        TypeError: If func is not callable.
    """
    if not callable(func):
        raise TypeError("func must be callable")
    if chunksize is not None and not isinstance(chunksize, int):
        raise TypeError("chunksize must be an int or None")
    with create_pool(processes=processes) as pool:
        return pool.map(func, iterable, chunksize=chunksize)


def pool_starmap(
    func: Callable[..., Any],
    iterable: Iterable[Sequence[Any]],
    chunksize: int | None = None,
    processes: int | None = None,
) -> list[Any]:
    """Starmap using process pool.

    Args:
        func: Function to apply.
        iterable: Iterable of argument tuples.
        chunksize: Chunk size.
        processes: Number of processes.

    Returns:
        List of results.

    Raises:
        TypeError: If func is not callable.
    """
    if not callable(func):
        raise TypeError("func must be callable")
    if chunksize is not None and not isinstance(chunksize, int):
        raise TypeError("chunksize must be an int or None")
    with create_pool(processes=processes) as pool:
        return pool.starmap(func, iterable, chunksize=chunksize)


# Queue utilities
def create_queue(maxsize: int = 0, context: str | None = None) -> mp.Queue:
    """Create a multiprocessing Queue.

    Args:
        maxsize: Maximum queue size (0 means unlimited).
        context: Context name.

    Returns:
        Queue instance.

    Raises:
        TypeError: If maxsize is not an int.
    """
    if not isinstance(maxsize, int):
        raise TypeError("maxsize must be an int")
    ctx = get_context(context) if context else mp.get_context()
    return ctx.Queue(maxsize)


def create_simple_queue(context: str | None = None) -> mp.SimpleQueue:
    """Create a SimpleQueue.

    Args:
        context: Context name.

    Returns:
        SimpleQueue instance.
    """
    ctx = get_context(context) if context else mp.get_context()
    return ctx.SimpleQueue()


# Lock utilities
def create_lock(context: str | None = None) -> Any:
    """Create a Lock.

    Args:
        context: Context name.

    Returns:
        Lock instance.
    """
    ctx = get_context(context) if context else mp.get_context()
    return ctx.Lock()


def create_rlock(context: str | None = None) -> Any:
    """Create an RLock.

    Args:
        context: Context name.

    Returns:
        RLock instance.
    """
    ctx = get_context(context) if context else mp.get_context()
    return ctx.RLock()


def create_semaphore(value: int = 1, context: str | None = None) -> Any:
    """Create a Semaphore.

    Args:
        value: Initial value.
        context: Context name.

    Returns:
        Semaphore instance.

    Raises:
        TypeError: If value is not an int.
    """
    if not isinstance(value, int):
        raise TypeError("value must be an int")
    ctx = get_context(context) if context else mp.get_context()
    return ctx.Semaphore(value)


def create_event(context: str | None = None) -> Any:
    """Create an Event.

    Args:
        context: Context name.

    Returns:
        Event instance.
    """
    ctx = get_context(context) if context else mp.get_context()
    return ctx.Event()


def create_condition(lock: Any = None, context: str | None = None) -> Any:
    """Create a Condition.

    Args:
        lock: Optional lock to use.
        context: Context name.

    Returns:
        Condition instance.

    Raises:
        TypeError: If lock is not a Lock/RLock or None.
    """
    if lock is not None and not isinstance(lock, (mp.Lock, mp.RLock)):  # type: ignore[arg-type]
        raise TypeError("lock must be a Lock, RLock, or None")
    ctx = get_context(context) if context else mp.get_context()
    return ctx.Condition(lock)


# Shared memory utilities
def create_value(
    typecode_or_type: Any,
    *args: Any,
    lock: Any = True,
    context: str | None = None,
) -> Any:
    """Create a shared value.

    Args:
        typecode_or_type: Type code or type.
        *args: Initializer args.
        lock: Whether to use lock.
        context: Context name.

    Returns:
        Shared value.

    Raises:
        TypeError: If lock is invalid type.
    """
    if not isinstance(lock, (bool, mp.Lock, mp.RLock)):  # type: ignore[arg-type]
        raise TypeError("lock must be bool or Lock/RLock")
    ctx = get_context(context) if context else mp.get_context()
    return ctx.Value(typecode_or_type, *args, lock=lock)


def create_array(
    typecode_or_type: Any,
    size_or_initializer: Any,
    *,
    lock: Any = True,
    context: str | None = None,
) -> Any:
    """Create a shared array.

    Args:
        typecode_or_type: Type code.
        size_or_initializer: Size or initializer sequence.
        lock: Lock setting.
        context: Context name.

    Returns:
        Shared array.

    Raises:
        TypeError: If lock is invalid type.
    """
    if not isinstance(lock, (bool, mp.Lock, mp.RLock)):  # type: ignore[arg-type]
        raise TypeError("lock must be bool or Lock/RLock")
    ctx = get_context(context) if context else mp.get_context()
    return ctx.Array(typecode_or_type, size_or_initializer, lock=lock)


# Process utilities
def create_process(
    target: Callable[..., Any] | None = None,
    args: Iterable[Any] = (),
    kwargs: dict[str, Any] | None = None,
    name: str | None = None,
    daemon: bool | None = None,
    context: str | None = None,
) -> mp.Process:
    """Create a Process.

    Args:
        target: Target function.
        args: Positional args.
        kwargs: Keyword args.
        name: Process name.
        daemon: Daemon flag.
        context: Context name.

    Returns:
        Process instance.

    Raises:
        TypeError: If target is not callable or None.
    """
    if target is not None and not callable(target):
        raise TypeError("target must be callable or None")
    ctx = get_context(context) if context else mp.get_context()
    return ctx.Process(
        target=target,
        args=tuple(args),
        kwargs=kwargs or {},
        name=name,
        daemon=daemon,
    )


def run_in_process(
    func: Callable[..., Any],
    *args: Any,
    timeout: float | None = None,
    context: str | None = None,
) -> Any:
    """Run a function in a separate process and return its result.

    Args:
        func: Function to run.
        *args: Arguments.
        timeout: Timeout in seconds.
        context: Context name.

    Returns:
        Result of func.

    Raises:
        TypeError: If func is not callable.
        multiprocessing.TimeoutError: If timeout exceeded.
    """
    if not callable(func):
        raise TypeError("func must be callable")
    if timeout is not None and not isinstance(timeout, (int, float)):
        raise TypeError("timeout must be a number or None")

    result_queue: MPQueue = create_queue(context=context)
    p = create_process(target=_worker, args=(func, args, result_queue), context=context)
    p.start()
    try:
        result = result_queue.get(timeout=timeout)
        if isinstance(result, Exception):
            raise result
        return result
    finally:
        p.join(timeout=0.1)
        if p.is_alive():
            p.terminate()
            p.join()


def _worker(func: Callable[..., Any], args: tuple[Any, ...], q: MPQueue) -> None:
    try:
        q.put(func(*args))
    except Exception as e:
        q.put(e)


def is_forking() -> bool:
    """Check if current start method is fork."""
    return mp.get_start_method() == "fork"


def is_spawn() -> bool:
    """Check if current start method is spawn."""
    return mp.get_start_method() == "spawn"


def is_forkserver() -> bool:
    """Check if current start method is forkserver."""
    return mp.get_start_method() == "forkserver"


__all__ = [
    "get_context",
    "cpu_count",
    "active_children",
    "current_process",
    "freeze_support",
    "create_pool",
    "pool_map",
    "pool_starmap",
    "create_queue",
    "create_simple_queue",
    "create_lock",
    "create_rlock",
    "create_semaphore",
    "create_event",
    "create_condition",
    "create_value",
    "create_array",
    "create_process",
    "run_in_process",
    "is_forking",
    "is_spawn",
    "is_forkserver",
]
