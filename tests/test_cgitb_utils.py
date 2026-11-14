"""Tests for cgitb_utils."""

import importlib
import sys
import unittest
from unittest import mock

import cgitb_utils


class TestCgitbUtils(unittest.TestCase):
    def test_exports(self) -> None:
        for name in [
            "enable",
            "disable",
            "reset",
            "lookup",
            "scanvars",
            "handler",
            "text",
            "html",
            "small",
            "strong",
            "grey",
            "pink",
            "blue",
            "is_available",
        ]:
            self.assertTrue(hasattr(cgitb_utils, name))

    def test_is_available(self) -> None:
        self.assertIs(cgitb_utils.is_available(), True)

    def test_small_wraps_html(self) -> None:
        self.assertEqual(cgitb_utils.small("x"), "<small>x</small>")

    def test_strong_wraps_html(self) -> None:
        self.assertEqual(cgitb_utils.strong("x"), "<strong>x</strong>")

    def test_grey_wraps_html(self) -> None:
        self.assertEqual(cgitb_utils.grey("x"), '<font color="#909090">x</font>')

    def test_pink_wraps_html(self) -> None:
        self.assertEqual(cgitb_utils.pink("x"), "<span style='color: pink'>x</span>")

    def test_blue_wraps_html(self) -> None:
        self.assertEqual(cgitb_utils.blue("x"), "<span style='color: blue'>x</span>")

    def test_disable_does_not_raise(self) -> None:
        cgitb_utils.disable()
        self.assertIs(sys.excepthook, sys.__excepthook__)

    def test_unavailable_branch(self) -> None:
        try:
            with mock.patch.dict(sys.modules, {"cgitb": None}):
                reloaded = importlib.reload(cgitb_utils)
                self.assertIs(reloaded.is_available(), False)
                for name in [
                    "enable",
                    "reset",
                    "lookup",
                    "scanvars",
                    "handler",
                    "text",
                    "html",
                ]:
                    with self.assertRaises(RuntimeError):
                        getattr(reloaded, name)()
                # The pure HTML formatters do not depend on cgitb.
                self.assertEqual(reloaded.small("x"), "<small>x</small>")
                self.assertEqual(reloaded.strong("x"), "<strong>x</strong>")
                self.assertEqual(reloaded.grey("x"), '<font color="#909090">x</font>')
                self.assertEqual(
                    reloaded.pink("x"), "<span style='color: pink'>x</span>"
                )
                self.assertEqual(
                    reloaded.blue("x"), "<span style='color: blue'>x</span>"
                )
                reloaded.disable()
                self.assertIs(sys.excepthook, sys.__excepthook__)
        finally:
            importlib.reload(cgitb_utils)


if __name__ == "__main__":
    unittest.main()
