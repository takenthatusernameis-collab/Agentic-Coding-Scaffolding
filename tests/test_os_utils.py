"""Unit tests for os_utils module."""

import os
import unittest
from unittest import mock

from os_utils import (
    expand_path,
    find_executable,
    get_cpu_count,
    get_disk_usage,
    get_platform_info,
    get_user_home,
    get_username,
    is_executable,
)


class TestGetPlatformInfo(unittest.TestCase):
    def test_get_platform_info(self):
        info = get_platform_info()
        self.assertIsInstance(info, dict)
        for key in (
            "system",
            "release",
            "version",
            "machine",
            "processor",
            "python_version",
            "python_implementation",
        ):
            self.assertIn(key, info)
            self.assertIsInstance(info[key], str)


class TestGetCpuCount(unittest.TestCase):
    def test_get_cpu_count(self):
        count = get_cpu_count()
        self.assertIsInstance(count, int)
        self.assertGreaterEqual(count, 1)


class TestGetDiskUsage(unittest.TestCase):
    def test_get_disk_usage(self):
        usage = get_disk_usage("/")
        self.assertIsInstance(usage, dict)
        for key in ("total", "used", "free", "percent"):
            self.assertIn(key, usage)
        self.assertGreaterEqual(usage["total"], 0)
        self.assertGreaterEqual(usage["used"], 0)
        self.assertGreaterEqual(usage["free"], 0)
        self.assertGreaterEqual(usage["percent"], 0)
        self.assertLessEqual(usage["percent"], 100)

    def test_get_disk_usage_type_error(self):
        with self.assertRaises(TypeError):
            get_disk_usage(123)  # type: ignore[arg-type]

    def test_get_disk_usage_not_found(self):
        with self.assertRaises(FileNotFoundError):
            get_disk_usage("/nonexistent/os_utils/path/xyz")


class TestGetUserHome(unittest.TestCase):
    def test_get_user_home(self):
        home = get_user_home()
        self.assertIsInstance(home, str)
        self.assertTrue(os.path.isdir(home))


class TestGetUsername(unittest.TestCase):
    def test_get_username(self):
        name = get_username()
        self.assertIsInstance(name, str)

    def test_get_username_fallback(self):
        with mock.patch.object(os, "getlogin", side_effect=OSError("no tty")):
            with mock.patch.dict(os.environ, {}, clear=True):
                self.assertEqual(get_username(), "")


class TestFindExecutable(unittest.TestCase):
    def test_find_executable(self):
        result = find_executable("python3") or find_executable("python")
        if result is not None:
            self.assertTrue(os.path.isfile(result))

    def test_find_executable_not_found(self):
        self.assertIsNone(find_executable("__nonexistent_os_utils_executable__"))

    def test_find_executable_type_error(self):
        with self.assertRaises(TypeError):
            find_executable(123)  # type: ignore[arg-type]


class TestExpandPath(unittest.TestCase):
    def test_expand_path(self):
        result = expand_path("~")
        self.assertEqual(result, os.path.abspath(os.path.expanduser("~")))
        self.assertTrue(os.path.isabs(result))

    def test_expand_path_type_error(self):
        with self.assertRaises(TypeError):
            expand_path(123)  # type: ignore[arg-type]


class TestIsExecutable(unittest.TestCase):
    def test_is_executable(self):
        python = find_executable("python3") or find_executable("python")
        if python is not None:
            self.assertTrue(is_executable(python))

    def test_is_executable_not_executable(self):
        self.assertFalse(is_executable("/nonexistent/os_utils/path/xyz"))

    def test_is_executable_type_error(self):
        with self.assertRaises(TypeError):
            is_executable(123)  # type: ignore[arg-type]


if __name__ == "__main__":
    unittest.main()
