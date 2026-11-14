"""Tests for mailcap_utils."""

from __future__ import annotations

import importlib
import os
import sys
import tempfile
import unittest
from unittest import mock

import mailcap_utils


class TestMailcapUtils(unittest.TestCase):
    def test_exports(self) -> None:
        for name in mailcap_utils.__all__:
            self.assertTrue(hasattr(mailcap_utils, name))

    def test_is_available_returns_bool(self) -> None:
        self.assertIsInstance(mailcap_utils.is_available(), bool)

    def test_getcaps_returns_dict(self) -> None:
        caps = mailcap_utils.getcaps()
        self.assertIsInstance(caps, dict)

    def test_list_mailcap_files_returns_list(self) -> None:
        files = mailcap_utils.list_mailcap_files()
        self.assertIsInstance(files, list)

    def test_read_mailcap_file(self) -> None:
        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".mailcap") as f:
            f.write("text/plain; cat %s\n")
            path = f.name
        try:
            with open(path) as fh:
                with self.assertWarns(DeprecationWarning):
                    caps = mailcap_utils.read_mailcap_file(fh)
            self.assertIsInstance(caps, dict)
        finally:
            os.unlink(path)

    def test_parse_line(self) -> None:
        result = mailcap_utils.parse_line("text/plain; cat %s\n")
        self.assertIsInstance(result, tuple)
        self.assertEqual(len(result), 2)

    def test_parse_field(self) -> None:
        line = "view=cat %s; test=echo"
        name, i = mailcap_utils.parse_field(line, 0, len(line))
        self.assertIsInstance(name, str)
        self.assertIsInstance(i, int)

    def test_find_match(self) -> None:
        caps = {"text/plain": [{"view": "cat %s"}]}
        result = mailcap_utils.find_match(caps, "text/plain")
        self.assertIsInstance(result, tuple)

    def test_lookup(self) -> None:
        caps = {"text/plain": [{"view": "cat %s"}]}
        entries = mailcap_utils.lookup(caps, "text/plain")
        self.assertIsInstance(entries, list)

    def test_subst(self) -> None:
        result = mailcap_utils.subst("cat %s", "text/plain", "/tmp/file.txt")
        self.assertTrue(result is None or isinstance(result, str))

    def test_find_param(self) -> None:
        result = mailcap_utils.find_param("test", ["test=hello", "other=world"])
        self.assertIsInstance(result, str)


class TestUnavailableModule(unittest.TestCase):
    """Verify the Python 3.13+ path where :mod:`mailcap` no longer ships."""

    def test_unavailable_branch(self) -> None:
        try:
            with mock.patch.dict(sys.modules, {"mailcap": None}):
                reloaded = importlib.reload(mailcap_utils)
                assert reloaded.is_available() is False
                with self.assertRaises(RuntimeError):
                    reloaded.getcaps()
                with self.assertRaises(RuntimeError):
                    reloaded.list_mailcap_files()
                with self.assertRaises(RuntimeError):
                    reloaded.read_mailcap_file(object())
                with self.assertRaises(RuntimeError):
                    reloaded.parse_line("text/plain; cat %s\n")
                with self.assertRaises(RuntimeError):
                    reloaded.parse_field("a=b", 0, 3)
                with self.assertRaises(RuntimeError):
                    reloaded.find_match({}, "text/plain")
                with self.assertRaises(RuntimeError):
                    reloaded.lookup({}, "text/plain")
                with self.assertRaises(RuntimeError):
                    reloaded.subst("cat %s", "text/plain", "/tmp/x")
                with self.assertRaises(RuntimeError):
                    reloaded.find_param("x", [])
        finally:
            importlib.reload(mailcap_utils)
        assert mailcap_utils.is_available() is True


if __name__ == "__main__":
    unittest.main()
