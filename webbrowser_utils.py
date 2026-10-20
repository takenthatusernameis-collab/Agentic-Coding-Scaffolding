"""Web browser utilities wrapping the standard library :mod:`webbrowser` module.

The standard library module launches a browser for a URL and keeps a registry
of the browsers it knows about.  The helpers in this module validate their
arguments before the standard library is reached, so a caller gets a clear
``TypeError`` or ``ValueError`` instead of a browser failing halfway through a
launch.
"""

from __future__ import annotations

import webbrowser as _webbrowser
from typing import Any

__all__: list[str] = [
    "Error",
    "open_url",
    "open_new",
    "open_new_tab",
    "get_controller",
    "register_browser",
    "register_standard_browsers",
]

Error = _webbrowser.Error


def _require_url(url: object) -> str:
    """Return *url* when it is a usable URL string."""
    if not isinstance(url, str):
        raise TypeError(f"url must be a str, got {type(url).__name__}")
    if not url:
        raise ValueError("url must not be empty")
    return url


def _require_new(new: object) -> int:
    """Return *new* when it is one of the three documented window modes."""
    if isinstance(new, bool) or not isinstance(new, int):
        raise TypeError(f"new must be an int, got {type(new).__name__}")
    if new not in (0, 1, 2):
        raise ValueError(f"new must be 0, 1, or 2, got {new}")
    return new


def open_url(url: str, new: int = 0, autoraise: bool = True) -> bool:
    """Display *url* using the default browser.

    Args:
        url: The URL to open.
        new: 0 = same window, 1 = new window, 2 = new tab.
        autoraise: Whether to raise the window.

    Returns:
        True when a browser was launched successfully.

    Raises:
        TypeError: If an argument has the wrong type.
        ValueError: If the URL is empty or ``new`` is not a window mode.
    """
    _require_url(url)
    _require_new(new)
    if not isinstance(autoraise, bool):
        raise TypeError(f"autoraise must be a bool, got {type(autoraise).__name__}")
    return bool(_webbrowser.open(url, new=new, autoraise=autoraise))


def open_new(url: str) -> bool:
    """Open *url* in a new browser window.

    Args:
        url: The URL to open.

    Returns:
        True when a browser was launched successfully.
    """
    _require_url(url)
    return bool(_webbrowser.open_new(url))


def open_new_tab(url: str) -> bool:
    """Open *url* in a new browser tab.

    Args:
        url: The URL to open.

    Returns:
        True when a browser was launched successfully.
    """
    _require_url(url)
    return bool(_webbrowser.open_new_tab(url))


def get_controller(using: str | None = None) -> Any:
    """Return a browser controller.

    Args:
        using: The name of a registered browser, or ``None`` for the default.

    Returns:
        The controller object, or ``None`` when no browser is available.
    """
    if using is not None:
        if not isinstance(using, str):
            raise TypeError(f"using must be a str or None, got {type(using).__name__}")
        if not using:
            raise ValueError("using must not be empty")
    return _webbrowser.get(using)


def register_browser(
    name: str,
    klass: Any,
    instance: Any = None,
    *,
    preferred: bool = False,
) -> None:
    """Register a browser controller class under *name*.

    Args:
        name: The name the browser is registered under.
        klass: The controller class.
        instance: An optional controller instance used instead of *klass*.
        preferred: Whether the browser becomes the preferred one.
    """
    if not isinstance(name, str):
        raise TypeError(f"name must be a str, got {type(name).__name__}")
    if not name:
        raise ValueError("name must not be empty")
    if not isinstance(preferred, bool):
        raise TypeError(f"preferred must be a bool, got {type(preferred).__name__}")
    _webbrowser.register(name, klass, instance, preferred=preferred)


def register_standard_browsers() -> None:
    """Register the browsers the standard library can discover on this system."""
    _webbrowser.register_standard_browsers()
