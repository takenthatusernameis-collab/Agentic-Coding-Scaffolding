"""Tests for netrc_utils."""

import os
import tempfile
import unittest

from netrc_utils import NetrcParseError, netrc


class TestNetrcUtils(unittest.TestCase):
    def test_parse_netrc(self):
        with tempfile.TemporaryDirectory() as d:
            path = os.path.join(d, ".netrc")
            with open(path, "w") as f:
                f.write("machine example.com login alice password secret\n")
            n = netrc(path)
            self.assertEqual(n.authenticators("example.com"), ("alice", "", "secret"))

    def test_default_entry(self):
        with tempfile.TemporaryDirectory() as d:
            path = os.path.join(d, ".netrc")
            with open(path, "w") as f:
                f.write("default login anon password anon\n")
            n = netrc(path)
            self.assertEqual(n.authenticators("anything"), ("anon", "", "anon"))

    def test_missing_host_returns_none(self):
        with tempfile.TemporaryDirectory() as d:
            path = os.path.join(d, ".netrc")
            with open(path, "w") as f:
                f.write("machine example.com login alice password secret\n")
            n = netrc(path)
            self.assertIsNone(n.authenticators("nope.com"))

    def test_parse_error(self):
        with tempfile.TemporaryDirectory() as d:
            path = os.path.join(d, ".netrc")
            with open(path, "w") as f:
                f.write("garbage token\n")
            with self.assertRaises(NetrcParseError):
                netrc(path)

    def test_repr(self):
        with tempfile.TemporaryDirectory() as d:
            path = os.path.join(d, ".netrc")
            with open(path, "w") as f:
                f.write("machine example.com login alice password secret\n")
            n = netrc(path)
            self.assertIn("example.com", repr(n))


if __name__ == "__main__":
    unittest.main()
