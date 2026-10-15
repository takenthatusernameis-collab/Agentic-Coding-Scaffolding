"""Design pattern utilities.

This module provides reusable implementations of common software design
patterns: Singleton, Factory, Observer, and Strategy.
"""

from __future__ import annotations

import threading
from typing import Any, Callable, Dict, List, TypeVar

T = TypeVar("T")


class Singleton(type):
    """Metaclass that restricts a class to a single instance.

    Thread-safe: only one instance is created per class, even when multiple
    threads attempt construction concurrently.

    Example:
        >>> class Service(metaclass=Singleton):
        ...     pass
        >>> Service() is Service()
        True
    """

    _instances: Dict[type, Any] = {}
    _lock: threading.Lock = threading.Lock()

    def __call__(cls, *args, **kwargs):  # type: ignore[override]
        if cls not in Singleton._instances:
            with Singleton._lock:
                if cls not in Singleton._instances:
                    Singleton._instances[cls] = super().__call__(*args, **kwargs)
        return Singleton._instances[cls]


class SingletonBase(metaclass=Singleton):
    """Base class for classes that should have only one instance.

    Subclasses automatically share a single instance per subclass.
    """


class Factory:
    """Registry-based factory for creating objects by name.

    Creators are registered under a string key and invoked with any
    positional or keyword arguments when :meth:`create` is called.
    """

    def __init__(self) -> None:
        self._creators: Dict[str, Callable[..., Any]] = {}

    def register(self, name: str, creator: Callable[..., Any]) -> None:
        """Register a creator callable under ``name``.

        Args:
            name: Key used to look up the creator.
            creator: Callable used to create instances.

        Raises:
            TypeError: If ``creator`` is not callable.
        """
        if not callable(creator):
            raise TypeError("creator must be callable")
        self._creators[name] = creator

    def create(self, name: str, *args, **kwargs) -> Any:
        """Create and return an object registered under ``name``.

        Args:
            name: Key of the registered creator.
            args: Positional arguments forwarded to the creator.
            kwargs: Keyword arguments forwarded to the creator.

        Raises:
            KeyError: If no creator is registered for ``name``.
        """
        if name not in self._creators:
            raise KeyError(f"Unknown type: {name!r}")
        return self._creators[name](*args, **kwargs)

    def unregister(self, name: str) -> None:
        """Remove the creator registered under ``name``.

        Raises:
            KeyError: If no creator is registered for ``name``.
        """
        if name not in self._creators:
            raise KeyError(f"Unknown type: {name!r}")
        del self._creators[name]

    def types(self) -> List[str]:
        """Return the sorted list of registered creator names."""
        return sorted(self._creators)


class Observer:
    """Base class for observer objects.

    Subclasses implement :meth:`update` to react to changes in an
    :class:`Observable` subject.
    """

    def update(self, subject: Any, data: Any = None) -> None:
        """Called when the observed subject changes.

        Args:
            subject: The observable that changed.
            data: Optional data describing the change.
        """
        raise NotImplementedError


class Observable:
    """Subject that notifies registered observers of changes."""

    def __init__(self) -> None:
        self._observers: List[Observer] = []

    def attach(self, observer: Observer) -> None:
        """Register ``observer`` to receive change notifications.

        Args:
            observer: The observer to attach.

        Raises:
            TypeError: If ``observer`` is not an :class:`Observer` instance.
        """
        if not isinstance(observer, Observer):
            raise TypeError("observer must be an Observer instance")
        if observer in self._observers:
            return
        self._observers.append(observer)

    def detach(self, observer: Observer) -> None:
        """Unregister ``observer``.

        Raises:
            ValueError: If ``observer`` is not attached.
        """
        self._observers.remove(observer)

    def notify(self, data: Any = None) -> None:
        """Notify all attached observers with optional ``data``."""
        for observer in list(self._observers):
            observer.update(self, data)


class Strategy:
    """Base class for strategy objects.

    Subclasses implement :meth:`execute` to encapsulate an interchangeable
    algorithm.
    """

    def execute(self, *args, **kwargs) -> Any:
        """Execute the strategy algorithm.

        Args:
            args: Positional arguments for the algorithm.
            kwargs: Keyword arguments for the algorithm.

        Returns:
            The result of the algorithm.
        """
        raise NotImplementedError


class StrategyContext:
    """Context that delegates work to a pluggable :class:`Strategy`."""

    def __init__(self, strategy: Strategy) -> None:
        """Initialize the context with ``strategy``.

        Args:
            strategy: The strategy to delegate to.

        Raises:
            TypeError: If ``strategy`` is not a :class:`Strategy` instance.
        """
        if not isinstance(strategy, Strategy):
            raise TypeError("strategy must be a Strategy instance")
        self._strategy = strategy

    @property
    def strategy(self) -> Strategy:
        """The currently configured strategy."""
        return self._strategy

    @strategy.setter
    def strategy(self, strategy: Strategy) -> None:
        """Replace the current strategy.

        Raises:
            TypeError: If ``strategy`` is not a :class:`Strategy` instance.
        """
        if not isinstance(strategy, Strategy):
            raise TypeError("strategy must be a Strategy instance")
        self._strategy = strategy

    def execute(self, *args, **kwargs) -> Any:
        """Delegate to the current strategy."""
        return self._strategy.execute(*args, **kwargs)
