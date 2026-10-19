import os
import tempfile
import unittest

from runpy_utils import run_module, run_path


class TestRunpyUtils(unittest.TestCase):
    def test_run_module_type_error(self):
        with self.assertRaises(TypeError):
            run_module(123)

    def test_run_path_type_error(self):
        with self.assertRaises(TypeError):
            run_path(123)

    def test_run_path(self):
        with tempfile.TemporaryDirectory() as d:
            p = os.path.join(d, "m.py")
            with open(p, "w") as f:
                f.write("x = 42\n")
            ns = run_path(p)
            self.assertEqual(ns["x"], 42)


if __name__ == "__main__":
    unittest.main()
