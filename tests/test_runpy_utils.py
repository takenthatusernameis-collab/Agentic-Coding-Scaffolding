import os
import tempfile
import unittest

from runpy_utils import run_module, run_path


class TestRunModule(unittest.TestCase):
    def test_run_module_returns_namespace(self):
        result = run_module("base64")
        self.assertIn("b64encode", result)
        self.assertIn("b64decode", result)

    def test_run_module_with_init_globals(self):
        result = run_module("base64", init_globals={"__name__": "base64"})
        self.assertIn("b64encode", result)

    def test_run_module_rejects_non_str(self):
        with self.assertRaises(TypeError):
            run_module(123)


class TestRunPath(unittest.TestCase):
    def test_run_path_executes_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "script.py")
            with open(path, "w") as f:
                f.write("ANSWER = 6 * 7\n")
            result = run_path(path)
            self.assertEqual(result["ANSWER"], 42)

    def test_run_path_with_run_name(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "script.py")
            with open(path, "w") as f:
                f.write("VALUE = __name__\n")
            result = run_path(path, run_name="custom")
            self.assertEqual(result["VALUE"], "custom")

    def test_run_path_rejects_non_str(self):
        with self.assertRaises(TypeError):
            run_path(None)


if __name__ == "__main__":
    unittest.main()
