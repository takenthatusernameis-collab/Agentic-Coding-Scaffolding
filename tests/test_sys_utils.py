"""Unit tests for sys_utils module."""

import sys
import unittest

from sys_utils import (
    get_argv,
    get_executable,
    get_frame_info,
    get_path,
    get_platform,
    get_python_version,
    get_python_version_string,
    get_recursion_limit,
    get_refcount,
    get_stderr_encoding,
    get_stdin_encoding,
    get_stdout_encoding,
    is_interactive,
    set_recursion_limit,
)


class TestGetPythonVersion(unittest.TestCase):
    def test_get_python_version(self):
        version = get_python_version()
        self.assertIsInstance(version, dict)
        for key in ("major", "minor", "micro", "releaselevel", "serial"):
            self.assertIn(key, version)
        self.assertEqual(version["major"], sys.version_info.major)
        self.assertEqual(version["minor"], sys.version_info.minor)
        self.assertEqual(version["micro"], sys.version_info.micro)
        self.assertIsInstance(version["releaselevel"], str)
        self.assertIsInstance(version["serial"], int)


class TestGetPythonVersionString(unittest.TestCase):
    def test_get_python_version_string(self):
        version_string = get_python_version_string()
        self.assertIsInstance(version_string, str)
        self.assertTrue(version_string.startswith(sys.version.split(" ")[0]))


class TestGetExecutable(unittest.TestCase):
    def test_get_executable(self):
        executable = get_executable()
        self.assertIsInstance(executable, str)
        self.assertEqual(executable, sys.executable)


class TestGetArgv(unittest.TestCase):
    def test_get_argv(self):
        argv = get_argv()
        self.assertIsInstance(argv, list)
        for arg in argv:
            self.assertIsInstance(arg, str)
        self.assertEqual(argv, sys.argv)
        # Return a copy, not the live list
        self.assertIsNot(argv, sys.argv)


class TestGetPlatform(unittest.TestCase):
    def test_get_platform(self):
        platform = get_platform()
        self.assertIsInstance(platform, str)
        self.assertEqual(platform, sys.platform)


class TestGetPath(unittest.TestCase):
    def test_get_path(self):
        path = get_path()
        self.assertIsInstance(path, list)
        for entry in path:
            self.assertIsInstance(entry, str)
        self.assertEqual(path, sys.path)
        self.assertIsNot(path, sys.path)


class TestGetRecursionLimit(unittest.TestCase):
    def test_get_recursion_limit(self):
        limit = get_recursion_limit()
        self.assertIsInstance(limit, int)
        self.assertGreaterEqual(limit, 1)
        self.assertEqual(limit, sys.getrecursionlimit())


class TestSetRecursionLimit(unittest.TestCase):
    def test_set_recursion_limit(self):
        original = sys.getrecursionlimit()
        try:
            set_recursion_limit(100)
            self.assertEqual(sys.getrecursionlimit(), 100)
            self.assertEqual(get_recursion_limit(), 100)
        finally:
            sys.setrecursionlimit(original)

    def test_set_recursion_limit_invalid_type(self):
        with self.assertRaises(TypeError):
            set_recursion_limit("100")
        with self.assertRaises(TypeError):
            set_recursion_limit(100.0)
        with self.assertRaises(TypeError):
            set_recursion_limit(True)

    def test_set_recursion_limit_invalid_value(self):
        with self.assertRaises(ValueError):
            set_recursion_limit(0)
        with self.assertRaises(ValueError):
            set_recursion_limit(-1)


class TestGetStdoutEncoding(unittest.TestCase):
    def test_get_stdout_encoding(self):
        encoding = get_stdout_encoding()
        self.assertTrue(encoding is None or isinstance(encoding, str))


class TestGetStderrEncoding(unittest.TestCase):
    def test_get_stderr_encoding(self):
        encoding = get_stderr_encoding()
        self.assertTrue(encoding is None or isinstance(encoding, str))


class TestGetStdinEncoding(unittest.TestCase):
    def test_get_stdin_encoding(self):
        encoding = get_stdin_encoding()
        self.assertTrue(encoding is None or isinstance(encoding, str))


class TestIsInteractive(unittest.TestCase):
    def test_is_interactive(self):
        result = is_interactive()
        self.assertIsInstance(result, bool)


class TestGetFrameInfo(unittest.TestCase):
    def test_get_frame_info(self):
        def inner():
            return get_frame_info(0)

        info = inner()
        self.assertIsInstance(info, dict)
        for key in ("filename", "lineno", "function", "code_context", "index"):
            self.assertIn(key, info)
        self.assertEqual(info["function"], "inner")
        self.assertIsInstance(info["filename"], str)
        self.assertIsInstance(info["lineno"], int)

    def test_get_frame_info_invalid_type(self):
        with self.assertRaises(TypeError):
            get_frame_info("0")
        with self.assertRaises(TypeError):
            get_frame_info(True)

    def test_get_frame_info_negative_depth(self):
        with self.assertRaises(ValueError):
            get_frame_info(-1)


class TestGetRefcount(unittest.TestCase):
    def test_get_refcount(self):
        obj = object()
        count = get_refcount(obj)
        self.assertIsInstance(count, int)
        self.assertGreaterEqual(count, 1)


if __name__ == "__main__":
    unittest.main()
