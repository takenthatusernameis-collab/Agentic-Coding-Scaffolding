"""Tests for grp_utils."""

import unittest
from unittest.mock import patch

from grp_utils import (
    Group,
    getgrall,
    getgrgid,
    getgrnam,
    is_available,
)


class TestGrpUtils(unittest.TestCase):
    def test_is_available(self):
        self.assertIsInstance(is_available(), bool)

    def test_getgrgid_reads_root_on_unix(self):
        if not is_available():
            self.skipTest("grp module not available")
        record = getgrgid(0)
        self.assertIsInstance(record, Group)
        self.assertEqual(record.gid, 0)
        self.assertIsInstance(record.name, str)
        self.assertIsInstance(record.mem, list)
        # tuple unpacking works
        name, passwd, gid, mem = record
        self.assertEqual(name, record.name)
        self.assertEqual(gid, record.gid)

    def test_getgrnam_reads_root_on_unix(self):
        if not is_available():
            self.skipTest("grp module not available")
        record = getgrnam("root")
        self.assertIsInstance(record, Group)
        self.assertEqual(record.gid, 0)
        self.assertEqual(record.name, "root")

    def test_getgrall_returns_list(self):
        if not is_available():
            self.skipTest("grp module not available")
        records = getgrall()
        self.assertIsInstance(records, list)
        self.assertGreater(len(records), 0)
        self.assertIsInstance(records[0], Group)

    def test_getgrgid_validates_arguments(self):
        with self.assertRaises(TypeError):
            getgrgid("0")  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            getgrgid(True)  # type: ignore[arg-type]
        with self.assertRaises(ValueError):
            getgrgid(-1)

    def test_getgrnam_validates_arguments(self):
        with self.assertRaises(TypeError):
            getgrnam(0)  # type: ignore[arg-type]
        with self.assertRaises(ValueError):
            getgrnam("")

    def test_getgrgid_missing_raises_keyerror(self):
        if not is_available():
            self.skipTest("grp module not available")
        with self.assertRaises(KeyError):
            getgrgid(99999)

    def test_getgrnam_missing_raises_keyerror(self):
        if not is_available():
            self.skipTest("grp module not available")
        with self.assertRaises(KeyError):
            getgrnam("thisgroupdoesnotexist12345")

    def test_missing_module_raises_runtimeerror(self):
        with patch("grp_utils._grp", None):
            with self.assertRaises(RuntimeError):
                getgrgid(0)
            with self.assertRaises(RuntimeError):
                getgrnam("root")
            with self.assertRaises(RuntimeError):
                getgrall()
