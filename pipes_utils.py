"""Pipeline utilities wrapping the standard library :mod:`pipes`."""

from __future__ import annotations

import shlex
from typing import Any

try:
    import pipes as _pipes
    _PIPES_AVAILABLE = True
except Exception:  # pragma: no cover - exercised when pipes is unavailable
    _pipes = None  # type: ignore[assignment]
    _PIPES_AVAILABLE = False

__all__: list[str] = [
    "Template",
    "quote",
    "quote_command",
    "create_template",
    "is_available",
    "make_pipeline",
    "step_kinds",
]


def _require_pipes(name: str) -> None:
    if not _PIPES_AVAILABLE:
        raise RuntimeError(f"pipes module is not available; {name} cannot be used")


if _PIPES_AVAILABLE:
    Template = _pipes.Template
    quote = _pipes.quote
else:  # pragma: no cover - exercised when pipes is unavailable
    class Template:  # type: ignore[no-redef]
        def __init__(self, *args: Any, **kwargs: Any) -> None:
            raise RuntimeError("pipes module is not available")

    def quote(value: str) -> str:  # type: ignore[misc]
        return shlex.quote(value)


def quote_command(command: str) -> str:
    """Quote a command for shell safety."""
    if not isinstance(command, str):
        raise TypeError("command must be a str")
    return quote(command)


def create_template() -> Template:
    """Create a new pipeline template."""
    _require_pipes("create_template")
    return _pipes.Template()


def is_available() -> bool:
    """Return True if the standard library :mod:`pipes` module is available."""
    return _PIPES_AVAILABLE


def make_pipeline(*commands: str) -> Template:
    """Create a pipeline template from commands."""
    for cmd in commands:
        if not isinstance(cmd, str):
            raise TypeError("commands must be strings")
    _require_pipes("make_pipeline")
    t = _pipes.Template()
    # pipes.Template uses different API; just return configured template
    for cmd in commands:
        t.append(cmd, "--")  # simple form
    return t


def step_kinds() -> list[str]:
    """Return supported pipeline step kinds."""
    return ["FILEIN", "FILEOUT", "SOURCE", "SINK"]
