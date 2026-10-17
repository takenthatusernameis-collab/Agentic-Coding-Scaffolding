import unittest

from copy_utils import (
    copy_dict,
    deep_copy,
    deep_copy_dict,
    is_same_object,
    merge_copy,
    shallow_copy,
)


class TestShallowCopy(unittest.TestCase):
    def test_returns_equal_copy(self):
        original = [1, 2, 3]
        copied = shallow_copy(original)
        self.assertEqual(copied, original)
        self.assertIsNot(copied, original)

    def test_immutable_returns_equal(self):
        self.assertEqual(shallow_copy(42), 42)
        self.assertEqual(shallow_copy("hello"), "hello")

    def test_nested_list_shares_inner(self):
        original = [[1, 2], [3, 4]]
        copied = shallow_copy(original)
        self.assertEqual(copied, original)
        self.assertIsNot(copied, original)
        self.assertIs(copied[0], original[0])


class TestDeepCopy(unittest.TestCase):
    def test_returns_equal_copy(self):
        original = [1, 2, 3]
        copied = deep_copy(original)
        self.assertEqual(copied, original)
        self.assertIsNot(copied, original)

    def test_nested_list_is_independent(self):
        original = [[1, 2], [3, 4]]
        copied = deep_copy(original)
        self.assertEqual(copied, original)
        self.assertIsNot(copied, original)
        self.assertIsNot(copied[0], original[0])
        copied[0].append(99)
        self.assertNotIn(99, original[0])

    def test_dict_is_independent(self):
        original = {"a": [1, 2], "b": {"c": 3}}
        copied = deep_copy(original)
        copied["a"].append(99)
        copied["b"]["c"] = 0
        self.assertNotIn(99, original["a"])
        self.assertEqual(original["b"]["c"], 3)


class TestCopyDict(unittest.TestCase):
    def test_shallow_dict_copy(self):
        original = {"a": 1, "b": 2}
        copied = copy_dict(original)
        self.assertEqual(copied, original)
        self.assertIsNot(copied, original)

    def test_nested_dict_shares_values(self):
        inner = {"x": 1}
        original = {"key": inner}
        copied = copy_dict(original)
        self.assertIs(copied["key"], inner)

    def test_non_dict_raises(self):
        with self.assertRaises(TypeError):
            copy_dict([1, 2, 3])  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            copy_dict("not a dict")  # type: ignore[arg-type]


class TestDeepCopyDict(unittest.TestCase):
    def test_deep_dict_copy(self):
        inner = {"x": 1}
        original = {"key": inner}
        copied = deep_copy_dict(original)
        self.assertEqual(copied, original)
        self.assertIsNot(copied, original)
        self.assertIsNot(copied["key"], inner)
        copied["key"]["x"] = 99
        self.assertEqual(original["key"]["x"], 1)

    def test_non_dict_raises(self):
        with self.assertRaises(TypeError):
            deep_copy_dict(None)  # type: ignore[arg-type]


class TestMergeCopy(unittest.TestCase):
    def test_merges_multiple(self):
        result = merge_copy({"a": 1}, {"b": 2}, {"a": 3})
        self.assertEqual(result, {"a": 3, "b": 2})

    def test_inputs_not_mutated(self):
        base = {"a": 1}
        override = {"b": 2}
        merge_copy(base, override)
        self.assertEqual(base, {"a": 1})
        self.assertEqual(override, {"b": 2})

    def test_empty(self):
        self.assertEqual(merge_copy(), {})

    def test_non_dict_raises(self):
        with self.assertRaises(TypeError):
            merge_copy({"a": 1}, [1, 2])  # type: ignore[arg-type]


class TestIsSameObject(unittest.TestCase):
    def test_same_object(self):
        obj = [1, 2, 3]
        self.assertTrue(is_same_object(obj, obj))

    def test_different_objects(self):
        self.assertFalse(is_same_object([1, 2], [1, 2]))
        self.assertFalse(is_same_object(1, 2))


if __name__ == "__main__":
    unittest.main()
