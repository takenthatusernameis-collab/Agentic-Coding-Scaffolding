"""Utilities for working with Python's atexit module.

This module provides convenient wrappers around stdlib `atexit` functions
for registering, unregistering, and managing exit handlers.
"""

from __future__ import annotations

import atexit
from typing import Any, Callable


def register(func: Callable[..., Any], *args: Any, **kwargs: Any) -> Callable[..., Any]:
    """Register a function to be called at program exit.

    Args:
        func: The function to register as an exit handler.
        *args: Positional arguments to pass to func when called.
        **kwargs: Keyword arguments to pass to func when called.

    Returns:
        The registered function (unchanged).

    Raises:
        TypeError: If func is not callable.
    """
    if not callable(func):
        raise TypeError("func must be callable")
    atexit.register(func, *args, **kwargs)
    return func


def unregister(func: Callable[..., Any]) -> bool:
    """Unregister an exit handler function.

    Args:
        func: The function to unregister.

    Returns:
        True if the function was successfully unregistered, False otherwise.

    Raises:
        TypeError: If func is not callable.
    """
    if not callable(func):
        raise TypeError("func must be callable")
    try:
        # atexit.unregister only exists in Python 3.7+, but we target modern Python
        atexit.unregister(func)
        return True
    except (ValueError, AttributeError):
        # If function not registered or unregister not available
        return False


def clear() -> None:
    """Clear all registered exit handlers.

    This removes all functions registered via atexit.register.
    Note: This affects the global atexit state for the current process.
    """
    try:
        # Clear handlers by unregistering all - but we need to track them
        # atexit doesn't provide a direct clear; alternative approach
        atexit._clear()  # type: ignore[attr-defined]
    except (AttributeError, Exception):
        # Fallback: not all Python implementations expose _clear
        # In practice, we can only unregister what we know; but for this util,
        # try to reset by manipulating internal state if available
        pass


def get_registered() -> list[Callable[..., Any]]:
    """Get a list of registered exit handler functions.

    Returns:
        A list of callable functions currently registered as exit handlers.

    Note:
        This relies on internal implementation details of atexit module.
        The exact content and order may vary by Python implementation.
    """
    try:
        # Access internal handlers list
        return list(getattr(atexit, "_exithandlers", []))  # type: ignore[attr-defined]
    except Exception:
        return []


def run_exit_handlers() -> None:
    """Run all registered exit handlers immediately.

    This executes all exit handlers in reverse order of registration,
    similar to what happens at normal program exit. After running,
    handlers are typically removed depending on implementation, but
    behavior may vary.
    """
    atexit._run_exitfuncs()  # type: ignore[attr-defined]


# Convenience function aliases
def add(func: Callable[..., Any], *args: Any, **kwargs: Any) -> Callable[..., Any]:
    """Alias for register()."""
    return register(func, *args, **kwargs)


def remove(func: Callable[..., Any]) -> bool:
    """Alias for unregister()."""
    return unregister(func)


__all__ = [
    "register",
    "unregister",
    "clear",
    "get_registered",
    "run_exit_handlers",
    "add",
    "remove",
]
