"""Graph and dependency resolution utilities.

This module provides topological sorting and cycle detection for
directed graphs using only the Python standard library (``graphlib``).
"""

from __future__ import annotations

from graphlib import CycleError, TopologicalSorter
from typing import Any, Callable, Dict, Iterable, List, Mapping, Sequence

__all__: list[str] = [
    "dependency_order",
    "has_cycle",
    "is_valid_ordering",
    "topological_sort",
]


def topological_sort(nodes: Mapping[Any, Iterable[Any]]) -> List[Any]:
    """Return the nodes of a directed graph in topological order.

    Args:
        nodes: Mapping of each node to an iterable of its predecessor
            nodes (dependencies). A node with no predecessors maps to
            an empty iterable.

    Returns:
        A list of nodes ordered so that every dependency appears before
        the nodes that depend on it.

    Raises:
        TypeError: If ``nodes`` is not a mapping.
        ValueError: If the graph contains a cycle.

    Examples:
        >>> topological_sort({"a": [], "b": ["a"], "c": ["a", "b"]})
        ['a', 'b', 'c']
    """
    if not isinstance(nodes, Mapping):
        raise TypeError("nodes must be a mapping of node to predecessors")
    sorter = TopologicalSorter(dict(nodes))
    try:
        return list(sorter.static_order())
    except CycleError as exc:
        raise ValueError("graph contains a cycle") from exc


def has_cycle(nodes: Mapping[Any, Iterable[Any]]) -> bool:
    """Return ``True`` if the directed graph contains a cycle.

    Args:
        nodes: Mapping of each node to an iterable of its predecessor
            nodes (dependencies).

    Returns:
        ``True`` if the graph contains a cycle, ``False`` otherwise.

    Examples:
        >>> has_cycle({"a": [], "b": ["a"]})
        False
        >>> has_cycle({"a": ["b"], "b": ["a"]})
        True
    """
    try:
        topological_sort(nodes)
    except ValueError:
        return True
    return False


def dependency_order(
    items: Sequence[Any], get_dependencies: Callable[[Any], Iterable[Any]]
) -> List[Any]:
    """Return ``items`` ordered so dependencies come before dependents.

    Args:
        items: The items to order.
        get_dependencies: Callable that, given an item, returns an
            iterable of its dependencies (which must be in ``items``).

    Returns:
        A list of all items in dependency order.

    Raises:
        TypeError: If ``items`` is not a sequence.
        ValueError: If the dependency graph contains a cycle or a
            dependency is missing from ``items``.

    Examples:
        >>> dependency_order(
        ...     ["deploy", "build", "deps"],
        ...     lambda task: {
        ...         "deploy": ["build"],
        ...         "build": ["deps"],
        ...         "deps": [],
        ...     }.get(task, []),
        ... )
        ['deps', 'build', 'deploy']
    """
    if not isinstance(items, Sequence) or isinstance(items, (str, bytes)):
        raise TypeError("items must be a sequence")
    item_set = set(items)
    nodes: Dict[Any, List[Any]] = {}
    for item in items:
        dependencies = list(get_dependencies(item))
        missing = set(dependencies) - item_set
        if missing:
            raise ValueError(f"dependencies not in items for {item!r}: {sorted(missing)}")
        nodes[item] = dependencies
    return topological_sort(nodes)


def is_valid_ordering(order: Sequence[Any], nodes: Mapping[Any, Iterable[Any]]) -> bool:
    """Return ``True`` if ``order`` is a valid topological order of ``nodes``.

    Args:
        order: Candidate ordering of the graph nodes.
        nodes: Mapping of each node to an iterable of its predecessor
            nodes (dependencies).

    Returns:
        ``True`` if every dependency appears before its dependent in
        ``order`` and the node sets match, ``False`` otherwise.
    """
    try:
        position = {node: index for index, node in enumerate(order)}
    except TypeError:
        return False
    if set(order) != set(nodes):
        return False
    for node, predecessors in nodes.items():
        for predecessor in predecessors:
            if position.get(predecessor, -1) >= position.get(node, -1):
                return False
    return True


if __name__ == "__main__":
    import json

    example = {
        "install_deps": [],
        "build": ["install_deps"],
        "test": ["build"],
        "deploy": ["test"],
    }
    print(
        json.dumps(
            {
                "order": topological_sort(example),
                "has_cycle": has_cycle(example),
            },
            indent=2,
        )
    )
