"""Chunking utilities for splitting iterables into fixed-size pieces."""

from __future__ import annotations

from typing import Any, Iterable, Iterator, List

__all__: list[str] = [
    "chunk",
    "chunk_count",
    "chunk_pad",
    "chunked",
    "chunks",
    "even_chunks",
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


def chunk_count(iterable: Iterable[Any], size: int) -> int:
    """Return the number of chunks of ``size`` produced from ``iterable``.

    Args:
        iterable: The iterable to count chunks for.
        size: The chunk size.

    Returns:
        The number of chunks (including a trailing partial chunk).

    Raises:
        TypeError: If ``size`` is not an int.
        ValueError: If ``size`` is not positive.
    """
    if not isinstance(size, int):
        raise TypeError("size must be int")
    if size <= 0:
        raise ValueError("size must be positive")
    count = 0
    current = 0
    for _ in iterable:
        current += 1
        if current == size:
            count += 1
            current = 0
    if current:
        count += 1
    return count


def iter_chunked(iterable: Iterable[Any], size: int) -> Iterator[List[Any]]:
    """Alias for ichunk."""
    yield from ichunk(iterable, size)


def even_chunks(iterable: Iterable[Any], n: int) -> List[List[Any]]:
    """Split *iterable* into *n* chunks of roughly equal size.

    The total number of items is distributed so that the first
    ``len(items) % n`` chunks contain one extra element when the count does
    not divide evenly. Empty input yields an empty list.

    Args:
        iterable: The iterable to split.
        n: The number of chunks to produce.

    Returns:
        A list of *n* lists (or fewer when the input has fewer than *n*
        items; trailing empty chunks are dropped).

    Raises:
        TypeError: If *n* is not an int.
        ValueError: If *n* is not positive.
    """
    if not isinstance(n, int):
        raise TypeError("n must be int")
    if isinstance(n, bool):
        raise TypeError("n must be int")
    if n <= 0:
        raise ValueError("n must be positive")
    items = list(iterable)
    if not items:
        return []
    base, remainder = divmod(len(items), n)
    result: List[List[Any]] = []
    index = 0
    for i in range(n):
        size = base + (1 if i < remainder else 0)
        if size == 0:
            break
        result.append(items[index : index + size])
        index += size
    return result


def chunk_pad(iterable: Iterable[Any], size: int, pad_value: Any = None) -> List[List[Any]]:
    """Split *iterable* into chunks of *size*, padding the last chunk.

    Like :func:`chunk`, but the final (possibly partial) chunk is padded with
    *pad_value* so that every returned chunk has exactly *size* elements.
    Empty input yields an empty list.

    Args:
        iterable: The iterable to split.
        size: The chunk size.
        pad_value: Value used to pad the final partial chunk.

    Returns:
        A list of chunks, each of length *size*.

    Raises:
        TypeError: If *size* is not an int.
        ValueError: If *size* is not positive.
    """
    if not isinstance(size, int):
        raise TypeError("size must be int")
    if isinstance(size, bool):
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
        current = current + [pad_value] * (size - len(current))
        result.append(current)
    return result
