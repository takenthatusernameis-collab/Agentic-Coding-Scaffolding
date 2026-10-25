"""Tests for case_utils module."""

import unittest

from case_utils import (
    camel_case,
    constant_case,
    dot_case,
    kebab_case,
    pascal_case,
    screaming_snake_case,
    sentence_case,
    slash_case,
    snake_case,
    spinal_case,
    title_case,
    train_case,
)


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


class TestSnakeCase(unittest.TestCase):
    def test_simple(self):
        self.assertEqual(snake_case("Hello World"), "hello_world")

    def test_camel_case(self):
        self.assertEqual(snake_case("xmlParser"), "xml_parser")

    def test_pascal_case(self):
        self.assertEqual(snake_case("HelloWorld"), "hello_world")

    def test_already_snake(self):
        self.assertEqual(snake_case("already_snake"), "already_snake")

    def test_mixed_separators(self):
        self.assertEqual(snake_case("foo-bar.baz"), "foo_bar_baz")

    def test_empty(self):
        self.assertEqual(snake_case(""), "")

    def test_non_string(self):
        with self.assertRaises(TypeError):
            snake_case(123)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            snake_case(None)  # type: ignore[arg-type]


class TestCamelCase(unittest.TestCase):
    def test_simple(self):
        self.assertEqual(camel_case("hello world"), "helloWorld")

    def test_snake_case(self):
        self.assertEqual(camel_case("xml_parser"), "xmlParser")

    def test_kebab_case(self):
        self.assertEqual(camel_case("hello-world"), "helloWorld")

    def test_pascal_case(self):
        self.assertEqual(camel_case("HelloWorld"), "helloWorld")

    def test_already_camel(self):
        self.assertEqual(camel_case("alreadyCamel"), "alreadyCamel")

    def test_empty(self):
        self.assertEqual(camel_case(""), "")

    def test_non_string(self):
        with self.assertRaises(TypeError):
            camel_case(123)  # type: ignore[arg-type]


if __name__ == "__main__":
    unittest.main()


class TestCaseAliases(unittest.TestCase):
    def test_screaming_snake_case(self):
        self.assertEqual(screaming_snake_case("hello world"), "HELLO_WORLD")

    def test_spinal_case(self):
        self.assertEqual(spinal_case("hello world"), "hello-world")

    def test_train_case(self):
        self.assertEqual(train_case("hello world"), "HelloWorld")

    def test_dot_case(self):
        self.assertEqual(dot_case("hello world"), "hello.world")

    def test_slash_case(self):
        self.assertEqual(slash_case("hello world"), "hello/world")

    def test_title_case(self):
        self.assertEqual(title_case("hello world"), "Hello World")
        self.assertEqual(title_case("xml_parser"), "Xml Parser")

    def test_sentence_case(self):
        self.assertEqual(sentence_case("hello WORLD"), "Hello world")
