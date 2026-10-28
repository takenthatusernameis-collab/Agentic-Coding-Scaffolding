import unittest

from greeting_utils import (
    format_farewell,
    format_greeting,
    format_names,
    format_thanks,
    format_welcome,
)


class TestGreetingUtils(unittest.TestCase):
    def test_format_greeting_default(self):
        self.assertEqual(format_greeting("World"), "Hello, World!")

    def test_format_greeting_custom(self):
        self.assertEqual(format_greeting("Alice", "Hi"), "Hi, Alice!")

    def test_format_greeting_empty_name(self):
        self.assertEqual(format_greeting(""), "Hello, !")

    def test_format_names(self):
        self.assertEqual(
            format_names(["Alice", "Bob"]),
            "Hello, Alice! Hello, Bob!",
        )

    def test_format_names_custom_greeting(self):
        self.assertEqual(
            format_names(["Carol"], "Hey"),
            "Hey, Carol!",
        )

    def test_format_names_empty(self):
        self.assertEqual(format_names([]), "")


class TestFormatFarewell(unittest.TestCase):
    def test_default(self):
        self.assertEqual(format_farewell("World"), "Goodbye, World!")

    def test_custom(self):
        self.assertEqual(format_farewell("Alice", "Bye"), "Bye, Alice!")

    def test_empty_name(self):
        self.assertEqual(format_farewell(""), "Goodbye, !")

    def test_type_error_name(self):
        with self.assertRaises(TypeError):
            format_farewell(123)  # type: ignore[arg-type]

    def test_type_error_farewell(self):
        with self.assertRaises(TypeError):
            format_farewell("Alice", 5)  # type: ignore[arg-type]


class TestFormatWelcome(unittest.TestCase):
    def test_default(self):
        self.assertEqual(format_welcome("World"), "Welcome, World!")

    def test_custom(self):
        self.assertEqual(format_welcome("Alice", "Hi"), "Hi, Alice!")

    def test_empty_name(self):
        self.assertEqual(format_welcome(""), "Welcome, !")

    def test_type_error_name(self):
        with self.assertRaises(TypeError):
            format_welcome(123)  # type: ignore[arg-type]

    def test_type_error_welcome(self):
        with self.assertRaises(TypeError):
            format_welcome("Alice", 5)  # type: ignore[arg-type]


class TestFormatThanks(unittest.TestCase):
    def test_default(self):
        self.assertEqual(format_thanks("World"), "Thanks, World!")

    def test_custom(self):
        self.assertEqual(format_thanks("Alice", "Cheers"), "Cheers, Alice!")

    def test_empty_name(self):
        self.assertEqual(format_thanks(""), "Thanks, !")

    def test_type_error_name(self):
        with self.assertRaises(TypeError):
            format_thanks(123)  # type: ignore[arg-type]

    def test_type_error_thanks(self):
        with self.assertRaises(TypeError):
            format_thanks("Alice", 5)  # type: ignore[arg-type]


if __name__ == "__main__":
    unittest.main()
