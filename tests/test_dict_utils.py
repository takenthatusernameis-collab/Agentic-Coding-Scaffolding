"""Tests for dict_utils module."""

import unittest

from dict_utils import deep_merge, filter_dict, flatten_dict, invert_dict, safe_get, unflatten_dict


class TestDeepMerge(unittest.TestCase):
    def test_deep_merge_basic(self) -> None:
        d1 = {"a": 1, "b": {"c": 2}}
        d2 = {"b": {"d": 3}, "e": 4}
        result = deep_merge(d1, d2)
        self.assertEqual(result["a"], 1)
        self.assertEqual(result["b"]["c"], 2)
        self.assertEqual(result["b"]["d"], 3)
        self.assertEqual(result["e"], 4)

    def test_deep_merge_overwrite(self) -> None:
        d1 = {"a": 1}
        d2 = {"a": 2}
        result = deep_merge(d1, d2)
        self.assertEqual(result["a"], 2)

    def test_deep_merge_no_overwrite_nested(self) -> None:
        d1 = {"a": {"b": 1, "c": 2}}
        d2 = {"a": {"b": 3}}
        result = deep_merge(d1, d2)
        self.assertEqual(result["a"]["b"], 3)
        self.assertEqual(result["a"]["c"], 2)


class TestFlattenDict(unittest.TestCase):
    def test_flatten_basic(self) -> None:
        d = {"a": 1, "b": {"c": 2, "d": 3}}
        result = flatten_dict(d)
        self.assertEqual(result["a"], 1)
        self.assertEqual(result["b.c"], 2)
        self.assertEqual(result["b.d"], 3)

    def test_flatten_with_sep(self) -> None:
        d = {"a": {"b": {"c": 1}}}
        result = flatten_dict(d, sep="_")
        self.assertEqual(result["a_b_c"], 1)

    def test_flatten_parent_key(self) -> None:
        d = {"b": 2}
        result = flatten_dict(d, parent_key="a")
        self.assertEqual(result["a.b"], 2)


class TestUnflattenDict(unittest.TestCase):
    def test_unflatten_basic(self) -> None:
        d = {"a.b.c": 1, "a.b.d": 2}
        result = unflatten_dict(d)
        self.assertEqual(result["a"]["b"]["c"], 1)
        self.assertEqual(result["a"]["b"]["d"], 2)

    def test_unflatten_simple(self) -> None:
        d = {"a": 1, "b": 2}
        result = unflatten_dict(d)
        self.assertEqual(result["a"], 1)
        self.assertEqual(result["b"], 2)


class TestSafeGet(unittest.TestCase):
    def test_safe_get_basic(self) -> None:
        d = {"a": {"b": {"c": 1}}}
        self.assertEqual(safe_get(d, "a", "b", "c"), 1)

    def test_safe_get_default(self) -> None:
        d = {"a": 1}
        self.assertEqual(safe_get(d, "b", default="missing"), "missing")
        self.assertIsNone(safe_get(d, "b"))

    def test_safe_get_partial(self) -> None:
        d = {"a": 1}
        self.assertEqual(safe_get(d, "a", "b", default="x"), "x")


class TestInvertDict(unittest.TestCase):
    def test_invert_basic(self) -> None:
        d = {"a": 1, "b": 2}
        result = invert_dict(d)
        self.assertEqual(result[1], "a")
        self.assertEqual(result[2], "b")

    def test_invert_duplicate_values_raises(self) -> None:
        d = {"a": 1, "b": 1}
        with self.assertRaises(ValueError):
            invert_dict(d)


class TestFilterDict(unittest.TestCase):
    def test_filter_dict_basic(self) -> None:
        d = {"a": 1, "b": 2, "c": 3}
        result = filter_dict(d, lambda k, v: v > 1)
        self.assertIn("b", result)
        self.assertIn("c", result)
        self.assertNotIn("a", result)

    def test_filter_dict_by_key(self) -> None:
        d = {"a1": 1, "b1": 2, "a2": 3}
        result = filter_dict(d, lambda k, v: k.startswith("a"))
        self.assertEqual(len(result), 2)
