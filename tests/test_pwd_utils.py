"""Tests for pwd_utils."""

import unittest
from unittest.mock import patch

from pwd_utils import (
    Passwd,
    getpwall,
    getpwnam,
    getpwuid,
    is_available,
)


class TestPwdUtils(unittest.TestCase):
    def test_is_available(self):
        self.assertIsInstance(is_available(), bool)

    def test_getpwuid_reads_root_on_unix(self):
        if not is_available():
            self.skipTest("pwd module not available")
        record = getpwuid(0)
        self.assertIsInstance(record, Passwd)
        self.assertEqual(record.uid, 0)
        self.assertIsInstance(record.name, str)
        self.assertIsInstance(record.gid, int)
        self.assertIsInstance(record.dir, str)
        self.assertIsInstance(record.shell, str)
        # tuple unpacking works
        name, passwd, uid, gid, gecos, dir_, shell = record
        self.assertEqual(name, record.name)
        self.assertEqual(uid, record.uid)

    def test_getpwnam_reads_root_on_unix(self):
        if not is_available():
            self.skipTest("pwd module not available")
        record = getpwnam("root")
        self.assertIsInstance(record, Passwd)
        self.assertEqual(record.uid, 0)
        self.assertEqual(record.name, "root")

    def test_getpwall_returns_list(self):
        if not is_available():
            self.skipTest("pwd module not available")
        records = getpwall()
        self.assertIsInstance(records, list)
        self.assertGreater(len(records), 0)
        self.assertIsInstance(records[0], Passwd)

    def test_getpwuid_validates_arguments(self):
        with self.assertRaises(TypeError):
            getpwuid("0")  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            getpwuid(True)  # type: ignore[arg-type]
        with self.assertRaises(ValueError):
            getpwuid(-1)

    def test_getpwnam_validates_arguments(self):
        with self.assertRaises(TypeError):
            getpwnam(0)  # type: ignore[arg-type]
        with self.assertRaises(ValueError):
            getpwnam("")

    def test_getpwuid_missing_raises_keyerror(self):
        if not is_available():
            self.skipTest("pwd module not available")
        with self.assertRaises(KeyError):
            getpwuid(99999)

    def test_getpwnam_missing_raises_keyerror(self):
        if not is_available():
            self.skipTest("pwd module not available")
        with self.assertRaises(KeyError):
            getpwnam("thisuserdoesnotexist12345")

    def test_missing_module_raises_runtimeerror(self):
        with patch("pwd_utils._pwd", None):
            with self.assertRaises(RuntimeError):
                getpwuid(0)
            with self.assertRaises(RuntimeError):
                getpwnam("root")
            with self.assertRaises(RuntimeError):
                getpwall()
