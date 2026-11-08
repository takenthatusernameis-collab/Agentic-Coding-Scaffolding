"""Tests for dict_utils module."""

import unittest

from dict_utils import (
    contains_key,
    contains_value,
    deep_merge,
    filter_dict,
    flatten_dict,
    has_key,
    has_value,
    invert_dict,
    is_invertible,
    keys_equal,
    merge,
    omit_keys,
    safe_get,
    select_keys,
    unflatten_dict,
    values_equal,
)


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


class TestMerge(unittest.TestCase):
    def test_merge_basic(self) -> None:
        d1 = {"a": 1, "b": 2}
        d2 = {"b": 3, "c": 4}
        result = merge(d1, d2)
        self.assertEqual(result, {"a": 1, "b": 3, "c": 4})

    def test_merge_non_overlapping(self) -> None:
        d1 = {"a": 1}
        d2 = {"b": 2}
        result = merge(d1, d2)
        self.assertEqual(result, {"a": 1, "b": 2})

    def test_merge_first_empty(self) -> None:
        self.assertEqual(merge({}, {"a": 1}), {"a": 1})

    def test_merge_second_empty(self) -> None:
        self.assertEqual(merge({"a": 1}, {}), {"a": 1})

    def test_merge_both_empty(self) -> None:
        self.assertEqual(merge({}, {}), {})

    def test_merge_is_shallow(self) -> None:
        d1 = {"a": {"x": 1}}
        d2 = {"a": {"y": 2}}
        result = merge(d1, d2)
        # Shallow: d2's nested dict replaces d1's entirely (no deep merge).
        self.assertEqual(result["a"], {"y": 2})

    def test_merge_does_not_mutate_inputs(self) -> None:
        d1 = {"a": 1, "b": 2}
        d2 = {"b": 3, "c": 4}
        result = merge(d1, d2)
        self.assertEqual(d1, {"a": 1, "b": 2})
        self.assertEqual(d2, {"b": 3, "c": 4})
        result["a"] = 99
        self.assertEqual(d1, {"a": 1, "b": 2})

    def test_merge_type_error(self) -> None:
        with self.assertRaises(TypeError):
            merge("x", {"a": 1})  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            merge({"a": 1}, "x")  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            merge(None, None)  # type: ignore[arg-type]


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


class TestHasKey(unittest.TestCase):
    def test_has_key_present(self) -> None:
        d = {"a": 1, "b": 2}
        self.assertTrue(has_key(d, "a"))
        self.assertTrue(has_key(d, "b"))

    def test_has_key_absent(self) -> None:
        d = {"a": 1, "b": 2}
        self.assertFalse(has_key(d, "c"))
        self.assertFalse(has_key(d, "z"))

    def test_has_key_empty_dict(self) -> None:
        self.assertFalse(has_key({}, "a"))

    def test_has_key_type_error(self) -> None:
        with self.assertRaises(TypeError):
            has_key("x", "a")  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            has_key(None, "a")  # type: ignore[arg-type]


class TestContainsKey(unittest.TestCase):
    def test_contains_key_present(self) -> None:
        d = {"a": 1, "b": 2}
        self.assertTrue(contains_key(d, "a"))
        self.assertTrue(contains_key(d, "b"))

    def test_contains_key_absent(self) -> None:
        d = {"a": 1, "b": 2}
        self.assertFalse(contains_key(d, "c"))
        self.assertFalse(contains_key(d, "z"))

    def test_contains_key_empty_dict(self) -> None:
        self.assertFalse(contains_key({}, "a"))

    def test_contains_key_matches_has_key(self) -> None:
        d = {"a": 1, "b": 2, "c": 3}
        for key in ("a", "b", "c", "z"):
            self.assertEqual(contains_key(d, key), has_key(d, key))

    def test_contains_key_type_error(self) -> None:
        with self.assertRaises(TypeError):
            contains_key("x", "a")  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            contains_key(None, "a")  # type: ignore[arg-type]


class TestKeysEqual(unittest.TestCase):
    def test_same_keys(self) -> None:
        self.assertTrue(keys_equal({"a": 1, "b": 2}, {"a": 3, "b": 4}))

    def test_different_keys(self) -> None:
        self.assertFalse(keys_equal({"a": 1}, {"a": 1, "b": 2}))

    def test_empty(self) -> None:
        self.assertTrue(keys_equal({}, {}))

    def test_type_error(self) -> None:
        with self.assertRaises(TypeError):
            keys_equal("not a dict", {})


class TestValuesEqual(unittest.TestCase):
    def test_same_values(self):
        self.assertTrue(values_equal({"a": 1, "b": 2}, {"c": 2, "d": 1}))

    def test_different(self):
        self.assertFalse(values_equal({"a": 1}, {"a": 1, "b": 2}))

    def test_empty(self):
        self.assertTrue(values_equal({}, {}))

    def test_type_error(self):
        with self.assertRaises(TypeError):
            values_equal("not a dict", {})


class TestHasValue(unittest.TestCase):
    def test_present(self) -> None:
        self.assertTrue(has_value({"a": 1, "b": 2}, 1))
        self.assertTrue(has_value({"a": 1, "b": 2}, 2))

    def test_absent(self) -> None:
        self.assertFalse(has_value({"a": 1, "b": 2}, 3))

    def test_empty(self) -> None:
        self.assertFalse(has_value({}, 1))

    def test_none_and_falsy(self) -> None:
        self.assertTrue(has_value({"a": None}, None))
        self.assertTrue(has_value({"a": 0}, 0))
        self.assertTrue(has_value({"a": False}, False))

    def test_type_error(self) -> None:
        with self.assertRaises(TypeError):
            has_value("x", 1)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            has_value(None, 1)  # type: ignore[arg-type]


class TestContainsValue(unittest.TestCase):
    def test_present(self) -> None:
        self.assertTrue(contains_value({"a": 1, "b": 2}, 1))

    def test_absent(self) -> None:
        self.assertFalse(contains_value({"a": 1, "b": 2}, 3))

    def test_empty(self) -> None:
        self.assertFalse(contains_value({}, 1))

    def test_matches_has_value(self) -> None:
        d = {"a": 1, "b": 2}
        for v in (1, 2, 3, None):
            self.assertEqual(contains_value(d, v), has_value(d, v))

    def test_type_error(self) -> None:
        with self.assertRaises(TypeError):
            contains_value("x", 1)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            contains_value(None, 1)  # type: ignore[arg-type]

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


def _safe_invert(d: dict) -> bool:
    """Helper mirroring invert_dict's success condition without raising."""
    try:
        invert_dict(d)
        return True
    except ValueError:
        return False


class TestIsInvertible(unittest.TestCase):
    def test_invertible_unique_values(self) -> None:
        self.assertTrue(is_invertible({"a": 1, "b": 2}))
        self.assertTrue(is_invertible({"a": 1, "b": "x"}))

    def test_not_invertible_duplicate_values(self) -> None:
        self.assertFalse(is_invertible({"a": 1, "b": 1}))
        self.assertFalse(is_invertible({"a": 1, "b": 1, "c": 2}))

    def test_empty_is_invertible(self) -> None:
        self.assertTrue(is_invertible({}))

    def test_single_entry(self) -> None:
        self.assertTrue(is_invertible({"a": 1}))

    def test_consistency_with_invert_dict(self) -> None:
        cases = [
            {"a": 1, "b": 2},
            {"a": 1, "b": 1},
            {},
            {"a": 1, "b": 2, "c": 3},
            {"a": 1, "b": 2, "c": 1},
        ]
        for d in cases:
            self.assertEqual(is_invertible(d), _safe_invert(d), msg=f"mismatch for {d}")

    def test_type_error(self) -> None:
        with self.assertRaises(TypeError):
            is_invertible("x")  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            is_invertible(None)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            is_invertible([1, 2])  # type: ignore[arg-type]


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


class TestSelectKeys(unittest.TestCase):
    def test_select_keys_basic(self) -> None:
        d = {"a": 1, "b": 2, "c": 3}
        self.assertEqual(select_keys(d, ["a", "c"]), {"a": 1, "c": 3})

    def test_select_keys_missing(self) -> None:
        d = {"a": 1}
        self.assertEqual(select_keys(d, ["a", "z"]), {"a": 1})

    def test_select_keys_empty(self) -> None:
        d = {"a": 1}
        self.assertEqual(select_keys(d, []), {})

    def test_select_keys_type_error(self) -> None:
        with self.assertRaises(TypeError):
            select_keys("x", ["a"])  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            select_keys({"a": 1}, "a")  # type: ignore[arg-type]


class TestOmitKeys(unittest.TestCase):
    def test_omit_keys_basic(self) -> None:
        d = {"a": 1, "b": 2, "c": 3}
        self.assertEqual(omit_keys(d, ["b"]), {"a": 1, "c": 3})

    def test_omit_keys_missing(self) -> None:
        d = {"a": 1}
        self.assertEqual(omit_keys(d, ["z"]), {"a": 1})

    def test_omit_keys_empty(self) -> None:
        d = {"a": 1}
        self.assertEqual(omit_keys(d, []), {"a": 1})

    def test_omit_keys_type_error(self) -> None:
        with self.assertRaises(TypeError):
            omit_keys("x", ["a"])  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            omit_keys({"a": 1}, "a")  # type: ignore[arg-type]
