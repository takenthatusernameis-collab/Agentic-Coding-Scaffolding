"""Tests for encodings_utils."""

import unittest

import encodings_utils
from encodings_utils import (
    ALIASES,
    all_aliases,
    all_encodings,
    encoding_aliases,
    is_alias,
    is_known_encoding,
    normalize_encoding,
)


class TestEncodingsUtils(unittest.TestCase):
    """Verify the encoding name helpers of the wrapper."""

    def test_the_alias_mapping_is_read_only(self):
        with self.assertRaises(TypeError):
            ALIASES["no_such_alias"] = "utf_8"  # type: ignore[index]

    def test_normalize_encoding(self):
        self.assertEqual(normalize_encoding("UTF-8"), "UTF_8")
        self.assertEqual(normalize_encoding("utf8"), "utf8")
        self.assertEqual(normalize_encoding("latin-1"), "latin_1")
        self.assertEqual(normalize_encoding("cp1252"), "cp1252")

    def test_normalize_encoding_validates_its_argument(self):
        with self.assertRaises(TypeError):
            normalize_encoding(123)  # type: ignore[arg-type]

    def test_is_known_encoding(self):
        self.assertTrue(is_known_encoding("utf_8"))
        self.assertTrue(is_known_encoding("utf8"))
        self.assertTrue(is_known_encoding("ascii"))
        self.assertFalse(is_known_encoding("no_such_encoding"))

    def test_is_known_encoding_validates_its_argument(self):
        with self.assertRaises(TypeError):
            is_known_encoding(123)  # type: ignore[arg-type]

    def test_is_alias(self):
        self.assertTrue(is_alias("utf8"))
        self.assertTrue(is_alias("latin1"))
        self.assertFalse(is_alias("latin-1"))
        self.assertFalse(is_alias("utf_8"))
        self.assertFalse(is_alias("ascii"))
        self.assertFalse(is_alias("no_such_encoding"))

    def test_is_alias_validates_its_argument(self):
        with self.assertRaises(TypeError):
            is_alias(123)  # type: ignore[arg-type]

    def test_encoding_aliases(self):
        aliases = encoding_aliases("utf_8")
        self.assertIn("utf8", aliases)
        self.assertIn("u8", aliases)
        self.assertIn("cp65001", aliases)
        self.assertEqual(aliases, tuple(sorted(aliases)))
        aliases = encoding_aliases("utf8")
        self.assertEqual(aliases, encoding_aliases("utf_8"))

    def test_encoding_aliases_validates_its_arguments(self):
        with self.assertRaises(TypeError):
            encoding_aliases(123)  # type: ignore[arg-type]
        with self.assertRaises(ValueError):
            encoding_aliases("no_such_encoding")

    def test_all_aliases_is_read_only(self):
        aliases = all_aliases()
        with self.assertRaises(TypeError):
            aliases["no_such_alias"] = "utf_8"  # type: ignore[index]
        self.assertIn("utf8", aliases)
        self.assertEqual(aliases["utf8"], "utf_8")

    def test_all_encodings(self):
        encodings = all_encodings()
        self.assertEqual(encodings, tuple(sorted(encodings)))
        self.assertIn("utf_8", encodings)
        self.assertIn("ascii", encodings)
        self.assertEqual(len(encodings), len(set(encodings)))

    def test_all_aliases_matches_all_encodings(self):
        canonicals = set(all_encodings())
        for alias, target in all_aliases().items():
            self.assertIn(target, canonicals)

    def test_all_is_sorted_and_unique(self):
        self.assertIsNotNone(encodings_utils.__all__)
        self.assertEqual(
            len(encodings_utils.__all__), len(set(encodings_utils.__all__))
        )
        self.assertEqual(encodings_utils.__all__, sorted(encodings_utils.__all__))
        for name in encodings_utils.__all__:
            self.assertTrue(hasattr(encodings_utils, name), name)


if __name__ == "__main__":
    unittest.main()
