"""Tests for the exported-but-untested callable scanner."""

import ast
import importlib.util
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TOOL = ROOT / "tools" / "scan_untested.py"


def load_tool():
    """Return the scanner module loaded from its file path."""
    spec = importlib.util.spec_from_file_location("scan_untested", TOOL)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


scan_untested = load_tool()


class TestNameReferenced(unittest.TestCase):
    """Verify that a name is only "referenced" when it appears as a whole word.

    A bare substring test is too loose: the interactive ``help`` facade of
    ``pydoc_utils`` was reported as tested because ``help`` is a substring of
    ``helpers`` in the test prose. Word-boundary matching makes a reference
    real without reporting false positives for embedded substrings.
    """

    def test_a_whole_word_is_referenced(self):
        self.assertTrue(scan_untested.name_referenced("the help helper", "help"))

    def test_a_substring_is_not_referenced(self):
        self.assertFalse(scan_untested.name_referenced("the helpers", "help"))

    def test_a_prefix_is_not_referenced(self):
        self.assertFalse(scan_untested.name_referenced("the helper", "help"))

    def test_a_suffix_is_not_referenced(self):
        self.assertFalse(scan_untested.name_referenced("helpful", "help"))

    def test_an_underscored_name_is_referenced_as_a_whole_word(self):
        # ``_`` is a word character, so ``_help`` is a single whole word and is
        # correctly matched. The scanner skips underscore-prefixed names
        # separately (``scan_module`` filters ``name.startswith("_")``), so this
        # only verifies the matcher's own behaviour.
        self.assertTrue(scan_untested.name_referenced("the _help helper", "_help"))


class TestExportedNames(unittest.TestCase):
    """Verify that every spelling of ``__all__`` is recognized.

    The annotated form (``__all__: list[str] = [...]``) was previously ignored,
    which silently skipped every module that declared its exports with a type
    annotation and made the scanner report a false clean.
    """

    def test_a_plain_assignment_is_recognized(self):
        tree = ast.parse("__all__ = ['alpha', 'beta']")
        self.assertEqual(scan_untested.exported_names(tree), {"alpha", "beta"})

    def test_an_annotated_assignment_is_recognized(self):
        tree = ast.parse("__all__: list[str] = ['alpha', 'beta']")
        self.assertEqual(scan_untested.exported_names(tree), {"alpha", "beta"})

    def test_a_tuple_literal_is_recognized(self):
        tree = ast.parse("__all__ = ('alpha',)")
        self.assertEqual(scan_untested.exported_names(tree), {"alpha"})

    def test_non_string_entries_are_ignored(self):
        tree = ast.parse("__all__ = ['alpha', 42]")
        self.assertEqual(scan_untested.exported_names(tree), {"alpha"})

    def test_a_non_literal_export_list_is_unknown(self):
        tree = ast.parse("__all__ = list(('alpha',))")
        self.assertEqual(scan_untested.exported_names(tree), set())

    def test_a_module_without_all_is_empty(self):
        self.assertEqual(scan_untested.exported_names(ast.parse("value = 1")), set())

    def test_a_real_annotated_module_is_scanned(self):
        tree = ast.parse((ROOT / "telnetlib_utils.py").read_text())
        self.assertIn("read_some", scan_untested.exported_names(tree))


class TestSkipNames(unittest.TestCase):
    """Verify that interactive stdlib facades are filtered out by default."""

    def test_help_is_a_known_interactive_facade(self):
        self.assertIn("help", scan_untested.SKIP_NAMES)

    def test_pydoc_utils_help_is_not_reported_as_a_gap(self):
        gaps = scan_untested.scan_module(ROOT / "pydoc_utils.py", False)
        self.assertNotIn("help", gaps)


class TestScan(unittest.TestCase):
    """Verify the scanner reports no exported-but-untested callables."""

    def test_the_repository_is_clean(self):
        result = subprocess.run(
            [sys.executable, str(TOOL)],
            capture_output=True,
            text=True,
            timeout=120,
            check=False,
        )
        self.assertEqual(result.returncode, 0, msg=result.stdout + result.stderr)
        self.assertIn("no exported-but-untested callables", result.stdout)

    def test_the_all_flag_lists_everything(self):
        result = subprocess.run(
            [sys.executable, str(TOOL), "--all"],
            capture_output=True,
            text=True,
            timeout=120,
            check=False,
        )
        # With --all the scanner lists type variables, constants, classes, and
        # interactive facades too, so it must report something.
        self.assertGreater(len(result.stdout), 0)


if __name__ == "__main__":
    unittest.main()
