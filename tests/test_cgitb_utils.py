"""Tests for cgitb_utils."""

import sys
import unittest

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


if __name__ == "__main__":
    unittest.main()
