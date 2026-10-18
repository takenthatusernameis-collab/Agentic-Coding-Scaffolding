import unittest

from shlex_utils import join, quote, split


class TestShlexUtils(unittest.TestCase):
    def test_split(self):
        self.assertEqual(split("foo bar 'baz qux'"), ["foo", "bar", "baz qux"])

    def test_split_type_error(self):
        with self.assertRaises(TypeError):
            split(123)

    def test_quote(self):
        self.assertEqual(quote("foo bar"), "'foo bar'")

    def test_quote_type_error(self):
        with self.assertRaises(TypeError):
            quote(1)

    def test_join(self):
        self.assertEqual(join(["foo", "bar baz"]), "foo 'bar baz'")


if __name__ == "__main__":
    unittest.main()
