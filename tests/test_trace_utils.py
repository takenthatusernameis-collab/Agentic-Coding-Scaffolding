"""Tests for the trace_utils module."""

import os
import sys
import tempfile
import unittest
from pathlib import Path

import trace_utils

SCRIPT_SOURCE = """def unused():
    return "never"


def used():
    return "used"


used()
"""


def sample_function(first, second):
    """Return the sum of two numbers."""
    total = first + second
    return total


def write_script(directory, source=SCRIPT_SOURCE, name="sample_script.py"):
    """Write *source* into *directory* and return the path of the script."""
    path = Path(directory) / name
    path.write_text(source, encoding="utf-8")
    return path


class TestNewTracer(unittest.TestCase):
    """Verify the creation of tracers."""

    def test_new_tracer_returns_a_trace(self):
        self.assertIsInstance(trace_utils.new_tracer(), trace_utils.Trace)

    def test_new_tracer_counts_by_default(self):
        tracer = trace_utils.new_tracer()
        self.assertEqual(tracer.trace, 0)
        trace_utils.run_traced(sample_function, 1, 2, tracer=tracer)
        self.assertTrue(tracer.counts)

    def test_new_tracer_can_disable_counting(self):
        tracer = trace_utils.new_tracer(count=False)
        trace_utils.run_traced(sample_function, 1, 2, tracer=tracer)
        self.assertEqual(tracer.counts, {})

    def test_new_tracer_can_trace_the_lines(self):
        tracer = trace_utils.new_tracer(trace_lines=True)
        self.assertEqual(tracer.trace, 1)

    def test_new_tracer_records_the_called_functions(self):
        import trace

        tracer = trace_utils.new_tracer(count_funcs=True)
        self.assertIs(tracer.globaltrace.__func__, trace.Trace.globaltrace_countfuncs)

    def test_new_tracer_records_the_callers(self):
        import trace

        tracer = trace_utils.new_tracer(count_callers=True)
        self.assertIs(tracer.globaltrace.__func__, trace.Trace.globaltrace_trackcallers)

    def test_new_tracer_ignores_the_installation_prefixes_by_default(self):
        tracer = trace_utils.new_tracer()
        self.assertIn(sys.prefix, tracer.ignore._dirs)

    def test_new_tracer_accepts_directories_and_modules(self):
        tracer = trace_utils.new_tracer(ignoredirs=["/tmp"], ignoremods=["json"])
        self.assertIn("/tmp", tracer.ignore._dirs)
        self.assertIn("json", tracer.ignore._mods)

    def test_new_tracer_rejects_a_string_of_directories(self):
        with self.assertRaises(TypeError):
            trace_utils.new_tracer(ignoredirs="/tmp")  # type: ignore[arg-type]

    def test_new_tracer_rejects_a_directory_entry_that_is_not_a_string(self):
        with self.assertRaises(TypeError):
            trace_utils.new_tracer(ignoredirs=[1])  # type: ignore[list-item]

    def test_new_tracer_rejects_a_module_entry_that_is_not_a_string(self):
        with self.assertRaises(TypeError):
            trace_utils.new_tracer(ignoremods=[None])  # type: ignore[list-item]

    def test_new_tracer_rejects_a_flag_that_is_not_a_bool(self):
        with self.assertRaises(TypeError):
            trace_utils.new_tracer(count="yes")  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            trace_utils.new_tracer(trace_lines=1)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            trace_utils.new_tracer(count_funcs=None)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            trace_utils.new_tracer(count_callers="no")  # type: ignore[arg-type]

    def test_new_tracer_rejects_a_file_that_is_not_a_string(self):
        with self.assertRaises(TypeError):
            trace_utils.new_tracer(infile=1)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            trace_utils.new_tracer(outfile=1)  # type: ignore[arg-type]


class TestRunTraced(unittest.TestCase):
    """Verify running a callable under a tracer."""

    def test_run_traced_returns_the_result(self):
        value, _ = trace_utils.run_traced(sample_function, 1, 2)
        self.assertEqual(value, 3)

    def test_run_traced_returns_the_coverage_results(self):
        _, results = trace_utils.run_traced(sample_function, 1, 2)
        self.assertIsInstance(results, trace_utils.CoverageResults)

    def test_run_traced_passes_the_keyword_arguments(self):
        value, _ = trace_utils.run_traced(sample_function, first=2, second=5)
        self.assertEqual(value, 7)

    def test_run_traced_records_the_executed_lines(self):
        _, results = trace_utils.run_traced(sample_function, 1, 2)
        counts = trace_utils.counted_lines(results)
        self.assertTrue(counts)
        self.assertTrue(any(name == __file__ for name, _ in counts))

    def test_run_traced_uses_the_given_tracer(self):
        tracer = trace_utils.new_tracer()
        _, results = trace_utils.run_traced(sample_function, 1, 2, tracer=tracer)
        self.assertEqual(
            trace_utils.counted_lines(results),
            trace_utils.counted_lines(tracer.results()),
        )

    def test_run_traced_rejects_a_function_that_is_not_callable(self):
        with self.assertRaises(TypeError):
            trace_utils.run_traced("not callable")  # type: ignore[arg-type]

    def test_run_traced_rejects_a_tracer_that_is_not_a_trace(self):
        with self.assertRaises(TypeError):
            trace_utils.run_traced(sample_function, 1, 2, tracer=object())  # type: ignore[arg-type]


class TestRunScriptTraced(unittest.TestCase):
    """Verify running a script under a tracer."""

    def test_run_script_traced_returns_the_exit_code(self):
        with tempfile.TemporaryDirectory() as directory:
            script = write_script(directory)
            exit_code, results = trace_utils.run_script_traced(script)
        self.assertEqual(exit_code, 0)
        self.assertIsInstance(results, trace_utils.CoverageResults)

    def test_run_script_traced_records_the_lines_of_the_script(self):
        with tempfile.TemporaryDirectory() as directory:
            script = write_script(directory)
            _, results = trace_utils.run_script_traced(script)
        self.assertIn(str(script), trace_utils.line_counts(results))

    def test_run_script_traced_returns_the_exit_code_of_the_script(self):
        with tempfile.TemporaryDirectory() as directory:
            script = write_script(directory, "import sys\nsys.exit(3)\n")
            exit_code, _ = trace_utils.run_script_traced(script)
        self.assertEqual(exit_code, 3)

    def test_run_script_traced_treats_a_missing_exit_code_as_success(self):
        with tempfile.TemporaryDirectory() as directory:
            script = write_script(directory, "import sys\nsys.exit()\n")
            exit_code, _ = trace_utils.run_script_traced(script)
        self.assertEqual(exit_code, 0)

    def test_run_script_traced_coerces_a_bool_exit_code_to_int(self):
        # ``sys.exit(True)``/``sys.exit(False)`` are documented to exit with the
        # integer status 1/0; the helper must report an ``int`` rather than the
        # ``bool`` it was handed.
        with tempfile.TemporaryDirectory() as directory:
            script = write_script(directory, "import sys\nsys.exit(True)\n")
            exit_code, _ = trace_utils.run_script_traced(script)
        self.assertEqual(exit_code, 1)
        self.assertIs(type(exit_code), int)
        with tempfile.TemporaryDirectory() as directory:
            script = write_script(directory, "import sys\nsys.exit(False)\n")
            exit_code, _ = trace_utils.run_script_traced(script)
        self.assertEqual(exit_code, 0)
        self.assertIs(type(exit_code), int)

    def test_run_script_traced_reports_a_message_exit_code(self):
        with tempfile.TemporaryDirectory() as directory:
            script = write_script(directory, "import sys\nsys.exit('bye')\n")
            with tempfile.TemporaryDirectory() as errors:
                stderr = sys.stderr
                with open(os.path.join(errors, "err.txt"), "w", encoding="utf-8") as handle:
                    sys.stderr = handle
                    try:
                        exit_code, _ = trace_utils.run_script_traced(script)
                    finally:
                        sys.stderr = stderr
                with open(os.path.join(errors, "err.txt"), encoding="utf-8") as handle:
                    captured = handle.read()
        self.assertEqual(exit_code, 1)
        self.assertIn("bye", captured)

    def test_run_script_traced_ignores_a_directory(self):
        with tempfile.TemporaryDirectory() as directory:
            script = write_script(directory)
            tracer = trace_utils.new_tracer(ignoredirs=[directory])
            _, results = trace_utils.run_script_traced(script, tracer=tracer)
        self.assertNotIn(str(script), trace_utils.line_counts(results))

    def test_run_script_traced_rejects_a_missing_script(self):
        with self.assertRaises(FileNotFoundError):
            trace_utils.run_script_traced("/definitely/not/a/script.py")

    def test_run_script_traced_rejects_a_path_that_is_not_a_path(self):
        with self.assertRaises(TypeError):
            trace_utils.run_script_traced(42)  # type: ignore[arg-type]

    def test_run_script_traced_rejects_a_tracer_that_is_not_a_trace(self):
        with tempfile.TemporaryDirectory() as directory:
            script = write_script(directory)
            with self.assertRaises(TypeError):
                trace_utils.run_script_traced(script, tracer=object())  # type: ignore[arg-type]


class TestCountedLines(unittest.TestCase):
    """Verify the access to the recorded line counts."""

    def setUp(self):
        _, self.results = trace_utils.run_traced(sample_function, 1, 2)

    def test_counted_lines_maps_lines_to_counts(self):
        counts = trace_utils.counted_lines(self.results)
        self.assertTrue(all(isinstance(name, str) for name, _ in counts))
        self.assertTrue(all(isinstance(number, int) for _, number in counts))
        self.assertTrue(all(count > 0 for count in counts.values()))

    def test_counted_lines_of_an_empty_result_is_empty(self):
        self.assertEqual(trace_utils.counted_lines(trace_utils.CoverageResults()), {})

    def test_counted_lines_rejects_a_result_that_is_not_a_coverage_result(self):
        with self.assertRaises(TypeError):
            trace_utils.counted_lines({})  # type: ignore[arg-type]


class TestLineCounts(unittest.TestCase):
    """Verify the grouping of the recorded line counts."""

    def setUp(self):
        _, self.results = trace_utils.run_traced(sample_function, 1, 2)

    def test_line_counts_groups_the_counts_by_file(self):
        counts = trace_utils.line_counts(self.results)
        self.assertIn(__file__, counts)
        self.assertTrue(all(isinstance(number, int) for number in counts[__file__].values()))

    def test_line_counts_rejects_a_result_that_is_not_a_coverage_result(self):
        with self.assertRaises(TypeError):
            trace_utils.line_counts(None)  # type: ignore[arg-type]


class TestCalledFunctions(unittest.TestCase):
    """Verify the access to the recorded function calls."""

    def test_called_functions_is_empty_without_a_function_counter(self):
        _, results = trace_utils.run_traced(sample_function, 1, 2)
        self.assertEqual(trace_utils.called_functions(results), [])

    def test_called_functions_records_the_called_function(self):
        tracer = trace_utils.new_tracer(count_funcs=True)
        _, results = trace_utils.run_traced(sample_function, 1, 2, tracer=tracer)
        called = trace_utils.called_functions(results)
        self.assertTrue(called)
        self.assertTrue(all(len(entry) == 3 for entry in called))

    def test_called_functions_rejects_a_result_that_is_not_a_coverage_result(self):
        with self.assertRaises(TypeError):
            trace_utils.called_functions("results")  # type: ignore[arg-type]


class TestCallRelationships(unittest.TestCase):
    """Verify the access to the recorded calling relationships."""

    def test_call_relationships_is_empty_without_a_caller_counter(self):
        _, results = trace_utils.run_traced(sample_function, 1, 2)
        self.assertEqual(trace_utils.call_relationships(results), [])

    def test_call_relationships_records_the_caller(self):
        tracer = trace_utils.new_tracer(count_callers=True)
        _, results = trace_utils.run_traced(sample_function, 1, 2, tracer=tracer)
        relationships = trace_utils.call_relationships(results)
        self.assertTrue(relationships)
        self.assertTrue(
            all(len(caller) == 3 and len(callee) == 3 for caller, callee in relationships)
        )

    def test_call_relationships_rejects_a_result_that_is_not_a_coverage_result(self):
        with self.assertRaises(TypeError):
            trace_utils.call_relationships(None)  # type: ignore[arg-type]


class TestIsIgnoredFilename(unittest.TestCase):
    """Verify the detection of the files that are not reported."""

    def setUp(self):
        self.results = trace_utils.CoverageResults()

    def test_is_ignored_filename_is_true_for_a_virtual_file(self):
        self.assertTrue(trace_utils.is_ignored_filename(self.results, "<string>"))

    def test_is_ignored_filename_is_false_for_a_real_file(self):
        self.assertFalse(trace_utils.is_ignored_filename(self.results, __file__))

    def test_is_ignored_filename_rejects_a_filename_that_is_not_a_string(self):
        with self.assertRaises(TypeError):
            trace_utils.is_ignored_filename(self.results, None)  # type: ignore[arg-type]

    def test_is_ignored_filename_rejects_a_result_that_is_not_a_coverage_result(self):
        with self.assertRaises(TypeError):
            trace_utils.is_ignored_filename(object(), "file.py")  # type: ignore[arg-type]


class TestMergeResults(unittest.TestCase):
    """Verify the merging of coverage results."""

    def test_merge_results_adds_the_counts(self):
        _, first = trace_utils.run_traced(sample_function, 1, 2)
        _, second = trace_utils.run_traced(sample_function, 3, 4)
        merged = trace_utils.merge_results(first, second)
        counts = trace_utils.counted_lines(merged)
        self.assertTrue(all(count >= 2 for count in counts.values()))

    def test_merge_results_returns_the_merged_results(self):
        _, first = trace_utils.run_traced(sample_function, 1, 2)
        _, second = trace_utils.run_traced(sample_function, 3, 4)
        self.assertIs(trace_utils.merge_results(first, second), first)

    def test_merge_results_rejects_a_result_that_is_not_a_coverage_result(self):
        results = trace_utils.CoverageResults()
        with self.assertRaises(TypeError):
            trace_utils.merge_results(results, {})  # type: ignore[arg-type]

    def test_merge_results_rejects_an_other_result_that_is_not_a_coverage_result(self):
        results = trace_utils.CoverageResults()
        with self.assertRaises(TypeError):
            trace_utils.merge_results(results, None)  # type: ignore[arg-type]


class TestWriteCoverageReport(unittest.TestCase):
    """Verify the writing of the coverage report."""

    def test_write_coverage_report_writes_a_cover_file(self):
        with tempfile.TemporaryDirectory() as directory:
            script = write_script(directory)
            _, results = trace_utils.run_script_traced(script)
            coverdir = Path(directory) / "cover"
            trace_utils.write_coverage_report(results, coverdir=str(coverdir))
            written = sorted(path.name for path in coverdir.iterdir())
        self.assertTrue(any(name.endswith(".cover") for name in written))

    def test_write_coverage_report_rejects_a_coverdir_that_is_not_a_string(self):
        results = trace_utils.CoverageResults()
        with self.assertRaises(TypeError):
            trace_utils.write_coverage_report(results, coverdir=1)  # type: ignore[arg-type]

    def test_write_coverage_report_rejects_a_flag_that_is_not_a_bool(self):
        results = trace_utils.CoverageResults()
        with self.assertRaises(TypeError):
            trace_utils.write_coverage_report(results, show_missing="yes")  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            trace_utils.write_coverage_report(results, summary=1)  # type: ignore[arg-type]

    def test_write_coverage_report_rejects_a_result_that_is_not_a_coverage_result(self):
        with self.assertRaises(TypeError):
            trace_utils.write_coverage_report(object())  # type: ignore[arg-type]


class TestSummarizeCoverage(unittest.TestCase):
    """Verify the coverage summary of a run."""

    def test_summarize_coverage_returns_one_entry_per_file(self):
        _, results = trace_utils.run_traced(sample_function, 1, 2)
        summaries = trace_utils.summarize_coverage(results)
        self.assertTrue(summaries)
        entry = summaries[0]
        self.assertEqual(
            set(entry),
            {"file", "lines", "covered", "missing", "hits", "percent"},
        )

    def test_summarize_coverage_reports_the_uncovered_lines(self):
        with tempfile.TemporaryDirectory() as directory:
            script = write_script(directory)
            _, results = trace_utils.run_script_traced(script)
            summaries = trace_utils.summarize_coverage(results)
        entry = next(item for item in summaries if item["file"] == str(script))
        self.assertEqual(entry["covered"] + entry["missing"], entry["lines"])
        self.assertGreaterEqual(entry["missing"], 1)
        self.assertLess(entry["percent"], 100.0)
        self.assertEqual(entry["percent"], round(100.0 * entry["covered"] / entry["lines"], 1))

    def test_summarize_coverage_skips_the_ignored_files(self):
        results = trace_utils.CoverageResults(counts={("<string>", 1): 1})
        self.assertEqual(trace_utils.summarize_coverage(results), [])

    def test_summarize_coverage_rejects_a_result_that_is_not_a_coverage_result(self):
        with self.assertRaises(TypeError):
            trace_utils.summarize_coverage(None)  # type: ignore[arg-type]


class TestFormatCoverageSummary(unittest.TestCase):
    """Verify the rendering of a coverage summary."""

    def test_format_coverage_summary_renders_a_table(self):
        table = trace_utils.format_coverage_summary(
            [
                {
                    "file": "sample.py",
                    "lines": 10,
                    "covered": 8,
                    "missing": 2,
                    "hits": 12,
                    "percent": 80.0,
                }
            ]
        )
        self.assertIn("file", table)
        self.assertIn("sample.py", table)
        self.assertIn("80.0%", table)

    def test_format_coverage_summary_renders_the_header_without_entries(self):
        table = trace_utils.format_coverage_summary([])
        self.assertIn("cover%", table)

    def test_format_coverage_summary_rejects_a_summaries_that_is_not_a_sequence(self):
        with self.assertRaises(TypeError):
            trace_utils.format_coverage_summary("summary")  # type: ignore[arg-type]

    def test_format_coverage_summary_rejects_an_entry_that_is_not_a_mapping(self):
        with self.assertRaises(TypeError):
            trace_utils.format_coverage_summary(["summary"])  # type: ignore[list-item]


class TestClearCounts(unittest.TestCase):
    """Verify the discarding of the recorded counts."""

    def test_clear_counts_empties_the_counts(self):
        tracer = trace_utils.new_tracer()
        trace_utils.run_traced(sample_function, 1, 2, tracer=tracer)
        self.assertTrue(tracer.counts)
        trace_utils.clear_counts(tracer)
        self.assertEqual(tracer.counts, {})

    def test_clear_counts_rejects_a_tracer_that_is_not_a_trace(self):
        with self.assertRaises(TypeError):
            trace_utils.clear_counts(object())  # type: ignore[arg-type]


class TestExports(unittest.TestCase):
    """Verify the re-exported standard library names."""

    def test_trace_is_the_standard_library_class(self):
        import trace

        self.assertIs(trace_utils.Trace, trace.Trace)

    def test_coverage_results_is_the_standard_library_class(self):
        import trace

        self.assertIs(trace_utils.CoverageResults, trace.CoverageResults)

    def test_pragma_nocover_is_exported(self):
        self.assertIsInstance(trace_utils.PRAGMA_NOCOVER, str)


class TestValidationHelpers(unittest.TestCase):
    """Verify the internal validation helper functions."""

    def test_require_bool_raises_on_non_bool(self):
        from trace_utils import _require_bool

        with self.assertRaises(TypeError):
            _require_bool("yes", "flag")
        with self.assertRaises(TypeError):
            _require_bool(1, "flag")
        with self.assertRaises(TypeError):
            _require_bool(None, "flag")

    def test_require_bool_returns_bool(self):
        from trace_utils import _require_bool

        self.assertTrue(_require_bool(True, "flag"))
        self.assertFalse(_require_bool(False, "flag"))

    def test_require_text_raises_on_non_string(self):
        from trace_utils import _require_text

        with self.assertRaises(TypeError):
            _require_text(123, "name")
        with self.assertRaises(TypeError):
            _require_text(None, "name")

    def test_require_text_returns_string(self):
        from trace_utils import _require_text

        self.assertEqual(_require_text("hello", "name"), "hello")

    def test_require_path_raises_on_invalid_type(self):
        from trace_utils import _require_path

        with self.assertRaises(TypeError):
            _require_path(123, "path")
        with self.assertRaises(TypeError):
            _require_path(None, "path")

    def test_require_path_returns_path_for_path(self):
        from trace_utils import _require_path
        from pathlib import Path

        p = Path("/tmp")
        self.assertIs(_require_path(p, "path"), p)

    def test_require_path_returns_path_for_string(self):
        from trace_utils import _require_path
        from pathlib import Path

        result = _require_path("/tmp", "path")
        self.assertIsInstance(result, Path)
        self.assertEqual(result, Path("/tmp"))

    def test_require_path_returns_path_for_pathlike(self):
        from trace_utils import _require_path
        from pathlib import Path
        import os

        class PathLike:
            def __fspath__(self):
                return "/tmp/pathlike"

        result = _require_path(PathLike(), "path")
        self.assertIsInstance(result, Path)
        self.assertEqual(result, Path("/tmp/pathlike"))

    def test_require_text_sequence_raises_on_invalid(self):
        from trace_utils import _require_text_sequence

        with self.assertRaises(TypeError):
            _require_text_sequence("not a sequence", "name")
        with self.assertRaises(TypeError):
            _require_text_sequence([1], "name")
        with self.assertRaises(TypeError):
            _require_text_sequence(b"bytes", "name")

    def test_require_text_sequence_returns_list(self):
        from trace_utils import _require_text_sequence

        result = _require_text_sequence(["a", "b"], "name")
        self.assertEqual(result, ["a", "b"])
        result = _require_text_sequence(("a", "b"), "name")
        self.assertEqual(result, ["a", "b"])
        result = _require_text_sequence({"a", "b"}, "name")
        self.assertEqual(set(result), {"a", "b"})
        result = _require_text_sequence(frozenset(["a", "b"]), "name")
        self.assertEqual(set(result), {"a", "b"})

    def test_require_results_raises_on_invalid(self):
        from trace_utils import _require_results

        with self.assertRaises(TypeError):
            _require_results({}, "results")
        with self.assertRaises(TypeError):
            _require_results(None, "results")

    def test_require_results_returns_results(self):
        from trace_utils import _require_results, CoverageResults

        results = CoverageResults()
        self.assertIs(_require_results(results, "results"), results)

    def test_require_tracer_raises_on_invalid(self):
        from trace_utils import _require_tracer

        with self.assertRaises(TypeError):
            _require_tracer(object(), "tracer")
        with self.assertRaises(TypeError):
            _require_tracer(None, "tracer")

    def test_require_tracer_returns_tracer(self):
        from trace_utils import _require_tracer, Trace

        tracer = Trace()
        self.assertIs(_require_tracer(tracer, "tracer"), tracer)


class TestExecutableLines(unittest.TestCase):
    """Verify the _executable_lines helper function."""

    def test_executable_lines_returns_none_for_pyc_file(self):
        from trace_utils import _executable_lines

        result = _executable_lines(__file__ + "c")
        self.assertIsNone(result)

    def test_executable_lines_returns_none_for_missing_file(self):
        from trace_utils import _executable_lines

        result = _executable_lines("/definitely/not/a/file.py")
        self.assertIsNone(result)

    def test_executable_lines_returns_none_for_syntax_error(self):
        import tempfile
        from trace_utils import _executable_lines

        with tempfile.NamedTemporaryFile(suffix=".py", delete=False) as f:
            f.write(b"def invalid syntax:")
            path = f.name
        try:
            result = _executable_lines(path)
            self.assertIsNone(result)
        finally:
            os.unlink(path)

    def test_executable_lines_returns_lines_for_valid_file(self):
        from trace_utils import _executable_lines

        result = _executable_lines(__file__)
        self.assertIsInstance(result, set)
        self.assertTrue(len(result) > 0)


class TestRunScriptTracedEdgeCases(unittest.TestCase):
    """Verify edge cases in run_script_traced."""

    def test_run_script_traced_non_int_system_exit(self):
        with tempfile.TemporaryDirectory() as directory:
            script = Path(directory) / "exit_str.py"
            script.write_text("import sys\nsys.exit('message')\n", encoding="utf-8")
            exit_code, _ = trace_utils.run_script_traced(script)
            self.assertEqual(exit_code, 1)

    def test_run_script_traced_invalid_file_type_raises(self):
        with self.assertRaises(TypeError):
            trace_utils.run_script_traced(123)

    def test_run_script_traced_nonexistent_file_raises(self):
        with self.assertRaises(FileNotFoundError):
            trace_utils.run_script_traced(Path("/nonexistent/script.py"))


class TestCountedLinesEdgeCases(unittest.TestCase):
    """Verify edge cases in counted_lines."""

    def test_counted_lines_empty_results(self):
        self.assertEqual(trace_utils.counted_lines(trace_utils.CoverageResults()), {})

    def test_counted_lines_rejects_invalid(self):
        with self.assertRaises(TypeError):
            trace_utils.counted_lines({})


class TestLineCountsEdgeCases(unittest.TestCase):
    """Verify edge cases in line_counts."""

    def test_line_counts_rejects_invalid(self):
        with self.assertRaises(TypeError):
            trace_utils.line_counts(None)


class TestCallRelationshipsEdgeCases(unittest.TestCase):
    """Verify edge cases in call_relationships."""

    def test_call_relationships_rejects_invalid(self):
        with self.assertRaises(TypeError):
            trace_utils.call_relationships(None)


class TestIsIgnoredFilenameEdgeCases(unittest.TestCase):
    """Verify edge cases in is_ignored_filename."""

    def test_is_ignored_filename_rejects_non_string(self):
        with self.assertRaises(TypeError):
            trace_utils.is_ignored_filename(trace_utils.CoverageResults(), None)

    def test_is_ignored_filename_rejects_invalid_results(self):
        with self.assertRaises(TypeError):
            trace_utils.is_ignored_filename(object(), "file.py")


class TestMergeResultsEdgeCases(unittest.TestCase):
    """Verify edge cases in merge_results."""

    def test_merge_results_rejects_invalid_first(self):
        results = trace_utils.CoverageResults()
        with self.assertRaises(TypeError):
            trace_utils.merge_results({}, results)

    def test_merge_results_rejects_invalid_second(self):
        results = trace_utils.CoverageResults()
        with self.assertRaises(TypeError):
            trace_utils.merge_results(results, {})


class TestWriteCoverageReportEdgeCases(unittest.TestCase):
    """Verify edge cases in write_coverage_report."""

    def test_write_coverage_report_rejects_invalid_coverdir(self):
        results = trace_utils.CoverageResults()
        with self.assertRaises(TypeError):
            trace_utils.write_coverage_report(results, coverdir=1)

    def test_write_coverage_report_rejects_invalid_show_missing(self):
        results = trace_utils.CoverageResults()
        with self.assertRaises(TypeError):
            trace_utils.write_coverage_report(results, show_missing="yes")

    def test_write_coverage_report_rejects_invalid_summary(self):
        results = trace_utils.CoverageResults()
        with self.assertRaises(TypeError):
            trace_utils.write_coverage_report(results, summary=1)

    def test_write_coverage_report_rejects_invalid_results(self):
        with self.assertRaises(TypeError):
            trace_utils.write_coverage_report(object())


class TestSummarizeCoverageEdgeCases(unittest.TestCase):
    """Verify edge cases in summarize_coverage."""

    def test_summarize_coverage_rejects_invalid(self):
        with self.assertRaises(TypeError):
            trace_utils.summarize_coverage(None)

    def test_summarize_coverage_with_executable_lines_none(self):
        from trace_utils import CoverageResults
        results = CoverageResults()
        results.counts = {("nonexistent.py", 1): 1}
        summaries = trace_utils.summarize_coverage(results)
        # When _executable_lines returns None, it falls back to hit lines
        self.assertEqual(len(summaries), 1)
        self.assertEqual(summaries[0]["file"], "nonexistent.py")
        self.assertEqual(summaries[0]["covered"], 1)
        self.assertEqual(summaries[0]["percent"], 100.0)


class TestFormatCoverageSummaryEdgeCases(unittest.TestCase):
    """Verify edge cases in format_coverage_summary."""

    def test_format_coverage_summary_rejects_string(self):
        with self.assertRaises(TypeError):
            trace_utils.format_coverage_summary("not a sequence")

    def test_format_coverage_summary_rejects_non_mapping_entry(self):
        with self.assertRaises(TypeError):
            trace_utils.format_coverage_summary(["not a mapping"])


class TestDefaultIgnoredirs(unittest.TestCase):
    """Verify the _default_ignoredirs helper function."""

    def test_default_ignoredirs_returns_list(self):
        from trace_utils import _default_ignoredirs

        dirs = _default_ignoredirs()
        self.assertIsInstance(dirs, list)
        self.assertTrue(all(isinstance(d, str) for d in dirs))
        self.assertIn(sys.prefix, dirs)


class TestNewTracerEdgeCases(unittest.TestCase):
    """Verify edge cases in new_tracer."""

    def test_new_tracer_with_infile_and_outfile(self):
        tracer = trace_utils.new_tracer(infile="/tmp/in", outfile="/tmp/out")
        self.assertEqual(tracer.infile, "/tmp/in")
        self.assertEqual(tracer.outfile, "/tmp/out")


class TestRunTracedEdgeCases(unittest.TestCase):
    """Verify edge cases in run_traced."""

    def test_run_traced_with_custom_tracer(self):
        tracer = trace_utils.new_tracer(count=False)
        value, results = trace_utils.run_traced(sample_function, 1, 2, tracer=tracer)
        self.assertEqual(value, 3)
        self.assertEqual(results.counts, {})


class TestRunScriptTracedEdgeCases(unittest.TestCase):
    """Verify edge cases in run_script_traced."""

    def test_run_script_traced_non_int_system_exit(self):
        with tempfile.TemporaryDirectory() as directory:
            script = Path(directory) / "exit_str.py"
            script.write_text("import sys\nsys.exit('message')\n", encoding="utf-8")
            exit_code, _ = trace_utils.run_script_traced(script)
            self.assertEqual(exit_code, 1)

    def test_run_script_traced_invalid_file_type_raises(self):
        with self.assertRaises(TypeError):
            trace_utils.run_script_traced(123)

    def test_run_script_traced_nonexistent_file_raises(self):
        with self.assertRaises(FileNotFoundError):
            trace_utils.run_script_traced(Path("/nonexistent/script.py"))

    def test_run_script_traced_with_custom_tracer(self):
        with tempfile.TemporaryDirectory() as directory:
            script = write_script(directory)
            tracer = trace_utils.new_tracer(count=False)
            exit_code, results = trace_utils.run_script_traced(script, tracer=tracer)
            self.assertEqual(exit_code, 0)
            self.assertEqual(results.counts, {})


if __name__ == "__main__":
    unittest.main()
