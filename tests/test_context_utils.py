"""Unit tests for context_utils module."""

import os
import sys
import unittest
from io import StringIO

from context_utils import chdir, redirect_stderr, redirect_stdout, suppress, temp_environ


class TestChdir(unittest.TestCase):
    def test_chdir_changes_and_restores(self):
        original = os.getcwd()
        try:
            with chdir("/tmp"):
                self.assertEqual(os.getcwd(), "/tmp")
            self.assertEqual(os.getcwd(), original)
        finally:
            os.chdir(original)

    def test_chdir_restores_on_exception(self):
        original = os.getcwd()
        try:
            with self.assertRaises(RuntimeError):
                with chdir("/tmp"):
                    raise RuntimeError("boom")
            self.assertEqual(os.getcwd(), original)
        finally:
            os.chdir(original)

    def test_chdir_invalid_type(self):
        with self.assertRaises(TypeError):
            chdir(123)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            chdir(None)  # type: ignore[arg-type]

    def test_chdir_nonexistent_path(self):
        with self.assertRaises(FileNotFoundError):
            with chdir("/__nonexistent_context_utils_path__"):
                pass


class TestTempEnviron(unittest.TestCase):
    def test_temp_environ_sets_and_restores(self):
        key = "__CONTEXT_UTILS_TEST_VAR__"
        try:
            if key in os.environ:
                del os.environ[key]
            with temp_environ({key: "hello"}):
                self.assertEqual(os.environ[key], "hello")
            self.assertNotIn(key, os.environ)
        finally:
            os.environ.pop(key, None)

    def test_temp_environ_updates_existing(self):
        key = "__CONTEXT_UTILS_EXISTING__"
        previous = os.environ.get(key)
        try:
            os.environ[key] = "before"
            with temp_environ({key: "after"}):
                self.assertEqual(os.environ[key], "after")
            self.assertEqual(os.environ[key], "before")
        finally:
            if previous is None:
                os.environ.pop(key, None)
            else:
                os.environ[key] = previous

    def test_temp_environ_clear(self):
        key = "__CONTEXT_UTILS_CLEAR_TEST__"
        os.environ[key] = "present"
        try:
            with temp_environ({"NEW_VAR": "value"}, clear=True):
                self.assertEqual(os.environ["NEW_VAR"], "value")
                self.assertNotIn(key, os.environ)
            self.assertEqual(os.environ[key], "present")
        finally:
            os.environ.pop(key, None)
            os.environ.pop("NEW_VAR", None)

    def test_temp_environ_invalid_type(self):
        with self.assertRaises(TypeError):
            temp_environ("not a mapping")  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            temp_environ({"a": 1})  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            temp_environ({1: 2})  # type: ignore[arg-type]


class TestRedirectStdout(unittest.TestCase):
    def test_redirect_stdout_captures_output(self):
        buffer = StringIO()
        try:
            with redirect_stdout(buffer):
                print("captured", end="")
            self.assertEqual(buffer.getvalue(), "captured")
        finally:
            self.assertIs(sys.stdout, sys.__stdout__)

    def test_redirect_stdout_restores_on_exception(self):
        buffer = StringIO()
        try:
            with self.assertRaises(RuntimeError):
                with redirect_stdout(buffer):
                    raise RuntimeError("boom")
            self.assertIs(sys.stdout, sys.__stdout__)
        finally:
            self.assertIs(sys.stdout, sys.__stdout__)

    def test_redirect_stdout_invalid_target(self):
        with self.assertRaises(TypeError):
            redirect_stdout(123)  # type: ignore[arg-type]


class TestRedirectStderr(unittest.TestCase):
    def test_redirect_stderr_captures_output(self):
        buffer = StringIO()
        try:
            with redirect_stderr(buffer):
                print("captured-err", file=sys.stderr, end="")
            self.assertEqual(buffer.getvalue(), "captured-err")
        finally:
            self.assertIs(sys.stderr, sys.__stderr__)

    def test_redirect_stderr_restores_on_exception(self):
        buffer = StringIO()
        try:
            with self.assertRaises(RuntimeError):
                with redirect_stderr(buffer):
                    raise RuntimeError("boom")
            self.assertIs(sys.stderr, sys.__stderr__)
        finally:
            self.assertIs(sys.stderr, sys.__stderr__)


class TestSuppress(unittest.TestCase):
    def test_suppress_listed_exception(self):
        raised = False
        try:
            with suppress(ValueError):
                raised = True
                raise ValueError("ignore me")
        finally:
            pass
        self.assertTrue(raised)

    def test_suppress_propagates_unlisted_exception(self):
        with self.assertRaises(RuntimeError):
            with suppress(ValueError):
                raise RuntimeError("not suppressed")

    def test_suppress_no_exception(self):
        result = None
        with suppress(ValueError):
            result = "ok"
        self.assertEqual(result, "ok")


if __name__ == "__main__":
    unittest.main()
