"""Tests for gettext_utils module."""

import builtins
import unittest

from gettext_utils import (
    bindtextdomain,
    dgettext,
    dngettext,
    gettext,
    install,
    ngettext,
    textdomain,
)


class TestGettext(unittest.TestCase):
    def test_returns_message_when_no_translation(self):
        self.assertEqual(gettext("Hello"), "Hello")
        self.assertEqual(gettext("Goodbye"), "Goodbye")

    def test_returns_empty_string_when_set_empty(self):
        self.assertEqual(gettext(""), "")

    def test_non_string_raises(self):
        with self.assertRaises(TypeError):
            gettext(123)  # type: ignore[arg-type]


class TestDgettext(unittest.TestCase):
    def test_returns_message_when_no_translation(self):
        self.assertEqual(dgettext("messages", "Hello"), "Hello")

    def test_non_string_domain_raises(self):
        with self.assertRaises(TypeError):
            dgettext(123, "Hello")  # type: ignore[arg-type]

    def test_non_string_message_raises(self):
        with self.assertRaises(TypeError):
            dgettext("messages", 123)  # type: ignore[arg-type]


class TestNgettext(unittest.TestCase):
    def test_returns_singular_for_one(self):
        self.assertEqual(ngettext("one item", "many items", 1), "one item")

    def test_returns_plural_for_zero(self):
        self.assertEqual(ngettext("one item", "many items", 0), "many items")

    def test_returns_plural_for_other(self):
        self.assertEqual(ngettext("one item", "many items", 2), "many items")
        self.assertEqual(ngettext("one item", "many items", 10), "many items")

    def test_type_errors(self):
        with self.assertRaises(TypeError):
            ngettext(123, "many", 1)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            ngettext("one", 123, 1)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            ngettext("one", "many", "1")  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            ngettext("one", "many", True)  # type: ignore[arg-type]


class TestDngettext(unittest.TestCase):
    def test_returns_singular_for_one(self):
        self.assertEqual(dngettext("messages", "one item", "many items", 1), "one item")

    def test_returns_plural_for_other(self):
        self.assertEqual(dngettext("messages", "one item", "many items", 2), "many items")
        self.assertEqual(dngettext("messages", "one item", "many items", 0), "many items")

    def test_type_errors(self):
        with self.assertRaises(TypeError):
            dngettext(123, "one", "many", 1)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            dngettext("messages", 123, "many", 1)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            dngettext("messages", "one", 123, 1)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            dngettext("messages", "one", "many", "1")  # type: ignore[arg-type]


class TestTextdomain(unittest.TestCase):
    def test_set_and_get_domain(self):
        self.assertEqual(textdomain("myapp"), "myapp")
        self.assertEqual(textdomain(), "myapp")

    def test_none_returns_current_domain(self):
        textdomain("myapp")
        self.assertEqual(textdomain(None), "myapp")

    def test_invalid_type_raises(self):
        with self.assertRaises(TypeError):
            textdomain(123)  # type: ignore[arg-type]


class TestBindtextdomain(unittest.TestCase):
    def test_set_and_get_binding(self):
        self.assertEqual(bindtextdomain("myapp", "/tmp/locale"), "/tmp/locale")
        self.assertEqual(bindtextdomain("myapp"), "/tmp/locale")

    def test_none_localedir_returns_binding(self):
        bindtextdomain("myapp", "/tmp/locale")
        self.assertEqual(bindtextdomain("myapp", None), "/tmp/locale")

    def test_type_errors(self):
        with self.assertRaises(TypeError):
            bindtextdomain(123)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            bindtextdomain("myapp", 123)  # type: ignore[arg-type]
class TestInstall(unittest.TestCase):
    def test_installs_underscore_in_builtins(self):
        try:
            install("myapp", names=("gettext", "ngettext"))
            self.assertTrue(callable(builtins._))
            self.assertEqual(builtins._("Hello"), "Hello")
        finally:
            if hasattr(builtins, "_"):
                del builtins._

    def test_rejects_non_iterable_names(self):
        with self.assertRaises(TypeError):
            install("myapp", names=123)  # type: ignore[arg-type]

    def test_rejects_non_string_domain(self):
        with self.assertRaises(TypeError):
            install(123)  # type: ignore[arg-type]


if __name__ == "__main__":
    unittest.main()
