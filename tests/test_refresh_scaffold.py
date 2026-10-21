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


class TestHeredocDelimiter(unittest.TestCase):
    """Verify the delimiter that the tool derives for a file."""

    def test_a_module_uses_its_own_name(self):
        self.assertEqual(
            refresh_scaffold.heredoc_delimiter("ipaddress_utils.py"),
            "IPADDRESS_UTILS",
        )

    def test_a_test_is_prefixed_with_test(self):
        self.assertEqual(
            refresh_scaffold.heredoc_delimiter("tests/test_ipaddress_utils.py"),
            "TEST_IPADDRESS_UTILS",
        )

    def test_a_delimiter_avoids_the_body_of_the_file(self):
        delimiter = refresh_scaffold.unique_delimiter("sample_utils.py", "SAMPLE_UTILS\n")
        self.assertNotEqual(delimiter, "SAMPLE_UTILS")
        self.assertTrue(delimiter.startswith("SAMPLE_UTILS"))


class TestMissingCopies(unittest.TestCase):
    """Verify the detection of the wrapper files the generator does not embed."""

    def test_a_complete_generator_has_no_missing_copy(self):
        text = (ROOT / "scaffold.sh").read_text()
        self.assertEqual(refresh_scaffold.missing_copies(text), [])

    def test_a_generator_without_a_module_reports_it(self):
        text = (ROOT / "scaffold.sh").read_text()
        trimmed = text.replace(
            "cat > \"$OUTPUT_DIR/zipimport_utils.py\"",
            "cat > \"$OUTPUT_DIR/other.py\"",
        ).replace(
            "cat > \"$OUTPUT_DIR/tests/test_zipimport_utils.py\"",
            "cat > \"$OUTPUT_DIR/tests/test_other.py\"",
        )
        missing = refresh_scaffold.missing_copies(trimmed)
        self.assertIn("zipimport_utils.py", missing)
        self.assertIn("tests/test_zipimport_utils.py", missing)

    def test_the_wrapper_copies_pair_a_module_with_its_test(self):
        copies = refresh_scaffold.wrapper_copies()
        self.assertIn("zipimport_utils.py", copies)
        index = copies.index("zipimport_utils.py")
        self.assertEqual(copies[index + 1], "tests/test_zipimport_utils.py")


class TestAddMissingCopies(unittest.TestCase):
    """Verify the creation of the blocks the generator lacks."""

    def test_a_block_is_created_for_a_missing_module(self):
        text = "# a generator without any block\n"
        refreshed, added = refresh_scaffold.add_missing_copies(text)
        self.assertIn("zipimport_utils.py", added)
        self.assertIn("cat > \"$OUTPUT_DIR/zipimport_utils.py\" <<'ZIPIMPORT_UTILS'", refreshed)
        body = (ROOT / "zipimport_utils.py").read_text().rstrip("\n")
        self.assertIn(f"{body}\nZIPIMPORT_UTILS\n", refreshed)

    def test_a_test_is_placed_behind_its_module(self):
        text = (
            "cat > \"$OUTPUT_DIR/zipimport_utils.py\" <<'ZIPIMPORT_UTILS'\n"
            "a body\n"
            "ZIPIMPORT_UTILS\n"
        )
        refreshed, added = refresh_scaffold.add_missing_copies(text)
        self.assertIn("tests/test_zipimport_utils.py", added)
        self.assertLess(
            refreshed.index("cat > \"$OUTPUT_DIR/zipimport_utils.py\""),
            refreshed.index("cat > \"$OUTPUT_DIR/tests/test_zipimport_utils.py\""),
        )

    def test_a_created_block_is_separated_by_one_empty_line(self):
        text = (
            "cat > \"$OUTPUT_DIR/zipimport_utils.py\" <<'ZIPIMPORT_UTILS'\n"
            "a body\n"
            "ZIPIMPORT_UTILS\n"
        )
        refreshed, _ = refresh_scaffold.add_missing_copies(text)
        self.assertIn("ZIPIMPORT_UTILS\n\n# --- tests/test_zipimport_utils.py ---", refreshed)

    def test_a_complete_generator_stays_untouched(self):
        text = (ROOT / "scaffold.sh").read_text()
        refreshed, added = refresh_scaffold.add_missing_copies(text)
        self.assertEqual(added, [])
        self.assertEqual(refreshed, text)


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
