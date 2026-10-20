"""Tests for the scaffold refresh tool."""

import importlib.util
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TOOL = ROOT / "tools" / "refresh_scaffold.py"


def load_tool():
    """Return the refresh tool module loaded from its file path."""
    spec = importlib.util.spec_from_file_location("refresh_scaffold", TOOL)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


refresh_scaffold = load_tool()


def stale_scaffold() -> str:
    """Return a generator holding an outdated copy of ``doctest_utils.py``."""
    return (
        "cat > \"$OUTPUT_DIR/doctest_utils.py\" <<'DOCTEST_UTILS'\n"
        "an outdated body\n"
        "DOCTEST_UTILS\n"
    )


class TestIsVerbatimCopy(unittest.TestCase):
    """Verify which embedded files are copied verbatim."""

    def test_python_sources_are_verbatim(self):
        self.assertTrue(refresh_scaffold.is_verbatim_copy("sample_utils.py"))
        self.assertTrue(refresh_scaffold.is_verbatim_copy("tests/test_sample_utils.py"))

    def test_the_scaffold_command_documentation_is_verbatim(self):
        self.assertTrue(refresh_scaffold.is_verbatim_copy(".kilo/command/scaffold-project.md"))

    def test_templates_are_not_verbatim(self):
        self.assertFalse(refresh_scaffold.is_verbatim_copy("README.md"))
        self.assertFalse(refresh_scaffold.is_verbatim_copy("AGENTS.md"))
        self.assertFalse(refresh_scaffold.is_verbatim_copy("CHANGELOG.md"))


class TestRefresh(unittest.TestCase):
    """Verify the rewrite of the embedded copies."""

    def test_refresh_replaces_a_stale_body(self):
        refreshed, changed, stale = refresh_scaffold.refresh(stale_scaffold())
        expected = (ROOT / "doctest_utils.py").read_text().rstrip("\n")
        self.assertIn(expected, refreshed)
        self.assertEqual(changed, ["doctest_utils.py"])
        self.assertEqual(stale, [])

    def test_refresh_keeps_the_templates(self):
        text = (
            "cat > \"$OUTPUT_DIR/README.md\" <<'__README__'\n"
            "# ${PROJECT_NAME}\n"
            "__README__\n"
        )
        refreshed, changed, stale = refresh_scaffold.refresh(text)
        self.assertEqual(refreshed, text)
        self.assertEqual(changed, [])
        self.assertEqual(stale, [])

    def test_refresh_reports_a_missing_repository_copy(self):
        text = (
            "cat > \"$OUTPUT_DIR/absent_utils.py\" <<'ABSENT_UTILS'\n"
            "a body without a repository copy\n"
            "ABSENT_UTILS\n"
        )
        refreshed, changed, stale = refresh_scaffold.refresh(text)
        self.assertEqual(refreshed, text)
        self.assertEqual(changed, [])
        self.assertEqual(stale, ["absent_utils.py"])

    def test_refresh_leaves_a_current_copy_untouched(self):
        body = (ROOT / "doctest_utils.py").read_text().rstrip("\n")
        text = (
            "cat > \"$OUTPUT_DIR/doctest_utils.py\" <<'DOCTEST_UTILS'\n"
            f"{body}\n"
            "DOCTEST_UTILS\n"
        )
        refreshed, changed, stale = refresh_scaffold.refresh(text)
        self.assertEqual(refreshed, text)
        self.assertEqual(changed, [])
        self.assertEqual(stale, [])


class TestCommandLine(unittest.TestCase):
    """Verify the command line interface of the refresh tool."""

    def test_the_check_mode_reports_a_synchronised_generator(self):
        result = subprocess.run(
            [sys.executable, str(TOOL), "--check"],
            capture_output=True,
            text=True,
            timeout=120,
            check=False,
        )
        self.assertEqual(result.returncode, 0, msg=result.stdout + result.stderr)
        self.assertIn("in sync", result.stdout)


if __name__ == "__main__":
    unittest.main()
