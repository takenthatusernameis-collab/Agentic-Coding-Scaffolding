"""Tests for readline_utils.

The tests never touch the history file or the init file of the user: every
file is created in a temporary directory the test owns, and the state the
standard library keeps between two calls is restored after every test.  The
suite needs no terminal and no network.
"""

import os
import tempfile
import unittest
from unittest import mock

import readline_utils

try:
    import readline as _readline
except ImportError:  # pragma: no cover - the module is Unix-only
    _readline = None  # type: ignore[assignment]


@unittest.skipUnless(readline_utils.is_available(), "readline module not available")
class TestModuleContract(unittest.TestCase):
    """Verify the contract of the module."""

    def test_all_is_sorted_and_unique(self):
        self.assertEqual(readline_utils.__all__, sorted(set(readline_utils.__all__)))

    def test_every_name_exists(self):
        for name in readline_utils.__all__:
            self.assertTrue(hasattr(readline_utils, name), name)

    def test_is_available_reports_a_bool(self):
        self.assertIsInstance(readline_utils.is_available(), bool)

    def test_is_available_matches_the_standard_library(self):
        self.assertEqual(readline_utils.is_available(), _readline is not None)

    def test_the_default_history_file_is_the_history_of_the_user(self):
        self.assertEqual(
            readline_utils.default_history_file(),
            os.path.expanduser("~/.history"),
        )


@unittest.skipUnless(readline_utils.is_available(), "readline module not available")
class TestValidation(unittest.TestCase):
    """Verify the validation of the arguments.

    The arguments are validated before the standard library is reached, so the
    same error is raised on an interpreter that does not ship the module.
    """

    def setUp(self):
        patcher = mock.patch("readline_utils._readline")
        self.module = patcher.start()
        self.addCleanup(patcher.stop)

    def test_the_text_arguments_must_be_strings(self):
        for call in (
            lambda: readline_utils.parse_and_bind(42),
            lambda: readline_utils.add_history(42),
            lambda: readline_utils.insert_text(42),
            lambda: readline_utils.set_completer_delims(42),
            lambda: readline_utils.search_history(42),
            lambda: readline_utils.replace_history_item(1, 42),
        ):
            with self.assertRaises(TypeError):
                call()

    def test_the_file_arguments_must_be_paths(self):
        for call in (
            lambda: readline_utils.read_init_file(42),
            lambda: readline_utils.read_history_file(42),
            lambda: readline_utils.write_history_file(42),
            lambda: readline_utils.append_history_file(1, 42),
        ):
            with self.assertRaises(TypeError):
                call()

    def test_the_file_arguments_must_not_be_empty(self):
        for call in (
            lambda: readline_utils.read_init_file(""),
            lambda: readline_utils.read_history_file(""),
            lambda: readline_utils.write_history_file(""),
            lambda: readline_utils.append_history_file(1, ""),
        ):
            with self.assertRaises(ValueError):
                call()

    def test_the_positions_must_be_integers(self):
        for call in (
            lambda: readline_utils.get_history_item("1"),
            lambda: readline_utils.remove_history_item("1"),
            lambda: readline_utils.replace_history_item("1", "line"),
        ):
            with self.assertRaises(TypeError):
                call()

    def test_the_positions_must_not_be_booleans(self):
        with self.assertRaises(TypeError):
            readline_utils.get_history_item(True)

    def test_the_positions_must_start_at_one(self):
        for call in (
            lambda: readline_utils.get_history_item(0),
            lambda: readline_utils.remove_history_item(0),
            lambda: readline_utils.replace_history_item(0, "line"),
        ):
            with self.assertRaises(ValueError):
                call()

    def test_the_count_must_be_an_integer(self):
        with self.assertRaises(TypeError):
            readline_utils.append_history_file("1", "history")
        with self.assertRaises(TypeError):
            readline_utils.append_history_file(True, "history")

    def test_the_count_must_not_be_negative(self):
        with self.assertRaises(ValueError):
            readline_utils.append_history_file(-1, "history")

    def test_the_length_of_the_history_must_be_an_integer(self):
        with self.assertRaises(TypeError):
            readline_utils.set_history_length("10")
        with self.assertRaises(TypeError):
            readline_utils.set_history_length(True)

    def test_the_automatic_history_must_be_a_boolean(self):
        with self.assertRaises(TypeError):
            readline_utils.set_auto_history("yes")

    def test_the_hooks_must_be_callable(self):
        for call in (
            lambda: readline_utils.set_completer("completer"),
            lambda: readline_utils.set_startup_hook("hook"),
            lambda: readline_utils.set_pre_input_hook("hook"),
            lambda: readline_utils.set_completion_display_matches_hook("hook"),
        ):
            with self.assertRaises(TypeError):
                call()

    def test_the_standard_library_is_not_reached(self):
        with self.assertRaises(TypeError):
            readline_utils.add_history(42)
        self.module.add_history.assert_not_called()
        with self.assertRaises(ValueError):
            readline_utils.get_history_item(0)
        self.module.get_history_item.assert_not_called()


@unittest.skipUnless(readline_utils.is_available(), "readline module not available")
class TestDegradation(unittest.TestCase):
    """Verify the behavior on an interpreter that does not ship the module."""

    def setUp(self):
        patcher = mock.patch("readline_utils._readline", None)
        patcher.start()
        self.addCleanup(patcher.stop)

    def test_the_helpers_report_the_missing_module(self):
        for call in (
            lambda: readline_utils.parse_and_bind("set editing-mode emacs"),
            lambda: readline_utils.read_init_file("inputrc"),
            lambda: readline_utils.read_history_file("history"),
            lambda: readline_utils.write_history_file("history"),
            lambda: readline_utils.append_history_file(1, "history"),
            lambda: readline_utils.set_history_length(10),
            lambda: readline_utils.get_history_length(),
            lambda: readline_utils.get_current_history_length(),
            lambda: readline_utils.add_history("line"),
            lambda: readline_utils.clear_history(),
            lambda: readline_utils.get_history_item(1),
            lambda: readline_utils.remove_history_item(1),
            lambda: readline_utils.replace_history_item(1, "line"),
            lambda: readline_utils.history_items(),
            lambda: readline_utils.search_history("line"),
            lambda: readline_utils.set_completer(print),
            lambda: readline_utils.get_completer(),
            lambda: readline_utils.set_completer_delims(" "),
            lambda: readline_utils.get_completer_delims(),
            lambda: readline_utils.set_startup_hook(print),
            lambda: readline_utils.set_pre_input_hook(print),
            lambda: readline_utils.set_completion_display_matches_hook(print),
            lambda: readline_utils.get_completion_type(),
            lambda: readline_utils.get_begidx(),
            lambda: readline_utils.get_endidx(),
            lambda: readline_utils.get_line_buffer(),
            lambda: readline_utils.insert_text("text"),
            lambda: readline_utils.redisplay(),
            lambda: readline_utils.set_auto_history(True),
        ):
            with self.assertRaises(RuntimeError):
                call()


class TestHistory(unittest.TestCase):
    """Verify the helpers that work on the history of the editor."""

    def setUp(self):
        if not readline_utils.is_available():
            self.skipTest("readline module not available")
        readline_utils.clear_history()
        self.addCleanup(readline_utils.clear_history)

    def test_the_history_starts_empty(self):
        self.assertEqual(readline_utils.get_current_history_length(), 0)
        self.assertEqual(readline_utils.history_items(), [])

    def test_an_added_line_is_the_last_entry(self):
        readline_utils.add_history("first")
        readline_utils.add_history("second")
        self.assertEqual(readline_utils.get_current_history_length(), 2)
        self.assertEqual(readline_utils.get_history_item(1), "first")
        self.assertEqual(readline_utils.get_history_item(2), "second")

    def test_the_history_is_returned_as_a_list(self):
        readline_utils.add_history("first")
        readline_utils.add_history("second")
        self.assertEqual(readline_utils.history_items(), ["first", "second"])

    def test_an_entry_outside_the_history_is_none(self):
        readline_utils.add_history("first")
        self.assertIsNone(readline_utils.get_history_item(2))

    def test_the_history_is_cleared(self):
        readline_utils.add_history("first")
        readline_utils.clear_history()
        self.assertEqual(readline_utils.get_current_history_length(), 0)
        self.assertIsNone(readline_utils.get_history_item(1))

    def test_an_entry_is_removed_by_its_position(self):
        readline_utils.add_history("first")
        readline_utils.add_history("second")
        removed = readline_utils.remove_history_item(1)
        self.assertEqual(removed, "first")
        self.assertEqual(readline_utils.history_items(), ["second"])

    def test_an_entry_outside_the_history_cannot_be_removed(self):
        readline_utils.add_history("first")
        with self.assertRaises(ValueError):
            readline_utils.remove_history_item(2)

    def test_an_entry_is_replaced_by_its_position(self):
        readline_utils.add_history("first")
        readline_utils.add_history("second")
        replaced = readline_utils.replace_history_item(2, "other")
        self.assertEqual(replaced, "second")
        self.assertEqual(readline_utils.history_items(), ["first", "other"])

    def test_an_entry_outside_the_history_cannot_be_replaced(self):
        readline_utils.add_history("first")
        with self.assertRaises(ValueError):
            readline_utils.replace_history_item(5, "other")

    def test_the_entries_that_start_with_a_prefix_are_found(self):
        readline_utils.add_history("first")
        readline_utils.add_history("second")
        readline_utils.add_history("first again")
        self.assertEqual(
            readline_utils.search_history("first"),
            ["first", "first again"],
        )

    def test_the_entries_that_start_with_an_unknown_prefix_are_empty(self):
        readline_utils.add_history("first")
        self.assertEqual(readline_utils.search_history("other"), [])

    def test_the_maximal_length_of_the_history_is_reported(self):
        readline_utils.set_history_length(5)
        self.addCleanup(readline_utils.set_history_length, -1)
        self.assertEqual(readline_utils.get_history_length(), 5)

    def test_the_truncation_of_the_history_file_is_inhibited_by_default(self):
        self.assertLess(readline_utils.get_history_length(), 0)


class TestFiles(unittest.TestCase):
    """Verify the helpers that read and write files."""

    def setUp(self):
        if not readline_utils.is_available():
            self.skipTest("readline module not available")
        readline_utils.clear_history()
        self.addCleanup(readline_utils.clear_history)
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.path = os.path.join(self.directory.name, "history")

    def test_the_history_is_written_and_read_again(self):
        readline_utils.add_history("first")
        readline_utils.add_history("second")
        written = readline_utils.write_history_file(self.path)
        self.assertEqual(written, self.path)
        readline_utils.clear_history()
        readline_utils.read_history_file(self.path)
        self.assertEqual(readline_utils.history_items(), ["first", "second"])

    def test_the_entries_are_appended_to_the_file(self):
        readline_utils.add_history("first")
        readline_utils.add_history("second")
        readline_utils.write_history_file(self.path)
        readline_utils.add_history("third")
        appended = readline_utils.append_history_file(1, self.path)
        self.assertEqual(appended, self.path)
        with open(self.path, encoding="utf-8") as handle:
            self.assertEqual(handle.read().splitlines(), ["first", "second", "third"])

    def test_a_missing_history_file_is_reported(self):
        with self.assertRaises(OSError):
            readline_utils.read_history_file(self.path)

    def test_an_init_file_is_executed(self):
        path = os.path.join(self.directory.name, "inputrc")
        with open(path, "w", encoding="utf-8") as handle:
            handle.write("set editing-mode emacs\n")
        self.assertEqual(readline_utils.read_init_file(path), path)

    def test_a_missing_init_file_is_reported(self):
        with self.assertRaises(OSError):
            readline_utils.read_init_file(os.path.join(self.directory.name, "missing"))


class TestCompletion(unittest.TestCase):
    """Verify the helpers of the tab completion."""

    def setUp(self):
        if not readline_utils.is_available():
            self.skipTest("readline module not available")
        delimiters = readline_utils.get_completer_delims()
        self.addCleanup(readline_utils.set_completer_delims, delimiters)
        self.addCleanup(readline_utils.set_completer, None)

    def test_the_completer_is_set_and_removed(self):
        def completer(text, state):
            return None

        readline_utils.set_completer(completer)
        self.assertIs(readline_utils.get_completer(), completer)
        readline_utils.set_completer(None)
        self.assertIsNone(readline_utils.get_completer())

    def test_the_delimiters_are_set(self):
        readline_utils.set_completer_delims(" .")
        self.assertEqual(readline_utils.get_completer_delims(), " .")

    def test_a_completer_is_made_for_a_list_of_words(self):
        completer = readline_utils.make_completer(["gamma", "alpha", "beta"])
        self.assertEqual(completer("a", 0), "alpha")
        self.assertIsNone(completer("a", 1))

    def test_the_matches_of_a_completer_are_sorted(self):
        completer = readline_utils.make_completer(["beta", "alpha"])
        self.assertEqual(completer("", 0), "alpha")
        self.assertEqual(completer("", 1), "beta")
        self.assertIsNone(completer("", 2))

    def test_a_completer_ignores_a_duplicate_word(self):
        completer = readline_utils.make_completer(["alpha", "alpha"])
        self.assertEqual(completer("", 0), "alpha")
        self.assertIsNone(completer("", 1))

    def test_a_completer_validates_its_arguments(self):
        completer = readline_utils.make_completer(["alpha"])
        with self.assertRaises(TypeError):
            completer(42, 0)
        with self.assertRaises(TypeError):
            completer("a", "0")
        with self.assertRaises(ValueError):
            completer("a", -1)

    def test_the_words_must_be_strings(self):
        with self.assertRaises(TypeError):
            readline_utils.make_completer([42])
        with self.assertRaises(TypeError):
            readline_utils.make_completer("alpha")

    def test_the_type_of_the_completion_is_reported(self):
        self.assertIn(readline_utils.get_completion_type(), (0, 1, 2))


class TestEditor(unittest.TestCase):
    """Verify the helpers of the line editor."""

    def setUp(self):
        if not readline_utils.is_available():
            self.skipTest("readline module not available")
        self.addCleanup(readline_utils.set_auto_history, True)

    def test_the_line_buffer_is_reported(self):
        self.assertIsInstance(readline_utils.get_line_buffer(), str)

    def test_the_scope_of_the_completion_is_reported(self):
        self.assertIsInstance(readline_utils.get_begidx(), int)
        self.assertIsInstance(readline_utils.get_endidx(), int)

    def test_a_key_sequence_is_executed(self):
        self.assertIsNone(readline_utils.parse_and_bind("set editing-mode emacs"))

    def test_the_automatic_history_is_disabled_and_enabled(self):
        readline_utils.set_auto_history(False)
        readline_utils.set_auto_history(True)

    def test_the_hooks_of_the_editor_are_set_and_removed(self):
        readline_utils.set_startup_hook(lambda: None)
        readline_utils.set_startup_hook(None)
        if hasattr(_readline, "set_pre_input_hook"):
            readline_utils.set_pre_input_hook(lambda: None)
            readline_utils.set_pre_input_hook(None)
        readline_utils.set_completion_display_matches_hook(
            lambda substitution, matches, length: None
        )
        readline_utils.set_completion_display_matches_hook(None)

    def test_text_is_inserted_into_the_line_buffer(self):
        readline_utils.insert_text("text")
        readline_utils.redisplay()


if __name__ == "__main__":
    unittest.main()
