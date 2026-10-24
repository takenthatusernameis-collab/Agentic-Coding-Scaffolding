"""Graphlib utilities wrapping the standard library graphlib module.

Provides helpers for topological sorting and cycle detection using
graphlib.TopologicalSorter.
"""

from __future__ import annotations

from graphlib import CycleError, TopologicalSorter
from typing import Any, Dict, Iterable, List, Mapping, Optional, Set, Tuple

__all__ = [
    "CycleError",
    "TopologicalSorter",
    "topological_sort",
    "is_cyclic",
    "get_ready_order",
]


def topological_sort(
    graph: Mapping[Any, Iterable[Any]],
    *,
    predecessors: Optional[Mapping[Any, Iterable[Any]]] = None,
) -> List[Any]:
    """Perform a topological sort on a graph.

    Args:
        graph: Mapping from node to iterable of nodes it depends on
            (predecessors). Nodes not present as keys with dependencies
            are included if they appear.
        predecessors: If provided, use instead of inferring from graph.

    Returns:
        A list of nodes in topological order.

    Raises:
        TypeError: If graph is not a mapping.
        CycleError: If a cycle is detected.
    """
    if not isinstance(graph, Mapping):
        raise TypeError("graph must be a mapping")
    if predecessors is not None and not isinstance(predecessors, Mapping):
        raise TypeError("predecessors must be a mapping or None")

    ts = TopologicalSorter(graph if predecessors is None else None)
    if predecessors is not None:
        ts = TopologicalSorter()
        for node, preds in predecessors.items():
            for p in preds:
                ts.add(node, p)
        # Add nodes with no predecessors
        for node in predecessors:
            try:
                # ensure node is known
                ts.add(node)
            except Exception:
                pass
    else:
        for node, deps in graph.items():
            for dep in deps:
                ts.add(node, dep)
            # also add nodes that appear only as deps
        # collect all nodes
        all_nodes = set(graph.keys())
        for deps in graph.values():
            for d in deps:
                all_nodes.add(d)
        for node in all_nodes:
            try:
                ts.add(node)
            except Exception:
                pass

    try:
        return list(ts.static_order())
    except CycleError:
        raise
    except Exception as exc:
        raise


def is_cyclic(graph: Mapping[Any, Iterable[Any]]) -> bool:
    """Check if the graph has a cycle.

    Args:
        graph: Mapping from node to iterable of predecessor nodes.

    Returns:
        True if a cycle exists, False otherwise.

    Raises:
        TypeError: If graph is not a mapping.
    """
    if not isinstance(graph, Mapping):
        raise TypeError("graph must be a mapping")
    try:
        topological_sort(graph)
        return False
    except CycleError:
        return True


def get_ready_order(graph: Mapping[Any, Iterable[Any]]) -> List[List[Any]]:
    """Get nodes grouped by readiness level (Kahn's algorithm levels).

    Args:
        graph: Mapping from node to iterable of predecessor nodes.

    Returns:
        List of lists, where each inner list contains nodes ready at that level.

    Raises:
        TypeError: If graph is not a mapping.
        CycleError: If a cycle is detected.
    """
    if not isinstance(graph, Mapping):
        raise TypeError("graph must be a mapping")

    ts = TopologicalSorter()
    all_nodes = set(graph.keys())
    for node, deps in graph.items():
        for dep in deps:
            ts.add(node, dep)
            all_nodes.add(dep)
    for node in all_nodes:
        try:
            ts.add(node)
        except Exception:
            pass

    try:
        result: List[List[Any]] = []
        ts.prepare()
        while ts.is_active():
            ready = list(ts.get_ready())
            if not ready:
                break
            result.append(sorted(ready, key=lambda x: str(x)))
            for node in ready:
                ts.done(node)
        return result
    except CycleError:
        raise
