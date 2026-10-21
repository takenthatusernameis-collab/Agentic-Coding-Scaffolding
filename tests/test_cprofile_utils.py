"""Tests for cprofile_utils."""

import contextlib
import cProfile as _cProfile
import io
import os
import sys
import tempfile
import unittest
from pathlib import Path
from typing import Any, Dict

import cprofile_utils
from cprofile_utils import (
    Profile,
    collect_stats,
    dump_stats,
    format_report,
    main,
    new_profiler,
    profile_call,
    run,
    runcall,
    runctx,
)


def _work(value: int = 10) -> int:
    """Return the sum of the numbers below *value*."""
    total = 0
    for number in range(value):
        total += number
    return total


def time_perf_counter() -> float:
    """Return the current time in seconds."""
    import time

    return time.perf_counter()


def monotonic_nanoseconds() -> int:
    """Return the current time in nanoseconds."""
    import time

    return time.monotonic_ns()


class TestModuleContract(unittest.TestCase):
    """Verify the contract of the module."""

    def test_all_is_sorted_and_unique(self):
        self.assertEqual(cprofile_utils.__all__, sorted(set(cprofile_utils.__all__)))

    def test_every_name_exists(self):
        for name in cprofile_utils.__all__:
            self.assertTrue(hasattr(cprofile_utils, name), name)

    def test_profile_is_the_standard_library_class(self):
        self.assertIs(Profile, _cProfile.Profile)

    def test_every_public_name_is_documented(self):
        for name in cprofile_utils.__all__:
            member = getattr(cprofile_utils, name)
            self.assertTrue(member.__doc__, name)


class TestNewProfiler(unittest.TestCase):
    """Verify creating a profiler."""

    def test_new_profiler_returns_a_profiler(self):
        self.assertIsInstance(new_profiler(), _cProfile.Profile)

    def test_new_profiler_accepts_the_switches(self):
        profiler = new_profiler(subcalls=False, builtins=False)
        self.assertIsInstance(profiler, _cProfile.Profile)

    def test_new_profiler_accepts_an_integer_timer(self):
        profiler = new_profiler(timer=monotonic_nanoseconds, timeunit=1e-9)
        self.assertIsInstance(profiler, _cProfile.Profile)

    def test_new_profiler_rejects_a_timer_that_is_not_callable(self):
        with self.assertRaises(TypeError):
            new_profiler(timer=42)  # type: ignore[arg-type]

    def test_new_profiler_rejects_a_timer_that_returns_a_float(self):
        with self.assertRaises(TypeError):
            new_profiler(timer=time_perf_counter, timeunit=1e-9)

    def test_new_profiler_rejects_a_timeunit_that_is_not_a_number(self):
        with self.assertRaises(TypeError):
            new_profiler(timeunit="1e-9")  # type: ignore[arg-type]

    def test_new_profiler_rejects_a_timeunit_that_is_not_positive(self):
        with self.assertRaises(ValueError):
            new_profiler(timeunit=0)
        with self.assertRaises(ValueError):
            new_profiler(timeunit=-1.0)

    def test_new_profiler_rejects_switches_that_are_not_booleans(self):
        with self.assertRaises(TypeError):
            new_profiler(subcalls=1)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            new_profiler(builtins=1)  # type: ignore[arg-type]


class TestRun(unittest.TestCase):
    """Verify profiling a single statement."""

    def test_run_prints_a_report(self):
        buffer = io.StringIO()
        with contextlib.redirect_stdout(buffer):
            run("total = sum(range(10))")
        self.assertIn("function calls", buffer.getvalue())

    def test_run_writes_the_statistics_to_a_file(self):
        with tempfile.TemporaryDirectory() as directory:
            path = os.path.join(directory, "stats.prof")
            with contextlib.redirect_stdout(io.StringIO()):
                run("total = sum(range(10))", filename=path)
            self.assertTrue(os.path.getsize(path) > 0)

    def test_run_rejects_a_statement_that_is_not_a_string(self):
        with self.assertRaises(TypeError):
            run(42)  # type: ignore[arg-type]

    def test_run_rejects_a_filename_that_is_not_a_string(self):
        with self.assertRaises(TypeError):
            run("total = 1", filename=42)  # type: ignore[arg-type]

    def test_run_rejects_a_sort_that_is_not_a_key(self):
        with self.assertRaises(TypeError):
            run("total = 1", sort=1.5)  # type: ignore[arg-type]


class TestRunctx(unittest.TestCase):
    """Verify profiling a statement in given namespaces."""

    def test_runctx_runs_the_statement_in_the_namespaces(self):
        namespace: Dict[str, Any] = {}
        with contextlib.redirect_stdout(io.StringIO()):
            runctx("total = sum(range(10))", namespace, namespace)
        self.assertEqual(namespace["total"], 45)

    def test_runctx_writes_the_statistics_to_a_file(self):
        with tempfile.TemporaryDirectory() as directory:
            path = os.path.join(directory, "stats.prof")
            namespace: Dict[str, Any] = {}
            with contextlib.redirect_stdout(io.StringIO()):
                runctx("total = 1", namespace, namespace, filename=path)
            self.assertTrue(os.path.getsize(path) > 0)

    def test_runctx_rejects_a_statement_that_is_not_a_string(self):
        with self.assertRaises(TypeError):
            runctx(42, {}, {})  # type: ignore[arg-type]

    def test_runctx_rejects_globals_that_are_not_a_dict(self):
        with self.assertRaises(TypeError):
            runctx("total = 1", [], {})  # type: ignore[arg-type]

    def test_runctx_rejects_locals_that_are_not_a_mapping(self):
        with self.assertRaises(TypeError):
            runctx("total = 1", {}, 42)  # type: ignore[arg-type]


class TestRuncall(unittest.TestCase):
    """Verify profiling a single call."""

    def test_runcall_returns_the_result_of_the_call(self):
        self.assertEqual(runcall(_work, 10), 45)

    def test_runcall_passes_the_arguments_on(self):
        self.assertEqual(runcall(_work, value=5), 10)

    def test_runcall_rejects_a_function_that_is_not_callable(self):
        with self.assertRaises(TypeError):
            runcall(42)  # type: ignore[arg-type]


class TestProfileCall(unittest.TestCase):
    """Verify profiling a call and reading its statistics."""

    def test_profile_call_returns_the_result_and_the_statistics(self):
        result, stats = profile_call(_work, 10)
        self.assertEqual(result, 45)
        self.assertTrue(stats)

    def test_profile_call_reports_the_profiled_function(self):
        _, stats = profile_call(_work, 10)
        names = [key[2] for key in stats]
        self.assertIn("_work", names)

    def test_profile_call_rejects_a_function_that_is_not_callable(self):
        with self.assertRaises(TypeError):
            profile_call(42)  # type: ignore[arg-type]


class TestCollectStats(unittest.TestCase):
    """Verify reading the statistics of a profiler."""

    def test_collect_stats_returns_the_statistics_of_the_profiler(self):
        profiler = new_profiler()
        profiler.runcall(_work, 10)
        stats = collect_stats(profiler)
        self.assertTrue(stats)
        for key, value in stats.items():
            self.assertEqual(len(key), 3)
            self.assertEqual(len(value), 5)

    def test_collect_stats_rejects_a_profiler_that_is_not_one(self):
        with self.assertRaises(TypeError):
            collect_stats(object())  # type: ignore[arg-type]


class TestFormatReport(unittest.TestCase):
    """Verify rendering the report of a profiling run."""

    def setUp(self):
        self.profiler = new_profiler()
        self.profiler.runcall(_work, 10)

    def test_format_report_returns_the_report_as_text(self):
        report = format_report(self.profiler)
        self.assertIn("function calls", report)
        self.assertIn("_work", report)

    def test_format_report_sorts_the_report(self):
        report = format_report(self.profiler, sort="calls")
        self.assertIn("Ordered by: call count", report)

    def test_format_report_sorts_the_report_by_an_index(self):
        report = format_report(self.profiler, sort=2)
        self.assertIn("Ordered by: cumulative time", report)

    def test_format_report_rejects_a_sort_index_that_is_unknown(self):
        with self.assertRaises(ValueError):
            format_report(self.profiler, sort=7)

    def test_format_report_limits_the_number_of_rows(self):
        report = format_report(self.profiler, limit=1)
        body = [line for line in report.splitlines() if line.strip()]
        self.assertLess(len(body), 10)

    def test_format_report_rejects_a_sort_key_that_is_unknown(self):
        with self.assertRaises(ValueError):
            format_report(self.profiler, sort="not-a-key")

    def test_format_report_rejects_a_sort_that_is_not_a_key(self):
        with self.assertRaises(TypeError):
            format_report(self.profiler, sort=1.5)  # type: ignore[arg-type]

    def test_format_report_rejects_a_limit_that_is_not_a_number(self):
        with self.assertRaises(TypeError):
            format_report(self.profiler, limit="1")  # type: ignore[arg-type]

    def test_format_report_rejects_a_limit_that_is_not_positive(self):
        with self.assertRaises(ValueError):
            format_report(self.profiler, limit=0)

    def test_format_report_rejects_a_profiler_that_is_not_one(self):
        with self.assertRaises(TypeError):
            format_report(object())  # type: ignore[arg-type]


class TestDumpStats(unittest.TestCase):
    """Verify writing the statistics of a profiling run to a file."""

    def setUp(self):
        self.profiler = new_profiler()
        self.profiler.runcall(_work, 10)

    def test_dump_stats_writes_a_readable_file(self):
        import pstats

        with tempfile.TemporaryDirectory() as directory:
            path = os.path.join(directory, "stats.prof")
            written = dump_stats(self.profiler, path)
            self.assertEqual(written, path)
            self.assertTrue(os.path.getsize(path) > 0)
            self.assertTrue(pstats.Stats(path).stats)

    def test_dump_stats_accepts_a_path(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "stats.prof"
            written = dump_stats(self.profiler, path)
            self.assertEqual(written, str(path))
            self.assertTrue(path.exists())

    def test_dump_stats_rejects_a_path_that_is_not_a_path(self):
        with self.assertRaises(TypeError):
            dump_stats(self.profiler, 42)  # type: ignore[arg-type]

    def test_dump_stats_rejects_a_profiler_that_is_not_one(self):
        with self.assertRaises(TypeError):
            dump_stats(object(), "stats.prof")  # type: ignore[arg-type]


class TestMain(unittest.TestCase):
    """Verify the command-line interface of the module."""

    def test_main_profiles_a_script(self):
        with tempfile.TemporaryDirectory() as directory:
            script = Path(directory) / "script.py"
            script.write_text("total = sum(range(10))\n", encoding="utf-8")
            original_path = list(sys.path)
            try:
                with contextlib.redirect_stdout(io.StringIO()):
                    exit_code = main([str(script)])
            finally:
                sys.path[:] = original_path
            self.assertEqual(exit_code, 0)

    def test_main_reports_the_usage_when_no_arguments_are_given(self):
        original_path = list(sys.path)
        try:
            with contextlib.redirect_stdout(io.StringIO()):
                exit_code = main([])
        finally:
            sys.path[:] = original_path
        self.assertEqual(exit_code, 2)

    def test_main_restores_the_arguments_of_the_process(self):
        original_argv = list(sys.argv)
        original_path = list(sys.path)
        try:
            with contextlib.redirect_stdout(io.StringIO()):
                main([])
        finally:
            sys.path[:] = original_path
        self.assertEqual(sys.argv, original_argv)

    def test_main_rejects_arguments_that_are_not_a_list(self):
        with self.assertRaises(TypeError):
            main("stats.prof")  # type: ignore[arg-type]


if __name__ == "__main__":
    unittest.main()
