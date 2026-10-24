"""Tests for graphlib_utils module."""

from graphlib import CycleError

from graphlib_utils import (
    TopologicalSorter,
    get_ready_order,
    is_cyclic,
    topological_sort,
)


def test_topological_sort_simple():
    graph = {"D": {"B", "C"}, "C": {"A"}, "B": {"A"}, "A": set()}
    result = topological_sort(graph)
    assert result.index("A") < result.index("B")
    assert result.index("A") < result.index("C")
    assert result.index("B") < result.index("D")
    assert result.index("C") < result.index("D")


def test_topological_sort_linear():
    graph = {"3": {"2"}, "2": {"1"}, "1": set()}
    assert topological_sort(graph) == ["1", "2", "3"]


def test_is_cyclic_true():
    graph = {"A": {"B"}, "B": {"A"}}
    assert is_cyclic(graph) is True


def test_is_cyclic_false():
    graph = {"A": set(), "B": {"A"}}
    assert is_cyclic(graph) is False


def test_topological_sort_cycle_error():
    graph = {"A": {"B"}, "B": {"A"}}
    try:
        topological_sort(graph)
        assert False
    except CycleError:
        pass


def test_get_ready_order():
    graph = {"D": {"B", "C"}, "C": {"A"}, "B": {"A"}, "A": set()}
    levels = get_ready_order(graph)
    assert levels[0] == ["A"]
    assert set(levels[1]) == {"B", "C"}
    assert levels[2] == ["D"]


def test_topological_sort_type_error():
    try:
        topological_sort("not a mapping")
        assert False
    except TypeError:
        pass


def test_is_cyclic_type_error():
    try:
        is_cyclic([])
        assert False
    except TypeError:
        pass


def test_graphlib_export():
    assert TopologicalSorter is not None
