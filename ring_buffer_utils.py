"""Fixed-size circular buffer (ring buffer) utilities."""

from __future__ import annotations

from collections.abc import Iterable, Iterator
from typing import Any, Generic, Optional, TypeVar

T = TypeVar("T")


class RingBuffer(Generic[T]):
    """A fixed-capacity circular buffer.

    Appending to a full buffer overwrites the oldest element, keeping only
    the most recent ``capacity`` items.
    """

    def __init__(self, capacity: int) -> None:
        if not isinstance(capacity, int) or isinstance(capacity, bool):
            raise TypeError("capacity must be an integer")
        if capacity <= 0:
            raise ValueError("capacity must be greater than 0")
        self._capacity = capacity
        self._data: list[Optional[T]] = [None] * capacity
        self._head = 0
        self._size = 0

    def __len__(self) -> int:
        return self._size

    def __iter__(self) -> Iterator[T]:
        for i in range(self._size):
            yield self._data[(self._head + i) % self._capacity]  # type: ignore[misc]

    def __repr__(self) -> str:
        return f"{type(self).__name__}({list(self)}, capacity={self._capacity})"

    @property
    def capacity(self) -> int:
        """Return the maximum number of elements the buffer can hold."""
        return self._capacity

    @property
    def is_full(self) -> bool:
        """Return True when the buffer holds ``capacity`` elements."""
        return self._size == self._capacity

    @property
    def is_empty(self) -> bool:
        """Return True when the buffer holds no elements."""
        return self._size == 0

    def append(self, value: T) -> None:
        """Append ``value``, overwriting the oldest element when full."""
        idx = (self._head + self._size) % self._capacity
        self._data[idx] = value
        if self.is_full:
            self._head = (self._head + 1) % self._capacity
        else:
            self._size += 1

    def get(self, index: int) -> T:
        """Return the element at logical ``index`` (0 is the oldest)."""
        if not isinstance(index, int) or isinstance(index, bool):
            raise TypeError("index must be an integer")
        if index < 0 or index >= self._size:
            raise IndexError("ring buffer index out of range")
        return self._data[(self._head + index) % self._capacity]  # type: ignore[return-value]

    def peek(self) -> T:
        """Return the oldest element without removing it."""
        if self.is_empty:
            raise IndexError("peek from empty ring buffer")
        return self._data[self._head]  # type: ignore[return-value]

    def pop(self) -> T:
        """Remove and return the oldest element."""
        if self.is_empty:
            raise IndexError("pop from empty ring buffer")
        value = self._data[self._head]
        self._data[self._head] = None
        self._head = (self._head + 1) % self._capacity
        self._size -= 1
        return value  # type: ignore[return-value]

    def clear(self) -> None:
        """Remove all elements from the buffer."""
        self._data = [None] * self._capacity
        self._head = 0
        self._size = 0

    def to_list(self) -> list[T]:
        """Return the elements from oldest to newest as a list."""
        return list(self)

    @classmethod
    def from_list(cls, items: Iterable[T], capacity: Optional[int] = None) -> "RingBuffer[T]":
        """Build a ring buffer from ``items``.

        Args:
            items: Elements to load, oldest first.
            capacity: Buffer capacity (defaults to the number of items).
        """
        item_list = list(items)
        cap = len(item_list) if capacity is None else capacity
        buffer = cls(cap)
        for value in item_list:
            buffer.append(value)
        return buffer


def create(capacity: int) -> RingBuffer[Any]:
    """Create an empty ring buffer with the given capacity."""
    return RingBuffer(capacity)


def append(buffer: RingBuffer[T], value: T) -> RingBuffer[T]:
    """Append ``value`` to ``buffer`` and return it."""
    buffer.append(value)
    return buffer


def get(buffer: RingBuffer[T], index: int) -> T:
    """Return the element at logical ``index`` in ``buffer``."""
    return buffer.get(index)


def pop(buffer: RingBuffer[T]) -> T:
    """Remove and return the oldest element of ``buffer``."""
    return buffer.pop()


def peek(buffer: RingBuffer[T]) -> T:
    """Return the oldest element of ``buffer`` without removing it."""
    return buffer.peek()


def is_empty(buffer: RingBuffer[T]) -> bool:
    """Return True when ``buffer`` holds no elements."""
    return buffer.is_empty


def is_full(buffer: RingBuffer[T]) -> bool:
    """Return True when ``buffer`` holds ``capacity`` elements."""
    return buffer.is_full


def size(buffer: RingBuffer[T]) -> int:
    """Return the number of elements in ``buffer``."""
    return len(buffer)


def clear(buffer: RingBuffer[T]) -> None:
    """Remove all elements from ``buffer``."""
    buffer.clear()


def to_list(buffer: RingBuffer[T]) -> list[T]:
    """Return the elements of ``buffer`` from oldest to newest."""
    return buffer.to_list()
