import unittest

from greeting_utils import format_greeting, format_names


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


if __name__ == '__main__':
    unittest.main()
