"""Unit tests for platform_utils module."""

import unittest

from platform_utils import (
    get_machine,
    get_node,
    get_platform,
    get_processor,
    get_python_build,
    get_python_compiler,
    get_python_implementation,
    get_python_revision,
    get_python_version,
    get_python_version_tuple,
    get_release,
    get_system,
    get_uname,
    get_version,
    platform_info,
)


class TestPlatformUtils(unittest.TestCase):
    def test_get_system(self):
        result = get_system()
        self.assertIsInstance(result, str)
        self.assertGreater(len(result), 0)

    def test_get_release(self):
        result = get_release()
        self.assertIsInstance(result, str)

    def test_get_version(self):
        result = get_version()
        self.assertIsInstance(result, str)

    def test_get_machine(self):
        result = get_machine()
        self.assertIsInstance(result, str)
        self.assertGreater(len(result), 0)

    def test_get_processor(self):
        result = get_processor()
        self.assertIsInstance(result, str)

    def test_get_node(self):
        result = get_node()
        self.assertIsInstance(result, str)

    def test_get_python_implementation(self):
        result = get_python_implementation()
        self.assertIsInstance(result, str)
        self.assertIn(result, ("CPython", "PyPy", "Jython", "IronPython"))

    def test_get_python_version(self):
        result = get_python_version()
        self.assertIsInstance(result, str)
        parts = result.split(".")
        self.assertGreaterEqual(len(parts), 2)

    def test_get_python_version_tuple(self):
        result = get_python_version_tuple()
        self.assertIsInstance(result, tuple)
        self.assertGreaterEqual(len(result), 2)

    def test_get_python_build(self):
        result = get_python_build()
        self.assertIsInstance(result, tuple)
        self.assertEqual(len(result), 2)

    def test_get_python_compiler(self):
        result = get_python_compiler()
        self.assertIsInstance(result, str)

    def test_get_python_revision(self):
        result = get_python_revision()
        self.assertIsInstance(result, str)

    def test_get_uname(self):
        result = get_uname()
        self.assertTrue(hasattr(result, "system"))
        self.assertTrue(hasattr(result, "release"))
        self.assertTrue(hasattr(result, "version"))
        self.assertTrue(hasattr(result, "machine"))
        self.assertTrue(hasattr(result, "node"))
        self.assertTrue(hasattr(result, "processor"))

    def test_get_platform(self):
        result = get_platform()
        self.assertIsInstance(result, str)
        result2 = get_platform(aliased=False, terse=False)
        self.assertIsInstance(result2, str)

    def test_get_platform_type_errors(self):
        with self.assertRaises(TypeError):
            get_platform(aliased="false")  # type: ignore
        with self.assertRaises(TypeError):
            get_platform(terse="false")  # type: ignore

    def test_platform_info(self):
        info = platform_info()
        self.assertIsInstance(info, dict)
        for key in (
            "system",
            "release",
            "version",
            "machine",
            "processor",
            "node",
            "python_implementation",
            "python_version",
            "python_build",
            "python_compiler",
            "python_revision",
        ):
            self.assertIn(key, info)
