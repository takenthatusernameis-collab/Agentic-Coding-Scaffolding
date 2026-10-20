"""I/O multiplexing utilities (wrapping :mod:`select`).

The :mod:`select` module provides direct access to the operating system's
I/O multiplexing primitives. This wrapper exposes a small, validated surface
over :func:`select.select` and the :class:`select.poll` object so callers can
wait for file descriptors to become readable or writable without having to
remember the exact argument order or error types of the standard library.
"""

from __future__ import annotations

import select as _select
from typing import List, Optional, Sequence, Tuple

__all__ = [
    "PIPE_BUF",
    "create_poller",
    "poll_poll",
    "poll_register",
    "select",
]


def _require_list(value: object, name: str) -> List[int]:
    """Return *value* when it is a list of integers, otherwise raise."""
    if not isinstance(value, list):
        raise TypeError(f"{name} must be a list, got {type(value).__name__}")
    for index, item in enumerate(value):
        if isinstance(item, bool) or not isinstance(item, int):
            raise TypeError(
                f"{name}[{index}] must be an int, got {type(item).__name__}"
            )
    return value


def _require_optional_number(
    value: object, name: str
) -> Optional[float]:
    """Return *value* as a float when it is a number or None, otherwise raise."""
    if value is None:
        return None
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise TypeError(f"{name} must be a number or None, got {type(value).__name__}")
    if value < 0:
        raise ValueError(f"{name} must not be negative")
    return float(value)


def _require_int(value: object, name: str) -> int:
    """Return *value* when it is a non-bool int, otherwise raise."""
    if isinstance(value, bool) or not isinstance(value, int):
        raise TypeError(f"{name} must be an int, got {type(value).__name__}")
    return value


def select(
    rlist: Sequence[int],
    wlist: Sequence[int],
    xlist: Sequence[int],
    timeout: Optional[float] = None,
) -> Tuple[List[int], List[int], List[int]]:
    """Wait for I/O completion on a set of file descriptors.

    Wraps :func:`select.select` with input validation. Returns three lists
    of file descriptors that are ready for reading, writing, or have an
    exceptional condition, respectively.

    Args:
        rlist: File descriptors to wait for readability.
        wlist: File descriptors to wait for writability.
        xlist: File descriptors to wait for exceptional conditions.
        timeout: Maximum time to wait in seconds, or ``None`` to block
            indefinitely.

    Returns:
        A tuple ``(readable, writable, exceptional)`` of file descriptor
        lists.

    Raises:
        TypeError: If any descriptor list is not a list of ints, or if
            *timeout* is not a number or None.
        ValueError: If *timeout* is negative.
        OSError: If an underlying descriptor is invalid or the call fails.

    Examples:
        >>> import os
        >>> read_fd, write_fd = os.pipe()
        >>> readable, writable, exceptional = select([read_fd], [], [], 0)
        >>> readable == []
        True
        >>> os.close(read_fd)
        >>> os.close(write_fd)
    """
    reads = _require_list(rlist, "rlist")
    writes = _require_list(wlist, "wlist")
    exceptions = _require_list(xlist, "xlist")
    timeout_value = _require_optional_number(timeout, "timeout")
    readable, writable, exceptional = _select.select(
        reads, writes, exceptions, timeout_value
    )
    return list(readable), list(writable), list(exceptional)


def create_poller() -> _select.poll:
    """Create a new poll object.

    Returns:
        A :class:`select.poll` instance ready to have file descriptors
        registered with :func:`poll_register`.

    Raises:
        AttributeError: If the platform does not provide ``select.poll``.
    """
    return _select.poll()


def poll_register(poller: _select.poll, fd: int, events: int) -> None:
    """Register a file descriptor with a poll object.

    Args:
        poller: A :class:`select.poll` instance.
        fd: The file descriptor to register.
        events: The event mask (e.g. ``select.POLLIN`` or ``select.POLLOUT``).

    Raises:
        TypeError: If *poller* has no ``register`` method, or *fd*/*events*
            are not ints.
        OSError: If *fd* is invalid.
    """
    if not hasattr(poller, "register"):
        raise TypeError(
            "poller must be a select.poll-like object with a register method"
        )
    file_descriptor = _require_int(fd, "fd")
    event_mask = _require_int(events, "events")
    poller.register(file_descriptor, event_mask)


def poll_poll(
    poller: _select.poll, timeout: Optional[float] = None
) -> List[Tuple[int, int]]:
    """Poll a poll object for registered events.

    Args:
        poller: A :class:`select.poll` instance.
        timeout: Maximum time to wait in seconds, or ``None`` to block.

    Returns:
        A list of ``(fd, event)`` pairs for descriptors with pending events.

    Raises:
        TypeError: If *poller* has no ``poll`` method or *timeout* is invalid.
        ValueError: If *timeout* is negative.
    """
    if not hasattr(poller, "poll"):
        raise TypeError(
            "poller must be a select.poll-like object with a poll method"
        )
    timeout_value = _require_optional_number(timeout, "timeout")
    return poller.poll(timeout_value)


PIPE_BUF = _select.PIPE_BUF
