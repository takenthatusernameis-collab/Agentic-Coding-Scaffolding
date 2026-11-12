"""Unit tests for argcomplete_utils.py."""

from __future__ import annotations

import argparse
import sys
import unittest
from unittest.mock import MagicMock, patch

try:
    import argcomplete_utils
except ImportError:
    argcomplete_utils = None  # type: ignore[assignment]


@unittest.skipIf(argcomplete_utils is None, "argcomplete_utils not importable")
class TestAvailability(unittest.TestCase):
    """Tests for module availability checking."""

    def test_is_available_returns_bool(self):
        """is_available should return a boolean."""
        self.assertIsInstance(argcomplete_utils.is_available(), bool)


@unittest.skipIf(argcomplete_utils is None, "argcomplete_utils not importable")
class TestModuleContract(unittest.TestCase):
    """Tests for module-level contract."""

    def test_all_is_sorted_and_unique(self):
        """__all__ should be sorted and contain unique entries."""
        all_list = argcomplete_utils.__all__
        self.assertEqual(all_list, sorted(all_list))
        self.assertEqual(len(all_list), len(set(all_list)))

    def test_every_name_exists(self):
        """Every name in __all__ should exist in the module."""
        for name in argcomplete_utils.__all__:
            self.assertTrue(hasattr(argcomplete_utils, name), name)

    def test_standard_library_not_imported_at_module_level(self):
        """argcomplete should not be imported at module level if not available."""
        if argcomplete_utils.is_available():
            import argcomplete

            self.assertIs(argcomplete_utils.argcomplete, argcomplete)
        else:
            self.assertIsNone(argcomplete_utils.argcomplete)


@unittest.skipIf(argcomplete_utils is None, "argcomplete_utils not importable")
class TestAutocomplete(unittest.TestCase):
    """Tests for autocomplete function."""

    def test_autocomplete_raises_import_error_when_unavailable(self):
        """autocomplete should raise ImportError when argcomplete is unavailable."""
        if argcomplete_utils.is_available():
            self.skipTest("argcomplete is available")

        parser = argparse.ArgumentParser()
        with self.assertRaisesRegex(ImportError, "argcomplete is not installed"):
            argcomplete_utils.autocomplete(parser)

    def test_autocomplete_raises_type_error_for_invalid_parser(self):
        """autocomplete should raise TypeError for non-ArgumentParser."""
        if not argcomplete_utils.is_available():
            self.skipTest("argcomplete not available")

        with self.assertRaisesRegex(TypeError, "Expected argparse.ArgumentParser"):
            argcomplete_utils.autocomplete("not a parser")

    @patch("argcomplete.autocomplete")
    def test_autocomplete_calls_argcomplete(self, mock_autocomplete):
        """autocomplete should delegate to argcomplete.autocomplete."""
        if not argcomplete_utils.is_available():
            self.skipTest("argcomplete not available")

        parser = argparse.ArgumentParser()
        argcomplete_utils.autocomplete(parser, always_complete_options=False)

        mock_autocomplete.assert_called_once_with(
            parser,
            always_complete_options=False,
            exit_method=sys.exit,
            print_suppressed=False,
        )


@unittest.skipIf(argcomplete_utils is None, "argcomplete_utils not importable")
class TestGetCompleter(unittest.TestCase):
    """Tests for get_completer function."""

    def test_get_completer_raises_import_error_when_unavailable(self):
        """get_completer should raise ImportError when argcomplete is unavailable."""
        if argcomplete_utils.is_available():
            self.skipTest("argcomplete is available")

        with self.assertRaisesRegex(ImportError, "argcomplete is not installed"):
            argcomplete_utils.get_completer({"a": "a", "b": "b"})

    def test_get_completer_raises_type_error_for_non_dict(self):
        """get_completer should raise TypeError for non-dict choices."""
        if not argcomplete_utils.is_available():
            self.skipTest("argcomplete not available")

        with self.assertRaisesRegex(TypeError, "choices must be dict"):
            argcomplete_utils.get_completer("not a dict")

    def test_get_completer_raises_type_error_for_non_string_choices(self):
        """get_completer should raise TypeError for non-string choices."""
        if not argcomplete_utils.is_available():
            self.skipTest("argcomplete not available")

        with self.assertRaisesRegex(TypeError, "all choices keys and values must be strings"):
            argcomplete_utils.get_completer({"a": 1})

    @patch("argcomplete_utils.ChoicesCompleter")
    def test_get_completer_returns_completer(self, mock_choices_completer):
        """get_completer should return a ChoicesCompleter instance."""
        if not argcomplete_utils.is_available():
            self.skipTest("argcomplete not available")

        mock_instance = MagicMock()
        mock_choices_completer.return_value = mock_instance

        result = argcomplete_utils.get_completer(
            {"option1": "option1", "option2": "option2"}
        )

        mock_choices_completer.assert_called_once_with(
            {"option1": "option1", "option2": "option2"}
        )
        self.assertIs(result, mock_instance)


@unittest.skipIf(argcomplete_utils is None, "argcomplete_utils not importable")
class TestGetFilesCompleter(unittest.TestCase):
    """Tests for get_files_completer function."""

    def test_get_files_completer_raises_import_error_when_unavailable(self):
        """get_files_completer should raise ImportError when argcomplete is unavailable."""
        if argcomplete_utils.is_available():
            self.skipTest("argcomplete is available")

        with self.assertRaisesRegex(ImportError, "argcomplete is not installed"):
            argcomplete_utils.get_files_completer()

    @patch("argcomplete_utils.FilesCompleter")
    def test_get_files_completer_returns_completer(self, mock_files_completer):
        """get_files_completer should return a FilesCompleter instance."""
        if not argcomplete_utils.is_available():
            self.skipTest("argcomplete not available")

        mock_instance = MagicMock()
        mock_files_completer.return_value = mock_instance

        result = argcomplete_utils.get_files_completer(directories=False)

        mock_files_completer.assert_called_once_with(allowednames=(), directories=False)
        self.assertIs(result, mock_instance)


if __name__ == "__main__":
    unittest.main()