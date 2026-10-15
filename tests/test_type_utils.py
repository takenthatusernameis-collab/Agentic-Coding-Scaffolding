"""Unit tests for type_utils module."""
import typing as t
import unittest

from type_utils import (
    get_type_args,
    is_generic,
    is_optional,
    is_subclass_safe,
    is_union,
    type_name,
)


class TestTypeUtils(unittest.TestCase):
    def test_is_optional_none(self):
        self.assertTrue(is_optional(t.Optional[int]))
        self.assertTrue(is_optional(t.Optional[str]))
        self.assertTrue(is_optional(t.Union[int, None]))
        self.assertTrue(is_optional(type(None)))
        self.assertFalse(is_optional(int))
        self.assertFalse(is_optional(str))

    def test_is_union(self):
        self.assertTrue(is_union(t.Union[int, str]))
        self.assertTrue(is_union(t.Union[int, str, None]))
        self.assertFalse(is_union(int))
        self.assertFalse(is_union(t.List[int]))

    def test_is_generic(self):
        self.assertTrue(is_generic(t.List[int]))
        self.assertTrue(is_generic(t.Dict[str, int]))
        self.assertTrue(is_generic(t.Set[str]))
        self.assertFalse(is_generic(int))
        self.assertFalse(is_generic(str))

    def test_get_type_args(self):
        self.assertEqual(get_type_args(t.List[int]), (int,))
        self.assertEqual(get_type_args(t.Dict[str, int]), (str, int))
        args = get_type_args(t.Union[int, str, None])
        self.assertIn(int, args)
        self.assertIn(str, args)
        self.assertIn(type(None), args)

    def test_type_name(self):
        self.assertEqual(type_name(int), "int")
        self.assertEqual(type_name(str), "str")
        name = type_name(t.List[int])
        self.assertTrue("List" in name or "list" in name)
        self.assertIn("int", name)
        name = type_name(t.Dict[str, int])
        self.assertTrue("Dict" in name or "dict" in name)
        self.assertIn("str", name)
        self.assertIn("int", name)
        self.assertEqual(type_name(None), "None")

    def test_is_subclass_safe(self):
        self.assertTrue(is_subclass_safe(bool, int))
        self.assertTrue(is_subclass_safe(str, object))
        self.assertFalse(is_subclass_safe(int, str))
        self.assertTrue(is_subclass_safe(bool, (int, str)))
        self.assertFalse(is_subclass_safe(is_subclass_safe, object))
        self.assertFalse(is_subclass_safe(42, int))


if __name__ == "__main__":
    unittest.main()
