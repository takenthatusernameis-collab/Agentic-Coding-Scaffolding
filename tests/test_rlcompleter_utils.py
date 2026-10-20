import unittest

from rlcompleter_utils import Completer, complete


class TestRlcompleterUtils(unittest.TestCase):
    def test_completer_complete(self):
        c = Completer({"foo": 1, "foobar": 2})
        result = c.complete("foo", 0)
        self.assertIn(result, ("foo", "foobar"))

    def test_completer_state_out_of_range(self):
        c = Completer({"foo": 1})
        c.complete("foo", 0)
        self.assertIsNone(c.complete("foo", 5))

    def test_completer_type_errors(self):
        c = Completer()
        with self.assertRaises(TypeError):
            c.complete(1, 0)
        with self.assertRaises(TypeError):
            c.complete("foo", "0")
        with self.assertRaises(TypeError):
            Completer("not a dict")

    def test_complete_function(self):
        result = complete("pri", 0, {"print": print})
        self.assertTrue(result.startswith("print"))

    def test_complete_type_errors(self):
        with self.assertRaises(TypeError):
            complete(1, 0)
        with self.assertRaises(TypeError):
            complete("pri", "0")
        with self.assertRaises(TypeError):
            complete("pri", 0, "not a dict")


if __name__ == "__main__":
    unittest.main()
