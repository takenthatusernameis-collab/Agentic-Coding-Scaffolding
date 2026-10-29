"""Maybe/Option type utilities for functional programming patterns."""

from typing import Any, Callable, Generic, Optional, TypeVar

T = TypeVar("T")
U = TypeVar("U")
E = TypeVar("E")
V = TypeVar("V")


class Maybe(Generic[T]):
    """Represents an optional value that may or may not exist."""

    __slots__ = ("_value", "_is_some")

    def __init__(self, value: Optional[T] = None, is_some: bool = True) -> None:
        """Initialize a Maybe instance."""
        if value is None and is_some:
            self._is_some = False
            self._value = None
        else:
            self._is_some = is_some and value is not None
            self._value = value if self._is_some else None

    @classmethod
    def some(cls, value: V) -> "Maybe[V]":
        """Create a Some variant with a value."""
        if value is None:
            raise TypeError("Some cannot contain None")
        return cls(value, is_some=True)  # type: ignore[arg-type,return-value]

    @staticmethod
    def nothing() -> "Maybe[Any]":
        """Create a Nothing variant."""
        return Maybe(None, is_some=False)

    @staticmethod
    def from_optional(value: Optional[V]) -> "Maybe[V]":
        """Create Maybe from a Python optional value."""
        if value is None:
            return Maybe.nothing()
        return Maybe.some(value)

    def is_some(self) -> bool:
        """Check if this is a Some variant."""
        return self._is_some

    def is_nothing(self) -> bool:
        """Check if this is a Nothing variant."""
        return not self._is_some

    def unwrap(self) -> T:
        """Get the value, raising an error if Nothing."""
        if not self._is_some:
            raise ValueError("Called unwrap on Nothing")
        assert self._value is not None
        return self._value

    def map_or(self, default: U, fn: Callable[[T], U]) -> U:
        """Apply a function to the contained value if Some, otherwise return default.

        >>> Maybe.some(2).map_or(0, lambda x: x * 3)
        6
        >>> Maybe.nothing().map_or(0, lambda x: x * 3)
        0
        """
        if not self._is_some or self._value is None:
            return default
        try:
            result = fn(self._value)
            return default if result is None else result
        except Exception:
            return default

    def map_or_else(self, default_fn: Callable[[], U], fn: Callable[[T], U]) -> U:
        """Apply a function to the contained value if Some, otherwise compute default.

        >>> Maybe.some(2).map_or_else(lambda: 0, lambda x: x * 3)
        6
        >>> Maybe.nothing().map_or_else(lambda: 0, lambda x: x * 3)
        0
        """
        if not self._is_some or self._value is None:
            try:
                return default_fn()
            except Exception:
                raise
        try:
            result = fn(self._value)
            if result is None:
                return default_fn()
            return result
        except Exception:
            try:
                return default_fn()
            except Exception:
                raise

    def unwrap_or(self, default: T) -> T:
        """Get the value or return a default if Nothing."""
        if self._is_some and self._value is not None:
            return self._value
        return default

    def unwrap_or_else(self, fn: Callable[[], T]) -> T:
        """Get the value or compute a default if Nothing."""
        if self._is_some and self._value is not None:
            return self._value
        return fn()

    def map(self, fn: Callable[[T], U]) -> "Maybe[U]":
        """Apply a function if Some, otherwise return Nothing."""
        if not self._is_some or self._value is None:
            return Maybe.nothing()
        try:
            result = fn(self._value)
            if result is None:
                return Maybe.nothing()
            return Maybe.some(result)
        except Exception:
            return Maybe.nothing()

    def flat_map(self, fn: Callable[[T], "Maybe[U]"]) -> "Maybe[U]":
        """Chain a function returning Maybe."""
        if not self._is_some or self._value is None:
            return Maybe.nothing()
        try:
            return fn(self._value)
        except Exception:
            return Maybe.nothing()

    def filter(self, predicate: Callable[[T], bool]) -> "Maybe[T]":
        """Filter the value if it doesn't match the predicate."""
        if not self._is_some or self._value is None:
            return Maybe.nothing()
        try:
            if predicate(self._value):
                return Maybe.some(self._value)
            return Maybe.nothing()
        except Exception:
            return Maybe.nothing()

    def and_then(self, fn: Callable[[T], "Maybe[U]"]) -> "Maybe[U]":
        """Alias for flat_map."""
        return self.flat_map(fn)

    def or_else(self, other: "Maybe[T]") -> "Maybe[T]":
        """Return self if Some, otherwise other."""
        if self._is_some:
            return self
        return other

    def __repr__(self) -> str:
        """String representation."""
        if self._is_some and self._value is not None:
            return f"Some({self._value!r})"
        return "Nothing"

    def __bool__(self) -> bool:
        """Boolean conversion."""
        return self._is_some

    def __eq__(self, other: object) -> bool:
        """Equality comparison."""
        if not isinstance(other, Maybe):
            return NotImplemented
        if self._is_some != other._is_some:
            return False
        if not self._is_some:
            return True
        return self._value == other._value


__all__ = [
    "Maybe",
]
