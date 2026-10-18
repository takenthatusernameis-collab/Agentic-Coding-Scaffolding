"""Selectors utilities wrapping the standard library selectors module.

This module provides a validated wrapper around the standard library ``selectors``
module for I/O multiplexing: creating default selectors, registering and
unregistering file objects, selecting ready I/O, and inspecting selector state.
All functions validate their inputs and raise ``TypeError`` for invalid arguments.
"""

from __future__ import annotations

import selectors
from typing import Any, Optional

# Re-export the standard event masks for convenience.
EVENT_READ = selectors.EVENT_READ
EVENT_WRITE = selectors.EVENT_WRITE

# Bitmask of every event flag the standard library selectors module defines.
_ALL_EVENTS = selectors.EVENT_READ | selectors.EVENT_WRITE


def _validate_fileobj(value: Any, name: str) -> None:
    """Validate that *value* is a file object or integer file descriptor.

    Args:
        value: The value to validate.
        name: The name of the argument (used in error messages).

    Raises:
        TypeError: If value is neither an int nor an object with ``fileno``.
    """
    if isinstance(value, int):
        return
    if not hasattr(value, "fileno"):
        raise TypeError(f"{name} must be a file object or integer file descriptor")


def _validate_events(events: Any, name: str) -> None:
    """Validate that *events* is a non-negative combination of selector event flags.

    Args:
        events: The event mask to validate.
        name: The name of the argument (used in error messages).

    Raises:
        TypeError: If events is not an integer.
        ValueError: If events contains flags other than EVENT_READ/EVENT_WRITE.
    """
    if isinstance(events, bool) or not isinstance(events, int):
        raise TypeError(f"{name} must be an integer")
    if events < 0:
        raise ValueError(f"{name} must be non-negative")
    if events & ~_ALL_EVENTS:
        raise ValueError(f"{name} must only contain EVENT_READ and EVENT_WRITE")


def _validate_timeout(timeout: Any, name: str) -> None:
    """Validate that *timeout* is None or a non-negative real number.

    Args:
        timeout: The timeout value to validate.
        name: The name of the argument (used in error messages).

    Raises:
        TypeError: If timeout is not None or a real number.
        ValueError: If timeout is negative.
    """
    if timeout is None:
        return
    if isinstance(timeout, bool) or not isinstance(timeout, (int, float)):
        raise TypeError(f"{name} must be a number or None")
    if timeout < 0:
        raise ValueError(f"{name} must be non-negative")


def create_default_selector() -> selectors.DefaultSelector:
    """Return a new :class:`selectors.DefaultSelector` for the current platform.

    Returns:
        A default selector object ready for registrations.
    """
    return selectors.DefaultSelector()


def register(
    selector: selectors.BaseSelector,
    fileobj: Any,
    events: int,
    data: Optional[Any] = None,
) -> selectors.SelectorKey:
    """Register a file object with *selector* to be monitored for *events*.

    Args:
        selector: The selector to register with.
        fileobj: The file object (or integer file descriptor) to monitor.
        events: Event mask combining :data:`EVENT_READ` and/or :data:`EVENT_WRITE`.
        data: Optional opaque data to associate with the registration.

    Returns:
        A :class:`selectors.SelectorKey` describing the registration.

    Raises:
        TypeError: If selector is not a :class:`selectors.BaseSelector`, fileobj is
            invalid, or events is not an integer.
        ValueError: If events contains flags other than EVENT_READ/EVENT_WRITE.
    """
    if not isinstance(selector, selectors.BaseSelector):
        raise TypeError("selector must be a selectors.BaseSelector")
    _validate_fileobj(fileobj, "fileobj")
    _validate_events(events, "events")
    return selector.register(fileobj, events, data=data)


def unregister(selector: selectors.BaseSelector, fileobj: Any) -> selectors.SelectorKey:
    """Unregister a file object from *selector*.

    Args:
        selector: The selector to unregister from.
        fileobj: The file object (or integer file descriptor) to stop monitoring.

    Returns:
        The :class:`selectors.SelectorKey` that was removed.

    Raises:
        TypeError: If selector is not a :class:`selectors.BaseSelector` or fileobj
            is invalid.
        KeyError: If fileobj is not currently registered.
    """
    if not isinstance(selector, selectors.BaseSelector):
        raise TypeError("selector must be a selectors.BaseSelector")
    _validate_fileobj(fileobj, "fileobj")
    return selector.unregister(fileobj)


def select(
    selector: selectors.BaseSelector, timeout: Optional[float] = None
) -> list[tuple[selectors.SelectorKey, int]]:
    """Wait until some registered file objects are ready for I/O.

    Args:
        selector: The selector to wait on.
        timeout: Maximum time to wait in seconds (None blocks indefinitely).

    Returns:
        A list of ``(key, events)`` tuples for the file objects that are ready.

    Raises:
        TypeError: If selector is not a :class:`selectors.BaseSelector` or timeout
            is not a number or None.
        ValueError: If timeout is negative.
    """
    if not isinstance(selector, selectors.BaseSelector):
        raise TypeError("selector must be a selectors.BaseSelector")
    _validate_timeout(timeout, "timeout")
    return selector.select(timeout)


def get_key(selector: selectors.BaseSelector, fileobj: Any) -> selectors.SelectorKey:
    """Return the :class:`selectors.SelectorKey` for a registered file object.

    Args:
        selector: The selector to query.
        fileobj: The file object (or integer file descriptor) to look up.

    Returns:
        The selector key associated with *fileobj*.

    Raises:
        TypeError: If selector is not a :class:`selectors.BaseSelector` or fileobj
            is invalid.
        KeyError: If fileobj is not currently registered.
    """
    if not isinstance(selector, selectors.BaseSelector):
        raise TypeError("selector must be a selectors.BaseSelector")
    _validate_fileobj(fileobj, "fileobj")
    return selector.get_key(fileobj)


def get_map(selector: selectors.BaseSelector) -> dict[Any, selectors.SelectorKey]:
    """Return the mapping of registered file objects to their selector keys.

    Args:
        selector: The selector to query.

    Returns:
        A dictionary mapping file objects to :class:`selectors.SelectorKey` values.

    Raises:
        TypeError: If selector is not a :class:`selectors.BaseSelector`.
    """
    if not isinstance(selector, selectors.BaseSelector):
        raise TypeError("selector must be a selectors.BaseSelector")
    return dict(selector.get_map())


def close_selector(selector: selectors.BaseSelector) -> None:
    """Close *selector* and release any underlying resources.

    After calling this, the selector must not be used again.

    Args:
        selector: The selector to close.

    Raises:
        TypeError: If selector is not a :class:`selectors.BaseSelector`.
    """
    if not isinstance(selector, selectors.BaseSelector):
        raise TypeError("selector must be a selectors.BaseSelector")
    selector.close()
