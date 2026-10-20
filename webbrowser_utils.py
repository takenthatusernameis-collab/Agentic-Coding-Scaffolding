"""Utilities for launching and controlling web browsers (wrapping :mod:`webbrowser`)."""

import webbrowser as _webbrowser
from typing import Any

__all__ = [
    "Error",
    "open_url",
    "open_new",
    "open_new_tab",
    "get_controller",
    "register_browser",
]


class Error(_webbrowser.Error):
    """Re-exported :class:`webbrowser.Error`."""


def open_url(url: str, new: int = 0, autoraise: bool = True) -> bool:
    """Display *url* using the default browser.

    Args:
        url: The URL to open.
        new: 0 = same window, 1 = new window, 2 = new tab.
        autoraise: Whether to raise the window.

    Returns:
        True if a browser was successfully launched.
    """
    if not isinstance(url, str) or not url:
        raise ValueError("url must be a non-empty string")
    if new not in (0, 1, 2):
        raise ValueError("new must be 0, 1, or 2")
    return bool(_webbrowser.open(url, new=new, autoraise=autoraise))


def open_new(url: str) -> bool:
    """Open *url* in a new browser window."""
    if not isinstance(url, str) or not url:
        raise ValueError("url must be a non-empty string")
    return bool(_webbrowser.open_new(url))


def open_new_tab(url: str) -> bool:
    """Open *url* in a new browser tab."""
    if not isinstance(url, str) or not url:
        raise ValueError("url must be a non-empty string")
    return bool(_webbrowser.open_new_tab(url))


def get_controller(using: str | None = None) -> Any:
    """Return a browser controller for *using* (or the default)."""
    return _webbrowser.get(using)


def register_browser(
    name: str,
    klass: Any,
    instance: Any = None,
    *,
    preferred: bool = False,
) -> None:
    """Register a browser controller class."""
    if not isinstance(name, str) or not name:
        raise ValueError("name must be a non-empty string")
    _webbrowser.register(name, klass, instance, preferred=preferred)