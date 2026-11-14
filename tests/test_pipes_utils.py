"""Tests for pipes_utils."""

import importlib
import sys
import unittest
from unittest import mock

import pipes_utils


class TestPipesUtils(unittest.TestCase):
    def test_exports(self) -> None:
        for name in [
            "Template",
            "quote",
            "quote_command",
            "create_template",
            "is_available",
            "make_pipeline",
            "step_kinds",
        ]:
            self.assertTrue(hasattr(pipes_utils, name))

    def test_is_available(self) -> None:
        self.assertIs(pipes_utils.is_available(), True)

    def test_quote_and_quote_command(self) -> None:
        self.assertIsInstance(pipes_utils.quote("foo"), str)
        self.assertEqual(pipes_utils.quote_command("foo"), pipes_utils.quote("foo"))
        quoted = pipes_utils.quote_command("a b")
        self.assertIsInstance(quoted, str)
        self.assertIn("a", quoted)

    def test_quote_command_type_error(self) -> None:
        with self.assertRaises(TypeError):
            pipes_utils.quote_command(123)  # type: ignore[arg-type]

    def test_create_template(self) -> None:
        t = pipes_utils.create_template()
        self.assertIsInstance(t, pipes_utils.Template)

    def test_step_kinds(self) -> None:
        kinds = pipes_utils.step_kinds()
        self.assertEqual(kinds, ["FILEIN", "FILEOUT", "SOURCE", "SINK"])
        self.assertIsInstance(kinds, list)

    def test_make_pipeline(self) -> None:
        t = pipes_utils.make_pipeline("cat file.txt", "sort")
        self.assertIsInstance(t, pipes_utils.Template)
        steps = getattr(t, "steps")
        self.assertEqual(len(steps), 2)
        self.assertIsInstance(steps[0], tuple)

    def test_make_pipeline_rejects_non_string(self) -> None:
        with self.assertRaises(TypeError):
            pipes_utils.make_pipeline("cat", 1)  # type: ignore[arg-type]

    def test_unavailable_branch(self) -> None:
        try:
            with mock.patch.dict(sys.modules, {"pipes": None}):
                reloaded = importlib.reload(pipes_utils)
                self.assertIs(reloaded.is_available(), False)
                with self.assertRaises(RuntimeError):
                    reloaded.Template()
                with self.assertRaises(RuntimeError):
                    reloaded.create_template()
                with self.assertRaises(RuntimeError):
                    reloaded.make_pipeline("cat")
                # Shell quoting falls back to shlex when pipes is absent.
                self.assertEqual(reloaded.quote("a b"), "'a b'")
                self.assertEqual(reloaded.quote_command("a b"), "'a b'")
                self.assertEqual(
                    reloaded.step_kinds(), ["FILEIN", "FILEOUT", "SOURCE", "SINK"]
                )
        finally:
            importlib.reload(pipes_utils)


if __name__ == "__main__":
    unittest.main()
