"""Sequence utility functions for common sequence operations.

This module provides helpers for working with sequences, including
retrieving elements by position, slicing into head/tail portions,
splitting at an index, taking or dropping elements while a predicate
holds, interleaving multiple sequences, and forming adjacent pairs.
"""

from __future__ import annotations

from collections.abc import Callable, Sequence
from typing import Any, Iterator, List, Optional, Tuple, TypeVar

T = TypeVar("T")

__all__: list[str] = [
    "first",
    "last",
    "nth",
    "head",
    "tail",
    "split_at",
    "take_while",
    "drop_while",
    "interleave",
    "adjacent_pairs",
    "is_sorted",
]


def _require_sequence(sequence: Any) -> None:
    """Validate that ``sequence`` is a sequence, raising ``TypeError`` otherwise."""
    if not isinstance(sequence, Sequence):
        raise TypeError("sequence must be a sequence (e.g. list, tuple, str)")


def first(sequence: Sequence[T]) -> Optional[T]:
    """Return the first element of ``sequence``, or ``None`` if it is empty.

    Args:
        sequence: The sequence to inspect.

    Returns:
        The first element, or ``None`` when the sequence has no elements.

    Raises:
        TypeError: If ``sequence`` is not a sequence.

    Examples:
        >>> first([1, 2, 3])
        1
        >>> first([])
    """
    _require_sequence(sequence)
    return sequence[0] if sequence else None


def last(sequence: Sequence[T]) -> Optional[T]:
    """Return the last element of ``sequence``, or ``None`` if it is empty.

    Args:
        sequence: The sequence to inspect.

    Returns:
        The last element, or ``None`` when the sequence has no elements.

    Raises:
        TypeError: If ``sequence`` is not a sequence.

    Examples:
        >>> last([1, 2, 3])
        3
        >>> last("")
    """
    _require_sequence(sequence)
    return sequence[-1] if sequence else None


def nth(sequence: Sequence[T], n: int) -> Optional[T]:
    """Return the element at index ``n``, or ``None`` if out of range.

    Negative indices are supported, mirroring normal sequence indexing.

    Args:
        sequence: The sequence to inspect.
        n: The index of the element to retrieve.

    Returns:
        The element at index ``n``, or ``None`` when the index is invalid.

    Raises:
        TypeError: If ``sequence`` is not a sequence or ``n`` is not an int.

    Examples:
        >>> nth([1, 2, 3], 1)
        2
        >>> nth([1, 2, 3], 5)
    """
    _require_sequence(sequence)
    if not isinstance(n, int) or isinstance(n, bool):
        raise TypeError("n must be an integer")
    try:
        return sequence[n]
    except IndexError:
        return None


def head(sequence: Sequence[T], n: int = 1) -> List[T]:
    """Return the first ``n`` elements of ``sequence``.

    Args:
        sequence: The sequence to slice.
        n: The number of leading elements to return (default: 1).

    Returns:
        A list of the first ``n`` elements.

    Raises:
        TypeError: If ``sequence`` is not a sequence or ``n`` is not an int.
        ValueError: If ``n`` is negative.

    Examples:
        >>> head([1, 2, 3, 4], 2)
        [1, 2]
    """
    _require_sequence(sequence)
    if not isinstance(n, int) or isinstance(n, bool):
        raise TypeError("n must be an integer")
    if n < 0:
        raise ValueError("n must be non-negative")
    return list(sequence[:n])


def tail(sequence: Sequence[T], n: int = 1) -> List[T]:
    """Return the last ``n`` elements of ``sequence``.

    Args:
        sequence: The sequence to slice.
        n: The number of trailing elements to return (default: 1).

    Returns:
        A list of the last ``n`` elements.

    Raises:
        TypeError: If ``sequence`` is not a sequence or ``n`` is not an int.
        ValueError: If ``n`` is negative.

    Examples:
        >>> tail([1, 2, 3, 4], 2)
        [3, 4]
    """
    _require_sequence(sequence)
    if not isinstance(n, int) or isinstance(n, bool):
        raise TypeError("n must be an integer")
    if n < 0:
        raise ValueError("n must be non-negative")
    if n == 0:
        return []
    return list(sequence[-n:])


def split_at(sequence: Sequence[T], index: int) -> Tuple[List[T], List[T]]:
    """Split ``sequence`` into ``(first_part, rest)`` at ``index``.

    The index is clamped to the valid range, so splitting beyond the length
    returns the whole sequence as the first part and an empty second part.

    Args:
        sequence: The sequence to split.
        index: The position at which to split.

    Returns:
        A tuple of ``(first_part, rest)`` lists.

    Raises:
        TypeError: If ``sequence`` is not a sequence or ``index`` is not an int.

    Examples:
        >>> split_at([1, 2, 3, 4], 2)
        ([1, 2], [3, 4])
    """
    _require_sequence(sequence)
    if not isinstance(index, int) or isinstance(index, bool):
        raise TypeError("index must be an integer")
    index = max(0, min(index, len(sequence)))
    return list(sequence[:index]), list(sequence[index:])


def take_while(sequence: Sequence[T], predicate: Callable[[T], bool]) -> List[T]:
    """Return elements from ``sequence`` while ``predicate`` returns true.

    Stops at the first element for which ``predicate`` is false.

    Args:
        sequence: The sequence to consume.
        predicate: A function returning ``True`` to keep taking elements.

    Returns:
        A list of leading elements satisfying the predicate.

    Raises:
        TypeError: If ``sequence`` is not a sequence or ``predicate`` is not
            callable.

    Examples:
        >>> take_while([1, 2, 3, 4], lambda x: x < 3)
        [1, 2]
    """
    _require_sequence(sequence)
    if not callable(predicate):
        raise TypeError("predicate must be callable")
    result: List[T] = []
    for item in sequence:
        if predicate(item):
            result.append(item)
        else:
            break
    return result


def drop_while(sequence: Sequence[T], predicate: Callable[[T], bool]) -> List[T]:
    """Drop elements from ``sequence`` while ``predicate`` returns true.

    Once ``predicate`` returns false, all remaining elements are kept.

    Args:
        sequence: The sequence to consume.
        predicate: A function returning ``True`` to keep dropping elements.

    Returns:
        A list of elements after the first one failing the predicate.

    Raises:
        TypeError: If ``sequence`` is not a sequence or ``predicate`` is not
            callable.

    Examples:
        >>> drop_while([1, 2, 3, 4], lambda x: x < 3)
        [3, 4]
    """
    _require_sequence(sequence)
    if not callable(predicate):
        raise TypeError("predicate must be callable")
    result: List[T] = []
    dropping = True
    for item in sequence:
        if dropping and predicate(item):
            continue
        dropping = False
        result.append(item)
    return result


def interleave(*sequences: Sequence[T]) -> List[T]:
    """Round-robin interleave elements from multiple sequences.

    Elements are taken in turn from each sequence until all are exhausted.

    Args:
        *sequences: Sequences to interleave.

    Returns:
        A list with elements taken round-robin from each input.

    Raises:
        TypeError: If any argument is not a sequence.

    Examples:
        >>> interleave([1, 2], [3, 4])
        [1, 3, 2, 4]
    """
    for seq in sequences:
        _require_sequence(seq)
    iterators = [iter(seq) for seq in sequences]
    result: List[T] = []
    active = len(iterators)
    while active:
        next_iterators: List[Iterator[T]] = []
        active = 0
        for it in iterators:
            try:
                result.append(next(it))
                next_iterators.append(it)
                active += 1
            except StopIteration:
                pass
        iterators = next_iterators
    return result


def adjacent_pairs(sequence: Sequence[T]) -> List[Tuple[T, T]]:
    """Return consecutive ``(element, next_element)`` pairs from ``sequence``.

    Args:
        sequence: The sequence to pair up.

    Returns:
        A list of adjacent pairs. Empty for sequences with fewer than two
        elements.

    Raises:
        TypeError: If ``sequence`` is not a sequence.

    Examples:
        >>> adjacent_pairs([1, 2, 3])
        [(1, 2), (2, 3)]
    """
    _require_sequence(sequence)
    return [(sequence[i], sequence[i + 1]) for i in range(len(sequence) - 1)]


def is_sorted(
    sequence: Sequence[T],
    *,
    key: Optional[Callable[[T], Any]] = None,
    reverse: bool = False,
) -> bool:
    """Return ``True`` if ``sequence`` is sorted.

    Args:
        sequence: The sequence to inspect.
        key: An optional key function applied before comparison.
        reverse: When true, checks for descending order instead.

    Returns:
        ``True`` if the sequence is sorted in the requested direction.

    Raises:
        TypeError: If ``sequence`` is not a sequence or ``key`` is not callable.

    Examples:
        >>> is_sorted([1, 2, 3])
        True
        >>> is_sorted([3, 2, 1], reverse=True)
        True
    """
    _require_sequence(sequence)
    if key is not None and not callable(key):
        raise TypeError("key must be callable")
    if len(sequence) < 2:
        return True
    mapped = [key(item) if key is not None else item for item in sequence]
    should_precede = (lambda a, b: a > b) if reverse else (lambda a, b: a < b)
    for i in range(len(mapped) - 1):
        if should_precede(mapped[i + 1], mapped[i]):
            return False
    return True


if __name__ == "__main__":
    import doctest

    doctest.testmod()
