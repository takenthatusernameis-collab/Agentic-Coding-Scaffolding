"""Tests for doctest_utils module."""

import contextlib
import doctest
import io
import os
import sys
import tempfile
import types
import unittest

import doctest_utils


def add(first, second):
    """Return the sum of two numbers.

    >>> add(1, 2)
    3
    """
    return first + second


def _sample_module(docstring):
    """Return a module whose docstring holds *docstring*."""
    module = types.ModuleType("sample_module")
    module.__doc__ = docstring
    return module


class TestParseDoctests(unittest.TestCase):
    """Verify parsing of doctest examples out of text."""

    def test_parse_doctests_returns_a_list(self):
        result = doctest_utils.parse_doctests(">>> 1 + 1\n2\n")
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 1)

    def test_parse_doctests_collects_the_examples(self):
        test = doctest_utils.parse_doctests(">>> 1 + 1\n2\n")[0]
        self.assertEqual(len(test.examples), 1)
        self.assertEqual(test.examples[0].source.strip(), "1 + 1")

    def test_parse_doctests_returns_an_empty_list_without_examples(self):
        self.assertEqual(doctest_utils.parse_doctests("Nothing to run here."), [])

    def test_parse_doctests_uses_the_given_name(self):
        test = doctest_utils.parse_doctests(">>> 1 + 1\n2\n", name="sample")[0]
        self.assertEqual(test.name, "sample")

    def test_parse_doctests_makes_the_globals_available(self):
        test = doctest_utils.parse_doctests(">>> value\n42\n", globs={"value": 42})[0]
        self.assertEqual(test.globs["value"], 42)

    def test_parse_doctests_requires_a_string(self):
        with self.assertRaises(TypeError):
            doctest_utils.parse_doctests(None)  # type: ignore[arg-type]

    def test_parse_doctests_requires_a_string_name(self):
        with self.assertRaises(TypeError):
            doctest_utils.parse_doctests(">>> 1\n", name=7)  # type: ignore[arg-type]

    def test_parse_doctests_rejects_non_mapping_globals(self):
        with self.assertRaises(TypeError):
            doctest_utils.parse_doctests(">>> 1\n", globs=["value"])  # type: ignore[arg-type]

    def test_parse_doctests_rejects_a_negative_line_number(self):
        with self.assertRaises(ValueError):
            doctest_utils.parse_doctests(">>> 1\n", lineno=-1)


class TestFindDoctests(unittest.TestCase):
    """Verify discovery of doctests inside modules and objects."""

    def test_find_doctests_finds_the_examples_of_a_module(self):
        module = _sample_module(">>> 1 + 1\n2\n")
        tests = doctest_utils.find_doctests(module)
        self.assertTrue(tests)
        self.assertEqual(tests[0].name, "sample_module")

    def test_find_doctests_finds_the_examples_of_a_function(self):
        tests = doctest_utils.find_doctests(add)
        self.assertTrue(tests)
        self.assertEqual(len(tests[0].examples), 1)

    def test_find_doctests_returns_an_empty_list_without_examples(self):
        self.assertEqual(doctest_utils.find_doctests(_sample_module("Plain text.")), [])

    def test_find_doctests_requires_a_string_name(self):
        with self.assertRaises(TypeError):
            doctest_utils.find_doctests(add, name=7)  # type: ignore[arg-type]


class TestRunStringExamples(unittest.TestCase):
    """Verify running the doctest examples of a string."""

    def test_run_string_examples_passes_for_correct_output(self):
        results = doctest_utils.run_string_examples(">>> 1 + 1\n2\n")
        self.assertEqual(results.failed, 0)
        self.assertEqual(results.attempted, 1)

    def test_run_string_examples_fails_for_wrong_output(self):
        with contextlib.redirect_stdout(io.StringIO()):
            results = doctest_utils.run_string_examples(">>> 1 + 1\n3\n")
        self.assertEqual(results.failed, 1)
        self.assertEqual(results.attempted, 1)

    def test_run_string_examples_reports_no_attempts_without_examples(self):
        results = doctest_utils.run_string_examples("Nothing to run here.")
        self.assertEqual(results.attempted, 0)

    def test_run_string_examples_makes_the_globals_available(self):
        results = doctest_utils.run_string_examples(">>> value\n42\n", globs={"value": 42})
        self.assertEqual(results.failed, 0)

    def test_run_string_examples_requires_a_string(self):
        with self.assertRaises(TypeError):
            doctest_utils.run_string_examples(None)  # type: ignore[arg-type]

    def test_run_string_examples_requires_a_boolean_verbose_flag(self):
        with self.assertRaises(TypeError):
            doctest_utils.run_string_examples(">>> 1\n", verbose="yes")  # type: ignore[arg-type]


class TestRunDocstringExamples(unittest.TestCase):
    """Verify running the doctest examples of a docstring."""

    def test_run_docstring_examples_passes_for_correct_output(self):
        results = doctest_utils.run_docstring_examples(add)
        self.assertEqual(results.failed, 0)
        self.assertEqual(results.attempted, 1)

    def test_run_docstring_examples_reports_no_attempts_without_a_docstring(self):
        def undocumented():
            pass

        results = doctest_utils.run_docstring_examples(undocumented)
        self.assertEqual(results.failed, 0)
        self.assertEqual(results.attempted, 0)

    def test_run_docstring_examples_requires_a_string_name(self):
        with self.assertRaises(TypeError):
            doctest_utils.run_docstring_examples(add, name=7)  # type: ignore[arg-type]

    def test_run_docstring_examples_rejects_non_mapping_globals(self):
        with self.assertRaises(TypeError):
            doctest_utils.run_docstring_examples(add, globs=["value"])  # type: ignore[arg-type]


class TestRunModuleExamples(unittest.TestCase):
    """Verify running every doctest example of a module."""

    def test_run_module_examples_passes_for_correct_output(self):
        results = doctest_utils.run_module_examples(_sample_module(">>> 1 + 1\n2\n"))
        self.assertEqual(results.failed, 0)
        self.assertEqual(results.attempted, 1)

    def test_run_module_examples_fails_for_wrong_output(self):
        with contextlib.redirect_stdout(io.StringIO()):
            results = doctest_utils.run_module_examples(_sample_module(">>> 1 + 1\n3\n"))
        self.assertEqual(results.failed, 1)

    def test_run_module_examples_requires_a_module(self):
        with self.assertRaises(TypeError):
            doctest_utils.run_module_examples("not a module")  # type: ignore[arg-type]

    def test_run_module_examples_requires_a_boolean_verbose_flag(self):
        with self.assertRaises(TypeError):
            doctest_utils.run_module_examples(_sample_module(">>> 1\n"), verbose=1)  # type: ignore[arg-type]


class TestRunFileExamples(unittest.TestCase):
    """Verify running the doctest examples of a text file."""

    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix="doctest-utils-")

    def tearDown(self):
        for root, dirs, files in os.walk(self.tmp, topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))
            for name in dirs:
                os.rmdir(os.path.join(root, name))
        os.rmdir(self.tmp)

    def _write(self, name, text):
        path = os.path.join(self.tmp, name)
        with open(path, "w", encoding="utf-8") as handle:
            handle.write(text)
        return path

    def test_run_file_examples_passes_for_correct_output(self):
        path = self._write("sample.txt", ">>> 1 + 1\n2\n")
        results = doctest_utils.run_file_examples(path)
        self.assertEqual(results.failed, 0)
        self.assertEqual(results.attempted, 1)

    def test_run_file_examples_fails_for_wrong_output(self):
        path = self._write("sample.txt", ">>> 1 + 1\n3\n")
        with contextlib.redirect_stdout(io.StringIO()):
            results = doctest_utils.run_file_examples(path)
        self.assertEqual(results.failed, 1)

    def test_run_file_examples_resolves_against_the_base_directory(self):
        self._write("sample.txt", ">>> 1 + 1\n2\n")
        results = doctest_utils.run_file_examples("sample.txt", base_dir=self.tmp)
        self.assertEqual(results.failed, 0)
        self.assertEqual(results.attempted, 1)

    def test_run_file_examples_requires_a_string_path(self):
        with self.assertRaises(TypeError):
            doctest_utils.run_file_examples(None)  # type: ignore[arg-type]

    def test_run_file_examples_requires_a_string_base_directory(self):
        with self.assertRaises(TypeError):
            doctest_utils.run_file_examples("sample.txt", base_dir=7)  # type: ignore[arg-type]

    def test_run_file_examples_reports_a_missing_file(self):
        with self.assertRaises(OSError):
            doctest_utils.run_file_examples(os.path.join(self.tmp, "absent.txt"))


class TestSummarizeResults(unittest.TestCase):
    """Verify the one line summary of a doctest run."""

    def test_summarize_results_reports_a_passing_run(self):
        results = doctest_utils.run_string_examples(">>> 1 + 1\n2\n")
        self.assertEqual(doctest_utils.summarize_results(results), "1 doctests passed")

    def test_summarize_results_reports_a_failing_run(self):
        with contextlib.redirect_stdout(io.StringIO()):
            results = doctest_utils.run_string_examples(">>> 1 + 1\n3\n")
        self.assertEqual(
            doctest_utils.summarize_results(results),
            "1 of 1 doctests failed",
        )

    def test_summarize_results_requires_the_result_counters(self):
        with self.assertRaises(TypeError):
            doctest_utils.summarize_results(object())

    def test_summarize_results_rejects_negative_counters(self):
        class Broken:
            failed = -1
            attempted = 1

        with self.assertRaises(ValueError):
            doctest_utils.summarize_results(Broken())


class TestFormatFailure(unittest.TestCase):
    """Verify the readable description of a doctest failure."""

    def test_format_failure_describes_a_mismatch(self):
        example = doctest.Example("1 + 1", "2")
        failure = doctest.DocTestFailure("sample", example, "3")
        description = doctest_utils.format_failure(failure)
        self.assertIn("Expected:", description)
        self.assertIn("Got:", description)
        self.assertIn("2", description)

    def test_format_failure_describes_an_unexpected_exception(self):
        example = doctest.Example("raise ValueError('boom')", "boom")
        try:
            raise ValueError("boom")
        except ValueError:
            failure = doctest.UnexpectedException("sample", example, sys.exc_info())
        description = doctest_utils.format_failure(failure)
        self.assertIn("ValueError", description)
        self.assertIn("boom", description)

    def test_format_failure_rejects_other_objects(self):
        with self.assertRaises(TypeError):
            doctest_utils.format_failure("not a failure")


if __name__ == "__main__":
    unittest.main()
