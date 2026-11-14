"""Cgitb utilities wrapping the standard library :mod:`cgitb`."""

from __future__ import annotations

import sys
from collections.abc import Callable
from typing import Any

try:
    import cgitb as _cgitb
    _CGITB_AVAILABLE = True
except Exception:  # pragma: no cover - exercised when cgitb is unavailable
    _cgitb = None  # type: ignore[assignment]
    _CGITB_AVAILABLE = False

__all__: list[str] = [
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
]


def _require_cgitb(name: str) -> None:
    if not _CGITB_AVAILABLE:
        raise RuntimeError(f"cgitb module is not available; {name} cannot be used")


if _CGITB_AVAILABLE:
    enable: Callable[..., Any] = _cgitb.enable
    reset: Callable[..., Any] = getattr(_cgitb, "reset", lambda: None)
    lookup: Callable[..., Any] = getattr(_cgitb, "lookup", lambda *args, **kwargs: None)
    scanvars: Callable[..., Any] = getattr(
        _cgitb, "scanvars", lambda *args, **kwargs: ([], [])
    )
    handler: Callable[..., Any] = getattr(_cgitb, "handler", lambda *args, **kwargs: None)
    text: Callable[..., Any] = getattr(_cgitb, "text", lambda *args, **kwargs: "")
    html: Callable[..., Any] = getattr(_cgitb, "html", lambda *args, **kwargs: "")
else:  # pragma: no cover - exercised when cgitb is unavailable
    def enable(*args: Any, **kwargs: Any) -> Any:  # type: ignore[no-redef]
        _require_cgitb("enable")

    def reset(*args: Any, **kwargs: Any) -> Any:  # type: ignore[no-redef]
        _require_cgitb("reset")

    def lookup(*args: Any, **kwargs: Any) -> Any:  # type: ignore[no-redef]
        _require_cgitb("lookup")

    def scanvars(*args: Any, **kwargs: Any) -> Any:  # type: ignore[no-redef]
        _require_cgitb("scanvars")

    def handler(*args: Any, **kwargs: Any) -> Any:  # type: ignore[no-redef]
        _require_cgitb("handler")

    def text(*args: Any, **kwargs: Any) -> Any:  # type: ignore[no-redef]
        _require_cgitb("text")

    def html(*args: Any, **kwargs: Any) -> Any:  # type: ignore[no-redef]
        _require_cgitb("html")


small: Callable[[Any], str] = getattr(
    _cgitb, "small", lambda value: f"<small>{value}</small>"
)
strong: Callable[[Any], str] = getattr(
    _cgitb, "strong", lambda value: f"<strong>{value}</strong>"
)
grey: Callable[[Any], str] = getattr(
    _cgitb, "grey", lambda value: f"<font color=\"#909090\">{value}</font>"
)
pink: Callable[[Any], str] = getattr(
    _cgitb, "pink", lambda value: f"<span style='color: pink'>{value}</span>"
)
blue: Callable[[Any], str] = getattr(
    _cgitb, "blue", lambda value: f"<span style='color: blue'>{value}</span>"
)


def disable() -> None:
    if _CGITB_AVAILABLE and hasattr(_cgitb, "disable"):
        _cgitb.disable()
        return
    sys.excepthook = sys.__excepthook__


def is_available() -> bool:
    """Return True if the standard library :mod:`cgitb` module is available."""
    return _CGITB_AVAILABLE
