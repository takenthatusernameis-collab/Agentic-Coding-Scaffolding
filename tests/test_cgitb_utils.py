import unittest
import warnings

import cgitb_utils


class TestCgitbUtils(unittest.TestCase):
    def test_hook_class(self):
        self.assertTrue(callable(cgitb_utils.hook_class()))

    def test_html(self):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            out = cgitb_utils.html((ValueError, ValueError("boom"), None), 3)
        self.assertIsInstance(out, str)

    def test_text(self):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            out = cgitb_utils.text((ValueError, ValueError("boom"), None), 3)
        self.assertIsInstance(out, str)

    def test_reset(self):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            cgitb_utils.reset()


if __name__ == "__main__":
    unittest.main()
