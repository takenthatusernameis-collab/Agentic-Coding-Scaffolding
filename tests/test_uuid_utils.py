"""Unit tests for uuid_utils module."""

import unittest
from uuid import UUID

from uuid_utils import (
    generate_uuid,
    generate_uuid1,
    generate_uuid4,
    is_valid_uuid,
    parse_uuid,
)


class TestGenerateUUID(unittest.TestCase):
    def test_generate_uuid_default(self):
        result = generate_uuid()
        self.assertTrue(is_valid_uuid(result))
        self.assertEqual(len(result), 36)

    def test_generate_uuid4(self):
        result = generate_uuid(version=4)
        self.assertTrue(is_valid_uuid(result, version=4))

    def test_generate_uuid1(self):
        result = generate_uuid(version=1)
        self.assertTrue(is_valid_uuid(result, version=1))

    def test_generate_uuid_invalid_version(self):
        with self.assertRaises(ValueError):
            generate_uuid(version=2)


class TestGenerateUUID4(unittest.TestCase):
    def test_generate_uuid4_returns_valid(self):
        result = generate_uuid4()
        self.assertTrue(is_valid_uuid(result))
        self.assertEqual(UUID(result).version, 4)


class TestGenerateUUID1(unittest.TestCase):
    def test_generate_uuid1_returns_valid(self):
        result = generate_uuid1()
        self.assertTrue(is_valid_uuid(result))
        self.assertEqual(UUID(result).version, 1)


class TestIsValidUUID(unittest.TestCase):
    def test_valid_uuid4(self):
        self.assertTrue(is_valid_uuid("f47ac10b-58cc-4372-a567-0e02b2c3d479"))

    def test_valid_uuid4_with_version(self):
        self.assertTrue(is_valid_uuid("f47ac10b-58cc-4372-a567-0e02b2c3d479", version=4))

    def test_invalid_uuid4_version_mismatch(self):
        # This is a UUID4 format-wise
        self.assertFalse(is_valid_uuid("f47ac10b-58cc-4372-a567-0e02b2c3d479", version=1))

    def test_invalid_uuid_string(self):
        self.assertFalse(is_valid_uuid("not-a-uuid"))
        self.assertFalse(is_valid_uuid(""))
        self.assertFalse(is_valid_uuid("12345"))
        self.assertFalse(is_valid_uuid(None))  # type: ignore

    def test_invalid_uuid_types(self):
        self.assertFalse(is_valid_uuid(123))  # type: ignore
        self.assertFalse(is_valid_uuid([]))  # type: ignore


class TestParseUUID(unittest.TestCase):
    def test_parse_valid_uuid(self):
        uuid_str = "f47ac10b-58cc-4372-a567-0e02b2c3d479"
        result = parse_uuid(uuid_str)
        self.assertIsInstance(result, UUID)
        self.assertEqual(str(result), uuid_str)

    def test_parse_invalid_uuid(self):
        with self.assertRaises(ValueError):
            parse_uuid("not-a-uuid")


if __name__ == "__main__":
    unittest.main()
