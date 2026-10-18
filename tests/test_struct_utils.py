"""Unit tests for struct_utils module."""

import unittest

from struct_utils import (
    calcsize,
    is_valid_format,
    pack,
    pack_into,
    unpack,
    unpack_from,
)


class TestPack(unittest.TestCase):
    def test_pack_short_little_endian(self):
        self.assertEqual(pack("<h", 255), b"\xff\x00")

    def test_pack_ints_big_endian(self):
        self.assertEqual(pack(">ii", 1, 2), b"\x00\x00\x00\x01\x00\x00\x00\x02")

    def test_pack_roundtrip(self):
        self.assertEqual(unpack("<h", pack("<h", 255)), (255,))

    def test_pack_type_error_fmt(self):
        with self.assertRaises(TypeError):
            pack(123, 1)  # type: ignore[arg-type]

    def test_pack_invalid_format(self):
        with self.assertRaises(ValueError):
            pack("!!invalid!!", 1)

    def test_pack_wrong_number_of_values(self):
        with self.assertRaises(ValueError):
            pack("<ii", 1)


class TestUnpack(unittest.TestCase):
    def test_unpack_short_little_endian(self):
        self.assertEqual(unpack("<h", b"\xff\x00"), (255,))

    def test_unpack_ints_big_endian(self):
        self.assertEqual(unpack(">ii", b"\x00\x00\x00\x01\x00\x00\x00\x02"), (1, 2))

    def test_unpack_type_error_fmt(self):
        with self.assertRaises(TypeError):
            unpack(123, b"\x00\x00")  # type: ignore[arg-type]

    def test_unpack_type_error_buffer(self):
        with self.assertRaises(TypeError):
            unpack("<h", "not bytes")  # type: ignore[arg-type]

    def test_unpack_invalid_format(self):
        with self.assertRaises(ValueError):
            unpack("!!invalid!!", b"\x00\x00")

    def test_unpack_buffer_too_short(self):
        with self.assertRaises(ValueError):
            unpack("<ii", b"\x00\x00\x00\x01")


class TestPackInto(unittest.TestCase):
    def test_pack_into(self):
        buf = bytearray(8)
        pack_into(">ii", buf, 0, 1, 2)
        self.assertEqual(buf, bytearray(b"\x00\x00\x00\x01\x00\x00\x00\x02"))

    def test_pack_into_offset(self):
        buf = bytearray(12)
        pack_into(">ii", buf, 4, 1, 2)
        self.assertEqual(buf[4:12], b"\x00\x00\x00\x01\x00\x00\x00\x02")

    def test_pack_into_type_error_buffer(self):
        with self.assertRaises(TypeError):
            pack_into("<h", b"\x00\x00", 0, 1)  # type: ignore[arg-type]

    def test_pack_into_type_error_offset(self):
        with self.assertRaises(TypeError):
            pack_into("<h", bytearray(2), "0", 1)  # type: ignore[arg-type]

    def test_pack_into_negative_offset(self):
        with self.assertRaises(ValueError):
            pack_into("<h", bytearray(2), -1, 1)

    def test_pack_into_invalid_format(self):
        with self.assertRaises(ValueError):
            pack_into("!!invalid!!", bytearray(2), 0, 1)

    def test_pack_into_not_enough_room(self):
        with self.assertRaises(ValueError):
            pack_into("<ii", bytearray(2), 0, 1, 2)


class TestUnpackFrom(unittest.TestCase):
    def test_unpack_from(self):
        data = b"\x00\x00\x00\x01\x00\x00\x00\x02"
        self.assertEqual(unpack_from(">ii", data, 0), (1, 2))

    def test_unpack_from_offset(self):
        data = b"\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x02"
        self.assertEqual(unpack_from(">ii", data, 4), (1, 2))

    def test_unpack_from_type_error_fmt(self):
        with self.assertRaises(TypeError):
            unpack_from(123, b"\x00\x00\x00\x01")  # type: ignore[arg-type]

    def test_unpack_from_type_error_buffer(self):
        with self.assertRaises(TypeError):
            unpack_from("<h", "not bytes", 0)  # type: ignore[arg-type]

    def test_unpack_from_type_error_offset(self):
        with self.assertRaises(TypeError):
            unpack_from("<h", b"\x00\x00", "0")  # type: ignore[arg-type]

    def test_unpack_from_negative_offset(self):
        with self.assertRaises(ValueError):
            unpack_from("<h", b"\x00\x00", -1)

    def test_unpack_from_invalid_format(self):
        with self.assertRaises(ValueError):
            unpack_from("!!invalid!!", b"\x00\x00")


class TestCalcsize(unittest.TestCase):
    def test_calcsize_short(self):
        self.assertEqual(calcsize("<h"), 2)

    def test_calcsize_ints(self):
        self.assertEqual(calcsize(">ii"), 8)

    def test_calcsize_type_error(self):
        with self.assertRaises(TypeError):
            calcsize(123)  # type: ignore[arg-type]

    def test_calcsize_invalid_format(self):
        with self.assertRaises(ValueError):
            calcsize("!!invalid!!")


class TestIsValidFormat(unittest.TestCase):
    def test_is_valid_format_true(self):
        self.assertTrue(is_valid_format("<h"))
        self.assertTrue(is_valid_format(">ii"))

    def test_is_valid_format_false(self):
        self.assertFalse(is_valid_format("!!invalid!!"))

    def test_is_valid_format_type_error_returns_false(self):
        self.assertFalse(is_valid_format(123))  # type: ignore[arg-type]


if __name__ == "__main__":
    unittest.main()
