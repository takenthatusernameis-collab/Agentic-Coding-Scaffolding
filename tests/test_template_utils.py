"""Unit tests for the template_utils module."""

import unittest

from template_utils import (
    extract_placeholders,
    has_placeholders,
    render_from_dict,
    render_template,
    safe_substitute,
    substitute,
)


class TestRenderTemplate(unittest.TestCase):
    """Test cases for render_template function."""

    def test_basic_substitution(self) -> None:
        result = render_template("Hello {name}!", name="World")
        self.assertEqual(result, "Hello World!")

    def test_multiple_placeholders(self) -> None:
        result = render_template(
            "{greeting} {name}, you are {age} years old",
            greeting="Hi",
            name="Alice",
            age=30,
        )
        self.assertEqual(result, "Hi Alice, you are 30 years old")

    def test_no_placeholders(self) -> None:
        result = render_template("Hello World")
        self.assertEqual(result, "Hello World")

    def test_numeric_formatting(self) -> None:
        result = render_template("Pi is {0:.2f}", 3.14159)
        self.assertEqual(result, "Pi is 3.14")

    def test_missing_key_raises(self) -> None:
        with self.assertRaises(KeyError):
            render_template("Hello {name}!")

    def test_non_string_template(self) -> None:
        with self.assertRaises(TypeError):
            render_template(123)  # type: ignore


class TestSubstitute(unittest.TestCase):
    """Test cases for substitute function."""

    def test_basic_substitution(self) -> None:
        result = substitute("Hello $name!", name="World")
        self.assertEqual(result, "Hello World!")

    def test_braces_substitution(self) -> None:
        result = substitute("Hello ${name}!", name="World")
        self.assertEqual(result, "Hello World!")

    def test_multiple_placeholders(self) -> None:
        result = substitute("$greeting $name", greeting="Hi", name="Alice")
        self.assertEqual(result, "Hi Alice")

    def test_with_mapping(self) -> None:
        result = substitute("Hello $name", mapping={"name": "World"})
        self.assertEqual(result, "Hello World")

    def test_mapping_and_kwargs(self) -> None:
        result = substitute("$a $b", mapping={"a": "Hello"}, b="World")
        self.assertEqual(result, "Hello World")

    def test_missing_key_raises(self) -> None:
        with self.assertRaises(KeyError):
            substitute("Hello $name!")

    def test_non_string_template(self) -> None:
        with self.assertRaises(TypeError):
            substitute(123)  # type: ignore


class TestSafeSubstitute(unittest.TestCase):
    """Test cases for safe_substitute function."""

    def test_basic_substitution(self) -> None:
        result = safe_substitute("Hello $name!", name="World")
        self.assertEqual(result, "Hello World!")

    def test_missing_key_preserved(self) -> None:
        result = safe_substitute("Hello $name!")
        self.assertEqual(result, "Hello $name!")

    def test_partial_substitution(self) -> None:
        result = safe_substitute("Hello $name, you are $age", name="Alice")
        self.assertEqual(result, "Hello Alice, you are $age")

    def test_with_braces(self) -> None:
        result = safe_substitute("Hello ${name}", name="World")
        self.assertEqual(result, "Hello World")

    def test_non_string_template(self) -> None:
        with self.assertRaises(TypeError):
            safe_substitute(123)  # type: ignore


class TestRenderFromDict(unittest.TestCase):
    """Test cases for render_from_dict function."""

    def test_basic_render(self) -> None:
        result = render_from_dict("Hello {name}!", {"name": "World"})
        self.assertEqual(result, "Hello World!")

    def test_multiple_keys(self) -> None:
        result = render_from_dict("{a} {b}", {"a": "Hi", "b": "there"})
        self.assertEqual(result, "Hi there")

    def test_missing_key_with_default(self) -> None:
        result = render_from_dict("Hello {name}!", {}, default="Guest")
        self.assertEqual(result, "Hello Guest!")

    def test_partial_keys(self) -> None:
        result = render_from_dict("{greeting} {name}", {"greeting": "Hi"}, default="Friend")
        self.assertEqual(result, "Hi Friend")

    def test_no_context(self) -> None:
        result = render_from_dict("Hello {name}", default="World")
        self.assertEqual(result, "Hello World")

    def test_none_context(self) -> None:
        result = render_from_dict("Hello {name}", context=None, default="World")
        self.assertEqual(result, "Hello World")

    def test_non_string_template(self) -> None:
        with self.assertRaises(TypeError):
            render_from_dict(123, {})  # type: ignore

    def test_non_mapping_context(self) -> None:
        with self.assertRaises(TypeError):
            render_from_dict("Hi", "not a dict")  # type: ignore


class TestHasPlaceholders(unittest.TestCase):
    """Test cases for has_placeholders function."""

    def test_has_format_placeholder(self) -> None:
        self.assertTrue(has_placeholders("Hello {name}"))

    def test_has_multiple_format_placeholders(self) -> None:
        self.assertTrue(has_placeholders("{a} {b} {c}"))

    def test_has_template_placeholder(self) -> None:
        self.assertTrue(has_placeholders("Hello $name"))

    def test_has_template_braces(self) -> None:
        self.assertTrue(has_placeholders("Hello ${name}"))

    def test_no_placeholders(self) -> None:
        self.assertFalse(has_placeholders("Hello World"))

    def test_empty_string(self) -> None:
        self.assertFalse(has_placeholders(""))

    def test_mixed_placeholders(self) -> None:
        self.assertTrue(has_placeholders("Hello {name} and $age"))

    def test_non_string_template(self) -> None:
        with self.assertRaises(TypeError):
            has_placeholders(123)  # type: ignore


class TestExtractPlaceholders(unittest.TestCase):
    """Test cases for extract_placeholders function."""

    def test_extract_format_placeholders(self) -> None:
        result = extract_placeholders("Hello {name}, you are {age}")
        self.assertIn("name", result)
        self.assertIn("age", result)

    def test_extract_format_with_spec(self) -> None:
        result = extract_placeholders("Value: {num:.2f}, Text: {name}")
        self.assertIn("num", result)
        self.assertIn("name", result)

    def test_extract_template_placeholders(self) -> None:
        result = extract_placeholders("Hello $name and $age")
        self.assertIn("name", result)
        self.assertIn("age", result)

    def test_extract_template_braces(self) -> None:
        result = extract_placeholders("Hello ${name}")
        self.assertIn("name", result)

    def test_extract_mixed(self) -> None:
        result = extract_placeholders("{greeting} $name")
        self.assertIn("greeting", result)
        self.assertIn("name", result)

    def test_extract_no_duplicates(self) -> None:
        result = extract_placeholders("{name} $name")
        self.assertEqual(result.count("name"), 1)

    def test_no_placeholders(self) -> None:
        result = extract_placeholders("Hello World")
        self.assertEqual(result, [])

    def test_skip_numeric_indices(self) -> None:
        result = extract_placeholders("Hello {0} and {1}")
        # Numeric indices should be skipped
        self.assertEqual(result, [])

    def test_empty_string(self) -> None:
        result = extract_placeholders("")
        self.assertEqual(result, [])

    def test_non_string_template(self) -> None:
        with self.assertRaises(TypeError):
            extract_placeholders(123)  # type: ignore


if __name__ == "__main__":
    unittest.main()
