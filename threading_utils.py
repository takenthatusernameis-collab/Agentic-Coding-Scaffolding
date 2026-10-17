"""Threading utilities wrapping the standard library threading module.

This module provides a validated wrapper around the standard library ``threading``
module for lock, semaphore, event, condition, timer, and thread operations. All
functions validate their inputs and raise ``TypeError`` for invalid arguments.
"""

from __future__ import annotations

import threading
from typing import Any, Callable, Optional, TypeVar

T = TypeVar("T")

# threading.Lock is a factory function, not a class, so capture the actual lock type.
_LockType = type(threading.Lock())


def _validate_callable(value: Any, name: str) -> None:
    """Validate that *value* is callable, raising ``TypeError`` otherwise.

    Args:
        value: The value to validate.
        name: The name of the argument (used in error messages).

    Raises:
        TypeError: If value is not callable.
    """
    if not callable(value):
        raise TypeError(f"{name} must be callable")


def _validate_positive_int(value: Any, name: str) -> None:
    """Validate that *value* is a positive integer, raising ``TypeError`` otherwise.

    Args:
        value: The value to validate.
        name: The name of the argument (used in error messages).

    Raises:
        TypeError: If value is not a positive integer.
    """
    if isinstance(value, bool) or not isinstance(value, int) or value < 1:
        raise TypeError(f"{name} must be a positive integer")


def _validate_non_negative_int(value: Any, name: str) -> None:
    """Validate that *value* is a non-negative integer, raising ``TypeError`` otherwise.

    Args:
        value: The value to validate.
        name: The name of the argument (used in error messages).

    Raises:
        TypeError: If value is not a non-negative integer.
    """
    if isinstance(value, bool) or not isinstance(value, int) or value < 0:
        raise TypeError(f"{name} must be a non-negative integer")


def _validate_non_negative_float(value: Any, name: str) -> None:
    """Validate that *value* is a non-negative real number, raising ``TypeError`` otherwise.

    Args:
        value: The value to validate.
        name: The name of the argument (used in error messages).

    Raises:
        TypeError: If value is not a non-negative int or float.
    """
    if isinstance(value, bool) or not isinstance(value, (int, float)) or value < 0:
        raise TypeError(f"{name} must be a non-negative number")


def create_lock() -> threading.Lock:
    """Return a new :class:`threading.Lock`.

    Returns:
        An unlocked lock object.
    """
    return threading.Lock()


def create_rlock() -> threading.RLock:
    """Return a new :class:`threading.RLock` (reentrant lock).

    Returns:
        An unlocked reentrant lock object.
    """
    return threading.RLock()


def create_semaphore(value: int = 1) -> threading.Semaphore:
    """Return a new :class:`threading.Semaphore` with the given initial value.

    Args:
        value: The initial internal counter (default: 1).

    Returns:
        A semaphore object.

    Raises:
        TypeError: If value is not a non-negative integer.

    Examples:
        >>> sem = create_semaphore(2)
        >>> sem.acquire()
        True
        >>> sem.acquire()
        True
        >>> sem.acquire(blocking=False)
        False
    """
    _validate_non_negative_int(value, "value")
    return threading.Semaphore(value)


def create_bounded_semaphore(value: int = 1) -> threading.BoundedSemaphore:
    """Return a new :class:`threading.BoundedSemaphore` with the given initial value.

    Args:
        value: The initial internal counter (default: 1).

    Returns:
        A bounded semaphore object.

    Raises:
        TypeError: If value is not a non-negative integer.
    """
    _validate_non_negative_int(value, "value")
    return threading.BoundedSemaphore(value)


def create_event() -> threading.Event:
    """Return a new :class:`threading.Event` with its internal flag set to false.

    Returns:
        An event object.
    """
    return threading.Event()


def create_condition(lock: Optional[threading.Lock] = None) -> threading.Condition:
    """Return a new :class:`threading.Condition` using the given lock.

    Args:
        lock: An optional lock to use. If omitted, a new lock is created.

    Returns:
        A condition variable object.

    Raises:
        TypeError: If lock is not a :class:`threading.Lock` or ``None``.
    """
    if lock is not None and not isinstance(lock, _LockType):
        raise TypeError("lock must be a threading.Lock or None")
    return threading.Condition(lock=lock)


def create_timer(
    interval: float,
    function: Callable[..., None],
    args: Optional[tuple] = None,
    kwargs: Optional[dict] = None,
) -> threading.Timer:
    """Return a new :class:`threading.Timer` that runs *function* after *interval* seconds.

    Args:
        interval: The number of seconds to wait before calling *function*.
        function: The callable to invoke after the interval.
        args: Optional positional arguments to pass to *function*.
        kwargs: Optional keyword arguments to pass to *function*.

    Returns:
        A timer object (not yet started).

    Raises:
        TypeError: If interval is not a non-negative number or function is not callable.

    Examples:
        >>> timer = create_timer(0.01, lambda: None)
        >>> timer.cancel()
    """
    _validate_non_negative_float(interval, "interval")
    _validate_callable(function, "function")
    return threading.Timer(interval, function, args=args or (), kwargs=kwargs or {})


def create_thread(
    target: Callable[..., T],
    args: Optional[tuple] = None,
    kwargs: Optional[dict] = None,
    name: Optional[str] = None,
    daemon: bool = False,
) -> threading.Thread:
    """Return a new :class:`threading.Thread` configured with the given settings.

    Args:
        target: The callable to invoke in the new thread.
        args: Optional positional arguments to pass to *target*.
        kwargs: Optional keyword arguments to pass to *target*.
        name: Optional thread name.
        daemon: Whether the thread is a daemon thread (default: False).

    Returns:
        A thread object (not yet started).

    Raises:
        TypeError: If target is not callable, name is not a string or None, or daemon is not a bool.
    """
    _validate_callable(target, "target")
    if name is not None and not isinstance(name, str):
        raise TypeError("name must be a string or None")
    if not isinstance(daemon, bool):
        raise TypeError("daemon must be a bool")
    return threading.Thread(
        target=target, args=args or (), kwargs=kwargs or {}, name=name, daemon=daemon
    )


def current_thread() -> threading.Thread:
    """Return the :class:`threading.Thread` object corresponding to the caller's thread.

    Returns:
        The current thread object.
    """
    return threading.current_thread()


def active_count() -> int:
    """Return the number of :class:`threading.Thread` objects currently alive.

    Returns:
        The count of alive threads (including the caller).
    """
    return threading.active_count()


def enumerate_threads() -> list[threading.Thread]:
    """Return a list of all :class:`threading.Thread` objects currently alive.

    Returns:
        A list of alive thread objects.
    """
    return list(threading.enumerate())


def synchronized(
    lock: Optional[threading.Lock] = None,
) -> Callable[[Callable[..., T]], Callable[..., T]]:
    """Return a decorator that serializes calls to a function using a lock.

    Args:
        lock: An optional lock to use. If omitted, a new lock is created per decorated function.

    Returns:
        A decorator that wraps *func* so concurrent calls are serialized.

    Raises:
        TypeError: If lock is not a :class:`threading.Lock` or ``None``.
    """
    if lock is None:
        lock = threading.Lock()
    elif not isinstance(lock, _LockType):
        raise TypeError("lock must be a threading.Lock or None")

    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        def wrapper(*args: Any, **kwargs: Any) -> T:
            with lock:
                return func(*args, **kwargs)

        return wrapper

    return decorator
