import unittest

from pprint_utils import isreadable, isrecursive, pformat, pprint, saferepr


class TestPprintUtils(unittest.TestCase):
    def test_pformat(self):
        self.assertEqual(pformat({"a": 1, "b": 2}), "{'a': 1, 'b': 2}")

    def test_pprint_returns_none(self):
        import io

        buf = io.StringIO()
        self.assertIsNone(pprint({"a": 1}, stream=buf))

    def test_isreadable(self):
        self.assertTrue(isreadable([1, 2, 3]))

    def test_isrecursive(self):
        d = {}
        d["self"] = d
        self.assertTrue(isrecursive(d))

    def test_saferepr(self):
        d = {}
        d["self"] = d
        self.assertIn("...", saferepr(d))


if __name__ == "__main__":
    unittest.main()
