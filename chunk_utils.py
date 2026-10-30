"""Chunking utilities for splitting iterables into fixed-size pieces."""

from __future__ import annotations

from typing import Any, Iterable, Iterator, List

__all__: list[str] = [
    "chunk",
    "chunked",
    "chunks",
    "ichunk",
    "iter_chunked",
]


def chunk(iterable: Iterable[Any], size: int) -> List[List[Any]]:
    """Split an iterable into chunks of the given size."""
    if not isinstance(size, int):
        raise TypeError("size must be int")
    if size <= 0:
        raise ValueError("size must be positive")
    result: List[List[Any]] = []
    current: List[Any] = []
    for item in iterable:
        current.append(item)
        if len(current) == size:
            result.append(current)
            current = []
    if current:
        result.append(current)
    return result


def chunks(iterable: Iterable[Any], size: int) -> List[List[Any]]:
    """Alias for chunk."""
    return chunk(iterable, size)


def chunked(iterable: Iterable[Any], size: int) -> List[List[Any]]:
    """Alias for chunk."""
    return chunk(iterable, size)


def ichunk(iterable: Iterable[Any], size: int) -> Iterator[List[Any]]:
    """Split an iterable into chunks yielding them lazily."""
    if not isinstance(size, int):
        raise TypeError("size must be int")
    if size <= 0:
        raise ValueError("size must be positive")
    current: List[Any] = []
    for item in iterable:
        current.append(item)
        if len(current) == size:
            yield current
            current = []
    if current:
        yield current


def iter_chunked(iterable: Iterable[Any], size: int) -> Iterator[List[Any]]:
    """Alias for ichunk."""
    yield from ichunk(iterable, size)
