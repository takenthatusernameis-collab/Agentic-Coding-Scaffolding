"""Tests for select_tests module."""

import importlib.util
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parent.parent
TOOL = ROOT / "tools" / "select_tests.py"


def load_tool():
    """Return the select-tests module loaded from its file path."""
    spec = importlib.util.spec_from_file_location("select_tests", TOOL)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

select_tests = load_tool()


class TestGetChangedAndUntrackedFromGit(unittest.TestCase):
    """Test the internal helper that parses git status output."""

    def test_no_changes_returns_empty_lists(self):
        with mock.patch.object(select_tests, "run_git") as mock_run:
            mock_run.return_value = subprocess.CompletedProcess(
                ["git", "status"], 0, "", ""
            )
            changed, untracked = select_tests._get_changed_and_untracked_from_git()
            self.assertEqual(changed, [])
            self.assertEqual(untracked, [])

    def test_changed_files_are_parsed(self):
        output = " M foo_utils.py\n M bar_utils.py\n"
        with mock.patch.object(select_tests, "run_git") as mock_run:
            mock_run.return_value = subprocess.CompletedProcess(
                ["git", "status"], 0, output, ""
            )
            changed, untracked = select_tests._get_changed_and_untracked_from_git()
            self.assertEqual(changed, ["foo_utils.py", "bar_utils.py"])
            self.assertEqual(untracked, [])

    def test_untracked_files_are_parsed_when_enabled(self):
        output = "?? new_utils.py\n M existing_utils.py\n"
        with mock.patch.object(select_tests, "run_git") as mock_run:
            mock_run.return_value = subprocess.CompletedProcess(
                ["git", "status"], 0, output, ""
            )
            changed, untracked = select_tests._get_changed_and_untracked_from_git(
                include_untracked=True
            )
            self.assertEqual(changed, ["existing_utils.py"])
            self.assertEqual(untracked, ["new_utils.py"])

    def test_untracked_files_are_ignored_when_disabled(self):
        output = "?? new_utils.py\n M existing_utils.py\n"
        with mock.patch.object(select_tests, "run_git") as mock_run:
            mock_run.return_value = subprocess.CompletedProcess(
                ["git", "status"], 0, output, ""
            )
            changed, untracked = select_tests._get_changed_and_untracked_from_git(
                include_untracked=False
            )
            self.assertEqual(changed, ["existing_utils.py"])
            self.assertEqual(untracked, [])

    def test_git_failure_returns_empty_lists(self):
        with mock.patch.object(select_tests, "run_git") as mock_run:
            mock_run.return_value = subprocess.CompletedProcess(
                ["git", "status"], 1, "", "fatal: not a git repo"
            )
            changed, untracked = select_tests._get_changed_and_untracked_from_git()
            self.assertEqual(changed, [])
            self.assertEqual(untracked, [])

    def test_base_and_head_args_are_passed(self):
        with mock.patch.object(select_tests, "run_git") as mock_run:
            mock_run.return_value = subprocess.CompletedProcess(
                ["git", "diff"], 0, "", ""
            )
            select_tests._get_changed_and_untracked_from_git(base="HEAD~1", head="HEAD")
            args = mock_run.call_args_list[0][0][0]
            self.assertIn("HEAD~1", args)
            self.assertIn("HEAD", args)

    def test_base_uses_git_diff_not_status(self):
        """A committed range must be resolved with ``git diff``.

        ``git status`` cannot diff two commits; a bare ref before ``--`` is a
        pathspec, so the old ``git status --porcelain <base> <head>`` form always
        reported an empty delta. This asserts the base path issues ``git diff``.
        """
        with mock.patch.object(select_tests, "run_git") as mock_run:
            mock_run.return_value = subprocess.CompletedProcess(
                ["git", "diff"], 0, "foo_utils.py\n", ""
            )
            changed, untracked = select_tests._get_changed_and_untracked_from_git(
                base="HEAD~1", head="HEAD"
            )
            args = mock_run.call_args_list[0][0][0]
            self.assertEqual(args[:4], ["git", "diff", "--name-only", "HEAD~1"])
            self.assertEqual(changed, ["foo_utils.py"])
            self.assertEqual(untracked, [])

    def test_source_globs_are_passed_as_pathspecs(self):
        with mock.patch.object(select_tests, "run_git") as mock_run:
            mock_run.return_value = subprocess.CompletedProcess(
                ["git", "status"], 0, "", ""
            )
            select_tests._get_changed_and_untracked_from_git()
            args = mock_run.call_args[0][0]
            for glob in select_tests.SOURCE_GLOBS:
                self.assertIn(glob, args)


class TestGetChangedFilesFromGit(unittest.TestCase):
    """Test the public wrapper for changed files only."""

    def test_delegates_to_internal_helper(self):
        with mock.patch.object(
            select_tests, "_get_changed_and_untracked_from_git"
        ) as mock_internal:
            mock_internal.return_value = (["foo.py"], ["bar.py"])
            result = select_tests.get_changed_files_from_git()
            self.assertEqual(result, ["foo.py"])
            mock_internal.assert_called_once_with(None, "HEAD", include_untracked=False)

    def test_passes_base_and_head(self):
        with mock.patch.object(
            select_tests, "_get_changed_and_untracked_from_git"
        ) as mock_internal:
            mock_internal.return_value = ([], [])
            select_tests.get_changed_files_from_git(base="abc", head="def")
            mock_internal.assert_called_once_with("abc", "def", include_untracked=False)


class TestGetUntrackedFiles(unittest.TestCase):
    """Test the public wrapper for untracked files."""

    def test_delegates_to_internal_helper(self):
        with mock.patch.object(
            select_tests, "_get_changed_and_untracked_from_git"
        ) as mock_internal:
            mock_internal.return_value = (["foo.py"], ["bar.py", "baz.py"])
            result = select_tests.get_untracked_files()
            self.assertEqual(result, ["bar.py", "baz.py"])
            mock_internal.assert_called_once_with(base=None, head="HEAD", include_untracked=True)


class TestMapSourceToTest(unittest.TestCase):
    """Test the source-to-test mapping logic."""

    def test_full_suite_triggers_root_files(self):
        for trigger in [
            "Makefile",
            "pyproject.toml",
            "scaffold.sh",
            "README.md",
            "AGENTS.md",
            "CHANGELOG.md",
        ]:
            with self.subTest(trigger=trigger):
                result = select_tests.map_source_to_test(trigger)
                self.assertEqual(result, "FULL_SUITE")

    def test_full_suite_triggers_subdirectory_files(self):
        # Only .kilo/command/*.md files trigger full suite (no direct test mapping)
        for trigger in [".kilo/command/scaffold-project.md"]:
            with self.subTest(trigger=trigger):
                result = select_tests.map_source_to_test(trigger)
                self.assertEqual(result, "FULL_SUITE")

    def test_tools_py_file_with_test(self):
        result = select_tests.map_source_to_test("tools/verify_state_delta.py")
        self.assertEqual(result, "tests.test_verify_state_delta")

    def test_tools_py_file_without_test(self):
        result = select_tests.map_source_to_test("tools/nonexistent_tool.py")
        self.assertEqual(result, "FULL_SUITE")

    def test_root_wrapper_module_with_test(self):
        result = select_tests.map_source_to_test("abc_utils.py")
        self.assertEqual(result, "tests.test_abc_utils")

    def test_root_non_wrapper_module_with_test(self):
        # These non-wrapper modules now have tests
        result = select_tests.map_source_to_test("stats.py")
        self.assertEqual(result, "tests.test_stats")

    def test_test_file_maps_to_its_own_module(self):
        """A changed test file must select its own test module.

        Returning ``None`` here made ``make test`` fall back to the smoke test
        for a test-only edit, so the edited test was silently never exercised
        locally; the module is the best targeted test for its own change.
        """
        result = select_tests.map_source_to_test("tests/test_abc_utils.py")
        self.assertEqual(result, "tests.test_abc_utils")

    def test_non_test_file_in_tests_dir_is_ignored(self):
        # A helper module under tests/ is not itself a test module.
        result = select_tests.map_source_to_test("tests/helpers.py")
        self.assertIsNone(result)

    def test_kilo_command_md(self):
        result = select_tests.map_source_to_test(".kilo/command/scaffold-project.md")
        self.assertEqual(result, "FULL_SUITE")

    def test_other_md_file(self):
        result = select_tests.map_source_to_test("docs/something.md")
        self.assertIsNone(result)

    def test_path_not_under_root(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "outside_utils.py"
            path.write_text("# test")
            result = select_tests.map_source_to_test(str(path))
            self.assertIsNone(result)


class TestSelectTests(unittest.TestCase):
    """Test the test selection logic."""

    def test_empty_list_returns_empty(self):
        modules, run_full = select_tests.select_tests([])
        self.assertEqual(modules, [])
        self.assertFalse(run_full)

    def test_single_wrapper_module(self):
        modules, run_full = select_tests.select_tests(["abc_utils.py"])
        self.assertEqual(modules, ["tests.test_abc_utils"])
        self.assertFalse(run_full)

    def test_multiple_wrapper_modules(self):
        modules, run_full = select_tests.select_tests(["abc_utils.py", "aifc_utils.py"])
        self.assertEqual(sorted(modules), ["tests.test_abc_utils", "tests.test_aifc_utils"])
        self.assertFalse(run_full)

    def test_full_suite_trigger_stops_early(self):
        modules, run_full = select_tests.select_tests(["abc_utils.py", "Makefile"])
        self.assertTrue(run_full)
        self.assertEqual(modules, [])

    def test_full_suite_trigger_first(self):
        modules, run_full = select_tests.select_tests(["Makefile", "abc_utils.py"])
        self.assertTrue(run_full)
        self.assertEqual(modules, [])

    def test_duplicate_modules_deduplicated(self):
        modules, run_full = select_tests.select_tests(["abc_utils.py", "abc_utils.py"])
        self.assertEqual(modules, ["tests.test_abc_utils"])
        self.assertFalse(run_full)

    def test_unknown_file_ignored(self):
        modules, run_full = select_tests.select_tests(["unknown.txt", "abc_utils.py"])
        self.assertEqual(modules, ["tests.test_abc_utils"])
        self.assertFalse(run_full)

    def test_tool_file_with_test(self):
        modules, run_full = select_tests.select_tests(["tools/verify_state_delta.py"])
        self.assertEqual(modules, ["tests.test_verify_state_delta"])
        self.assertFalse(run_full)

    def test_tool_file_without_test_triggers_full_suite(self):
        modules, run_full = select_tests.select_tests(["tools/nonexistent_tool.py"])
        self.assertTrue(run_full)
        self.assertEqual(modules, [])

    def test_changed_test_file_selects_its_own_module(self):
        modules, run_full = select_tests.select_tests(["tests/test_abc_utils.py"])
        self.assertEqual(modules, ["tests.test_abc_utils"])
        self.assertFalse(run_full)

    def test_changed_source_and_test_files_are_both_selected(self):
        modules, run_full = select_tests.select_tests(
            ["abc_utils.py", "tests/test_abc_utils.py"]
        )
        self.assertEqual(modules, ["tests.test_abc_utils"])
        self.assertFalse(run_full)


class TestGetAllTestModules(unittest.TestCase):
    """Test the all-test-modules enumeration."""

    def test_returns_list_of_test_modules(self):
        modules = select_tests.get_all_test_modules()
        self.assertIsInstance(modules, list)
        self.assertTrue(len(modules) > 0)
        for module in modules:
            self.assertTrue(module.startswith("tests.test_"))

    def test_includes_known_test_modules(self):
        modules = select_tests.get_all_test_modules()
        self.assertIn("tests.test_abc_utils", modules)
        self.assertIn("tests.test_stats", modules)


class TestMain(unittest.TestCase):
    """Test the command-line entry point."""

    def setUp(self):
        self._saved_argv = sys.argv

    def tearDown(self):
        sys.argv = self._saved_argv

    def run_main(self, args: list[str]) -> tuple[int, str, str]:
        sys.argv = ["select_tests.py"] + args
        import io
        from contextlib import redirect_stderr, redirect_stdout

        stdout_buf = io.StringIO()
        stderr_buf = io.StringIO()
        with redirect_stdout(stdout_buf), redirect_stderr(stderr_buf):
            try:
                rc = select_tests.main(args)
            except SystemExit as e:
                rc = e.code
        return rc, stdout_buf.getvalue(), stderr_buf.getvalue()

    def test_all_flag_returns_all_modules(self):
        rc, out, err = self.run_main(["--all"])
        self.assertEqual(rc, 0)
        lines = out.strip().splitlines()
        self.assertTrue(len(lines) > 0)
        for line in lines:
            self.assertTrue(line.startswith("tests.test_"))

    def test_all_flag_with_json(self):
        rc, out, err = self.run_main(["--all", "--json"])
        self.assertEqual(rc, 0)
        import json
        data = json.loads(out)
        self.assertIn("modules", data)
        self.assertIn("run_full_suite", data)
        self.assertFalse(data["run_full_suite"])
        self.assertTrue(len(data["modules"]) > 0)

    def test_changed_files_flag(self):
        rc, out, err = self.run_main(["--changed-files", "abc_utils.py", "aifc_utils.py"])
        self.assertEqual(rc, 0)
        lines = out.strip().splitlines()
        self.assertEqual(sorted(lines), ["tests.test_abc_utils", "tests.test_aifc_utils"])

    def test_changed_files_with_json(self):
        rc, out, err = self.run_main(["--changed-files", "abc_utils.py", "--json"])
        self.assertEqual(rc, 0)
        import json
        data = json.loads(out)
        self.assertIn("modules", data)
        self.assertIn("run_full_suite", data)
        self.assertFalse(data["run_full_suite"])
        self.assertEqual(data["modules"], ["tests.test_abc_utils"])

    def test_changed_files_full_suite_trigger(self):
        rc, out, err = self.run_main(["--changed-files", "Makefile"])
        self.assertEqual(rc, 0)
        self.assertEqual(out.strip(), "FULL_SUITE")

    def test_changed_test_file_flag(self):
        rc, out, err = self.run_main(["--changed-files", "tests/test_abc_utils.py"])
        self.assertEqual(rc, 0)
        self.assertEqual(out.strip(), "tests.test_abc_utils")

    def test_help_flag(self):
        rc, out, err = self.run_main(["--help"])
        self.assertEqual(rc, 0)
        self.assertIn("Select relevant tests", out)

    def test_from_git_flag(self):
        with mock.patch.object(
            select_tests, "_get_changed_and_untracked_from_git"
        ) as mock_internal:
            mock_internal.return_value = (["abc_utils.py"], [])
            rc, out, err = self.run_main(["--from-git"])
            self.assertEqual(rc, 0)
            self.assertIn("tests.test_abc_utils", out)


class TestFullSuiteTriggers(unittest.TestCase):
    """Verify that FULL_SUITE_TRIGGERS covers critical files."""

    def test_contains_makefile(self):
        self.assertIn("Makefile", select_tests.FULL_SUITE_TRIGGERS)

    def test_contains_pyproject(self):
        self.assertIn("pyproject.toml", select_tests.FULL_SUITE_TRIGGERS)

    def test_contains_scaffold_sh(self):
        self.assertIn("scaffold.sh", select_tests.FULL_SUITE_TRIGGERS)

    def test_contains_readme(self):
        self.assertIn("README.md", select_tests.FULL_SUITE_TRIGGERS)

    def test_contains_agents_md(self):
        self.assertIn("AGENTS.md", select_tests.FULL_SUITE_TRIGGERS)

    def test_contains_changelog(self):
        self.assertIn("CHANGELOG.md", select_tests.FULL_SUITE_TRIGGERS)

    def test_contains_command_doc(self):
        self.assertIn(".kilo/command/scaffold-project.md", select_tests.FULL_SUITE_TRIGGERS)

    def test_contains_tool_files(self):
        # Tool files are no longer in FULL_SUITE_TRIGGERS since they have test mappings
        self.assertNotIn("tools/verify_state_delta.py", select_tests.FULL_SUITE_TRIGGERS)
        self.assertNotIn("tools/refresh_scaffold.py", select_tests.FULL_SUITE_TRIGGERS)
        self.assertNotIn("tools/scan_untested.py", select_tests.FULL_SUITE_TRIGGERS)
        self.assertNotIn("tools/select_tests.py", select_tests.FULL_SUITE_TRIGGERS)


class TestSourceGlobs(unittest.TestCase):
    """Verify that SOURCE_GLOBS covers the editable surface."""

    def test_contains_py_files(self):
        self.assertIn("*.py", select_tests.SOURCE_GLOBS)

    def test_contains_makefile(self):
        self.assertIn("Makefile", select_tests.SOURCE_GLOBS)

    def test_contains_pyproject(self):
        self.assertIn("pyproject.toml", select_tests.SOURCE_GLOBS)

    def test_contains_scaffold_sh(self):
        self.assertIn("scaffold.sh", select_tests.SOURCE_GLOBS)

    def test_contains_readme(self):
        self.assertIn("README.md", select_tests.SOURCE_GLOBS)

    def test_contains_agents_md(self):
        self.assertIn("AGENTS.md", select_tests.SOURCE_GLOBS)

    def test_contains_changelog(self):
        self.assertIn("CHANGELOG.md", select_tests.SOURCE_GLOBS)

    def test_contains_command_doc(self):
        self.assertIn(".kilo/command/scaffold-project.md", select_tests.SOURCE_GLOBS)

    def test_contains_tools_py(self):
        self.assertIn("tools/*.py", select_tests.SOURCE_GLOBS)


class TestGitRangeRegression(unittest.TestCase):
    """A committed range must be reported via ``git diff``.

    Regression guard for a real bug: ``_get_changed_and_untracked_from_git``
    computed the delta with ``git status --porcelain <base> <head>``. ``git
    status`` does not take a commit range; a bare ref before ``--`` is a
    pathspec, so the command matched nothing and ``--from-git --base`` silently
    reported no changed files even when source files changed between the two
    commits. This builds a throwaway repository with a source file committed in
    a second commit and asserts the base range reports it.
    """

    def setUp(self):
        self._saved_root = select_tests.ROOT
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        repo = Path(self._tmp.name)
        select_tests.ROOT = repo

        def git(*args: str) -> str:
            result = subprocess.run(
                ["git", *args], cwd=repo, capture_output=True, text=True, check=True
            )
            return result.stdout.strip()

        git("init", "-q")
        git("config", "user.email", "test@example.com")
        git("config", "user.name", "test")
        (repo / "main.py").write_text("x = 1\n")
        git("add", ".")
        git("commit", "-qm", "one")
        self._first = git("rev-parse", "HEAD")
        (repo / "main.py").write_text("x = 2\n")
        (repo / "main_utils.py").write_text("y = 1\n")
        git("add", ".")
        git("commit", "-qm", "two")

    def tearDown(self):
        select_tests.ROOT = self._saved_root

    def test_committed_source_change_is_detected_for_base_range(self):
        changed, untracked = select_tests._get_changed_and_untracked_from_git(
            base=self._first, head="HEAD"
        )
        self.assertEqual(untracked, [])
        self.assertIn("main.py", changed)
        self.assertIn("main_utils.py", changed)

    def test_no_change_between_head_and_itself(self):
        changed, untracked = select_tests._get_changed_and_untracked_from_git(
            base="HEAD", head="HEAD"
        )
        self.assertEqual(changed, [])
        self.assertEqual(untracked, [])


if __name__ == "__main__":
    unittest.main()
