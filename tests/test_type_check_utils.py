"""Tests for the :mod:`type_check_utils` wrapper."""

from __future__ import annotations

import unittest

import type_check_utils


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

    def test_ensure_type(self) -> None:
        self.assertEqual(type_check_utils.ensure_type("hi", str), "hi")
        with self.assertRaises(TypeError):
            type_check_utils.ensure_type(123, str)

    def test_coerce_to_str(self) -> None:
        self.assertEqual(type_check_utils.coerce_to_str(123), "123")
        self.assertEqual(type_check_utils.coerce_to_str([1, 2]), "[1, 2]")


if __name__ == "__main__":
    unittest.main()
