"""Tests for pstats_utils module."""

import io
import pstats
import unittest

import pstats_utils


class TestPstatsUtils(unittest.TestCase):
    def test_new_stats(self):
        s = pstats_utils.new_stats()
        self.assertIsInstance(s, pstats.Stats)

    def test_new_stats_with_stream(self):
        buf = io.StringIO()
        s = pstats_utils.new_stats(stream=buf)
        self.assertIsInstance(s, pstats.Stats)

    def test_new_stats_bad_stream(self):
        with self.assertRaises(TypeError):
            pstats_utils.new_stats(stream=123)

    def test_load_stats_no_args(self):
        with self.assertRaises(ValueError):
            pstats_utils.load_stats()

    def test_add_stats_type_error(self):
        with self.assertRaises(TypeError):
            pstats_utils.add_stats(123)

    def test_add_stats_no_files(self):
        s = pstats_utils.new_stats()
        with self.assertRaises(ValueError):
            pstats_utils.add_stats(s)

    def test_sort_stats(self):
        s = pstats_utils.new_stats()
        result = pstats_utils.sort_stats(s, "time")
        self.assertIs(result, s)

    def test_sort_stats_type_error(self):
        with self.assertRaises(TypeError):
            pstats_utils.sort_stats(123)

    def test_strip_dirs(self):
        s = pstats_utils.new_stats()
        result = pstats_utils.strip_dirs(s)
        self.assertIs(result, s)

    def test_strip_dirs_type_error(self):
        with self.assertRaises(TypeError):
            pstats_utils.strip_dirs(123)

    def test_reverse_order(self):
        s = pstats_utils.new_stats()
        result = pstats_utils.reverse_order(s)
        self.assertIs(result, s)

    def test_reverse_order_type_error(self):
        with self.assertRaises(TypeError):
            pstats_utils.reverse_order(123)

    def test_dump_stats(self):
        s = pstats_utils.new_stats()
        result = pstats_utils.dump_stats(s, "/tmp/test.pstats")
        self.assertIsNone(result)

    def test_dump_stats_type_error(self):
        s = pstats_utils.new_stats()
        with self.assertRaises(TypeError):
            pstats_utils.dump_stats(s, 123)
        with self.assertRaises(TypeError):
            pstats_utils.dump_stats(123, "file.pstats")

    def test_print_stats(self):
        s = pstats_utils.new_stats()
        result = pstats_utils.print_stats(s)
        self.assertIs(result, s)

    def test_print_stats_type_error(self):
        with self.assertRaises(TypeError):
            pstats_utils.print_stats(123)

    def test_print_stats_with_sort_prints_once(self):
        import cProfile
        import os
        import tempfile

        with tempfile.TemporaryDirectory() as tmp:
            prof_path = os.path.join(tmp, "sample.prof")
            cProfile.run("sum(range(100))", prof_path)
            buf = io.StringIO()
            stats = pstats_utils.new_stats(prof_path, stream=buf)
            pstats_utils.print_stats(stats, sort="cumulative")
            text = buf.getvalue()
        # The header line is emitted once per report; a double print would
        # reproduce it twice.
        self.assertEqual(text.count("function calls"), 1)
        self.assertIn("Ordered by: cumulative time", text)

    def test_sort_key_export(self):
        self.assertTrue(hasattr(pstats_utils, "SortKey"))


if __name__ == "__main__":
    unittest.main()
