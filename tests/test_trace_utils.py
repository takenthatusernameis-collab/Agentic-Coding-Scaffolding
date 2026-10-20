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


if __name__ == "__main__":
    unittest.main()
