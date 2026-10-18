import unittest

from fnmatch_utils import filter_names, match, match_case, translate


class TestFnmatchUtils(unittest.TestCase):
    def test_match(self):
        self.assertTrue(match("foo.txt", "*.txt"))
        self.assertFalse(match("foo.py", "*.txt"))

    def test_match_case(self):
        self.assertTrue(match_case("foo.txt", "*.txt"))
        self.assertFalse(match_case("foo.TXT", "*.txt"))

    def test_filter_names(self):
        self.assertEqual(filter_names(["a.txt", "b.py", "c.txt"], "*.txt"), ["a.txt", "c.txt"])

    def test_translate(self):
        import re

        self.assertTrue(re.match(translate("*.txt"), "foo.txt"))

    def test_type_errors(self):
        with self.assertRaises(TypeError):
            match(123, "*.txt")
        with self.assertRaises(TypeError):
            match("x", 123)
        with self.assertRaises(TypeError):
            match_case(1, "p")
        with self.assertRaises(TypeError):
            filter_names("abc", "*.txt")
        with self.assertRaises(TypeError):
            filter_names(["a"], 5)
        with self.assertRaises(TypeError):
            translate(5)


if __name__ == "__main__":
    unittest.main()
