"""Tests for the exported-but-untested callable scanner."""

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
