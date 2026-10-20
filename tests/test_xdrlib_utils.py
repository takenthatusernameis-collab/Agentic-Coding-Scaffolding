"""Unit tests for xdrlib_utils module."""

import unittest

import xdrlib_utils
from xdrlib_utils import (
    ConversionError,
    Error,
    Packer,
    Unpacker,
    pack_array,
    pack_bool,
    pack_bytes,
    pack_double,
    pack_enum,
    pack_farray,
    pack_float,
    pack_fopaque,
    pack_fstring,
    pack_hyper,
    pack_int,
    pack_list,
    pack_opaque,
    pack_string,
    pack_uhyper,
    pack_uint,
    pack_uint_array,
    unpack_array,
    unpack_bool,
    unpack_bytes,
    unpack_double,
    unpack_enum,
    unpack_farray,
    unpack_float,
    unpack_fopaque,
    unpack_fstring,
    unpack_hyper,
    unpack_int,
    unpack_list,
    unpack_opaque,
    unpack_string,
    unpack_uhyper,
    unpack_uint,
    unpack_uint_array,
)


def _pack_uint_item(packer, item):
    """Write a single unsigned integer into *packer*."""
    packer.pack_uint(item)


def _unpack_uint_item(unpacker):
    """Read a single unsigned integer from *unpacker*."""
    return unpacker.unpack_uint()


class TestReExports(unittest.TestCase):
    """Verify the standard library objects are re-exported."""

    def test_packer_and_unpacker_are_exported(self) -> None:
        self.assertTrue(isinstance(Packer, type))
        self.assertTrue(isinstance(Unpacker, type))

    def test_error_classes_are_exported(self) -> None:
        self.assertTrue(isinstance(Error, type))
        self.assertTrue(isinstance(ConversionError, type))

    def test_conversion_error_derives_from_error(self) -> None:
        self.assertTrue(issubclass(ConversionError, Error))

    def test_module_exports_every_public_name(self) -> None:
        for name in xdrlib_utils.__all__:
            with self.subTest(name=name):
                self.assertTrue(hasattr(xdrlib_utils, name))


class TestUnsignedIntegers(unittest.TestCase):
    """Exercise the unsigned integer helpers."""

    def test_pack_uint_uses_four_big_endian_bytes(self) -> None:
        self.assertEqual(pack_uint(1), b"\x00\x00\x00\x01")

    def test_pack_uint_accepts_the_largest_value(self) -> None:
        self.assertEqual(pack_uint(xdrlib_utils.UINT_MAX), b"\xff\xff\xff\xff")

    def test_unpack_uint_returns_the_packed_value(self) -> None:
        self.assertEqual(unpack_uint(pack_uint(1234)), 1234)

    def test_unpack_uint_accepts_bytes_like_objects(self) -> None:
        self.assertEqual(unpack_uint(bytearray(b"\x00\x00\x00\x02")), 2)
        self.assertEqual(unpack_uint(memoryview(b"\x00\x00\x00\x03")), 3)

    def test_pack_uint_rejects_non_integers(self) -> None:
        with self.assertRaises(TypeError):
            pack_uint("1")  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            pack_uint(1.0)  # type: ignore[arg-type]

    def test_pack_uint_rejects_booleans(self) -> None:
        with self.assertRaises(TypeError):
            pack_uint(True)  # type: ignore[arg-type]

    def test_pack_uint_rejects_out_of_range_values(self) -> None:
        with self.assertRaises(ValueError):
            pack_uint(-1)
        with self.assertRaises(ValueError):
            pack_uint(xdrlib_utils.UINT_MAX + 1)

    def test_unpack_uint_rejects_invalid_data(self) -> None:
        with self.assertRaises(TypeError):
            unpack_uint("abcd")  # type: ignore[arg-type]
        with self.assertRaises(ValueError):
            unpack_uint(b"\x00\x00")
        with self.assertRaises(ValueError):
            unpack_uint(b"")

    def test_pack_uhyper_uses_eight_bytes(self) -> None:
        self.assertEqual(pack_uhyper(1), b"\x00\x00\x00\x00\x00\x00\x00\x01")

    def test_unpack_uhyper_returns_the_packed_value(self) -> None:
        self.assertEqual(unpack_uhyper(pack_uhyper(2**63)), 2**63)

    def test_pack_uhyper_rejects_invalid_values(self) -> None:
        with self.assertRaises(TypeError):
            pack_uhyper("1")  # type: ignore[arg-type]
        with self.assertRaises(ValueError):
            pack_uhyper(-1)
        with self.assertRaises(ValueError):
            pack_uhyper(xdrlib_utils.UHYPER_MAX + 1)

    def test_unpack_uhyper_rejects_truncated_data(self) -> None:
        with self.assertRaises(ValueError):
            unpack_uhyper(b"\x00\x00\x00\x00")


class TestSignedIntegers(unittest.TestCase):
    """Exercise the signed integer helpers."""

    def test_pack_int_uses_four_big_endian_bytes(self) -> None:
        self.assertEqual(pack_int(-1), b"\xff\xff\xff\xff")

    def test_unpack_int_returns_the_packed_value(self) -> None:
        self.assertEqual(unpack_int(pack_int(-42)), -42)

    def test_pack_int_rejects_invalid_values(self) -> None:
        with self.assertRaises(TypeError):
            pack_int(None)  # type: ignore[arg-type]
        with self.assertRaises(ValueError):
            pack_int(xdrlib_utils.INT_MAX + 1)
        with self.assertRaises(ValueError):
            pack_int(xdrlib_utils.INT_MIN - 1)

    def test_unpack_int_rejects_truncated_data(self) -> None:
        with self.assertRaises(ValueError):
            unpack_int(b"\x00\x00\x00")

    def test_pack_hyper_uses_eight_bytes(self) -> None:
        self.assertEqual(pack_hyper(-1), b"\xff\xff\xff\xff\xff\xff\xff\xff")

    def test_unpack_hyper_returns_the_packed_value(self) -> None:
        self.assertEqual(unpack_hyper(pack_hyper(-2**40)), -2**40)
        self.assertEqual(unpack_hyper(pack_hyper(2**40)), 2**40)

    def test_pack_hyper_rejects_invalid_values(self) -> None:
        with self.assertRaises(TypeError):
            pack_hyper(1.5)  # type: ignore[arg-type]
        with self.assertRaises(ValueError):
            pack_hyper(xdrlib_utils.HYPER_MAX + 1)
        with self.assertRaises(ValueError):
            pack_hyper(xdrlib_utils.HYPER_MIN - 1)

    def test_unpack_hyper_rejects_truncated_data(self) -> None:
        with self.assertRaises(ValueError):
            unpack_hyper(b"\x00\x00\x00\x00\x00\x00\x00")


class TestEnumerations(unittest.TestCase):
    """Exercise the enumeration helpers."""

    def test_pack_enum_encodes_a_signed_integer(self) -> None:
        self.assertEqual(pack_enum(3), pack_int(3))

    def test_unpack_enum_returns_the_packed_value(self) -> None:
        self.assertEqual(unpack_enum(pack_enum(3)), 3)

    def test_pack_enum_rejects_invalid_values(self) -> None:
        with self.assertRaises(TypeError):
            pack_enum("3")  # type: ignore[arg-type]
        with self.assertRaises(ValueError):
            pack_enum(xdrlib_utils.INT_MAX + 1)

    def test_unpack_enum_rejects_truncated_data(self) -> None:
        with self.assertRaises(ValueError):
            unpack_enum(b"\x00\x00")


class TestBooleans(unittest.TestCase):
    """Exercise the boolean helpers."""

    def test_pack_bool_uses_four_bytes(self) -> None:
        self.assertEqual(pack_bool(True), b"\x00\x00\x00\x01")
        self.assertEqual(pack_bool(False), b"\x00\x00\x00\x00")

    def test_unpack_bool_returns_the_packed_value(self) -> None:
        self.assertIs(unpack_bool(pack_bool(True)), True)
        self.assertIs(unpack_bool(pack_bool(False)), False)

    def test_unpack_bool_treats_every_non_zero_value_as_true(self) -> None:
        self.assertIs(unpack_bool(b"\x00\x00\x00\x02"), True)

    def test_pack_bool_rejects_non_booleans(self) -> None:
        with self.assertRaises(TypeError):
            pack_bool(1)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            pack_bool("yes")  # type: ignore[arg-type]

    def test_unpack_bool_rejects_truncated_data(self) -> None:
        with self.assertRaises(ValueError):
            unpack_bool(b"\x00")


class TestFloatingPointNumbers(unittest.TestCase):
    """Exercise the floating point helpers."""

    def test_pack_float_uses_four_bytes(self) -> None:
        self.assertEqual(pack_float(1.0), b"\x3f\x80\x00\x00")

    def test_unpack_float_returns_the_packed_value(self) -> None:
        self.assertAlmostEqual(unpack_float(pack_float(0.5)), 0.5)

    def test_pack_double_uses_eight_bytes(self) -> None:
        self.assertEqual(pack_double(1.0), b"\x3f\xf0\x00\x00\x00\x00\x00\x00")

    def test_unpack_double_returns_the_packed_value(self) -> None:
        self.assertAlmostEqual(unpack_double(pack_double(0.25)), 0.25)

    def test_pack_float_accepts_integers(self) -> None:
        self.assertEqual(pack_float(1), pack_float(1.0))

    def test_pack_float_rejects_invalid_values(self) -> None:
        with self.assertRaises(TypeError):
            pack_float("1.0")  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            pack_float(True)  # type: ignore[arg-type]
        with self.assertRaises(ValueError):
            pack_float(xdrlib_utils.FLOAT_MAX * 10)

    def test_pack_double_rejects_invalid_values(self) -> None:
        with self.assertRaises(TypeError):
            pack_double(None)  # type: ignore[arg-type]
        with self.assertRaises(ValueError):
            pack_double(10**400)

    def test_unpack_float_rejects_truncated_data(self) -> None:
        with self.assertRaises(ValueError):
            unpack_float(b"\x3f\x80")

    def test_unpack_double_rejects_truncated_data(self) -> None:
        with self.assertRaises(ValueError):
            unpack_double(b"\x3f\xf0\x00")


class TestStrings(unittest.TestCase):
    """Exercise the string helpers."""

    def test_pack_string_prefixes_the_length(self) -> None:
        self.assertEqual(pack_string(b"ab"), b"\x00\x00\x00\x02ab\x00\x00")

    def test_pack_string_pads_to_four_bytes(self) -> None:
        self.assertEqual(pack_string(b"a"), b"\x00\x00\x00\x01a\x00\x00\x00")

    def test_unpack_string_returns_the_packed_value(self) -> None:
        self.assertEqual(unpack_string(pack_string(b"hello")), b"hello")

    def test_unpack_string_accepts_an_empty_string(self) -> None:
        self.assertEqual(unpack_string(pack_string(b"")), b"")

    def test_pack_string_rejects_non_bytes(self) -> None:
        with self.assertRaises(TypeError):
            pack_string("ab")  # type: ignore[arg-type]

    def test_pack_string_accepts_bytes_like_objects(self) -> None:
        self.assertEqual(pack_string(bytearray(b"ab")), pack_string(b"ab"))

    def test_unpack_string_rejects_truncated_data(self) -> None:
        with self.assertRaises(ValueError):
            unpack_string(b"\x00\x00\x00\x08ab")

    def test_pack_bytes_matches_pack_string(self) -> None:
        self.assertEqual(pack_bytes(b"ab"), pack_string(b"ab"))

    def test_unpack_bytes_returns_the_packed_value(self) -> None:
        self.assertEqual(unpack_bytes(pack_bytes(b"ab")), b"ab")

    def test_unpack_bytes_rejects_truncated_data(self) -> None:
        with self.assertRaises(ValueError):
            unpack_bytes(b"\x00\x00\x00\x08ab")

    def test_pack_opaque_matches_pack_string(self) -> None:
        self.assertEqual(pack_opaque(b"ab"), pack_string(b"ab"))

    def test_unpack_opaque_returns_the_packed_value(self) -> None:
        self.assertEqual(unpack_opaque(pack_opaque(b"ab")), b"ab")

    def test_unpack_opaque_rejects_truncated_data(self) -> None:
        with self.assertRaises(ValueError):
            unpack_opaque(b"\x00\x00")


class TestFixedLengthStrings(unittest.TestCase):
    """Exercise the fixed length string helpers."""

    def test_pack_fstring_pads_to_four_bytes(self) -> None:
        self.assertEqual(pack_fstring(4, b"ab"), b"ab\x00\x00")

    def test_pack_fstring_truncates_longer_payloads(self) -> None:
        self.assertEqual(pack_fstring(2, b"abcd"), b"ab\x00\x00")

    def test_unpack_fstring_returns_the_packed_value(self) -> None:
        self.assertEqual(unpack_fstring(2, pack_fstring(2, b"ab")), b"ab")
        self.assertEqual(unpack_fstring(4, pack_fstring(4, b"ab")), b"ab\x00\x00")

    def test_pack_fstring_rejects_invalid_values(self) -> None:
        with self.assertRaises(TypeError):
            pack_fstring("4", b"ab")  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            pack_fstring(4, "ab")  # type: ignore[arg-type]
        with self.assertRaises(ValueError):
            pack_fstring(-1, b"ab")

    def test_unpack_fstring_rejects_invalid_values(self) -> None:
        with self.assertRaises(ValueError):
            unpack_fstring(-1, b"ab")
        with self.assertRaises(ValueError):
            unpack_fstring(4, b"ab")

    def test_pack_fopaque_matches_pack_fstring(self) -> None:
        self.assertEqual(pack_fopaque(4, b"ab"), pack_fstring(4, b"ab"))

    def test_unpack_fopaque_returns_the_packed_value(self) -> None:
        self.assertEqual(unpack_fopaque(2, pack_fopaque(2, b"ab")), b"ab")
        self.assertEqual(unpack_fopaque(4, pack_fopaque(4, b"ab")), b"ab\x00\x00")

    def test_unpack_fopaque_rejects_truncated_data(self) -> None:
        with self.assertRaises(ValueError):
            unpack_fopaque(4, b"ab")


class TestArrays(unittest.TestCase):
    """Exercise the array helpers."""

    def test_pack_array_prefixes_the_item_count(self) -> None:
        encoded = pack_array([1, 2], _pack_uint_item)
        self.assertEqual(encoded, b"\x00\x00\x00\x02\x00\x00\x00\x01\x00\x00\x00\x02")

    def test_unpack_array_returns_the_packed_items(self) -> None:
        encoded = pack_array([1, 2], _pack_uint_item)
        self.assertEqual(unpack_array(encoded, _unpack_uint_item), [1, 2])

    def test_pack_array_accepts_an_empty_sequence(self) -> None:
        self.assertEqual(pack_array([], _pack_uint_item), b"\x00\x00\x00\x00")

    def test_pack_array_rejects_invalid_arguments(self) -> None:
        with self.assertRaises(TypeError):
            pack_array("ab", _pack_uint_item)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            pack_array([1], "not callable")  # type: ignore[arg-type]

    def test_unpack_array_rejects_invalid_arguments(self) -> None:
        with self.assertRaises(TypeError):
            unpack_array(b"", "not callable")  # type: ignore[arg-type]
        with self.assertRaises(ValueError):
            unpack_array(b"\x00\x00\x00", _unpack_uint_item)

    def test_unpack_array_reports_truncated_items(self) -> None:
        with self.assertRaises(ValueError):
            unpack_array(b"\x00\x00\x00\x02\x00\x00\x00\x01", _unpack_uint_item)

    def test_pack_farray_writes_no_length_prefix(self) -> None:
        self.assertEqual(
            pack_farray(2, [1, 2], _pack_uint_item),
            b"\x00\x00\x00\x01\x00\x00\x00\x02",
        )

    def test_unpack_farray_returns_the_packed_items(self) -> None:
        encoded = pack_farray(2, [1, 2], _pack_uint_item)
        self.assertEqual(unpack_farray(2, encoded, _unpack_uint_item), [1, 2])

    def test_pack_farray_rejects_a_mismatched_count(self) -> None:
        with self.assertRaises(ValueError):
            pack_farray(2, [1], _pack_uint_item)

    def test_pack_farray_rejects_invalid_arguments(self) -> None:
        with self.assertRaises(TypeError):
            pack_farray("2", [1, 2], _pack_uint_item)  # type: ignore[arg-type]
        with self.assertRaises(ValueError):
            pack_farray(-1, [], _pack_uint_item)

    def test_unpack_farray_rejects_invalid_arguments(self) -> None:
        with self.assertRaises(ValueError):
            unpack_farray(-1, b"", _unpack_uint_item)
        with self.assertRaises(TypeError):
            unpack_farray(1, b"", "not callable")  # type: ignore[arg-type]

    def test_unpack_farray_reports_truncated_items(self) -> None:
        with self.assertRaises(ValueError):
            unpack_farray(2, b"\x00\x00\x00\x01", _unpack_uint_item)


class TestLists(unittest.TestCase):
    """Exercise the list helpers."""

    def test_pack_list_marks_every_item(self) -> None:
        encoded = pack_list([1], _pack_uint_item)
        self.assertEqual(encoded, b"\x00\x00\x00\x01\x00\x00\x00\x01\x00\x00\x00\x00")

    def test_unpack_list_returns_the_packed_items(self) -> None:
        encoded = pack_list([1, 2], _pack_uint_item)
        self.assertEqual(unpack_list(encoded, _unpack_uint_item), [1, 2])

    def test_pack_list_accepts_an_empty_sequence(self) -> None:
        self.assertEqual(pack_list([], _pack_uint_item), b"\x00\x00\x00\x00")

    def test_unpack_list_stops_at_the_terminator(self) -> None:
        encoded = pack_list([1], _pack_uint_item) + b"\x00\x00\x00\x2a"
        self.assertEqual(unpack_list(encoded, _unpack_uint_item), [1])

    def test_pack_list_rejects_invalid_arguments(self) -> None:
        with self.assertRaises(TypeError):
            pack_list(b"ab", _pack_uint_item)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            pack_list([1], None)  # type: ignore[arg-type]

    def test_unpack_list_rejects_an_unknown_flag(self) -> None:
        with self.assertRaises(ConversionError):
            unpack_list(b"\x00\x00\x00\x02", _unpack_uint_item)

    def test_unpack_list_rejects_truncated_data(self) -> None:
        with self.assertRaises(ValueError):
            unpack_list(b"", _unpack_uint_item)


class TestUnsignedIntegerArrays(unittest.TestCase):
    """Exercise the convenience array helpers."""

    def test_pack_uint_array_prefixes_the_item_count(self) -> None:
        self.assertEqual(
            pack_uint_array([1, 2]),
            b"\x00\x00\x00\x02\x00\x00\x00\x01\x00\x00\x00\x02",
        )

    def test_unpack_uint_array_returns_the_packed_items(self) -> None:
        self.assertEqual(unpack_uint_array(pack_uint_array([1, 2])), [1, 2])

    def test_unpack_uint_array_matches_the_generic_helper(self) -> None:
        encoded = pack_uint_array([4, 5])
        self.assertEqual(unpack_uint_array(encoded), unpack_array(encoded, _unpack_uint_item))

    def test_pack_uint_array_rejects_invalid_values(self) -> None:
        with self.assertRaises(TypeError):
            pack_uint_array([1, "2"])  # type: ignore[list-item]
        with self.assertRaises(ValueError):
            pack_uint_array([1, -1])
        with self.assertRaises(TypeError):
            pack_uint_array("12")  # type: ignore[arg-type]

    def test_unpack_uint_array_rejects_truncated_data(self) -> None:
        with self.assertRaises(ValueError):
            unpack_uint_array(b"\x00\x00\x00\x02\x00\x00\x00\x01")


if __name__ == "__main__":
    unittest.main()
