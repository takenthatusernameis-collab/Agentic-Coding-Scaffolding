"""Set operation utilities for common set-theoretic and combinatorial tasks."""

from typing import Any, Iterable, Iterator, List, Sequence, Set, Tuple, TypeVar

T = TypeVar("T")

__all__ = [
    "T",
    "cartesian_product",
    "count_difference",
    "count_intersection",
    "count_symmetric_difference",
    "count_union",
    "difference",
    "has_intersection",
    "intersection",
    "is_disjoint",
    "is_equal",
    "is_not_equal",
    "is_proper_subset",
    "is_proper_superset",
    "is_subset",
    "is_superset",
    "power_set",
    "symmetric_difference",
    "union",
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


def has_intersection(a: Iterable[Any], b: Iterable[Any]) -> bool:
    """Check whether ``a`` and ``b`` share at least one common element.

    This is the boolean companion to :func:`intersection` and the logical
    negation of :func:`is_disjoint`.

    Args:
        a: First iterable.
        b: Second iterable.

    Returns:
        ``True`` when the intersection of ``a`` and ``b`` is non-empty,
        otherwise ``False``.

    Raises:
        TypeError: If ``a`` or ``b`` is not iterable.

    Examples:
        >>> has_intersection([1, 2], [2, 3])
        True
        >>> has_intersection([1, 2], [3, 4])
        False
        >>> has_intersection([], [1, 2])
        False
    """
    return count_intersection(a, b) > 0


def is_disjoint(a: Iterable[Any], b: Iterable[Any]) -> bool:
    """Check whether ``a`` and ``b`` share no common elements.

    Args:
        a: First iterable.
        b: Second iterable.

    Returns:
        ``True`` if the intersection of ``a`` and ``b`` is empty, otherwise
        ``False``.

    Raises:
        TypeError: If ``a`` or ``b`` is not iterable.

    Examples:
        >>> is_disjoint([1, 2], [3, 4])
        True
        >>> is_disjoint([1, 2], [2, 3])
        False
    """
    return not (_to_set(a) & _to_set(b))


def is_proper_subset(a: Iterable[Any], b: Iterable[Any]) -> bool:
    """Check whether every element of ``a`` is in ``b`` and ``b`` has more.

    A proper (strict) subset relationship means ``a`` is a subset of ``b``
    but the two sets are not equal.

    Args:
        a: Candidate proper subset iterable.
        b: Superset iterable.

    Returns:
        ``True`` if ``a`` is a proper subset of ``b``, otherwise ``False``.

    Raises:
        TypeError: If ``a`` or ``b`` is not iterable.

    Examples:
        >>> is_proper_subset([1, 2], [1, 2, 3])
        True
        >>> is_proper_subset([1, 2], [1, 2])
        False
        >>> is_proper_subset([1, 4], [1, 2, 3])
        False
    """
    sa = _to_set(a)
    sb = _to_set(b)
    return sa < sb


def is_proper_superset(a: Iterable[Any], b: Iterable[Any]) -> bool:
    """Check whether ``a`` contains every element of ``b`` and has more.

    A proper (strict) superset relationship means ``a`` is a superset of
    ``b`` but the two sets are not equal.

    Args:
        a: Candidate proper superset iterable.
        b: Subset iterable.

    Returns:
        ``True`` if ``a`` is a proper superset of ``b``, otherwise ``False``.

    Raises:
        TypeError: If ``a`` or ``b`` is not iterable.

    Examples:
        >>> is_proper_superset([1, 2, 3], [1, 2])
        True
        >>> is_proper_superset([1, 2], [1, 2])
        False
        >>> is_proper_superset([1, 2], [2, 3])
        False
    """
    sa = _to_set(a)
    sb = _to_set(b)
    return sa > sb


def is_equal(a: Iterable[Any], b: Iterable[Any]) -> bool:
    """Check whether two iterables contain the same set of elements.

    Order, multiplicity, and the concrete iterable type of the inputs do
    not matter; only the distinct elements they yield are compared.

    Args:
        a: First iterable.
        b: Second iterable.

    Returns:
        ``True`` when *a* and *b* represent the same set, ``False`` otherwise.

    Raises:
        TypeError: If *a* or *b* is not iterable.

    Examples:
        >>> is_equal([1, 2, 3], [3, 2, 1])
        True
        >>> is_equal([1, 2, 2, 3], [1, 2, 3])
        True
        >>> is_equal([1, 2], [1, 2, 3])
        False
        >>> is_equal([], [])
        True
    """
    return _to_set(a) == _to_set(b)


def is_not_equal(a: Iterable[Any], b: Iterable[Any]) -> bool:
    """Check whether two iterables contain different sets of elements.

    This is the boolean companion to :func:`is_equal`. Order, multiplicity,
    and the concrete iterable type of the inputs do not matter; only the
    distinct elements they yield are compared.

    Args:
        a: First iterable.
        b: Second iterable.

    Returns:
        ``True`` when *a* and *b* do not represent the same set, ``False``
        otherwise.

    Raises:
        TypeError: If *a* or *b* is not iterable.

    Examples:
        >>> is_not_equal([1, 2], [1, 2, 3])
        True
        >>> is_not_equal([1, 2, 3], [3, 2, 1])
        False
        >>> is_not_equal([1, 2, 2, 3], [1, 2, 3])
        False
        >>> is_not_equal([], [1])
        True
    """
    return not is_equal(a, b)


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


def count_intersection(a: Iterable[Any], b: Iterable[Any]) -> int:
    """Return the number of distinct elements common to both ``a`` and ``b``.

    This is the integer companion to :func:`intersection` and the count
    counterpart of :func:`has_intersection`. Only distinct elements are
    counted, so duplicate occurrences in either input contribute at most
    one to the result.

    Args:
        a: First iterable.
        b: Second iterable.

    Returns:
        The number of distinct elements in the intersection of ``a`` and
        ``b``.

    Raises:
        TypeError: If ``a`` or ``b`` is not iterable.

    Examples:
        >>> count_intersection([1, 2, 3], [2, 3, 4])
        2
        >>> count_intersection([1, 2], [3, 4])
        0
        >>> count_intersection([], [1, 2])
        0
        >>> count_intersection([1, 1, 2], [2, 2])
        1
        >>> count_intersection("abc", "cd")
        1
    """
    return len(intersection(a, b))


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


def count_union(a: Iterable[Any], b: Iterable[Any]) -> int:
    """Return the number of distinct elements present in either ``a`` or ``b``.

    This is the integer companion to :func:`union`. Only distinct elements
    are counted, so duplicate occurrences in either input contribute at most
    one to the result.

    Args:
        a: First iterable.
        b: Second iterable.

    Returns:
        The number of distinct elements in the union of ``a`` and ``b``.

    Raises:
        TypeError: If ``a`` or ``b`` is not iterable.

    Examples:
        >>> count_union([1, 2], [2, 3])
        3
        >>> count_union([1, 2], [3, 4])
        4
        >>> count_union([], [])
        0
        >>> count_union([1, 1, 2], [2, 2])
        2
        >>> count_union("abc", "cd")
        4
    """
    return len(union(a, b))


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


def count_difference(a: Iterable[Any], b: Iterable[Any]) -> int:
    """Return the number of distinct elements in ``a`` that are not in ``b``.

    This is the integer companion to :func:`difference`. Only distinct
    elements are counted, so duplicate occurrences in ``a`` contribute at
    most one to the result.

    Args:
        a: First iterable.
        b: Second iterable.

    Returns:
        The number of distinct elements in the difference ``a - b``.

    Raises:
        TypeError: If ``a`` or ``b`` is not iterable.

    Examples:
        >>> count_difference([1, 2, 3], [2])
        2
        >>> count_difference([1, 2], [3, 4])
        2
        >>> count_difference([], [1, 2])
        0
        >>> count_difference([1, 1, 2], [2])
        1
        >>> count_difference("abc", "cd")
        2
    """
    return len(difference(a, b))


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


def count_symmetric_difference(a: Iterable[Any], b: Iterable[Any]) -> int:
    """Return the number of distinct elements in either ``a`` or ``b`` but not both.

    This is the integer companion to :func:`symmetric_difference`. Only
    distinct elements are counted, so duplicate occurrences in either input
    contribute at most one to the result.

    Args:
        a: First iterable.
        b: Second iterable.

    Returns:
        The number of distinct elements in the symmetric difference of ``a``
        and ``b``.

    Raises:
        TypeError: If ``a`` or ``b`` is not iterable.

    Examples:
        >>> count_symmetric_difference([1, 2, 3], [2, 3, 4])
        2
        >>> count_symmetric_difference([1, 2], [3, 4])
        4
        >>> count_symmetric_difference([1, 2], [1, 2])
        0
        >>> count_symmetric_difference([1, 1, 2], [2, 2])
        1
        >>> count_symmetric_difference("abc", "cd")
        3
    """
    return len(symmetric_difference(a, b))


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
