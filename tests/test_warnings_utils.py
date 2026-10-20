"""Tests for warnings_utils module."""

import unittest
import warnings

import warnings_utils


class TestWarn(unittest.TestCase):
    def test_warn_issues_warning(self):
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            warnings_utils.warn("test message", category=DeprecationWarning)
            self.assertEqual(len(w), 1)
            self.assertIsInstance(w[0].category, type)
            self.assertTrue(issubclass(w[0].category, DeprecationWarning))

    def test_warn_type_error(self):
        with self.assertRaises(TypeError):
            warnings_utils.warn(123)
        with self.assertRaises(TypeError):
            warnings_utils.warn("msg", category=str)
        with self.assertRaises(TypeError):
            warnings_utils.warn("msg", stacklevel="1")


class TestSimpleFilter(unittest.TestCase):
    def test_simplefilter(self):
        warnings_utils.simplefilter("ignore", category=RuntimeWarning)
        warnings_utils.simplefilter("always", append=True)

    def test_simplefilter_type_errors(self):
        with self.assertRaises(TypeError):
            warnings_utils.simplefilter(123)
        with self.assertRaises(TypeError):
            warnings_utils.simplefilter("ignore", append="yes")


class TestFilterwarnings(unittest.TestCase):
    def test_filterwarnings(self):
        warnings_utils.filterwarnings("ignore", message="test", category=UserWarning)
        warnings_utils.filterwarnings("default", module="test_module")


class TestResetwarnings(unittest.TestCase):
    def test_resetwarnings(self):
        warnings_utils.simplefilter("ignore")
        warnings_utils.resetwarnings()


class TestCatchWarnings(unittest.TestCase):
    def test_catch_warnings(self):
        with warnings_utils.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            warnings.warn("hello")
            self.assertTrue(len(w) >= 1)


class TestShowAndFormat(unittest.TestCase):
    def test_formatwarning(self):
        w = DeprecationWarning("old")
        result = warnings_utils.formatwarning(w, DeprecationWarning, "test.py", 10)
        self.assertIsInstance(result, str)
        self.assertIn("DeprecationWarning", result)

    def test_showwarning(self):
        w = UserWarning("note")
        warnings_utils.showwarning(w, UserWarning, "test.py", 5)


if __name__ == "__main__":
    unittest.main()
