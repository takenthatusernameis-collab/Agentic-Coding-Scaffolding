"""Set operation utilities for common set-theoretic and combinatorial tasks."""

from typing import Any, Iterable, Iterator, List, Sequence, Set, Tuple, TypeVar

T = TypeVar("T")

__all__: List[str] = [
    "is_subset",
    "is_superset",
    "intersection",
    "union",
    "difference",
    "symmetric_difference",
    "cartesian_product",
    "power_set",
]


def _to_set(items: Iterable[Any]) -> Set[Any]:
    """Convert an iterable to a set, raising ``TypeError`` for non-iterables.

    Args:
        items: An iterable of hashable elements.

    Returns:
        A set containing the elements of ``items``.

    Raises:
        TypeError: If ``items`` is not iterable.
    """
    try:
        return set(items)
    except TypeError as exc:
        raise TypeError("items must be an iterable") from exc


def is_subset(a: Iterable[Any], b: Iterable[Any]) -> bool:
    """Check whether every element of ``a`` is contained in ``b``.

    Args:
        a: Candidate subset iterable.
        b: Superset iterable.

    Returns:
        ``True`` if ``a`` is a subset of ``b``, otherwise ``False``.

    Raises:
        TypeError: If ``a`` or ``b`` is not iterable.

    Examples:
        >>> is_subset([1, 2], [1, 2, 3])
        True
        >>> is_subset([1, 4], [1, 2, 3])
        False
    """
    return _to_set(a).issubset(_to_set(b))


def is_superset(a: Iterable[Any], b: Iterable[Any]) -> bool:
    """Check whether ``a`` contains every element of ``b``.

    Args:
        a: Candidate superset iterable.
        b: Subset iterable.

    Returns:
        ``True`` if ``a`` is a superset of ``b``, otherwise ``False``.

    Raises:
        TypeError: If ``a`` or ``b`` is not iterable.

    Examples:
        >>> is_superset([1, 2, 3], [2])
        True
        >>> is_superset([1, 2], [2, 3])
        False
    """
    return _to_set(a).issuperset(_to_set(b))


def intersection(a: Iterable[Any], b: Iterable[Any]) -> Set[Any]:
    """Return the set of elements common to both ``a`` and ``b``.

    Args:
        a: First iterable.
        b: Second iterable.

    Returns:
        A new set containing the intersection.

    Raises:
        TypeError: If ``a`` or ``b`` is not iterable.

    Examples:
        >>> intersection([1, 2, 3], [2, 3, 4])
        {2, 3}
    """
    return _to_set(a) & _to_set(b)


def union(a: Iterable[Any], b: Iterable[Any]) -> Set[Any]:
    """Return the set of elements present in either ``a`` or ``b``.

    Args:
        a: First iterable.
        b: Second iterable.

    Returns:
        A new set containing the union.

    Raises:
        TypeError: If ``a`` or ``b`` is not iterable.

    Examples:
        >>> union([1, 2], [2, 3])
        {1, 2, 3}
    """
    return _to_set(a) | _to_set(b)


def difference(a: Iterable[Any], b: Iterable[Any]) -> Set[Any]:
    """Return elements in ``a`` that are not in ``b``.

    Args:
        a: First iterable.
        b: Second iterable.

    Returns:
        A new set containing the difference ``a - b``.

    Raises:
        TypeError: If ``a`` or ``b`` is not iterable.

    Examples:
        >>> difference([1, 2, 3], [2])
        {1, 3}
    """
    return _to_set(a) - _to_set(b)


def symmetric_difference(a: Iterable[Any], b: Iterable[Any]) -> Set[Any]:
    """Return elements in either ``a`` or ``b`` but not both.

    Args:
        a: First iterable.
        b: Second iterable.

    Returns:
        A new set containing the symmetric difference.

    Raises:
        TypeError: If ``a`` or ``b`` is not iterable.

    Examples:
        >>> symmetric_difference([1, 2, 3], [2, 3, 4])
        {1, 4}
    """
    return _to_set(a) ^ _to_set(b)


def cartesian_product(a: Sequence[Any], b: Sequence[Any]) -> Iterator[Tuple[Any, Any]]:
    """Yield ordered pairs from the Cartesian product of two sequences.

    Args:
        a: First sequence.
        b: Second sequence.

    Yields:
        Tuples ``(x, y)`` for every ``x`` in ``a`` and ``y`` in ``b``,
        preserving the iteration order of both inputs.

    Raises:
        TypeError: If ``a`` or ``b`` is not a sequence.

    Examples:
        >>> list(cartesian_product([1, 2], ["a", "b"]))
        [(1, 'a'), (1, 'b'), (2, 'a'), (2, 'b')]
    """
    if not isinstance(a, (list, tuple, str, bytes)) and not hasattr(a, "__iter__"):
        raise TypeError("a must be a sequence")
    if not isinstance(b, (list, tuple, str, bytes)) and not hasattr(b, "__iter__"):
        raise TypeError("b must be a sequence")
    for x in a:
        for y in b:
            yield (x, y)


def power_set(items: Iterable[T]) -> Iterator[Tuple[T, ...]]:
    """Yield every subset of ``items`` as a tuple.

    The empty set is yielded first, followed by subsets ordered by
    increasing cardinality. For an input of length ``n``, exactly
    ``2 ** n`` subsets are produced.

    Args:
        items: An iterable of hashable elements.

    Yields:
        Tuples representing each subset, preserving the input order of
        elements within each subset.

    Raises:
        TypeError: If ``items`` is not iterable.

    Examples:
        >>> [len(s) for s in power_set([1, 2])]
        [0, 1, 1, 2]
    """
    elements: List[T] = list(items)
    n = len(elements)
    for mask in range(1 << n):
        yield tuple(elements[i] for i in range(n) if mask & (1 << i))
