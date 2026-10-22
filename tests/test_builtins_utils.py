"""Tests for :mod:`builtins_utils`."""

from __future__ import annotations

import unittest

from builtins_utils import (
    absolute,
    all_true,
    any_true,
    ascii_str,
    binary_string,
    boolean,
    callable_object,
    character,
    divmod_pair,
    format_value,
    get_hash,
    hex_string,
    is_instance,
    is_subclass,
    iterator,
    length,
    maximum,
    minimum,
    octal_string,
    ordinal,
    power,
    representation,
    round_number,
    sorted_list,
    summation,
)


class TestBuiltinsUtils(unittest.TestCase):
    def test_absolute(self) -> None:
        self.assertEqual(absolute(-5), 5)
        self.assertEqual(absolute(5), 5)

    def test_all_true(self) -> None:
        self.assertTrue(all_true([True, 1, "x"]))
        self.assertFalse(all_true([True, 0, "x"]))
        self.assertTrue(all_true([]))
        with self.assertRaises(TypeError):
            all_true(123)  # type: ignore[arg-type]

    def test_any_true(self) -> None:
        self.assertTrue(any_true([False, 0, "x"]))
        self.assertFalse(any_true([False, 0, ""]))
        self.assertFalse(any_true([]))
        with self.assertRaises(TypeError):
            any_true(123)  # type: ignore[arg-type]

    def test_ascii_str(self) -> None:
        result = ascii_str("hello")
        self.assertIsInstance(result, str)

    def test_binary_string(self) -> None:
        self.assertEqual(binary_string(5), "0b101")
        with self.assertRaises(TypeError):
            binary_string(5.0)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            binary_string(True)  # type: ignore[arg-type]

    def test_boolean(self) -> None:
        self.assertEqual(boolean(), False)
        self.assertEqual(boolean(1), True)
        self.assertEqual(boolean([]), False)

    def test_callable_object(self) -> None:
        self.assertTrue(callable_object(len))
        self.assertFalse(callable_object(5))

    def test_character(self) -> None:
        self.assertEqual(character(65), "A")
        with self.assertRaises(TypeError):
            character(65.0)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            character(True)  # type: ignore[arg-type]
        with self.assertRaises(ValueError):
            character(-1)
        with self.assertRaises(ValueError):
            character(0x110000)

    def test_divmod_pair(self) -> None:
        self.assertEqual(divmod_pair(7, 3), (2, 1))

    def test_format_value(self) -> None:
        self.assertEqual(format_value(3.14159, ".2f"), "3.14")
        with self.assertRaises(TypeError):
            format_value(5, 123)  # type: ignore[arg-type]

    def test_get_hash(self) -> None:
        self.assertIsInstance(get_hash("hello"), int)

    def test_hex_string(self) -> None:
        self.assertEqual(hex_string(255), "0xff")
        with self.assertRaises(TypeError):
            hex_string(255.0)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            hex_string(True)  # type: ignore[arg-type]

    def test_is_instance(self) -> None:
        self.assertTrue(is_instance(5, int))
        self.assertTrue(is_instance(True, (bool, int)))
        with self.assertRaises(TypeError):
            is_instance(5, 123)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            is_instance(5, (123,))  # type: ignore[arg-type]

    def test_is_subclass(self) -> None:
        self.assertTrue(is_subclass(bool, int))
        self.assertTrue(is_subclass(bool, (int, str)))
        with self.assertRaises(TypeError):
            is_subclass(5, int)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            is_subclass(bool, 123)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            is_subclass(bool, (123,))  # type: ignore[arg-type]

    def test_iterator(self) -> None:
        it = iterator([1, 2, 3])
        self.assertEqual(next(it), 1)
        it2 = iterator(lambda: 1, 1)
        self.assertEqual(next(it2), 1)
        with self.assertRaises(TypeError):
            iterator(123)  # type: ignore[arg-type]

    def test_length(self) -> None:
        self.assertEqual(length([1, 2, 3]), 3)
        with self.assertRaises(TypeError):
            length(123)  # type: ignore[arg-type]

    def test_maximum(self) -> None:
        self.assertEqual(maximum(1, 2, 3), 3)
        self.assertEqual(maximum([1, 2, 3]), 3)

    def test_minimum(self) -> None:
        self.assertEqual(minimum(1, 2, 3), 1)
        self.assertEqual(minimum([1, 2, 3]), 1)

    def test_octal_string(self) -> None:
        self.assertEqual(octal_string(8), "0o10")
        with self.assertRaises(TypeError):
            octal_string(8.0)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            octal_string(True)  # type: ignore[arg-type]

    def test_ordinal(self) -> None:
        self.assertEqual(ordinal("A"), 65)
        with self.assertRaises(TypeError):
            ordinal(65)  # type: ignore[arg-type]
        with self.assertRaises(ValueError):
            ordinal("AB")
        with self.assertRaises(ValueError):
            ordinal("")

    def test_power(self) -> None:
        self.assertEqual(power(2, 3), 8)
        self.assertEqual(power(2, 3, 5), 3)

    def test_representation(self) -> None:
        self.assertEqual(representation("hello"), "'hello'")

    def test_round_number(self) -> None:
        self.assertEqual(round_number(3.7), 4)
        self.assertEqual(round_number(3.14159, 2), 3.14)
        with self.assertRaises(TypeError):
            round_number(3.14, 2.0)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            round_number(3.14, True)  # type: ignore[arg-type]

    def test_sorted_list(self) -> None:
        self.assertEqual(sorted_list([3, 1, 2]), [1, 2, 3])
        self.assertEqual(sorted_list([3, 1, 2], reverse=True), [3, 2, 1])
        self.assertEqual(sorted_list(["b", "a"], key=len), ["b", "a"])
        with self.assertRaises(TypeError):
            sorted_list(123)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            sorted_list([1, 2], reverse=1)  # type: ignore[arg-type]

    def test_summation(self) -> None:
        self.assertEqual(summation([1, 2, 3]), 6)
        self.assertEqual(summation([1, 2, 3], start=10), 16)
        with self.assertRaises(TypeError):
            summation(123)  # type: ignore[arg-type]


if __name__ == "__main__":
    unittest.main()
