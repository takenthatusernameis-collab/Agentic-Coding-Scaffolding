"""Tests for data_utils module."""

import unittest

from data_utils import (
    deep_copy,
    del_nested,
    flatten_dict,
    get_nested,
    invert_dict,
    merge_dicts,
    omit,
    pick,
    set_nested,
)


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


class TestInvertDict(unittest.TestCase):
    def test_invert_dict_basic(self) -> None:
        self.assertEqual(invert_dict({"a": 1, "b": 2}), {1: "a", 2: "b"})

    def test_invert_dict_empty(self) -> None:
        self.assertEqual(invert_dict({}), {})

    def test_invert_dict_single(self) -> None:
        self.assertEqual(invert_dict({"x": 42}), {42: "x"})

    def test_invert_dict_duplicate_values(self) -> None:
        with self.assertRaises(ValueError):
            invert_dict({"a": 1, "b": 1})

    def test_invert_dict_rejects_non_dict(self) -> None:
        with self.assertRaises(TypeError):
            invert_dict(["a", "b"])  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            invert_dict("ab")  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            invert_dict(None)  # type: ignore[arg-type]


class TestGetNested(unittest.TestCase):
    def test_get_nested_basic(self) -> None:
        self.assertEqual(get_nested({"a": {"b": 1}}, "a.b"), 1)

    def test_get_nested_deep(self) -> None:
        self.assertEqual(get_nested({"a": {"b": {"c": 3}}}, "a.b.c"), 3)

    def test_get_nested_missing_returns_default(self) -> None:
        self.assertIsNone(get_nested({"a": {"b": 1}}, "a.c"))
        self.assertEqual(get_nested({"a": {"b": 1}}, "a.c", default=0), 0)

    def test_get_nested_missing_top_level(self) -> None:
        self.assertIsNone(get_nested({"a": 1}, "b"))

    def test_get_nested_empty_dict(self) -> None:
        self.assertIsNone(get_nested({}, "a.b"))

    def test_get_nested_intermediate_not_dict(self) -> None:
        self.assertIsNone(get_nested({"a": 1}, "a.b"))

    def test_get_nested_custom_separator(self) -> None:
        self.assertEqual(get_nested({"a": {"b": 2}}, "a/b", sep="/"), 2)

    def test_get_nested_rejects_non_dict(self) -> None:
        with self.assertRaises(TypeError):
            get_nested(["a", "b"], "a.b")  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            get_nested("ab", "a.b")  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            get_nested(None, "a.b")  # type: ignore[arg-type]

    def test_get_nested_rejects_non_string_path(self) -> None:
        with self.assertRaises(TypeError):
            get_nested({"a": 1}, 1)  # type: ignore[arg-type]


class TestSetNested(unittest.TestCase):
    def test_set_nested_basic(self) -> None:
        d: dict = {}
        result = set_nested(d, "a.b.c", 1)
        self.assertEqual(d, {"a": {"b": {"c": 1}}})
        self.assertIs(result, d)

    def test_set_nested_deep(self) -> None:
        d = {"a": {"b": {"c": 1}}}
        result = set_nested(d, "a.b.d", 2)
        self.assertEqual(d, {"a": {"b": {"c": 1, "d": 2}}})
        self.assertIs(result, d)

    def test_set_nested_creates_intermediate(self) -> None:
        d: dict = {"a": {}}
        result = set_nested(d, "a.b.c", 5)
        self.assertEqual(d, {"a": {"b": {"c": 5}}})
        self.assertIs(result, d)

    def test_set_nested_overwrites_intermediate(self) -> None:
        d = {"a": 1}
        result = set_nested(d, "a.b.c", 9)
        self.assertEqual(d, {"a": {"b": {"c": 9}}})
        self.assertIs(result, d)

    def test_set_nested_top_level(self) -> None:
        d: dict = {}
        result = set_nested(d, "a", 42)
        self.assertEqual(d, {"a": 42})
        self.assertIs(result, d)

    def test_set_nested_custom_separator(self) -> None:
        d: dict = {}
        result = set_nested(d, "a/b/c", 7, sep="/")
        self.assertEqual(d, {"a": {"b": {"c": 7}}})
        self.assertIs(result, d)

    def test_set_nested_empty_dict(self) -> None:
        d: dict = {}
        result = set_nested(d, "a.b", 1)
        self.assertEqual(d, {"a": {"b": 1}})
        self.assertIs(result, d)

    def test_set_nested_rejects_non_dict(self) -> None:
        with self.assertRaises(TypeError):
            set_nested(["a", "b"], "a.b", 1)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            set_nested("ab", "a.b", 1)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            set_nested(None, "a.b", 1)  # type: ignore[arg-type]

    def test_set_nested_rejects_non_string_path(self) -> None:
        with self.assertRaises(TypeError):
            set_nested({"a": 1}, 1, 1)  # type: ignore[arg-type]

    def test_set_nested_rejects_empty_path(self) -> None:
        with self.assertRaises(ValueError):
            set_nested({"a": 1}, "", 1)
        with self.assertRaises(ValueError):
            set_nested({"a": 1}, ".", 1)


class TestDelNested(unittest.TestCase):
    def test_del_nested_basic(self) -> None:
        d = {"a": {"b": 1}}
        self.assertTrue(del_nested(d, "a.b"))
        self.assertEqual(d, {"a": {}})

    def test_del_nested_deep(self) -> None:
        d = {"a": {"b": {"c": 3}}}
        self.assertTrue(del_nested(d, "a.b.c"))
        self.assertEqual(d, {"a": {"b": {}}})

    def test_del_nested_missing_path_returns_false(self) -> None:
        d = {"a": {"b": 1}}
        self.assertFalse(del_nested(d, "a.c"))
        self.assertEqual(d, {"a": {"b": 1}})

    def test_del_nested_missing_top_level(self) -> None:
        d = {"a": 1}
        self.assertFalse(del_nested(d, "b"))
        self.assertEqual(d, {"a": 1})

    def test_del_nested_empty_dict(self) -> None:
        self.assertFalse(del_nested({}, "a.b"))

    def test_del_nested_intermediate_not_dict(self) -> None:
        d = {"a": 1}
        self.assertFalse(del_nested(d, "a.b"))

    def test_del_nested_custom_separator(self) -> None:
        d = {"a": {"b": 2}}
        self.assertTrue(del_nested(d, "a/b", sep="/"))
        self.assertEqual(d, {"a": {}})

    def test_del_nested_rejects_non_dict(self) -> None:
        with self.assertRaises(TypeError):
            del_nested(["a", "b"], "a.b")  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            del_nested("ab", "a.b")  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            del_nested(None, "a.b")  # type: ignore[arg-type]

    def test_del_nested_rejects_non_string_path(self) -> None:
        with self.assertRaises(TypeError):
            del_nested({"a": 1}, 1)  # type: ignore[arg-type]

    def test_del_nested_rejects_empty_path(self) -> None:
        with self.assertRaises(ValueError):
            del_nested({"a": 1}, "")
        with self.assertRaises(ValueError):
            del_nested({"a": 1}, ".")


if __name__ == "__main__":
    unittest.main()
