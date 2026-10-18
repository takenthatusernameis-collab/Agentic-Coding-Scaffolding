"""Unit tests for graphlib_utils module."""

import unittest

from graphlib_utils import (
    dependency_order,
    has_cycle,
    is_valid_ordering,
    topological_sort,
)


class TestTopologicalSort(unittest.TestCase):
    def test_empty_graph(self):
        self.assertEqual(topological_sort({}), [])

    def test_single_node(self):
        self.assertEqual(topological_sort({"a": []}), ["a"])

    def test_linear_chain(self):
        self.assertEqual(
            topological_sort({"c": ["b"], "b": ["a"], "a": []}),
            ["a", "b", "c"],
        )

    def test_independent_nodes(self):
        result = topological_sort({"a": [], "b": [], "c": []})
        self.assertEqual(sorted(result), ["a", "b", "c"])

    def test_diamond_dependencies(self):
        result = topological_sort({"d": ["b", "c"], "b": ["a"], "c": ["a"], "a": []})
        self.assertEqual(result[0], "a")
        self.assertEqual(result[-1], "d")
        self.assertLess(result.index("b"), result.index("d"))
        self.assertLess(result.index("c"), result.index("d"))

    def test_detects_cycle(self):
        with self.assertRaises(ValueError):
            topological_sort({"a": ["b"], "b": ["a"]})

    def test_self_loop_is_cycle(self):
        with self.assertRaises(ValueError):
            topological_sort({"a": ["a"]})

    def test_type_error_on_non_mapping(self):
        with self.assertRaises(TypeError):
            topological_sort(["a", "b"])  # type: ignore[arg-type]


class TestHasCycle(unittest.TestCase):
    def test_acyclic(self):
        self.assertFalse(has_cycle({"a": [], "b": ["a"]}))

    def test_cyclic(self):
        self.assertTrue(has_cycle({"a": ["b"], "b": ["a"]}))

    def test_self_loop(self):
        self.assertTrue(has_cycle({"a": ["a"]}))

    def test_empty(self):
        self.assertFalse(has_cycle({}))


class TestDependencyOrder(unittest.TestCase):
    def test_orders_by_dependency(self):
        def deps(task: str) -> list[str]:
            return {
                "deploy": ["test"],
                "test": ["build"],
                "build": ["install_deps"],
                "install_deps": [],
            }[task]

        result = dependency_order(["deploy", "test", "install_deps", "build"], deps)
        self.assertEqual(result, ["install_deps", "build", "test", "deploy"])

    def test_missing_dependency_raises(self):
        def deps(task: str) -> list[str]:
            return {"build": ["missing"]}.get(task, [])

        with self.assertRaises(ValueError):
            dependency_order(["build"], deps)

    def test_type_error_on_non_sequence(self):
        with self.assertRaises(TypeError):
            dependency_order({"a": []}, lambda x: [])  # type: ignore[arg-type]


class TestIsValidOrdering(unittest.TestCase):
    def test_valid_order(self):
        nodes = {"c": ["b"], "b": ["a"], "a": []}
        self.assertTrue(is_valid_ordering(["a", "b", "c"], nodes))

    def test_invalid_order(self):
        nodes = {"c": ["b"], "b": ["a"], "a": []}
        self.assertFalse(is_valid_ordering(["c", "b", "a"], nodes))

    def test_mismatched_node_sets(self):
        self.assertFalse(is_valid_ordering(["a", "b"], {"a": [], "b": [], "c": []}))

    def test_empty(self):
        self.assertTrue(is_valid_ordering([], {}))


if __name__ == "__main__":
    unittest.main()
