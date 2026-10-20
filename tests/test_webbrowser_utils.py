import unittest
from unittest.mock import patch

from webbrowser_utils import (
    Error,
    get_controller,
    open_new,
    open_new_tab,
    open_url,
    register_browser,
    register_standard_browsers,
)


class TestWebbrowserUtils(unittest.TestCase):
    def test_open_url_invalid(self):
        with self.assertRaises(ValueError):
            open_url("")
        with self.assertRaises(TypeError):
            open_url(123)  # type: ignore[arg-type]
        with self.assertRaises(ValueError):
            open_url("http://x", new=5)
        with self.assertRaises(TypeError):
            open_url("http://x", new="1")  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            open_url("http://x", autoraise="yes")  # type: ignore[arg-type]

    @patch("webbrowser_utils._webbrowser.open", return_value=True)
    def test_open_url(self, mock_open):
        self.assertTrue(open_url("http://example.com", new=1, autoraise=False))
        mock_open.assert_called_with("http://example.com", new=1, autoraise=False)

    @patch("webbrowser_utils._webbrowser.open", return_value=False)
    def test_open_url_reports_failure(self, mock_open):
        self.assertFalse(open_url("http://example.com"))
        mock_open.assert_called_once()

    @patch("webbrowser_utils._webbrowser.open_new", return_value=True)
    def test_open_new(self, mock_open):
        self.assertTrue(open_new("http://example.com"))
        mock_open.assert_called_with("http://example.com")

    @patch("webbrowser_utils._webbrowser.open_new_tab", return_value=True)
    def test_open_new_tab(self, mock_open):
        self.assertTrue(open_new_tab("http://example.com"))
        mock_open.assert_called_with("http://example.com")

    def test_open_new_invalid(self):
        with self.assertRaises(ValueError):
            open_new("")
        with self.assertRaises(TypeError):
            open_new(None)  # type: ignore[arg-type]

    def test_open_new_tab_invalid(self):
        with self.assertRaises(ValueError):
            open_new_tab("")
        with self.assertRaises(TypeError):
            open_new_tab(None)  # type: ignore[arg-type]

    @patch("webbrowser_utils._webbrowser.get", return_value="ctrl")
    def test_get_controller(self, mock_get):
        self.assertEqual(get_controller("firefox"), "ctrl")
        mock_get.assert_called_with("firefox")

    @patch("webbrowser_utils._webbrowser.get", return_value="ctrl")
    def test_get_controller_default(self, mock_get):
        self.assertEqual(get_controller(), "ctrl")
        mock_get.assert_called_with(None)

    def test_get_controller_invalid(self):
        with self.assertRaises(ValueError):
            get_controller("")
        with self.assertRaises(TypeError):
            get_controller(5)  # type: ignore[arg-type]

    @patch("webbrowser_utils._webbrowser.register")
    def test_register_browser(self, mock_reg):
        class K:
            pass

        register_browser("mybrowser", K, preferred=True)
        mock_reg.assert_called_with("mybrowser", K, None, preferred=True)

    def test_register_browser_invalid(self):
        with self.assertRaises(ValueError):
            register_browser("", object)
        with self.assertRaises(TypeError):
            register_browser(5, object)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            register_browser("name", object, preferred="yes")  # type: ignore[arg-type]

    @patch("webbrowser_utils._webbrowser.register_standard_browsers")
    def test_register_standard_browsers(self, mock_register):
        register_standard_browsers()
        mock_register.assert_called_once_with()

    def test_error_is_exception(self):
        self.assertTrue(issubclass(Error, Exception))


if __name__ == "__main__":
    unittest.main()
