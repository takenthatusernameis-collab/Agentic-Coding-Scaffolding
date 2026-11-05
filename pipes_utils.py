"""Pipeline utilities wrapping the standard library :mod:`pipes`."""

from __future__ import annotations

import pipes as _pipes

__all__: list[str] = [
    "Template",
    "quote",
    "quote_command",
    "create_template",
    "is_available",
    "make_pipeline",
    "step_kinds",
]

Template = _pipes.Template
quote = _pipes.quote


def quote_command(command: str) -> str:
    """Quote a command for shell safety."""
    if not isinstance(command, str):
        raise TypeError("command must be a str")
    return quote(command)


def create_template() -> _pipes.Template:
    """Create a new pipeline template."""
    return _pipes.Template()


def is_available() -> bool:
    """Return True if the standard library :mod:`pipes` module is available."""
    return True


def make_pipeline(*commands: str) -> _pipes.Template:
    """Create a pipeline template from commands."""
    for cmd in commands:
        if not isinstance(cmd, str):
            raise TypeError("commands must be strings")
    t = _pipes.Template()
    # pipes.Template uses different API; just return configured template
    for cmd in commands:
        t.append(cmd, "--")  # simple form
    return t


def step_kinds() -> list[str]:
    """Return supported pipeline step kinds."""
    return ["FILEIN", "FILEOUT", "SOURCE", "SINK"]
