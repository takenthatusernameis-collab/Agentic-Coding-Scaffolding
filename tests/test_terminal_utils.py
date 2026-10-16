"""Tests for terminal_utils module."""

import io
import unittest
from unittest.mock import patch

from terminal_utils import (
    ProgressBar,
    clear_screen,
    colorize,
    get_terminal_size,
    print_colored,
    progress_bar,
    prompt,
    supports_color,
)


class TestSupportsColor(unittest.TestCase):
    def test_returns_bool(self):
        self.assertIsInstance(supports_color(), bool)


class TestColorize(unittest.TestCase):
    def test_returns_plain_text_when_not_a_tty(self):
        self.assertEqual(colorize("hello", "red"), "hello")
        self.assertEqual(colorize("hello", "red", bold=True), "hello")

    def test_all_valid_colors_return_string(self):
        for color in ("black", "red", "green", "yellow", "blue", "magenta", "cyan", "white"):
            self.assertIsInstance(colorize("x", color), str)

    def test_invalid_color_raises_value_error(self):
        with self.assertRaises(ValueError):
            colorize("hello", "purple")

    def test_non_string_text_raises_type_error(self):
        with self.assertRaises(TypeError):
            colorize(123, "red")

    def test_non_string_color_raises_type_error(self):
        with self.assertRaises(TypeError):
            colorize("hello", 5)


class TestPrintColored(unittest.TestCase):
    def test_writes_to_stream(self):
        stream = io.StringIO()
        print_colored("hello", color="red", stream=stream)
        self.assertEqual(stream.getvalue(), "hello\n")

    def test_default_stream_is_stdout(self):
        with patch("sys.stdout", new_callable=io.StringIO) as mock_stdout:
            print_colored("hi")
            self.assertEqual(mock_stdout.getvalue(), "hi\n")


class TestClearScreen(unittest.TestCase):
    def test_writes_newlines_when_not_a_tty(self):
        stream = io.StringIO()
        with patch("terminal_utils.sys.stdout", stream):
            clear_screen()
        self.assertEqual(stream.getvalue(), "\n" * 50)


class TestGetTerminalSize(unittest.TestCase):
    def test_returns_tuple_of_two_positive_ints(self):
        columns, lines = get_terminal_size()
        self.assertIsInstance(columns, int)
        self.assertIsInstance(lines, int)
        self.assertGreater(columns, 0)
        self.assertGreater(lines, 0)


class TestProgressBar(unittest.TestCase):
    def test_total_must_be_positive(self):
        with self.assertRaises(ValueError):
            ProgressBar(0)
        with self.assertRaises(ValueError):
            ProgressBar(-3)
        with self.assertRaises(ValueError):
            ProgressBar(True)

    def test_fill_and_empty_must_be_single_characters(self):
        with self.assertRaises(ValueError):
            ProgressBar(1, fill="ab")
        with self.assertRaises(ValueError):
            ProgressBar(1, empty="")

    def test_render_shows_progress(self):
        stream = io.StringIO()
        bar = ProgressBar(10, width=10, stream=stream)
        bar.update(5)
        output = stream.getvalue()
        self.assertIn("[#####-----]", output)
        self.assertIn("50%", output)
        self.assertIn("(5/10)", output)

    def test_update_out_of_range_raises_value_error(self):
        bar = ProgressBar(5, stream=io.StringIO())
        with self.assertRaises(ValueError):
            bar.update(6)
        with self.assertRaises(ValueError):
            bar.update(-1)

    def test_update_non_integer_raises_type_error(self):
        bar = ProgressBar(5, stream=io.StringIO())
        with self.assertRaises(TypeError):
            bar.update("3")

    def test_update_after_finish_is_noop(self):
        stream = io.StringIO()
        bar = ProgressBar(2, stream=stream)
        bar.finish()
        before = stream.getvalue()
        bar.update(1)
        self.assertEqual(stream.getvalue(), before)

    def test_finish_writes_final_newline(self):
        stream = io.StringIO()
        bar = ProgressBar(3, stream=stream)
        bar.finish()
        self.assertIn("\n", stream.getvalue())

    def test_context_manager_finishes(self):
        stream = io.StringIO()
        with ProgressBar(4, stream=stream) as bar:
            bar.update(2)
        self.assertTrue(bar._finished)

    def test_yields_items(self):
        stream = io.StringIO()
        result = list(progress_bar([1, 2, 3], stream=stream))
        self.assertEqual(result, [1, 2, 3])

    def test_total_inferred_from_len(self):
        stream = io.StringIO()
        result = list(progress_bar([10, 20], stream=stream))
        self.assertEqual(result, [10, 20])

    def test_iterable_without_len_requires_total(self):
        def generator():
            yield 1
            yield 2

        with self.assertRaises(ValueError):
            list(progress_bar(generator()))

    def test_increment_advances(self):
        stream = io.StringIO()
        bar = ProgressBar(3, stream=stream)
        bar.update(increment=1)
        bar.update(increment=1)
        self.assertEqual(bar._current, 2)


class TestPrompt(unittest.TestCase):
    def test_returns_entered_value(self):
        with patch("builtins.input", return_value="Alice"):
            self.assertEqual(prompt("Name"), "Alice")

    def test_returns_default_on_empty_input(self):
        with patch("builtins.input", return_value=""):
            self.assertEqual(prompt("Name", default="Guest"), "Guest")

    def test_returns_empty_string_when_no_default(self):
        with patch("builtins.input", return_value=""):
            self.assertEqual(prompt("Name"), "")

    def test_raises_eof_error_on_closed_stream(self):
        with patch("builtins.input", side_effect=EOFError):
            with self.assertRaises(EOFError):
                prompt("Name")

    def test_non_string_message_raises_type_error(self):
        with self.assertRaises(TypeError):
            prompt(123)

    def test_non_string_default_raises_type_error(self):
        with self.assertRaises(TypeError):
            prompt("Name", default=5)


if __name__ == "__main__":
    unittest.main()
