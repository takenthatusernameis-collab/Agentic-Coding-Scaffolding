"""Unit tests for tree_utils module."""

import unittest

from tree_utils import (
    delete_nested,
    filter_tree,
    flatten_tree,
    get_nested,
    map_tree,
    set_nested,
    unflatten_tree,
)


class TestGetNested(unittest.TestCase):
    def test_get_nested_basic(self):
        d = {"a": {"b": {"c": 1}}}
        self.assertEqual(get_nested(d, ["a", "b", "c"]), 1)

    def test_get_nested_with_list(self):
        d = {"a": [10, 20, 30]}
        self.assertEqual(get_nested(d, ["a", 1]), 20)

    def test_get_nested_missing_with_default(self):
        d = {"a": {"b": 2}}
        self.assertEqual(get_nested(d, ["a", "x"], default="missing"), "missing")
        self.assertIsNone(get_nested(d, ["a", "x"]))

    def test_get_nested_partial_path(self):
        d = {"a": {"b": 2}}
        self.assertEqual(get_nested(d, ["a"]), {"b": 2})


class TestSetNested(unittest.TestCase):
    def test_set_nested_creates_intermediate(self):
        d = {}
        result = set_nested(d, ["a", "b", "c"], 1)
        self.assertEqual(d, {"a": {"b": {"c": 1}}})
        self.assertIs(result, d)

    def test_set_nested_overwrites(self):
        d = {"a": {"b": 1}}
        set_nested(d, ["a", "b"], 2)
        self.assertEqual(d, {"a": {"b": 2}})

    def test_set_nested_empty_keys(self):
        d = {"x": 1}
        set_nested(d, [], 5)
        self.assertEqual(d, {"x": 1})


class TestDeleteNested(unittest.TestCase):
    def test_delete_nested_success(self):
        d = {"a": {"b": {"c": 1}}}
        self.assertTrue(delete_nested(d, ["a", "b", "c"]))
        self.assertEqual(d, {"a": {"b": {}}})

    def test_delete_nested_missing(self):
        d = {"a": {"b": 1}}
        self.assertFalse(delete_nested(d, ["a", "x"]))
        self.assertFalse(delete_nested(d, ["x"]))

    def test_delete_nested_empty_keys(self):
        d = {"a": 1}
        self.assertFalse(delete_nested(d, []))


class TestFlattenTree(unittest.TestCase):
    def test_flatten_basic(self):
        d = {"a": {"b": {"c": 1, "d": 2}}, "e": 3}
        result = flatten_tree(d)
        self.assertEqual(result, {"a.b.c": 1, "a.b.d": 2, "e": 3})

    def test_flatten_with_custom_sep(self):
        d = {"a": {"b": 1}}
        result = flatten_tree(d, sep="/")
        self.assertEqual(result, {"a/b": 1})

    def test_flatten_empty_dict(self):
        self.assertEqual(flatten_tree({}), {})

    def test_flatten_non_dict(self):
        self.assertEqual(flatten_tree("hello"), {"": "hello"})


class TestUnflattenTree(unittest.TestCase):
    def test_unflatten_basic(self):
        flat = {"a.b.c": 1, "a.b.d": 2, "e": 3}
        result = unflatten_tree(flat)
        self.assertEqual(result, {"a": {"b": {"c": 1, "d": 2}}, "e": 3})

    def test_unflatten_custom_sep(self):
        flat = {"a/b": 1}
        result = unflatten_tree(flat, sep="/")
        self.assertEqual(result, {"a": {"b": 1}})

    def test_unflatten_empty(self):
        self.assertEqual(unflatten_tree({}), {})


class TestMapTree(unittest.TestCase):
    def test_map_tree_dict(self):
        result = map_tree(lambda x: x * 2, {"a": {"b": 1}, "c": 2})
        self.assertEqual(result, {"a": {"b": 2}, "c": 4})

    def test_map_tree_list(self):
        result = map_tree(lambda x: x * 2, {"a": [1, 2, 3]})
        self.assertEqual(result, {"a": [2, 4, 6]})

    def test_map_tree_tuple(self):
        result = map_tree(lambda x: x + 1, (1, 2))
        self.assertEqual(result, (2, 3))

    def test_map_tree_leaves(self):
        result = map_tree(lambda x: str(x).upper(), 5)
        self.assertEqual(result, "5")


class TestFilterTree(unittest.TestCase):
    def test_filter_tree_basic(self):
        result = filter_tree(lambda x: x > 1, {"a": 1, "b": 2, "c": {"d": 3, "e": 0}})
        self.assertEqual(result, {"b": 2, "c": {"d": 3}})

    def test_filter_tree_list(self):
        result = filter_tree(lambda x: x > 1, {"a": [1, 2, 0, 3]})
        self.assertEqual(result, {"a": [2, 3]})

    def test_filter_tree_all_filtered(self):
        result = filter_tree(lambda x: x > 10, {"a": 1, "b": 2})
        self.assertEqual(result, {})

    def test_filter_tree_tuple(self):
        result = filter_tree(lambda x: x > 1, (1, 2, 3))
        self.assertEqual(result, (2, 3))


if __name__ == "__main__":
    unittest.main()
