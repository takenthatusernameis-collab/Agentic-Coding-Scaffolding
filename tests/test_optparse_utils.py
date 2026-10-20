"""Tests for the optparse utilities."""

import sys
import unittest
from contextlib import redirect_stderr
from io import StringIO
from unittest import mock

import optparse_utils


class TestMakeParser(unittest.TestCase):
    """Exercise the parser factory."""

    def test_make_parser_returns_a_parser(self) -> None:
        parser = optparse_utils.make_parser()
        self.assertIsInstance(parser, optparse_utils.OptionParser)

    def test_make_parser_keeps_the_metadata(self) -> None:
        parser = optparse_utils.make_parser(
            usage="demo [options]",
            description="a demo",
            prog="demo",
            epilog="the end",
        )
        self.assertEqual(parser.get_prog_name(), "demo")
        self.assertEqual(parser.get_description(), "a demo")
        self.assertIn("demo [options]", parser.get_usage())
        self.assertIn("the end", parser.format_help())

    def test_make_parser_adds_a_version_option(self) -> None:
        parser = optparse_utils.make_parser(prog="demo", version="1.2.3")
        self.assertTrue(parser.has_option("--version"))

    def test_make_parser_can_drop_the_help_option(self) -> None:
        parser = optparse_utils.make_parser(add_help_option=False)
        self.assertFalse(parser.has_option("--help"))

    def test_make_parser_rejects_invalid_arguments(self) -> None:
        with self.assertRaises(TypeError):
            optparse_utils.make_parser(usage=42)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            optparse_utils.make_parser(add_help_option="yes")  # type: ignore[arg-type]
        with self.assertRaises(ValueError):
            optparse_utils.make_parser(conflict_handler="ignore")


class TestAddOption(unittest.TestCase):
    """Exercise the option helpers."""

    def setUp(self) -> None:
        self.parser = optparse_utils.make_parser(prog="demo")

    def test_add_option_registers_the_option(self) -> None:
        option = optparse_utils.add_option(self.parser, "--file", "-f")
        self.assertIsInstance(option, optparse_utils.Option)
        self.assertTrue(self.parser.has_option("--file"))
        self.assertTrue(self.parser.has_option("-f"))

    def test_add_option_derives_the_destination(self) -> None:
        option = optparse_utils.add_option(self.parser, "--dry-run")
        self.assertEqual(option.dest, "dry_run")

    def test_add_option_keeps_an_explicit_destination(self) -> None:
        option = optparse_utils.add_option(self.parser, "--dry-run", dest="dry")
        self.assertEqual(option.dest, "dry")

    def test_add_option_stores_the_value(self) -> None:
        optparse_utils.add_option(self.parser, "--file")
        options, _ = optparse_utils.parse_args(self.parser, ["--file", "demo.txt"])
        self.assertEqual(options.file, "demo.txt")

    def test_add_option_converts_the_value(self) -> None:
        optparse_utils.add_option(self.parser, "--count", type_="int")
        options, _ = optparse_utils.parse_args(self.parser, ["--count", "7"])
        self.assertEqual(options.count, 7)

    def test_add_option_accepts_a_type_object(self) -> None:
        optparse_utils.add_option(self.parser, "--count", type_=int)
        options, _ = optparse_utils.parse_args(self.parser, ["--count", "7"])
        self.assertEqual(options.count, 7)

    def test_add_option_accepts_a_converter(self) -> None:
        optparse_utils.add_option(
            self.parser, "--count", type_=optparse_utils.int_type
        )
        options, _ = optparse_utils.parse_args(self.parser, ["--count", "7"])
        self.assertEqual(options.count, 7)

    def test_add_option_accepts_a_standard_library_converter(self) -> None:
        def _convert(option, opt, value):
            return value.upper()

        optparse_utils.add_option(self.parser, "--name", type_=_convert)
        options, _ = optparse_utils.parse_args(self.parser, ["--name", "demo"])
        self.assertEqual(options.name, "DEMO")

    def test_add_option_rejects_an_invalid_value(self) -> None:
        optparse_utils.add_option(self.parser, "--count", type_="int")
        with self.assertRaises(optparse_utils.OptionParseError):
            optparse_utils.parse_args(
                self.parser, ["--count", "seven"], on_error="raise"
            )

    def test_add_option_restricts_the_choices(self) -> None:
        optparse_utils.add_option(self.parser, "--mode", choices=["fast", "slow"])
        options, _ = optparse_utils.parse_args(self.parser, ["--mode", "fast"])
        self.assertEqual(options.mode, "fast")
        with self.assertRaises(optparse_utils.OptionParseError):
            optparse_utils.parse_args(
                self.parser, ["--mode", "medium"], on_error="raise"
            )

    def test_add_option_uses_the_default(self) -> None:
        optparse_utils.add_option(self.parser, "--file", default="fallback")
        options, _ = optparse_utils.parse_args(self.parser, [])
        self.assertEqual(options.file, "fallback")

    def test_add_option_leaves_the_default_unset(self) -> None:
        optparse_utils.add_option(self.parser, "--file")
        defaults = optparse_utils.get_default_values(self.parser)
        self.assertIsNone(defaults.file)

    def test_add_option_supports_a_constant(self) -> None:
        optparse_utils.add_option(
            self.parser, "--level", action="store_const", const=3
        )
        options, _ = optparse_utils.parse_args(self.parser, ["--level"])
        self.assertEqual(options.level, 3)

    def test_add_option_supports_appending(self) -> None:
        optparse_utils.add_option(self.parser, "--tag", action="append")
        options, _ = optparse_utils.parse_args(self.parser, ["--tag", "a", "--tag", "b"])
        self.assertEqual(options.tag, ["a", "b"])

    def test_add_option_supports_several_values(self) -> None:
        optparse_utils.add_option(self.parser, "--pair", nargs=2)
        options, _ = optparse_utils.parse_args(self.parser, ["--pair", "a", "b"])
        self.assertEqual(options.pair, ("a", "b"))

    def test_add_option_records_the_help_text(self) -> None:
        optparse_utils.add_option(self.parser, "--file", help_text="the file")
        self.assertIn("the file", optparse_utils.format_help(self.parser))

    def test_add_option_uses_the_metavar(self) -> None:
        optparse_utils.add_option(self.parser, "--file", metavar="PATH")
        self.assertIn("PATH", optparse_utils.format_help(self.parser))

    def test_add_option_rejects_invalid_option_strings(self) -> None:
        with self.assertRaises(ValueError):
            optparse_utils.add_option(self.parser)
        with self.assertRaises(ValueError):
            optparse_utils.add_option(self.parser, "-")
        with self.assertRaises(ValueError):
            optparse_utils.add_option(self.parser, "--")
        with self.assertRaises(ValueError):
            optparse_utils.add_option(self.parser, "file")
        with self.assertRaises(TypeError):
            optparse_utils.add_option(self.parser, 42)  # type: ignore[arg-type]

    def test_add_option_rejects_invalid_actions(self) -> None:
        with self.assertRaises(ValueError):
            optparse_utils.add_option(self.parser, "--file", action="explode")
        with self.assertRaises(TypeError):
            optparse_utils.add_option(self.parser, "--file", action=42)  # type: ignore[arg-type]

    def test_add_option_rejects_invalid_types(self) -> None:
        with self.assertRaises(ValueError):
            optparse_utils.add_option(self.parser, "--file", type_="decimal")
        with self.assertRaises(ValueError):
            optparse_utils.add_option(self.parser, "--file", type_=bool)
        with self.assertRaises(TypeError):
            optparse_utils.add_option(self.parser, "--file", type_=42)  # type: ignore[arg-type]

    def test_add_option_rejects_invalid_choices(self) -> None:
        with self.assertRaises(TypeError):
            optparse_utils.add_option(self.parser, "--mode", choices="fast")
        with self.assertRaises(TypeError):
            optparse_utils.add_option(self.parser, "--mode", choices=[42])  # type: ignore[list-item]
        with self.assertRaises(ValueError):
            optparse_utils.add_option(self.parser, "--mode", choices=[])

    def test_add_option_rejects_invalid_nargs(self) -> None:
        with self.assertRaises(TypeError):
            optparse_utils.add_option(self.parser, "--pair", nargs="two")  # type: ignore[arg-type]
        with self.assertRaises(ValueError):
            optparse_utils.add_option(self.parser, "--pair", nargs=-1)

    def test_add_option_rejects_invalid_text(self) -> None:
        with self.assertRaises(TypeError):
            optparse_utils.add_option(self.parser, "--file", help_text=42)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            optparse_utils.add_option(self.parser, "--file", dest=42)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            optparse_utils.add_option(self.parser, "--file", metavar=42)  # type: ignore[arg-type]

    def test_add_option_rejects_a_foreign_container(self) -> None:
        with self.assertRaises(TypeError):
            optparse_utils.add_option(object(), "--file")  # type: ignore[arg-type]

    def test_add_option_detects_a_conflict(self) -> None:
        optparse_utils.add_option(self.parser, "--file")
        with self.assertRaises(optparse_utils.OptionConflictError):
            optparse_utils.add_option(self.parser, "--file")


class TestFlags(unittest.TestCase):
    """Exercise the flag and counter helpers."""

    def setUp(self) -> None:
        self.parser = optparse_utils.make_parser(prog="demo")

    def test_add_flag_defaults_to_false(self) -> None:
        optparse_utils.add_flag(self.parser, "--verbose", "-v")
        options, _ = optparse_utils.parse_args(self.parser, [])
        self.assertFalse(options.verbose)
        options, _ = optparse_utils.parse_args(self.parser, ["--verbose"])
        self.assertTrue(options.verbose)

    def test_add_flag_can_default_to_true(self) -> None:
        optparse_utils.add_flag(self.parser, "--quiet", default=True)
        options, _ = optparse_utils.parse_args(self.parser, [])
        self.assertTrue(options.quiet)
        options, _ = optparse_utils.parse_args(self.parser, ["--quiet"])
        self.assertFalse(options.quiet)

    def test_add_flag_rejects_invalid_defaults(self) -> None:
        with self.assertRaises(TypeError):
            optparse_utils.add_flag(self.parser, "--verbose", default="yes")  # type: ignore[arg-type]

    def test_add_count_option_counts_the_occurrences(self) -> None:
        optparse_utils.add_count_option(self.parser, "-v", "--verbose")
        options, _ = optparse_utils.parse_args(self.parser, ["-v", "-v", "--verbose"])
        self.assertEqual(options.verbose, 3)

    def test_add_count_option_starts_at_zero(self) -> None:
        optparse_utils.add_count_option(self.parser, "-v")
        options, _ = optparse_utils.parse_args(self.parser, [])
        self.assertEqual(options.v, 0)


class TestOptionGroups(unittest.TestCase):
    """Exercise the option group helper."""

    def test_add_option_group_returns_a_group(self) -> None:
        parser = optparse_utils.make_parser(prog="demo")
        group = optparse_utils.add_option_group(parser, "Advanced")
        self.assertIsInstance(group, optparse_utils.OptionGroup)

    def test_group_options_are_parsed(self) -> None:
        parser = optparse_utils.make_parser(prog="demo")
        group = optparse_utils.add_option_group(parser, "Advanced")
        optparse_utils.add_option(group, "--level", type_="int", default=1)
        options, _ = optparse_utils.parse_args(parser, ["--level", "5"])
        self.assertEqual(options.level, 5)

    def test_group_options_appear_in_the_help(self) -> None:
        parser = optparse_utils.make_parser(prog="demo")
        group = optparse_utils.add_option_group(parser, "Advanced", "advanced options")
        optparse_utils.add_option(group, "--level")
        help_text = optparse_utils.format_help(parser)
        self.assertIn("Advanced", help_text)
        self.assertIn("advanced options", help_text)

    def test_add_option_group_rejects_invalid_arguments(self) -> None:
        parser = optparse_utils.make_parser(prog="demo")
        with self.assertRaises(TypeError):
            optparse_utils.add_option_group(parser, 42)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            optparse_utils.add_option_group(parser, "Advanced", 42)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            optparse_utils.add_option_group(object(), "Advanced")  # type: ignore[arg-type]


class TestParseArgs(unittest.TestCase):
    """Exercise the parsing helper."""

    def setUp(self) -> None:
        self.parser = optparse_utils.make_parser(prog="demo")
        optparse_utils.add_option(self.parser, "--file")
        optparse_utils.add_flag(self.parser, "--verbose")

    def test_parse_args_returns_values_and_arguments(self) -> None:
        options, remaining = optparse_utils.parse_args(
            self.parser, ["--file", "demo.txt", "extra"]
        )
        self.assertEqual(options.file, "demo.txt")
        self.assertEqual(remaining, ["extra"])

    def test_parse_args_uses_sys_argv(self) -> None:
        with mock.patch.object(sys, "argv", ["demo", "--file", "demo.txt"]):
            options, remaining = optparse_utils.parse_args(self.parser)
        self.assertEqual(options.file, "demo.txt")
        self.assertEqual(remaining, [])

    def test_parse_args_exits_on_an_unknown_option(self) -> None:
        buffer = StringIO()
        with redirect_stderr(buffer):
            with self.assertRaises(SystemExit) as raised:
                optparse_utils.parse_args(self.parser, ["--unknown"])
        self.assertEqual(raised.exception.code, 2)
        self.assertIn("no such option", buffer.getvalue())

    def test_parse_args_raises_on_an_unknown_option(self) -> None:
        with self.assertRaises(optparse_utils.OptionParseError) as raised:
            optparse_utils.parse_args(self.parser, ["--unknown"], on_error="raise")
        self.assertIn("no such option", str(raised.exception))

    def test_parse_args_error_is_an_option_error(self) -> None:
        with self.assertRaises(optparse_utils.OptionError):
            optparse_utils.parse_args(self.parser, ["--unknown"], on_error="raise")

    def test_parse_args_rejects_an_invalid_mode(self) -> None:
        with self.assertRaises(ValueError):
            optparse_utils.parse_args(self.parser, [], on_error="ignore")

    def test_parse_args_rejects_invalid_arguments(self) -> None:
        with self.assertRaises(TypeError):
            optparse_utils.parse_args(self.parser, "--file")
        with self.assertRaises(TypeError):
            optparse_utils.parse_args(self.parser, [42])  # type: ignore[list-item]
        with self.assertRaises(TypeError):
            optparse_utils.parse_args(object(), [])  # type: ignore[arg-type]


class TestParserQueries(unittest.TestCase):
    """Exercise the query and mutation helpers."""

    def setUp(self) -> None:
        self.parser = optparse_utils.make_parser(prog="demo")
        optparse_utils.add_option(self.parser, "--file", help_text="the file")

    def test_get_option_returns_the_option(self) -> None:
        option = optparse_utils.get_option(self.parser, "--file")
        self.assertIsInstance(option, optparse_utils.Option)
        assert option is not None
        self.assertEqual(option.dest, "file")

    def test_get_option_returns_none_for_unknown_options(self) -> None:
        self.assertIsNone(optparse_utils.get_option(self.parser, "--unknown"))

    def test_has_option_reports_known_options(self) -> None:
        self.assertTrue(optparse_utils.has_option(self.parser, "--file"))
        self.assertFalse(optparse_utils.has_option(self.parser, "--unknown"))

    def test_remove_option_drops_the_option(self) -> None:
        optparse_utils.remove_option(self.parser, "--file")
        self.assertFalse(self.parser.has_option("--file"))

    def test_remove_option_rejects_unknown_options(self) -> None:
        with self.assertRaises(ValueError):
            optparse_utils.remove_option(self.parser, "--unknown")

    def test_queries_reject_invalid_arguments(self) -> None:
        with self.assertRaises(TypeError):
            optparse_utils.get_option(self.parser, 42)  # type: ignore[arg-type]
        with self.assertRaises(ValueError):
            optparse_utils.get_option(self.parser, "file")
        with self.assertRaises(TypeError):
            optparse_utils.has_option(object(), "--file")  # type: ignore[arg-type]

    def test_get_default_values_returns_the_defaults(self) -> None:
        defaults = optparse_utils.get_default_values(self.parser)
        self.assertIsInstance(defaults, optparse_utils.Values)
        self.assertIsNone(defaults.file)

    def test_set_defaults_changes_the_defaults(self) -> None:
        optparse_utils.set_defaults(self.parser, file="fallback")
        defaults = optparse_utils.get_default_values(self.parser)
        self.assertEqual(defaults.file, "fallback")

    def test_set_defaults_rejects_invalid_arguments(self) -> None:
        with self.assertRaises(TypeError):
            optparse_utils.set_defaults(object(), file="fallback")  # type: ignore[arg-type]

    def test_help_helpers_return_text(self) -> None:
        self.assertIn("demo", optparse_utils.get_usage(self.parser))
        self.assertIn("demo", optparse_utils.format_usage(self.parser))
        self.assertIn("the file", optparse_utils.format_help(self.parser))
        self.assertEqual(optparse_utils.get_prog_name(self.parser), "demo")
    def test_format_option_help_describes_a_single_option(self) -> None:
        option = optparse_utils.get_option(self.parser, "--file")
        self.assertIsNotNone(option)
        assert option is not None
        self.assertIn("the file", optparse_utils.format_option_help(self.parser, option))

    def test_format_option_help_rejects_foreign_options(self) -> None:
        with self.assertRaises(TypeError):
            optparse_utils.format_option_help(self.parser, object())  # type: ignore[arg-type]


class TestSuppressedOptions(unittest.TestCase):
    """Exercise the suppression constants."""

    def test_suppressed_option_is_hidden_from_the_help(self) -> None:
        parser = optparse_utils.make_parser(prog="demo")
        optparse_utils.add_option(
            parser, "--secret", help_text=optparse_utils.SUPPRESS_HELP
        )
        self.assertNotIn("secret", optparse_utils.format_help(parser))
        self.assertTrue(parser.has_option("--secret"))

    def test_suppressed_usage_is_honoured(self) -> None:
        parser = optparse_utils.make_parser(
            prog="demo", usage=optparse_utils.SUPPRESS_USAGE
        )
        self.assertEqual(optparse_utils.get_usage(parser), "")


class TestDestFor(unittest.TestCase):
    """Exercise the destination helper."""

    def test_dest_for_uses_the_long_option(self) -> None:
        self.assertEqual(optparse_utils.dest_for("--dry-run"), "dry_run")

    def test_dest_for_uses_the_short_option(self) -> None:
        self.assertEqual(optparse_utils.dest_for("-f"), "f")

    def test_dest_for_prefers_the_long_option(self) -> None:
        self.assertEqual(optparse_utils.dest_for("-f", "--file"), "file")

    def test_dest_for_rejects_invalid_arguments(self) -> None:
        with self.assertRaises(ValueError):
            optparse_utils.dest_for()
        with self.assertRaises(ValueError):
            optparse_utils.dest_for("file")
        with self.assertRaises(TypeError):
            optparse_utils.dest_for(42)  # type: ignore[arg-type]


class TestConverters(unittest.TestCase):
    """Exercise the value converters."""

    def test_string_type_returns_the_value(self) -> None:
        self.assertEqual(optparse_utils.string_type("demo"), "demo")

    def test_string_type_rejects_other_types(self) -> None:
        with self.assertRaises(TypeError):
            optparse_utils.string_type(42)  # type: ignore[arg-type]

    def test_int_type_converts_the_value(self) -> None:
        self.assertEqual(optparse_utils.int_type("7"), 7)

    def test_int_type_rejects_invalid_values(self) -> None:
        with self.assertRaises(optparse_utils.OptionValueError):
            optparse_utils.int_type("seven")
        with self.assertRaises(TypeError):
            optparse_utils.int_type(7)  # type: ignore[arg-type]

    def test_float_type_converts_the_value(self) -> None:
        self.assertEqual(optparse_utils.float_type("1.5"), 1.5)

    def test_float_type_rejects_invalid_values(self) -> None:
        with self.assertRaises(optparse_utils.OptionValueError):
            optparse_utils.float_type("one point five")
        with self.assertRaises(TypeError):
            optparse_utils.float_type(1.5)  # type: ignore[arg-type]

    def test_choice_type_accepts_a_known_choice(self) -> None:
        convert = optparse_utils.choice_type(["fast", "slow"])
        self.assertEqual(convert("fast"), "fast")

    def test_choice_type_rejects_an_unknown_choice(self) -> None:
        convert = optparse_utils.choice_type(["fast", "slow"])
        with self.assertRaises(optparse_utils.OptionValueError):
            convert("medium")

    def test_choice_type_rejects_invalid_choices(self) -> None:
        with self.assertRaises(TypeError):
            optparse_utils.choice_type("fast")
        with self.assertRaises(TypeError):
            optparse_utils.choice_type([42])  # type: ignore[list-item]
        with self.assertRaises(ValueError):
            optparse_utils.choice_type([])


class TestValuesToDict(unittest.TestCase):
    """Exercise the values helper."""

    def test_values_to_dict_returns_the_values(self) -> None:
        parser = optparse_utils.make_parser(prog="demo")
        optparse_utils.add_option(parser, "--file", default="fallback")
        options, _ = optparse_utils.parse_args(parser, [])
        values = optparse_utils.values_to_dict(options)
        self.assertIsInstance(values, dict)
        self.assertEqual(values["file"], "fallback")

    def test_values_to_dict_rejects_foreign_values(self) -> None:
        with self.assertRaises(TypeError):
            optparse_utils.values_to_dict({"file": "fallback"})  # type: ignore[arg-type]


if __name__ == "__main__":
    unittest.main()
