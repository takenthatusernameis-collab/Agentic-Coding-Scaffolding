"""Deprecation utilities for marking APIs as deprecated.

This module provides a ``deprecated`` decorator that wraps a callable and emits
a ``DeprecationWarning`` each time the wrapped callable is invoked, along with
optional guidance about the deprecation version and a suggested replacement.
"""

from __future__ import annotations

import functools
import warnings
from typing import Any, Callable, Optional, TypeVar, Union, overload

T = TypeVar("T")


@overload
def deprecated(
    func: Callable[..., T],
    *,
    version: Optional[str] = None,
    replacement: Optional[str] = None,
    message: Optional[str] = None,
) -> Callable[..., T]: ...


@overload
def deprecated(
    func: None = None,
    *,
    version: Optional[str] = None,
    replacement: Optional[str] = None,
    message: Optional[str] = None,
) -> Callable[[Callable[..., T]], Callable[..., T]]: ...


def deprecated(
    func: Optional[Callable[..., T]] = None,
    *,
    version: Optional[str] = None,
    replacement: Optional[str] = None,
    message: Optional[str] = None,
) -> Union[Callable[..., T], Callable[[Callable[..., T]], Callable[..., T]]]:
    """Mark a callable as deprecated.

    Wraps ``func`` so that every call emits a ``DeprecationWarning`` describing
    the deprecation. The warning includes an optional version (when the
    deprecation was introduced), an optional replacement (what to use instead),
    and an optional custom message.

    Args:
        func: The callable to mark as deprecated. When provided positionally,
            the decorator is applied with default options.
        version: Version in which the deprecation was introduced (optional).
        replacement: Dotted name or description of the suggested replacement
            (optional).
        message: Custom deprecation message. When omitted, a default message is
            constructed from the function name and the optional version and
            replacement fields.

    Returns:
        A wrapped callable that emits a ``DeprecationWarning`` on every
        invocation and otherwise forwards all arguments and return values to
        ``func``.

    Raises:
        TypeError: If ``func`` is provided and is not callable.

    Example:
        >>> @deprecated(version="2.0", replacement="use greet() instead")
        ... def say_hello() -> str:
        ...     return "hello"
        >>> say_hello()  # doctest: +SKIP
        'hello'
    """

    def decorator(target: Callable[..., T]) -> Callable[..., T]:
        if not callable(target):
            raise TypeError("func must be callable")

        parts = [message or f"{target.__name__} is deprecated"]
        if version is not None:
            parts.append(f"(since version {version})")
        if replacement is not None:
            parts.append(f"use {replacement} instead")
        warning_message = " ".join(parts)

        @functools.wraps(target)
        def wrapper(*args: Any, **kwargs: Any) -> T:
            warnings.warn(
                warning_message,
                category=DeprecationWarning,
                stacklevel=2,
            )
            return target(*args, **kwargs)

        return wrapper

    # Support both @deprecated and @deprecated(version=..., ...).
    if func is not None:
        return decorator(func)
    return decorator
