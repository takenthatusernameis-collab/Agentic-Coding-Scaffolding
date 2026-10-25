"""Tests for case_utils module."""

import unittest

from case_utils import constant_case, kebab_case, pascal_case


class TestKebabCase(unittest.TestCase):
    def test_simple(self):
        self.assertEqual(kebab_case("Hello World"), "hello-world")

    def test_camel_case(self):
        self.assertEqual(kebab_case("xmlParser"), "xml-parser")

    def test_pascal_case(self):
        self.assertEqual(kebab_case("HelloWorld"), "hello-world")

    def test_already_kebab(self):
        self.assertEqual(kebab_case("already-kebab"), "already-kebab")

    def test_mixed_separators(self):
        self.assertEqual(kebab_case("foo_bar.baz"), "foo-bar-baz")

    def test_empty(self):
        self.assertEqual(kebab_case(""), "")

    def test_non_string(self):
        with self.assertRaises(TypeError):
            kebab_case(123)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            kebab_case(None)  # type: ignore[arg-type]


class TestPascalCase(unittest.TestCase):
    def test_simple(self):
        self.assertEqual(pascal_case("hello world"), "HelloWorld")

    def test_snake_case(self):
        self.assertEqual(pascal_case("xml_parser"), "XmlParser")

    def test_kebab_case(self):
        self.assertEqual(pascal_case("hello-world"), "HelloWorld")

    def test_already_pascal(self):
        self.assertEqual(pascal_case("AlreadyPascal"), "AlreadyPascal")

    def test_empty(self):
        self.assertEqual(pascal_case(""), "")

    def test_non_string(self):
        with self.assertRaises(TypeError):
            pascal_case(123)  # type: ignore[arg-type]


class TestConstantCase(unittest.TestCase):
    def test_simple(self):
        self.assertEqual(constant_case("hello world"), "HELLO_WORLD")

    def test_camel_case(self):
        self.assertEqual(constant_case("xmlParser"), "XML_PARSER")

    def test_already_constant(self):
        self.assertEqual(constant_case("MAX_SIZE"), "MAX_SIZE")

    def test_empty(self):
        self.assertEqual(constant_case(""), "")

    def test_non_string(self):
        with self.assertRaises(TypeError):
            constant_case(True)  # type: ignore[arg-type]


if __name__ == "__main__":
    unittest.main()
