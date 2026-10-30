"""Unit tests for type_utils module."""

import typing as t
import unittest

from type_utils import (
    get_origin_name,
    get_type_args,
    is_any,
    is_callable,
    is_class_var,
    is_dict_type,
    is_generic,
    is_list_type,
    is_literal,
    is_none_type,
    is_optional,
    is_subclass_safe,
    is_tuple,
    is_type_var,
    is_union,
    type_name,
    unwrap_optional,
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

    def test_is_literal(self):
        self.assertTrue(is_literal(t.Literal["a", "b"]))
        self.assertTrue(is_literal(t.Literal[1, 2, 3]))
        self.assertFalse(is_literal(int))
        self.assertFalse(is_literal(str))
        self.assertFalse(is_literal(t.Union[int, str]))

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

    def test_is_type_var(self):
        T = t.TypeVar("T")
        self.assertTrue(is_type_var(T))
        self.assertFalse(is_type_var(int))
        self.assertFalse(is_type_var(str))
        self.assertFalse(is_type_var(None))

    def test_is_class_var(self):
        self.assertTrue(is_class_var(t.ClassVar[int]))
        self.assertTrue(is_class_var(t.ClassVar))
        self.assertFalse(is_class_var(int))
        self.assertFalse(is_class_var(str))
        self.assertFalse(is_class_var(None))

    def test_is_callable(self):
        self.assertTrue(is_callable(t.Callable))
        self.assertTrue(is_callable(t.Callable[[int], str]))
        self.assertTrue(is_callable(t.Callable[..., str]))
        self.assertTrue(is_callable(t.Callable[[int, str], None]))
        self.assertFalse(is_callable(int))
        self.assertFalse(is_callable(str))
        self.assertFalse(is_callable(t.List[int]))
        self.assertFalse(is_callable(None))

    def test_is_tuple(self):
        self.assertTrue(is_tuple(t.Tuple))
        self.assertTrue(is_tuple(t.Tuple[int, str]))
        self.assertTrue(is_tuple(t.Tuple[int, ...]))
        self.assertFalse(is_tuple(int))
        self.assertFalse(is_tuple(t.List[int]))
        self.assertFalse(is_tuple(None))

    def test_is_list_type(self):
        self.assertTrue(is_list_type(t.List))
        self.assertTrue(is_list_type(t.List[int]))
        self.assertFalse(is_list_type(int))
        self.assertFalse(is_list_type(t.Tuple[int, str]))
        self.assertFalse(is_list_type(None))

    def test_is_dict_type(self):
        self.assertTrue(is_dict_type(t.Dict))
        self.assertTrue(is_dict_type(t.Dict[str, int]))
        self.assertFalse(is_dict_type(int))
        self.assertFalse(is_dict_type(t.List[int]))
        self.assertFalse(is_dict_type(None))

    def test_get_origin_name(self):
        self.assertEqual(get_origin_name(t.List[int]), "list")
        self.assertEqual(get_origin_name(t.Dict[str, int]), "dict")
        self.assertEqual(get_origin_name(t.Tuple[int, str]), "tuple")
        self.assertEqual(get_origin_name(int), "int")
        self.assertEqual(get_origin_name(str), "str")

    def test_is_none_type(self):
        self.assertTrue(is_none_type(type(None)))
        self.assertTrue(is_none_type(None))
        self.assertFalse(is_none_type(int))
        self.assertFalse(is_none_type(str))

    def test_is_any(self):
        self.assertTrue(is_any(t.Any))
        self.assertFalse(is_any(int))
        self.assertFalse(is_any(str))
        self.assertFalse(is_any(None))

    def test_unwrap_optional(self):
        self.assertEqual(unwrap_optional(t.Optional[int]), int)
        self.assertEqual(unwrap_optional(t.Optional[str]), str)
        self.assertEqual(unwrap_optional(t.Union[int, None]), int)
        self.assertEqual(unwrap_optional(int), int)
        self.assertEqual(unwrap_optional(str), str)
        self.assertEqual(unwrap_optional(t.Union[int, str, None]),
                         t.Union[int, str])


if __name__ == "__main__":
    unittest.main()
