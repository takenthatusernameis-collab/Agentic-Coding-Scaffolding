"""Tests for the exported-but-untested callable scanner."""

import ast
import importlib.util
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TOOL = ROOT / "tools" / "scan_untested.py"

#: Every subprocess in this module runs with ``KILO_SCAN_UNTESTED_CACHE`` set to
#: a throwaway file, and the in-process module global is repointed at the same
#: file. Deleting the real ``.kilo/scan_untested_cache.json`` here (the previous
#: behaviour) forced every later test and the verification battery to re-parse all
#: 500+ modules, which dominated the suite's runtime.
_CACHE_TMPDIR = tempfile.TemporaryDirectory()
CACHE_FILE = Path(_CACHE_TMPDIR.name) / "scan_untested_cache.json"


def load_tool():
    """Return the scanner module loaded from its file path."""
    spec = importlib.util.spec_from_file_location("scan_untested", TOOL)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


scan_untested = load_tool()
scan_untested.CACHE_FILE = CACHE_FILE
os.environ[scan_untested.CACHE_ENV] = str(CACHE_FILE)


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

    def test_a_concatenated_export_list_keeps_the_static_names(self):
        """A ``__all__`` built with ``literal + dynamic`` still yields the
        static names instead of being silently skipped.

        ``resource_utils`` builds ``__all__`` this way
        (``[...] + sorted(_LIMITS)``), so without this handling the scanner
        would report an empty set for it and skip the module entirely.
        """
        source = '__all__ = ["alpha", "beta"] + sorted(_NAMES)'
        tree = ast.parse(source)
        self.assertEqual(scan_untested.exported_names(tree), {"alpha", "beta"})

    def test_a_concatenated_export_list_with_two_literals(self):
        source = "__all__ = ['alpha', 'beta'] + ['gamma']"
        tree = ast.parse(source)
        self.assertEqual(scan_untested.exported_names(tree), {"alpha", "beta", "gamma"})

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


class TestShowAll(unittest.TestCase):
    """Verify that ``--all`` widens the report instead of being a silent no-op.

    ``scan_module`` used to accept ``show_all`` and ignore it, so ``--all``
    produced the same empty report as the default. The flag is documented to
    list type variables, constants, classes, entry points, and interactive
    facades too, so it must actually widen the report.
    """

    def _module(self, source: str) -> Path:
        """Write *source* to a temporary module and return its path."""
        handle = tempfile.NamedTemporaryFile(
            "w", suffix=".py", delete=False, encoding="utf-8"
        )
        self.addCleanup(lambda: Path(handle.name).unlink(missing_ok=True))
        with handle:
            handle.write(source)
        return Path(handle.name)

    def test_default_reports_only_genuine_gaps(self):
        path = self._module(
            "from typing import TypeVar\n"
            "__all__ = ['alpha', 'K', 'main', 'Foo']\n"
            "T = TypeVar('T')\n"
            "K = 1\n"
            "def alpha():\n"
            "    return 1\n"
            "def main():\n"
            "    return 2\n"
            "class Foo:\n"
            "    pass\n"
        )
        self.assertEqual(scan_untested.scan_module(path, False), ["alpha"])

    def test_all_includes_filtered_names(self):
        path = self._module(
            "from typing import TypeVar\n"
            "__all__ = ['alpha', 'K', 'main', 'Foo']\n"
            "T = TypeVar('T')\n"
            "K = 1\n"
            "def alpha():\n"
            "    return 1\n"
            "def main():\n"
            "    return 2\n"
            "class Foo:\n"
            "    pass\n"
        )
        self.assertEqual(
            scan_untested.scan_module(path, True), ["Foo", "K", "alpha", "main"]
        )


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

    def test_the_default_report_is_empty(self):
        result = subprocess.run(
            [sys.executable, str(TOOL)],
            capture_output=True,
            text=True,
            timeout=120,
            check=False,
        )
        self.assertEqual(result.stdout.strip(), "no exported-but-untested callables")

    def test_the_all_flag_lists_everything(self):
        result = subprocess.run(
            [sys.executable, str(TOOL), "--all"],
            capture_output=True,
            text=True,
            timeout=120,
            check=False,
        )
        # With --all the scanner lists type variables, constants, classes, and
        # interactive facades too, so it must report them and exit non-zero.
        # The old implementation ignored the flag and printed the same "no ..."
        # message as the default, which this asserts against.
        self.assertNotEqual(result.returncode, 0, msg=result.stdout + result.stderr)
        self.assertNotIn("no exported-but-untested callables", result.stdout)
        self.assertIn("exported-but-untested callables", result.stdout)
        # ``code_utils`` exports the interactive ``interact`` facade, which the
        # default filters out but ``--all`` must surface.
        self.assertIn("interact", result.stdout)


class TestJSONOutput(unittest.TestCase):
    """Verify the JSON output format."""

    def test_json_output_when_clean(self):
        result = subprocess.run(
            [sys.executable, str(TOOL), "--json"],
            capture_output=True,
            text=True,
            timeout=120,
            check=False,
        )
        self.assertEqual(result.returncode, 0, msg=result.stdout + result.stderr)
        data = json.loads(result.stdout)
        self.assertEqual(data["total"], 0)
        self.assertEqual(data["gaps"], {})

    def test_json_output_with_all_flag(self):
        result = subprocess.run(
            [sys.executable, str(TOOL), "--all", "--json"],
            capture_output=True,
            text=True,
            timeout=120,
            check=False,
        )
        self.assertNotEqual(result.returncode, 0, msg=result.stdout + result.stderr)
        data = json.loads(result.stdout)
        self.assertEqual(data["total"], 262)
        self.assertIn("interact", data["gaps"].get("code_utils.py", []))
        self.assertIn("help", data["gaps"].get("pydoc_utils.py", []))

    def test_json_structure_is_valid(self):
        result = subprocess.run(
            [sys.executable, str(TOOL), "--json"],
            capture_output=True,
            text=True,
            timeout=120,
            check=False,
        )
        data = json.loads(result.stdout)
        self.assertIn("gaps", data)
        self.assertIn("total", data)
        self.assertIsInstance(data["gaps"], dict)
        self.assertIsInstance(data["total"], int)
        for module, names in data["gaps"].items():
            self.assertIsInstance(module, str)
            self.assertIsInstance(names, list)
            for name in names:
                self.assertIsInstance(name, str)


class TestSummaryOutput(unittest.TestCase):
    """Verify the ``--summary`` report format."""

    def test_summary_when_clean(self):
        result = subprocess.run(
            [sys.executable, str(TOOL), "--summary"],
            capture_output=True,
            text=True,
            timeout=120,
            check=False,
        )
        self.assertEqual(result.returncode, 0, msg=result.stdout + result.stderr)
        self.assertEqual(result.stdout.strip(), "no exported-but-untested callables")

    def test_summary_collapses_names_to_counts(self):
        result = subprocess.run(
            [sys.executable, str(TOOL), "--all", "--summary"],
            capture_output=True,
            text=True,
            timeout=120,
            check=False,
        )
        self.assertNotEqual(result.returncode, 0, msg=result.stdout + result.stderr)
        lines = result.stdout.splitlines()
        # Every module line is "name.py: <count>", not a per-name listing.
        module_lines = [line for line in lines if line.endswith(tuple("0123456789"))]
        self.assertGreater(len(module_lines), 0)
        for line in module_lines:
            module_name, _, count = line.partition(": ")
            self.assertTrue(module_name.endswith(".py"))
            self.assertTrue(count.isdigit())
        self.assertRegex(lines[-1], r"^\d+ exported-but-untested callables in \d+ modules$")
        # No per-name bullets leak into the summary.
        self.assertNotIn("  ", result.stdout)

    def test_summary_total_matches_json_total(self):
        summary = subprocess.run(
            [sys.executable, str(TOOL), "--all", "--summary"],
            capture_output=True,
            text=True,
            timeout=120,
            check=False,
        )
        json_run = subprocess.run(
            [sys.executable, str(TOOL), "--all", "--json"],
            capture_output=True,
            text=True,
            timeout=120,
            check=False,
        )
        data = json.loads(json_run.stdout)
        self.assertIn(f"{data['total']} exported-but-untested callables", summary.stdout)
        self.assertIn(f"in {len(data['gaps'])} modules", summary.stdout)

    def test_json_takes_precedence_over_summary(self):
        result = subprocess.run(
            [sys.executable, str(TOOL), "--summary", "--json"],
            capture_output=True,
            text=True,
            timeout=120,
            check=False,
        )
        data = json.loads(result.stdout)
        self.assertEqual(data["total"], 0)
        self.assertEqual(data["gaps"], {})


class TestFormatSummary(unittest.TestCase):
    """Verify the summary formatter as a pure function."""

    def test_clean_results_produce_a_fixed_message(self):
        self.assertEqual(
            scan_untested.format_summary({}, 0),
            "no exported-but-untested callables",
        )

    def test_results_are_one_line_per_module(self):
        summary = scan_untested.format_summary(
            {"a_utils.py": ["x", "y"], "b_utils.py": ["z"]}, 3
        )
        self.assertEqual(
            summary,
            "a_utils.py: 2\nb_utils.py: 1\n\n"
            "3 exported-but-untested callables in 2 modules",
        )


class TestCache(unittest.TestCase):
    """Verify the persistent per-module mtime cache.

    The module-level ``CACHE_FILE`` global is shared state, so every test that
    repoints it must restore the module's isolated cache file afterwards;
    otherwise the mutation leaks into other classes.
    """

    def setUp(self):
        self._saved_cache_file = scan_untested.CACHE_FILE
        self._tmpdir = tempfile.TemporaryDirectory()
        scan_untested.CACHE_FILE = Path(self._tmpdir.name) / "scan_untested_cache.json"

    def tearDown(self):
        scan_untested.CACHE_FILE = self._saved_cache_file
        self._tmpdir.cleanup()

    def test_load_cache_returns_empty_when_missing(self):
        self.assertEqual(scan_untested.load_cache(), {"modules": {}})

    def test_load_cache_returns_empty_when_corrupt(self):
        scan_untested.CACHE_FILE.write_text("not json {")
        self.assertEqual(scan_untested.load_cache(), {"modules": {}})

    def test_load_cache_returns_empty_when_shape_is_wrong(self):
        scan_untested.CACHE_FILE.write_text('["not", "a", "dict"]')
        self.assertEqual(scan_untested.load_cache(), {"modules": {}})

    def test_save_and_load_round_trips(self):
        scan_untested.save_cache(
            {
                "modules": {
                    "a_utils.py": {
                        "source_mtime": 1.0,
                        "test_mtime": 2.0,
                        "gaps_by_mode": {"default": ["foo", "bar"]},
                    }
                }
            }
        )
        self.assertEqual(
            scan_untested.load_cache(),
            {
                "modules": {
                    "a_utils.py": {
                        "source_mtime": 1.0,
                        "test_mtime": 2.0,
                        "gaps_by_mode": {"default": ["foo", "bar"]},
                    }
                }
            },
        )

    def test_cached_entry_returns_none_when_no_entry(self):
        self.assertIsNone(
            scan_untested.cached_entry({"modules": {}}, Path("a_utils.py"), 1.0, 2.0)
        )

    def test_cached_entry_returns_gaps_when_mtimes_match(self):
        cache = {
            "modules": {
                "a_utils.py": {
                    "source_mtime": 1.0,
                    "test_mtime": 2.0,
                    "gaps_by_mode": {"default": ["foo", "bar"]},
                }
            }
        }
        self.assertEqual(
            scan_untested.cached_entry(cache, Path("a_utils.py"), 1.0, 2.0),
            ["foo", "bar"],
        )

    def test_cached_entry_invalidates_when_source_mtime_changes(self):
        cache = {
            "modules": {
                "a_utils.py": {
                    "source_mtime": 1.0,
                    "test_mtime": 2.0,
                    "gaps_by_mode": {"default": ["foo"]},
                }
            }
        }
        self.assertIsNone(scan_untested.cached_entry(cache, Path("a_utils.py"), 9.0, 2.0))

    def test_cached_entry_invalidates_when_test_mtime_changes(self):
        cache = {
            "modules": {
                "a_utils.py": {
                    "source_mtime": 1.0,
                    "test_mtime": 2.0,
                    "gaps_by_mode": {"default": ["foo"]},
                }
            }
        }
        self.assertIsNone(scan_untested.cached_entry(cache, Path("a_utils.py"), 1.0, 9.0))

    def test_cached_entry_returns_none_for_non_list_gaps(self):
        cache = {
            "modules": {
                "a_utils.py": {
                    "source_mtime": 1.0,
                    "test_mtime": 2.0,
                    "gaps_by_mode": {"default": "not a list"},
                }
            }
        }
        self.assertIsNone(scan_untested.cached_entry(cache, Path("a_utils.py"), 1.0, 2.0))

    def test_cached_entry_supports_all_mode(self):
        cache = {
            "modules": {
                "a_utils.py": {
                    "source_mtime": 1.0,
                    "test_mtime": 2.0,
                    "gaps_by_mode": {"default": ["x"], "all": ["x", "Y"]},
                }
            }
        }
        self.assertEqual(
            scan_untested.cached_entry(cache, Path("a_utils.py"), 1.0, 2.0, True),
            ["x", "Y"],
        )
        self.assertEqual(
            scan_untested.cached_entry(cache, Path("a_utils.py"), 1.0, 2.0, False),
            ["x"],
        )

    def test_cached_entry_reads_legacy_default_gaps(self):
        cache = {
            "modules": {
                "a_utils.py": {
                    "source_mtime": 1.0,
                    "test_mtime": 2.0,
                    "gaps": ["legacy"],
                }
            }
        }
        self.assertEqual(
            scan_untested.cached_entry(cache, Path("a_utils.py"), 1.0, 2.0),
            ["legacy"],
        )
        self.assertIsNone(
            scan_untested.cached_entry(cache, Path("a_utils.py"), 1.0, 2.0, True)
        )

    def test_cache_file_honours_the_environment_override(self):
        # The test suite relocates the cache through this variable so an
        # end-to-end run never deletes the developer's real cache.
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "custom_cache.json"
            saved_env = os.environ.get(scan_untested.CACHE_ENV)
            os.environ[scan_untested.CACHE_ENV] = str(target)
            try:
                module = load_tool()
            finally:
                if saved_env is None:
                    os.environ.pop(scan_untested.CACHE_ENV, None)
                else:
                    os.environ[scan_untested.CACHE_ENV] = saved_env
            self.assertEqual(module.CACHE_FILE, target)


class TestCacheIntegration(unittest.TestCase):
    """Verify the cache behaves end-to-end across subprocess runs.

    The module-wide isolated cache is emptied once, here, so the two
    population assertions observe a genuine cold scan. Everything the later
    classes run is then served from that cache instead of re-parsing every
    module again.
    """

    @classmethod
    def setUpClass(cls):
        CACHE_FILE.unlink(missing_ok=True)

    def test_repeated_runs_produce_identical_output_and_populate_cache(self):
        first = subprocess.run(
            [sys.executable, str(TOOL)],
            capture_output=True,
            text=True,
            timeout=120,
            check=False,
        )
        second = subprocess.run(
            [sys.executable, str(TOOL)],
            capture_output=True,
            text=True,
            timeout=120,
            check=False,
        )
        self.assertEqual(first.returncode, 0, msg=first.stderr)
        self.assertEqual(second.returncode, 0, msg=second.stderr)
        self.assertEqual(first.stdout, second.stdout)
        self.assertTrue(CACHE_FILE.is_file(), "cache file should be written")
        data = json.loads(CACHE_FILE.read_text())
        self.assertIn("modules", data)
        self.assertIsInstance(data["modules"], dict)
        entry = next(iter(data["modules"].values()))
        self.assertIn("gaps_by_mode", entry)

    def test_all_mode_is_cached_per_mode(self):
        first = subprocess.run(
            [sys.executable, str(TOOL), "--all", "--json"],
            capture_output=True,
            text=True,
            timeout=120,
            check=False,
        )
        second = subprocess.run(
            [sys.executable, str(TOOL), "--all", "--json"],
            capture_output=True,
            text=True,
            timeout=120,
            check=False,
        )
        self.assertEqual(first.returncode, 1, msg=first.stderr)
        self.assertEqual(second.returncode, 1, msg=second.stderr)
        self.assertEqual(first.stdout, second.stdout)
        data = json.loads(CACHE_FILE.read_text())
        entry = next(iter(data["modules"].values()))
        self.assertIn("all", entry.get("gaps_by_mode", {}))


if __name__ == "__main__":
    unittest.main()
