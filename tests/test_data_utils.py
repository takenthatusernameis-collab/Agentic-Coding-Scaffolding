"""Tests for data_utils module."""

import unittest

from data_utils import deep_copy, flatten_dict, merge_dicts, omit, pick


class TestDeepCopy(unittest.TestCase):
    def test_deep_copy_simple_dict(self) -> None:
        original = {"a": 1, "b": 2}
        copied = deep_copy(original)
        self.assertEqual(original, copied)
        self.assertIsNot(original, copied)

    def test_deep_copy_nested(self) -> None:
        original = {"a": 1, "b": {"c": 3, "d": 4}}
        copied = deep_copy(original)
        self.assertEqual(original, copied)
        self.assertIsNot(original["b"], copied["b"])
        copied_b = copied["b"]
        if isinstance(copied_b, dict):
            copied_b["c"] = 99
        orig_b = original["b"]
        if isinstance(orig_b, dict):
            self.assertEqual(orig_b["c"], 3)

    def test_deep_copy_list(self) -> None:
        original = [1, 2, [3, 4]]
        copied = deep_copy(original)
        self.assertEqual(original, copied)
        self.assertIsNot(original, copied)
        # type: ignore[index]
        if isinstance(copied, list):
            self.assertIsNot(original[2], copied[2])

    def test_deep_copy_primitive(self) -> None:
        self.assertEqual(deep_copy(5), 5)
        self.assertEqual(deep_copy("hello"), "hello")


class TestMergeDicts(unittest.TestCase):
    def test_merge_dicts_basic(self) -> None:
        result = merge_dicts({"a": 1}, {"b": 2})
        self.assertEqual(result, {"a": 1, "b": 2})

    def test_merge_dicts_override(self) -> None:
        result = merge_dicts({"a": 1}, {"a": 3, "b": 2})
        self.assertEqual(result, {"a": 3, "b": 2})

    def test_merge_dicts_multiple(self) -> None:
        result = merge_dicts({"a": 1}, {"b": 2}, {"c": 3, "a": 4})
        self.assertEqual(result, {"a": 4, "b": 2, "c": 3})

    def test_merge_dicts_empty(self) -> None:
        self.assertEqual(merge_dicts(), {})
        self.assertEqual(merge_dicts({}, {"a": 1}), {"a": 1})


class TestPick(unittest.TestCase):
    def test_pick_basic(self) -> None:
        result = pick({"a": 1, "b": 2, "c": 3}, ["a", "c"])
        self.assertEqual(result, {"a": 1, "c": 3})

    def test_pick_missing_keys(self) -> None:
        result = pick({"a": 1, "b": 2}, ["a", "d"])
        self.assertEqual(result, {"a": 1})

    def test_pick_empty_keys(self) -> None:
        result = pick({"a": 1, "b": 2}, [])
        self.assertEqual(result, {})

    def test_pick_no_overlap(self) -> None:
        result = pick({"a": 1}, ["b", "c"])
        self.assertEqual(result, {})


class TestOmit(unittest.TestCase):
    def test_omit_basic(self) -> None:
        result = omit({"a": 1, "b": 2, "c": 3}, ["a", "c"])
        self.assertEqual(result, {"b": 2})

    def test_omit_missing_keys(self) -> None:
        result = omit({"a": 1, "b": 2}, ["c", "d"])
        self.assertEqual(result, {"a": 1, "b": 2})

    def test_omit_empty_keys(self) -> None:
        result = omit({"a": 1, "b": 2}, [])
        self.assertEqual(result, {"a": 1, "b": 2})

    def test_omit_all(self) -> None:
        result = omit({"a": 1, "b": 2}, ["a", "b"])
        self.assertEqual(result, {})


class TestFlattenDict(unittest.TestCase):
    def test_flatten_dict_simple(self) -> None:
        d = {"a": 1, "b": 2}
        result = flatten_dict(d)
        self.assertEqual(result, {"a": 1, "b": 2})

    def test_flatten_dict_nested(self) -> None:
        d = {"a": 1, "b": {"c": 2, "d": 3}}
        result = flatten_dict(d)
        self.assertEqual(result, {"a": 1, "b.c": 2, "b.d": 3})

    def test_flatten_dict_deep_nested(self) -> None:
        d = {"a": {"b": {"c": {"d": 1}}}}
        result = flatten_dict(d)
        self.assertEqual(result, {"a.b.c.d": 1})

    def test_flatten_dict_custom_sep(self) -> None:
        d = {"a": {"b": 2}}
        result = flatten_dict(d, sep="_")
        self.assertEqual(result, {"a_b": 2})

    def test_flatten_dict_mixed(self) -> None:
        d = {"a": 1, "b": {"c": 2}, "d": {"e": {"f": 3}}}
        result = flatten_dict(d)
        self.assertEqual(result, {"a": 1, "b.c": 2, "d.e.f": 3})


if __name__ == "__main__":
    unittest.main()
