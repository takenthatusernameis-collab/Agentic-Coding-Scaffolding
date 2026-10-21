"""Tests for pdb_utils."""

import io
import pdb as standard_pdb
import unittest
from unittest import mock

import pdb_utils
from pdb_utils import (
    Pdb,
    Restart,
    create_pdb,
    is_pdb_instance,
    pm,
    post_mortem,
    run,
    runcall,
    runctx,
    runeval,
    set_trace,
)


class TestModuleContract(unittest.TestCase):
    """Verify the contract of the module."""

    def test_all_is_sorted_and_unique(self):
        self.assertEqual(pdb_utils.__all__, sorted(set(pdb_utils.__all__)))

    def test_every_name_exists(self):
        for name in pdb_utils.__all__:
            self.assertTrue(hasattr(pdb_utils, name), name)

    def test_the_standard_library_classes_are_re_exported(self):
        self.assertIs(Pdb, standard_pdb.Pdb)
        self.assertIs(Restart, standard_pdb.Restart)


class TestDebuggerCreation(unittest.TestCase):
    """Verify the helpers that create a debugger."""

    def test_create_pdb_returns_a_debugger(self):
        debugger = create_pdb()
        self.assertIsInstance(debugger, Pdb)
        self.assertTrue(is_pdb_instance(debugger))

    def test_create_pdb_accepts_the_streams(self):
        debugger = create_pdb(stdin=io.StringIO(), stdout=io.StringIO())
        self.assertFalse(debugger.use_rawinput)

    def test_create_pdb_accepts_skip_patterns(self):
        debugger = create_pdb(skip=["unittest"])
        self.assertIn("unittest", debugger.skip)

    def test_create_pdb_rejects_a_bad_completekey(self):
        with self.assertRaises(TypeError):
            create_pdb(completekey=42)

    def test_create_pdb_rejects_a_bad_stream(self):
        with self.assertRaises(TypeError):
            create_pdb(stdin=object())
        with self.assertRaises(TypeError):
            create_pdb(stdout=object())

    def test_create_pdb_rejects_a_single_string(self):
        with self.assertRaises(TypeError):
            create_pdb(skip="unittest")

    def test_create_pdb_rejects_a_bad_skip(self):
        with self.assertRaises(TypeError):
            create_pdb(skip=42)
        with self.assertRaises(TypeError):
            create_pdb(skip=[42])

    def test_create_pdb_rejects_a_bad_flag(self):
        with self.assertRaises(TypeError):
            create_pdb(nosigint="yes")
        with self.assertRaises(TypeError):
            create_pdb(readrc="yes")

    def test_is_pdb_instance_rejects_other_objects(self):
        self.assertFalse(is_pdb_instance("not a debugger"))


class TestRunningUnderTheDebugger(unittest.TestCase):
    """Verify the helpers that run a program under the debugger."""

    def test_set_trace_forwards_the_header(self):
        with mock.patch.object(pdb_utils._pdb, "set_trace") as patched:
            set_trace("a header")
            patched.assert_called_once_with(header="a header")

    def test_set_trace_without_a_header(self):
        with mock.patch.object(pdb_utils._pdb, "set_trace") as patched:
            set_trace()
            patched.assert_called_once_with(header=None)

    def test_set_trace_rejects_a_bad_header(self):
        with self.assertRaises(TypeError):
            set_trace(header=42)

    def test_post_mortem_forwards_the_traceback(self):
        try:
            raise ValueError("boom")
        except ValueError as error:
            traceback = error.__traceback__
        with mock.patch.object(pdb_utils._pdb, "post_mortem") as patched:
            post_mortem(traceback)
            patched.assert_called_once_with(traceback)

    def test_post_mortem_rejects_a_bad_traceback(self):
        with self.assertRaises(TypeError):
            post_mortem("not a traceback")

    def test_pm_calls_the_standard_library(self):
        with mock.patch.object(pdb_utils._pdb, "pm") as patched:
            pm()
            patched.assert_called_once_with()

    def test_run_forwards_the_namespaces(self):
        with mock.patch.object(pdb_utils._pdb, "run", return_value=42) as patched:
            self.assertEqual(run("1 + 1", {"a": 1}, {"b": 2}), 42)
            patched.assert_called_once_with("1 + 1", {"a": 1}, {"b": 2})

    def test_run_rejects_a_bad_statement(self):
        with self.assertRaises(TypeError):
            run(42)

    def test_run_rejects_a_bad_namespace(self):
        with self.assertRaises(TypeError):
            run("1 + 1", globals="not a dict")
        with self.assertRaises(TypeError):
            run("1 + 1", locals="not a mapping")

    def test_runeval_forwards_the_namespaces(self):
        with mock.patch.object(pdb_utils._pdb, "runeval", return_value=7) as patched:
            self.assertEqual(runeval("1 + 1"), 7)
            patched.assert_called_once_with("1 + 1", None, None)

    def test_runeval_rejects_a_bad_expression(self):
        with self.assertRaises(TypeError):
            runeval(42)

    def test_runctx_forwards_the_namespaces(self):
        with mock.patch.object(pdb_utils._pdb, "runctx") as patched:
            runctx("1 + 1", {"a": 1}, {"b": 2})
            patched.assert_called_once_with("1 + 1", {"a": 1}, {"b": 2})

    def test_runctx_rejects_a_bad_namespace(self):
        with self.assertRaises(TypeError):
            runctx("1 + 1", "not a dict", {})
        with self.assertRaises(TypeError):
            runctx("1 + 1", {}, "not a mapping")

    def test_runcall_forwards_the_arguments(self):
        with mock.patch.object(pdb_utils._pdb, "runcall", return_value=3) as patched:
            self.assertEqual(runcall(len, "abc"), 3)
            patched.assert_called_once_with(len, "abc")

    def test_runcall_rejects_a_value_that_is_not_callable(self):
        with self.assertRaises(TypeError):
            runcall(42)


if __name__ == "__main__":
    unittest.main()
