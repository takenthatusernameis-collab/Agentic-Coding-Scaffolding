"""Tests for mimetypes_utils module."""

import mimetypes
import os
import tempfile
import unittest

import mimetypes_utils

# A MIME type and extension that are not part of the platform database.
_CUSTOM_TYPE = "application/x-kilo-test"
_CUSTOM_EXTENSION = ".kilotest"


def register_custom_type() -> None:
    """Register the custom type used by the tests."""
    mimetypes_utils.add_type(_CUSTOM_TYPE, _CUSTOM_EXTENSION)


class TestGuessType(unittest.TestCase):
    """Verify detection of the MIME type of a file."""

    def test_guess_type_returns_a_tuple(self):
        result = mimetypes_utils.guess_type("page.html")
        self.assertIsInstance(result, tuple)
        self.assertEqual(len(result), 2)

    def test_guess_type_of_known_extension(self):
        expected = mimetypes.guess_type("page.html")
        if expected[0] is None:
            self.skipTest("the platform MIME database does not know .html")
        self.assertEqual(mimetypes_utils.guess_type("page.html"), expected)

    def test_guess_type_of_unknown_extension(self):
        self.assertEqual(
            mimetypes_utils.guess_type("archive.definitely-not-a-type"),
            (None, None),
        )

    def test_guess_type_ignores_the_query_string(self):
        result = mimetypes_utils.guess_type("https://example.com/page.html?q=1")
        self.assertEqual(result, mimetypes.guess_type("https://example.com/page.html?q=1"))

    def test_guess_type_matches_the_standard_library(self):
        for url in ("a.txt", "b.html", "c.json", "d.png", "e.definitely-unknown"):
            with self.subTest(url=url):
                self.assertEqual(mimetypes_utils.guess_type(url), mimetypes.guess_type(url))

    def test_guess_type_supports_the_non_strict_database(self):
        url = "archive.definitely-not-a-type"
        self.assertEqual(
            mimetypes_utils.guess_type(url, strict=False),
            mimetypes.guess_type(url, strict=False),
        )

    def test_guess_type_requires_a_string(self):
        with self.assertRaises(TypeError):
            mimetypes_utils.guess_type(None)  # type: ignore[arg-type]

    def test_guess_type_requires_a_boolean_strict_flag(self):
        with self.assertRaises(TypeError):
            mimetypes_utils.guess_type("page.html", strict="yes")  # type: ignore[arg-type]


class TestGuessExtension(unittest.TestCase):
    """Verify lookup of the extension of a MIME type."""

    def setUp(self):
        register_custom_type()

    def test_guess_extension_returns_the_extension(self):
        self.assertEqual(
            mimetypes_utils.guess_extension(_CUSTOM_TYPE),
            _CUSTOM_EXTENSION,
        )

    def test_guess_extension_of_unknown_type(self):
        self.assertIsNone(mimetypes_utils.guess_extension("application/definitely-unknown"))

    def test_guess_extension_matches_the_standard_library(self):
        for mime_type in ("text/html", "text/plain", "application/json"):
            with self.subTest(mime_type=mime_type):
                self.assertEqual(
                    mimetypes_utils.guess_extension(mime_type),
                    mimetypes.guess_extension(mime_type),
                )

    def test_guess_extension_requires_a_string(self):
        with self.assertRaises(TypeError):
            mimetypes_utils.guess_extension(None)  # type: ignore[arg-type]

    def test_guess_extension_requires_a_boolean_strict_flag(self):
        with self.assertRaises(TypeError):
            mimetypes_utils.guess_extension("text/html", strict=1)  # type: ignore[arg-type]


class TestGuessAllExtensions(unittest.TestCase):
    """Verify lookup of every extension of a MIME type."""

    def setUp(self):
        register_custom_type()

    def test_guess_all_extensions_returns_a_list(self):
        extensions = mimetypes_utils.guess_all_extensions(_CUSTOM_TYPE)
        self.assertIsInstance(extensions, list)
        self.assertIn(_CUSTOM_EXTENSION, extensions)

    def test_guess_all_extensions_of_unknown_type(self):
        self.assertEqual(
            mimetypes_utils.guess_all_extensions("application/definitely-unknown"),
            [],
        )

    def test_guess_all_extensions_matches_the_standard_library(self):
        for mime_type in ("text/html", "application/json"):
            with self.subTest(mime_type=mime_type):
                self.assertEqual(
                    mimetypes_utils.guess_all_extensions(mime_type),
                    list(mimetypes.guess_all_extensions(mime_type)),
                )

    def test_guess_all_extensions_requires_a_string(self):
        with self.assertRaises(TypeError):
            mimetypes_utils.guess_all_extensions(None)  # type: ignore[arg-type]


class TestAddType(unittest.TestCase):
    """Verify registration of custom MIME type mappings."""

    def setUp(self):
        register_custom_type()

    def test_add_type_registers_the_mapping(self):
        mimetypes_utils.add_type("application/x-kilo-other", ".kiloother")
        self.assertEqual(
            mimetypes_utils.guess_type("data.kiloother"),
            ("application/x-kilo-other", None),
        )

    def test_add_type_returns_none(self):
        self.assertIsNone(mimetypes_utils.add_type("application/x-kilo-third", ".kilothird"))

    def test_add_type_requires_a_string_type(self):
        with self.assertRaises(TypeError):
            mimetypes_utils.add_type(None, ".kilo")  # type: ignore[arg-type]

    def test_add_type_requires_a_non_empty_extension(self):
        with self.assertRaises(ValueError):
            mimetypes_utils.add_type("application/x-kilo", "   ")

    def test_add_type_requires_a_boolean_strict_flag(self):
        with self.assertRaises(TypeError):
            mimetypes_utils.add_type("application/x-kilo", ".kilo", strict="no")  # type: ignore[arg-type]


class TestTypeForExtension(unittest.TestCase):
    """Verify lookup of the MIME type of an extension."""

    def setUp(self):
        register_custom_type()

    def test_type_for_extension_with_a_leading_dot(self):
        self.assertEqual(
            mimetypes_utils.type_for_extension(_CUSTOM_EXTENSION),
            _CUSTOM_TYPE,
        )

    def test_type_for_extension_without_a_leading_dot(self):
        self.assertEqual(
            mimetypes_utils.type_for_extension(_CUSTOM_EXTENSION.lstrip(".")),
            _CUSTOM_TYPE,
        )

    def test_type_for_extension_of_unknown_extension(self):
        self.assertIsNone(
            mimetypes_utils.type_for_extension(".definitely-not-a-type"),
        )

    def test_type_for_extension_requires_a_string(self):
        with self.assertRaises(TypeError):
            mimetypes_utils.type_for_extension(None)  # type: ignore[arg-type]

    def test_type_for_extension_rejects_an_empty_extension(self):
        with self.assertRaises(ValueError):
            mimetypes_utils.type_for_extension("")


class TestNormalizeExtension(unittest.TestCase):
    """Verify normalization of file extensions."""

    def test_normalize_extension_adds_the_leading_dot(self):
        self.assertEqual(mimetypes_utils.normalize_extension("html"), ".html")

    def test_normalize_extension_keeps_the_leading_dot(self):
        self.assertEqual(mimetypes_utils.normalize_extension(".html"), ".html")

    def test_normalize_extension_lowercases_the_extension(self):
        self.assertEqual(mimetypes_utils.normalize_extension(".HTML"), ".html")

    def test_normalize_extension_trims_whitespace(self):
        self.assertEqual(mimetypes_utils.normalize_extension("  .png  "), ".png")

    def test_normalize_extension_requires_a_string(self):
        with self.assertRaises(TypeError):
            mimetypes_utils.normalize_extension(None)  # type: ignore[arg-type]

    def test_normalize_extension_rejects_an_empty_extension(self):
        with self.assertRaises(ValueError):
            mimetypes_utils.normalize_extension("   ")


class TestInitDatabase(unittest.TestCase):
    """Verify initialization of the MIME type database."""

    def tearDown(self):
        mimetypes_utils.init_database()

    def test_init_database_restores_the_platform_defaults(self):
        mimetypes_utils.add_type("application/x-kilo-temporary", ".kilotemporary")
        self.assertEqual(
            mimetypes_utils.guess_type("data.kilotemporary"),
            ("application/x-kilo-temporary", None),
        )
        mimetypes_utils.init_database()
        self.assertIsNone(mimetypes_utils.guess_type("data.kilotemporary")[0])

    def test_init_database_reads_extra_files(self):
        with tempfile.TemporaryDirectory() as directory:
            path = os.path.join(directory, "custom.mime")
            with open(path, "w", encoding="utf-8") as handle:
                handle.write("text/x-kilomime kilomime\n")
            mimetypes_utils.init_database([path])
            self.assertEqual(
                mimetypes_utils.guess_type("data.kilomime"),
                ("text/x-kilomime", None),
            )

    def test_init_database_ignores_missing_files(self):
        mimetypes_utils.init_database(["/definitely/not/a/mime/file"])
        self.assertIsInstance(mimetypes_utils.guess_type("page.html"), tuple)

    def test_init_database_rejects_a_string(self):
        with self.assertRaises(TypeError):
            mimetypes_utils.init_database("/etc/mime.types")  # type: ignore[arg-type]

    def test_init_database_rejects_a_list_of_non_strings(self):
        with self.assertRaises(TypeError):
            mimetypes_utils.init_database([1])  # type: ignore[list-item]


class TestIsValidMimeType(unittest.TestCase):
    """Verify validation of MIME type strings."""

    def test_is_valid_mime_type_accepts_a_type_and_subtype(self):
        self.assertTrue(mimetypes_utils.is_valid_mime_type("text/html"))

    def test_is_valid_mime_type_accepts_a_structured_suffix(self):
        self.assertTrue(mimetypes_utils.is_valid_mime_type("application/vnd.api+json"))

    def test_is_valid_mime_type_rejects_a_missing_subtype(self):
        self.assertFalse(mimetypes_utils.is_valid_mime_type("text"))

    def test_is_valid_mime_type_rejects_an_empty_subtype(self):
        self.assertFalse(mimetypes_utils.is_valid_mime_type("text/"))

    def test_is_valid_mime_type_rejects_a_missing_type(self):
        self.assertFalse(mimetypes_utils.is_valid_mime_type("/html"))

    def test_is_valid_mime_type_rejects_an_empty_value(self):
        self.assertFalse(mimetypes_utils.is_valid_mime_type(""))

    def test_is_valid_mime_type_requires_a_string(self):
        with self.assertRaises(TypeError):
            mimetypes_utils.is_valid_mime_type(None)  # type: ignore[arg-type]


class TestMimeCategory(unittest.TestCase):
    """Verify extraction of the top level type of a MIME type."""

    def test_mime_category_of_a_text_type(self):
        self.assertEqual(mimetypes_utils.mime_category("text/html"), "text")

    def test_mime_category_is_lower_case(self):
        self.assertEqual(mimetypes_utils.mime_category("IMAGE/PNG"), "image")

    def test_mime_category_of_a_malformed_type(self):
        self.assertEqual(mimetypes_utils.mime_category("not-a-type"), "")

    def test_mime_category_requires_a_string(self):
        with self.assertRaises(TypeError):
            mimetypes_utils.mime_category(None)  # type: ignore[arg-type]


class TestIsTextMimeType(unittest.TestCase):
    """Verify detection of textual MIME types."""

    def test_is_text_mime_type_accepts_text_types(self):
        self.assertTrue(mimetypes_utils.is_text_mime_type("text/html"))
        self.assertTrue(mimetypes_utils.is_text_mime_type("text/plain"))

    def test_is_text_mime_type_accepts_textual_application_types(self):
        self.assertTrue(mimetypes_utils.is_text_mime_type("application/json"))
        self.assertTrue(mimetypes_utils.is_text_mime_type("application/xml"))

    def test_is_text_mime_type_rejects_binary_types(self):
        self.assertFalse(mimetypes_utils.is_text_mime_type("image/png"))
        self.assertFalse(mimetypes_utils.is_text_mime_type("application/pdf"))

    def test_is_text_mime_type_rejects_malformed_types(self):
        self.assertFalse(mimetypes_utils.is_text_mime_type("not-a-type"))

    def test_is_text_mime_type_requires_a_string(self):
        with self.assertRaises(TypeError):
            mimetypes_utils.is_text_mime_type(None)  # type: ignore[arg-type]


if __name__ == "__main__":
    unittest.main()
