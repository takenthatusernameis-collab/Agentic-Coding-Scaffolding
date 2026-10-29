"""Tests for the :mod:`type_check_utils` wrapper."""

from __future__ import annotations

import unittest
from typing import Protocol, runtime_checkable

import type_check_utils


class MyProtocol(Protocol):
    def do(self) -> None: ...


@runtime_checkable
class RCProtocol(Protocol):
    def do(self) -> None: ...


class TestIsProtocol(unittest.TestCase):
    def test_protocol_class(self) -> None:
        self.assertTrue(type_check_utils.is_protocol(MyProtocol))

    def test_runtime_checkable_protocol(self) -> None:
        self.assertTrue(type_check_utils.is_protocol(RCProtocol))

    def test_builtin_types_are_not_protocols(self) -> None:
        self.assertFalse(type_check_utils.is_protocol(int))
        self.assertFalse(type_check_utils.is_protocol(str))
        self.assertFalse(type_check_utils.is_protocol(float))
        self.assertFalse(type_check_utils.is_protocol(bool))
        self.assertFalse(type_check_utils.is_protocol(list))
        self.assertFalse(type_check_utils.is_protocol(dict))
        self.assertFalse(type_check_utils.is_protocol(tuple))
        self.assertFalse(type_check_utils.is_protocol(set))
        self.assertFalse(type_check_utils.is_protocol(object))
        self.assertFalse(type_check_utils.is_protocol(Exception))

    def test_non_class_raises_type_error(self) -> None:
        with self.assertRaises(TypeError):
            type_check_utils.is_protocol("not a class")
        with self.assertRaises(TypeError):
            type_check_utils.is_protocol(123)
        with self.assertRaises(TypeError):
            type_check_utils.is_protocol(None)
        with self.assertRaises(TypeError):
            type_check_utils.is_protocol([])
        with self.assertRaises(TypeError):
            type_check_utils.is_protocol({})


class TestIsNamedtuple(unittest.TestCase):
    def test_namedtuple_class(self) -> None:
        from collections import namedtuple

        Point = namedtuple("Point", ["x", "y"])
        self.assertTrue(type_check_utils.is_namedtuple(Point))

    def test_namedtuple_instance(self) -> None:
        from collections import namedtuple

        Point = namedtuple("Point", ["x", "y"])
        self.assertTrue(type_check_utils.is_namedtuple(Point(1, 2)))

    def test_plain_tuple_is_not_namedtuple(self) -> None:
        self.assertFalse(type_check_utils.is_namedtuple((1, 2)))
        self.assertFalse(type_check_utils.is_namedtuple(()))

    def test_non_tuple_is_not_namedtuple(self) -> None:
        self.assertFalse(type_check_utils.is_namedtuple([1, 2]))
        self.assertFalse(type_check_utils.is_namedtuple({"a": 1}))
        self.assertFalse(type_check_utils.is_namedtuple(42))
        self.assertFalse(type_check_utils.is_namedtuple("hello"))
        self.assertFalse(type_check_utils.is_namedtuple(None))


class TestTypedDictChecks(unittest.TestCase):
    def test_typed_dict_class(self) -> None:
        from typing import TypedDict

        class Point(TypedDict):
            x: int
            y: int

        self.assertTrue(type_check_utils.is_typeddict(Point))

    def test_plain_dict_is_not_typed_dict(self) -> None:
        self.assertFalse(type_check_utils.is_typeddict({"x": 1}))
        self.assertFalse(type_check_utils.is_typeddict({}))

    def test_non_dict_is_not_typed_dict(self) -> None:
        self.assertFalse(type_check_utils.is_typeddict([1, 2]))
        self.assertFalse(type_check_utils.is_typeddict((1, 2)))
        self.assertFalse(type_check_utils.is_typeddict(42))
        self.assertFalse(type_check_utils.is_typeddict("hello"))
        self.assertFalse(type_check_utils.is_typeddict(None))


class TestTypeChecks(unittest.TestCase):
    def test_is_str(self) -> None:
        self.assertTrue(type_check_utils.is_str("hello"))
        self.assertFalse(type_check_utils.is_str(123))
        self.assertFalse(type_check_utils.is_str(None))

    def test_is_int(self) -> None:
        self.assertTrue(type_check_utils.is_int(5))
        self.assertFalse(type_check_utils.is_int(5.0))
        self.assertFalse(type_check_utils.is_int(True))
        self.assertFalse(type_check_utils.is_int("5"))

    def test_is_float(self) -> None:
        self.assertTrue(type_check_utils.is_float(3.14))
        self.assertFalse(type_check_utils.is_float(3))

    def test_is_bool(self) -> None:
        self.assertTrue(type_check_utils.is_bool(True))
        self.assertFalse(type_check_utils.is_bool(1))

    def test_is_list(self) -> None:
        self.assertTrue(type_check_utils.is_list([1, 2, 3]))
        self.assertFalse(type_check_utils.is_list((1, 2)))

    def test_is_dict(self) -> None:
        self.assertTrue(type_check_utils.is_dict({"a": 1}))
        self.assertFalse(type_check_utils.is_dict([1, 2]))

    def test_is_tuple(self) -> None:
        self.assertTrue(type_check_utils.is_tuple((1, 2)))
        self.assertFalse(type_check_utils.is_tuple([1, 2]))

    def test_is_set(self) -> None:
        self.assertTrue(type_check_utils.is_set({1, 2}))
        self.assertFalse(type_check_utils.is_set([1, 2]))

    def test_is_none(self) -> None:
        self.assertTrue(type_check_utils.is_none(None))
        self.assertFalse(type_check_utils.is_none(0))

    def test_is_bytes(self) -> None:
        self.assertTrue(type_check_utils.is_bytes(b"hello"))
        self.assertTrue(type_check_utils.is_bytes(bytearray(b"hello")))
        self.assertFalse(type_check_utils.is_bytes("hello"))
        self.assertFalse(type_check_utils.is_bytes([]))

    def test_is_numeric(self) -> None:
        self.assertTrue(type_check_utils.is_numeric(5))
        self.assertTrue(type_check_utils.is_numeric(3.14))
        self.assertFalse(type_check_utils.is_numeric(True))
        self.assertFalse(type_check_utils.is_numeric("5"))

    def test_is_iterable(self) -> None:
        self.assertTrue(type_check_utils.is_iterable([1, 2, 3]))
        self.assertFalse(type_check_utils.is_iterable("hello"))
        self.assertFalse(type_check_utils.is_iterable(123))

    def test_is_callable(self) -> None:
        self.assertTrue(type_check_utils.is_callable(len))
        self.assertFalse(type_check_utils.is_callable(123))

    def test_is_module(self) -> None:
        import sys

        self.assertTrue(type_check_utils.is_module(sys))
        self.assertTrue(type_check_utils.is_module(type_check_utils))
        self.assertFalse(type_check_utils.is_module(42))
        self.assertFalse(type_check_utils.is_module(len))
        self.assertFalse(type_check_utils.is_module("sys"))
        self.assertFalse(type_check_utils.is_module(None))

    def test_ensure_type(self) -> None:
        self.assertEqual(type_check_utils.ensure_type("hi", str), "hi")
        with self.assertRaises(TypeError):
            type_check_utils.ensure_type(123, str)

    def test_coerce_to_str(self) -> None:
        self.assertEqual(type_check_utils.coerce_to_str(123), "123")
        self.assertEqual(type_check_utils.coerce_to_str([1, 2]), "[1, 2]")

    def test_coerce_to_int(self) -> None:
        self.assertEqual(type_check_utils.coerce_to_int(123), 123)
        self.assertEqual(type_check_utils.coerce_to_int("456"), 456)
        self.assertEqual(type_check_utils.coerce_to_int(True), 1)
        self.assertEqual(type_check_utils.coerce_to_int(False), 0)
        self.assertEqual(type_check_utils.coerce_to_int(3.99), 3)
        self.assertEqual(type_check_utils.coerce_to_int("-7"), -7)
        with self.assertRaises(ValueError):
            type_check_utils.coerce_to_int("not-a-number")
        with self.assertRaises(TypeError):
            type_check_utils.coerce_to_int([1, 2])
        with self.assertRaises(TypeError):
            type_check_utils.coerce_to_int(None)

    def test_coerce_to_float(self) -> None:
        self.assertEqual(type_check_utils.coerce_to_float(123), 123.0)
        self.assertEqual(type_check_utils.coerce_to_float("4.56"), 4.56)
        self.assertEqual(type_check_utils.coerce_to_float(True), 1.0)
        self.assertEqual(type_check_utils.coerce_to_float(False), 0.0)
        self.assertEqual(type_check_utils.coerce_to_float(3), 3.0)
        self.assertEqual(type_check_utils.coerce_to_float(-7.5), -7.5)
        self.assertEqual(type_check_utils.coerce_to_float("-7"), -7.0)
        self.assertEqual(type_check_utils.coerce_to_float("0"), 0.0)
        with self.assertRaises(ValueError):
            type_check_utils.coerce_to_float("not-a-float")
        with self.assertRaises(TypeError):
            type_check_utils.coerce_to_float([1, 2])
        with self.assertRaises(TypeError):
            type_check_utils.coerce_to_float(None)

    def test_coerce_to_bool(self) -> None:
        self.assertEqual(type_check_utils.coerce_to_bool(True), True)
        self.assertEqual(type_check_utils.coerce_to_bool(False), False)
        self.assertEqual(type_check_utils.coerce_to_bool(1), True)
        self.assertEqual(type_check_utils.coerce_to_bool(0), False)
        self.assertEqual(type_check_utils.coerce_to_bool(2), True)
        self.assertEqual(type_check_utils.coerce_to_bool(0.0), False)
        self.assertEqual(type_check_utils.coerce_to_bool(1.5), True)
        self.assertEqual(type_check_utils.coerce_to_bool("true"), True)
        self.assertEqual(type_check_utils.coerce_to_bool("False"), False)
        self.assertEqual(type_check_utils.coerce_to_bool("1"), True)
        self.assertEqual(type_check_utils.coerce_to_bool("0"), False)
        self.assertEqual(type_check_utils.coerce_to_bool("yes"), True)
        self.assertEqual(type_check_utils.coerce_to_bool("no"), False)
        with self.assertRaises(ValueError):
            type_check_utils.coerce_to_bool("not-a-bool")
        with self.assertRaises(TypeError):
            type_check_utils.coerce_to_bool([1, 2])
        with self.assertRaises(TypeError):
            type_check_utils.coerce_to_bool(None)


if __name__ == "__main__":
    unittest.main()
