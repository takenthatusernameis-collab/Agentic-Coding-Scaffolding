"""Unit tests for cli_utils module."""

import unittest
from unittest.mock import patch

from cli_utils import create_parser, main_wrapper, parse_arguments


class TestCreateParser(unittest.TestCase):
    def test_creates_parser_with_prog(self):
        parser = create_parser("my-tool", "A tool.")
        self.assertEqual(parser.prog, "my-tool")
        self.assertEqual(parser.description, "A tool.")

    def test_has_verbose_flag(self):
        parser = create_parser("my-tool", "A tool.")
        args = parser.parse_args(["-v"])
        self.assertTrue(args.verbose)

    def test_has_long_verbose_flag(self):
        parser = create_parser("my-tool", "A tool.")
        args = parser.parse_args(["--verbose"])
        self.assertTrue(args.verbose)

    def test_version_flag_exits(self):
        parser = create_parser("my-tool", "A tool.")
        with self.assertRaises(SystemExit):
            parser.parse_args(["--version"])


class TestParseArguments(unittest.TestCase):
    def test_parses_arguments(self):
        parser = create_parser("my-tool", "A tool.")
        args = parse_arguments(parser, ["-v"])
        self.assertTrue(args.verbose)

    def test_defaults_to_sys_argv(self):
        parser = create_parser("my-tool", "A tool.")
        with patch("sys.argv", ["my-tool", "-v"]):
            args = parse_arguments(parser)
            self.assertTrue(args.verbose)


class TestMainWrapper(unittest.TestCase):
    def test_returns_func_exit_code(self):
        def main(argv):
            return 0

        wrapped = main_wrapper(main)
        self.assertEqual(wrapped([]), 0)

    def test_returns_one_on_exception(self):
        def main(argv):
            raise ValueError("boom")

        wrapped = main_wrapper(main)
        self.assertEqual(wrapped([]), 1)

    def test_returns_130_on_keyboard_interrupt(self):
        def main(argv):
            raise KeyboardInterrupt

        wrapped = main_wrapper(main)
        self.assertEqual(wrapped([]), 130)

    def test_preserves_function_metadata(self):
        def main(argv):
            """The main function."""
            return 0

        wrapped = main_wrapper(main)
        self.assertEqual(wrapped.__name__, "main")
        self.assertEqual(wrapped.__doc__, "The main function.")


if __name__ == "__main__":
    unittest.main()
