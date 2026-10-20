"""Tests for uu_utils module."""

import os
import stat
import tempfile
import unittest
from unittest import mock

import uu_utils


class TestEncodeUu(unittest.TestCase):
    def test_encode_returns_ascii_text(self):
        encoded = uu_utils.encode_uu(b"hello world\n", name="greeting")
        self.assertIsInstance(encoded, str)
        self.assertTrue(encoded.startswith("begin "))
        self.assertTrue(encoded.endswith("end\n"))

    def test_encode_header_records_name_and_mode(self):
        encoded = uu_utils.encode_uu(b"payload", name="greeting", mode=0o644)
        header = uu_utils.parse_uu_header(encoded)
        self.assertEqual(header["name"], "greeting")
        self.assertEqual(header["mode"], "644")

    def test_encode_default_name_and_mode(self):
        encoded = uu_utils.encode_uu(b"payload")
        header = uu_utils.parse_uu_header(encoded)
        self.assertEqual(header["name"], "data")
        self.assertEqual(header["mode"], "666")

    def test_encode_accepts_bytearray(self):
        encoded = uu_utils.encode_uu(bytearray(b"payload"))
        self.assertEqual(uu_utils.decode_uu(encoded), b"payload")

    def test_encode_rejects_bad_types(self):
        with self.assertRaises(TypeError):
            uu_utils.encode_uu("not bytes")  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            uu_utils.encode_uu(b"payload", name=5)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            uu_utils.encode_uu(b"payload", mode="644")  # type: ignore[arg-type]

    def test_encode_rejects_out_of_range_mode(self):
        with self.assertRaises(ValueError):
            uu_utils.encode_uu(b"payload", mode=0o100000)


class TestDecodeUu(unittest.TestCase):
    def test_decode_roundtrip(self):
        encoded = uu_utils.encode_uu(b"hello world\n")
        self.assertEqual(uu_utils.decode_uu(encoded), b"hello world\n")

    def test_decode_accepts_bytes(self):
        encoded = uu_utils.encode_uu(b"payload")
        self.assertEqual(uu_utils.decode_uu(encoded.encode("ascii")), b"payload")

    def test_decode_binary_payload(self):
        payload = bytes(range(256))
        encoded = uu_utils.encode_uu(payload)
        self.assertEqual(uu_utils.decode_uu(encoded), payload)

    def test_decode_long_payload(self):
        payload = b"x" * 5000
        encoded = uu_utils.encode_uu(payload)
        self.assertEqual(uu_utils.decode_uu(encoded), payload)

    def test_decode_rejects_bad_type(self):
        with self.assertRaises(TypeError):
            uu_utils.decode_uu(123)  # type: ignore[arg-type]

    def test_decode_rejects_payload_without_header(self):
        with self.assertRaises(Exception):
            uu_utils.decode_uu("not a uuencoded payload")


class TestParseUuHeader(unittest.TestCase):
    def test_parse_header(self):
        encoded = uu_utils.encode_uu(b"payload", name="greeting", mode=0o600)
        self.assertEqual(
            uu_utils.parse_uu_header(encoded), {"mode": "600", "name": "greeting"}
        )

    def test_parse_header_accepts_bytes(self):
        encoded = uu_utils.encode_uu(b"payload", name="greeting")
        self.assertEqual(uu_utils.parse_uu_header(encoded.encode("ascii"))["name"], "greeting")

    def test_parse_header_rejects_missing_header(self):
        with self.assertRaises(ValueError):
            uu_utils.parse_uu_header("no header here")

    def test_parse_header_rejects_non_octal_mode(self):
        with self.assertRaises(ValueError):
            uu_utils.parse_uu_header("begin xyz file\n")

    def test_parse_header_rejects_bad_type(self):
        with self.assertRaises(TypeError):
            uu_utils.parse_uu_header(123)  # type: ignore[arg-type]


class TestIsUuencoded(unittest.TestCase):
    def test_is_uuencoded_true(self):
        self.assertTrue(uu_utils.is_uuencoded(uu_utils.encode_uu(b"payload")))

    def test_is_uuencoded_false(self):
        self.assertFalse(uu_utils.is_uuencoded("plain text"))
        self.assertFalse(uu_utils.is_uuencoded(""))

    def test_is_uuencoded_rejects_bad_type(self):
        with self.assertRaises(TypeError):
            uu_utils.is_uuencoded(123)  # type: ignore[arg-type]


class TestUuEncode(unittest.TestCase):
    def test_encode_writes_file(self):
        with tempfile.TemporaryDirectory() as directory:
            path = os.path.join(directory, "payload.uu")
            encoded = uu_utils.uu_encode(b"hello world\n", path)
            with open(path, "r", encoding="ascii") as handle:
                self.assertEqual(handle.read(), encoded)
            self.assertTrue(encoded.startswith("begin "))

    def test_encode_defaults_name_to_base_name(self):
        with tempfile.TemporaryDirectory() as directory:
            path = os.path.join(directory, "payload.uu")
            uu_utils.uu_encode(b"payload", path)
            self.assertEqual(uu_utils.parse_uu_header(open(path).read())["name"], "payload.uu")

    def test_encode_accepts_path_like(self):
        from pathlib import Path

        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "payload.uu"
            uu_utils.uu_encode(b"payload", path)
            self.assertTrue(path.is_file())

    def test_encode_roundtrip_through_file(self):
        with tempfile.TemporaryDirectory() as directory:
            path = os.path.join(directory, "payload.uu")
            uu_utils.uu_encode(b"hello world\n", path)
            self.assertEqual(uu_utils.uu_decode(path), b"hello world\n")

    def test_encode_rejects_bad_types(self):
        with self.assertRaises(TypeError):
            uu_utils.uu_encode("not bytes", "/tmp/payload.uu")  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            uu_utils.uu_encode(b"payload", 123)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            uu_utils.uu_encode(b"payload", "/tmp/payload.uu", name=5)  # type: ignore[arg-type]


class TestUuDecode(unittest.TestCase):
    def test_decode_returns_payload_without_writing(self):
        with tempfile.TemporaryDirectory() as directory:
            path = os.path.join(directory, "payload.uu")
            uu_utils.uu_encode(b"hello world\n", path)
            before = sorted(os.listdir(directory))
            self.assertEqual(uu_utils.uu_decode(path), b"hello world\n")
            self.assertEqual(sorted(os.listdir(directory)), before)

    def test_decode_writes_destination(self):
        with tempfile.TemporaryDirectory() as directory:
            source = os.path.join(directory, "payload.uu")
            destination = os.path.join(directory, "payload.bin")
            uu_utils.uu_encode(b"hello world\n", source)
            result = uu_utils.uu_decode(source, destination)
            self.assertEqual(result, b"hello world\n")
            with open(destination, "rb") as handle:
                self.assertEqual(handle.read(), b"hello world\n")

    def test_decode_applies_recorded_mode(self):
        with tempfile.TemporaryDirectory() as directory:
            source = os.path.join(directory, "payload.uu")
            destination = os.path.join(directory, "payload.bin")
            uu_utils.uu_encode(b"payload", source, mode=0o600)
            uu_utils.uu_decode(source, destination)
            self.assertEqual(stat.S_IMODE(os.stat(destination).st_mode), 0o600)

    def test_decode_mode_overrides_recorded_mode(self):
        with tempfile.TemporaryDirectory() as directory:
            source = os.path.join(directory, "payload.uu")
            destination = os.path.join(directory, "payload.bin")
            uu_utils.uu_encode(b"payload", source, mode=0o600)
            uu_utils.uu_decode(source, destination, mode=0o644)
            self.assertEqual(stat.S_IMODE(os.stat(destination).st_mode), 0o644)

    def test_decode_rejects_bad_types(self):
        with self.assertRaises(TypeError):
            uu_utils.uu_decode(123)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            uu_utils.uu_decode("/tmp/payload.uu", 123)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            uu_utils.uu_decode("/tmp/payload.uu", "/tmp/payload.bin", mode="600")  # type: ignore[arg-type]

    def test_decode_rejects_out_of_range_mode(self):
        with self.assertRaises(ValueError):
            uu_utils.uu_decode("/tmp/payload.uu", "/tmp/payload.bin", mode=0o100000)

    def test_decode_missing_file(self):
        with self.assertRaises(OSError):
            uu_utils.uu_decode("/nonexistent/payload.uu")


class TestUuUnavailable(unittest.TestCase):
    def test_helpers_report_missing_standard_library_module(self):
        with mock.patch.object(uu_utils, "_uu", None):
            with self.assertRaises(RuntimeError):
                uu_utils.encode_uu(b"payload")
            with self.assertRaises(RuntimeError):
                uu_utils.decode_uu("begin 666 data\n")
            with self.assertRaises(RuntimeError):
                uu_utils.uu_encode(b"payload", "/tmp/payload.uu")
            with self.assertRaises(RuntimeError):
                uu_utils.uu_decode("/tmp/payload.uu")


if __name__ == "__main__":
    unittest.main()
