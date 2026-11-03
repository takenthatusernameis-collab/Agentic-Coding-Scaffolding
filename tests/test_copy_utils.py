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
    def test_returns_distinct_object(self):
        original = [1, 2, 3]
        result = shallow_copy(original)
        self.assertIsNot(result, original)
        self.assertEqual(result, original)

    def test_shares_nested_references(self):
        nested = [4, 5]
        original = [1, nested]
        result = shallow_copy(original)
        self.assertIs(result[1], nested)

    def test_does_not_mutate_original(self):
        original = [1, 2, 3]
        result = shallow_copy(original)
        result.append(4)
        self.assertEqual(original, [1, 2, 3])


class TestDeepCopy(unittest.TestCase):
    def test_returns_distinct_object(self):
        original = [1, [2, 3]]
        result = deep_copy(original)
        self.assertIsNot(result, original)
        self.assertEqual(result, original)

    def test_clones_nested_references(self):
        nested = [4, 5]
        original = [1, nested]
        result = deep_copy(original)
        self.assertIsNot(result[1], nested)

    def test_mutation_isolation(self):
        original = [1, [2, 3]]
        result = deep_copy(original)
        result[1].append(4)
        self.assertEqual(original, [1, [2, 3]])


class TestCopyDict(unittest.TestCase):
    def test_returns_new_dict(self):
        original = {"a": 1, "b": 2}
        result = copy_dict(original)
        self.assertIsNot(result, original)
        self.assertEqual(result, original)

    def test_rejects_non_dict(self):
        with self.assertRaises(TypeError):
            copy_dict([1, 2, 3])

    def test_mutation_isolation(self):
        original = {"a": 1}
        result = copy_dict(original)
        result["a"] = 99
        self.assertEqual(original, {"a": 1})


class TestDeepCopyDict(unittest.TestCase):
    def test_returns_new_dict(self):
        original = {"a": [1, 2]}
        result = deep_copy_dict(original)
        self.assertIsNot(result, original)
        self.assertEqual(result, original)

    def test_rejects_non_dict(self):
        with self.assertRaises(TypeError):
            deep_copy_dict([1, 2, 3])

    def test_nested_mutation_isolation(self):
        original = {"a": [1, 2]}
        result = deep_copy_dict(original)
        result["a"].append(3)
        self.assertEqual(original, {"a": [1, 2]})


class TestMergeCopy(unittest.TestCase):
    def test_merges_multiple_dicts(self):
        result = merge_copy({"a": 1}, {"b": 2}, {"c": 3})
        self.assertEqual(result, {"a": 1, "b": 2, "c": 3})

    def test_later_dict_takes_precedence(self):
        result = merge_copy({"a": 1}, {"a": 2})
        self.assertEqual(result, {"a": 2})

    def test_returns_new_dict(self):
        first = {"a": 1}
        result = merge_copy(first)
        result["a"] = 99
        self.assertEqual(first, {"a": 1})

    def test_no_args_returns_empty(self):
        self.assertEqual(merge_copy(), {})

    def test_rejects_non_dict_argument(self):
        with self.assertRaises(TypeError):
            merge_copy({"a": 1}, [1, 2, 3])


class TestIsSameObject(unittest.TestCase):
    def test_same_object(self):
        obj = object()
        self.assertTrue(is_same_object(obj, obj))

    def test_different_objects(self):
        a = [1, 2]
        b = [1, 2]
        self.assertFalse(is_same_object(a, b))

    def test_equal_but_distinct(self):
        a = [1, 2]
        b = [1, 2]
        self.assertFalse(is_same_object(a, b))


if __name__ == "__main__":
    unittest.main()
