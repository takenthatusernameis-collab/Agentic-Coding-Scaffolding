import unittest

import keyword_utils


class TestKeywordUtils(unittest.TestCase):
    def test_is_keyword(self):
        self.assertTrue(keyword_utils.is_keyword("if"))
        self.assertFalse(keyword_utils.is_keyword("foo"))

    def test_is_soft_keyword(self):
        self.assertTrue(keyword_utils.is_soft_keyword("match"))
        self.assertFalse(keyword_utils.is_soft_keyword("if"))

    def test_kwlist(self):
        self.assertIn("def", keyword_utils.kwlist())

    def test_softkwlist(self):
        self.assertIn("match", keyword_utils.softkwlist())

    def test_type_error(self):
        with self.assertRaises(TypeError):
            keyword_utils.is_keyword(123)
        with self.assertRaises(TypeError):
            keyword_utils.is_soft_keyword(123)


if __name__ == "__main__":
    unittest.main()
