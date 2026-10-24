"""Either/Result type utilities for functional programming patterns."""

from typing import Any, Callable, Generic, Optional, TypeVar, cast

L = TypeVar("L")
R = TypeVar("R")
T = TypeVar("T")
U = TypeVar("U")
E = TypeVar("E")


class Either(Generic[L, R]):
    """Represents a value of one of two possible types (Left or Right)."""

    __slots__ = ("_value", "_is_right")

    def __init__(self, value: Any, is_right: bool = True) -> None:
        """Initialize an Either instance."""
        self._is_right = bool(is_right)
        self._value = value

    @classmethod
    def right(cls, value: R) -> "Either[Any, R]":
        """Create a Right variant (success/value case)."""
        return cls(value, is_right=True)

    @classmethod
    def left(cls, value: L) -> "Either[L, Any]":
        """Create a Left variant (error/failure case)."""
        return cls(value, is_right=False)

    @staticmethod
    def ok(value: R) -> "Either[Any, R]":
        """Alias for right."""
        return Either.right(value)

    @staticmethod
    def err(value: L) -> "Either[L, Any]":
        """Alias for left."""
        return Either.left(value)

    @staticmethod
    def from_optional(
        value: Optional[R], left_value: L
    ) -> "Either[L, R]":
        """Create Either from optional value."""
        if value is None:
            return Either.left(left_value)
        return Either.right(value)

    def is_right(self) -> bool:
        """Check if this is a Right variant."""
        return self._is_right

    def is_left(self) -> bool:
        """Check if this is a Left variant."""
        return not self._is_right

    def is_ok(self) -> bool:
        """Alias for is_right."""
        return self.is_right()

    def is_err(self) -> bool:
        """Alias for is_left."""
        return self.is_left()

    def unwrap(self) -> R:
        """Get the right value, raising an error if Left."""
        if not self._is_right:
            raise ValueError(f"Called unwrap on Left: {self._value!r}")
        return cast(R, self._value)

    def unwrap_left(self) -> L:
        """Get the left value, raising an error if Right."""
        if self._is_right:
            raise ValueError(f"Called unwrap_left on Right: {self._value!r}")
        return cast(L, self._value)

    def unwrap_or(self, default: R) -> R:
        """Get the right value or return a default if Left."""
        if self._is_right:
            return cast(R, self._value)
        return default

    def unwrap_or_else(self, fn: Callable[[L], R]) -> R:
        """Get the right value or compute from left if Left."""
        if self._is_right:
            return cast(R, self._value)
        return fn(self._value)

    def map(self, fn: Callable[[R], U]) -> "Either[L, U]":
        """Apply a function if Right, otherwise return Left unchanged."""
        if not self._is_right:
            return Either(self._value, is_right=False)
        try:
            result = fn(self._value)
            return Either.right(result)
        except Exception as e:
            return Either.left(cast(L, e))

    def map_left(self, fn: Callable[[L], T]) -> "Either[T, R]":
        """Apply a function if Left, otherwise return Right unchanged."""
        if self._is_right:
            return Either(self._value, is_right=True)
        try:
            result = fn(self._value)
            return Either.left(result)
        except Exception as e:
            return Either.left(cast(T, e))

    def flat_map(self, fn: Callable[[R], "Either[L, U]"]) -> "Either[L, U]":
        """Apply a function returning Either if Right, otherwise return Left."""
        if not self._is_right:
            return Either(self._value, is_right=False)
        try:
            result = fn(self._value)
            if isinstance(result, Either):
                return result
            return Either.right(result)
        except Exception as e:
            return Either.left(cast(L, e))

    def and_then(self, fn: Callable[[R], "Either[L, U]"]) -> "Either[L, U]":
        """Alias for flat_map."""
        return self.flat_map(fn)

    def filter(self, predicate: Callable[[R], bool]) -> "Either[L, R]":
        """Keep the Right value if it matches the predicate, otherwise turn it into a Left.

        A Left is returned unchanged, and an exception raised by the predicate is
        captured into a Left so the operation stays safe.
        """
        if not self._is_right:
            return Either(self._value, is_right=False)
        try:
            if predicate(self._value):
                return self
            return Either(self._value, is_right=False)
        except Exception as e:
            return Either(cast(L, e), is_right=False)

    def or_else(self, other: "Either[L, R]") -> "Either[L, R]":
        """Return self if Right, otherwise other."""
        if self._is_right:
            return self
        return other

    def fold(self, left_fn: Callable[[L], T], right_fn: Callable[[R], T]) -> T:
        """Apply one of two functions depending on variant."""
        if self._is_right:
            return right_fn(self._value)
        return left_fn(self._value)

    def swap(self) -> "Either[R, L]":
        """Swap Left and Right."""
        return Either(self._value, is_right=not self._is_right)

    def __repr__(self) -> str:
        """String representation."""
        if self._is_right:
            return f"Right({self._value!r})"
        return f"Left({self._value!r})"

    def __bool__(self) -> bool:
        """Boolean conversion - Right is truthy."""
        return self._is_right

    def __eq__(self, other: object) -> bool:
        """Equality comparison."""
        if not isinstance(other, Either):
            return NotImplemented
        if self._is_right != other._is_right:
            return False
        return cast(bool, self._value == other._value)


__all__ = [
    "Either",
]
