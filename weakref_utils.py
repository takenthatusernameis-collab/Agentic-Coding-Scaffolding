"""Weak reference utilities for managing weak references to objects."""

from __future__ import annotations

import weakref
from typing import Any, Callable, Generic, Optional, Protocol, TypeVar

T = TypeVar("T", bound=Any)


class BoundMethodProtocol(Protocol):
    __func__: Callable[..., Any]
    __self__: Any


class WeakRef(Generic[T]):
    """A simple wrapper for creating and accessing a weak reference.

    Args:
        obj: The object to weakly reference.

    Attributes:
        _ref: The underlying weakref.ref instance.
    """

    def __init__(self, obj: T) -> None:
        """Initialize a WeakRef for the given object.

        Args:
            obj: The object to weakly reference.
        """
        self._ref = weakref.ref(obj)

    def get(self) -> Optional[T]:
        """Return the referenced object if it still exists, otherwise None.

        Returns:
            The referenced object, or None if it has been garbage collected.
        """
        return self._ref()

    def is_alive(self) -> bool:
        """Check if the referenced object is still alive.

        Returns:
            True if the referenced object exists, False otherwise.
        """
        return self.get() is not None


class WeakMethod(Generic[T]):
    """A weak reference to a bound method.

    This prevents the object holding the bound method from keeping the target
    object alive indefinitely.

    Args:
        method: The bound method to weakly reference.
    """

    def __init__(self, method: Any) -> None:
        """Initialize a WeakMethod for the given bound method.

        Args:
            method: A bound method (e.g., instance.method).
        """
        self._func = weakref.ref(getattr(method, "__func__"))
        self._obj = weakref.ref(getattr(method, "__self__"))

    def get(self) -> Optional[Callable[..., Any]]:
        """Return the bound method if the target object is still alive.

        Returns:
            The bound method, or None if the target object has been garbage
            collected.
        """
        func = self._func()
        obj = self._obj()
        if func is None or obj is None:
            return None
        return func.__get__(obj, type(obj))  # type: ignore[no-any-return]

    def is_alive(self) -> bool:
        """Check if the target object is still alive.

        Returns:
            True if the target object exists, False otherwise.
        """
        return self.get() is not None


def create_weakref(obj: T) -> weakref.ref[T]:
    """Create a weak reference to an object.

    Args:
        obj: The object to weakly reference.

    Returns:
        A weakref.ref to the object.
    """
    return weakref.ref(obj)


def create_proxy(obj: T) -> Any:
    """Create a weak proxy to an object.

    A weak proxy behaves like the original object but does not prevent
    garbage collection. Accessing the proxy after the object is collected
    raises ReferenceError.

    Args:
        obj: The object to create a proxy for.

    Returns:
        A weakref.proxy to the object.
    """
    return weakref.proxy(obj)


def get_object(ref: weakref.ReferenceType[T]) -> Optional[T]:
    """Get the object from a weak reference if it still exists.

    Args:
        ref: A weak reference (weakref.ref, proxy, or custom).

    Returns:
        The referenced object, or None if it has been garbage collected.
    """
    # Check if it's a proxy
    if isinstance(ref, weakref.ProxyType):
        try:
            # Accessing the proxy to see if it's alive
            _ = ref.__class__.__name__  # trivial access
            return ref  # type: ignore[return-value]
        except ReferenceError:
            return None
    # Check if it's a ref
    try:
        result = ref() if callable(ref) else None
        return result
    except Exception:
        return None


def is_alive(ref: weakref.ReferenceType[T]) -> bool:
    """Check if a weak reference is still alive.

    Args:
        ref: A weak reference to check.

    Returns:
        True if the referenced object still exists, False otherwise.
    """
    obj = get_object(ref)
    return obj is not None


def create_finalizer(obj: Any, callback: Callable[..., Any]) -> weakref.finalize:
    """Create a finalizer that will call the callback when obj is garbage collected.

    Args:
        obj: The object to monitor for garbage collection.
        callback: The function to call when the object is collected.

    Returns:
        A weakref.finalize instance.
    """
    return weakref.finalize(obj, callback)
