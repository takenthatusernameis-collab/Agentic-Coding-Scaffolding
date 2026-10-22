"""Pipeline utilities wrapping the standard library :mod:`pipes` module.

The :mod:`pipes` module can build pipelines from a series of shell commands
and run them.  A :class:`~pipes.Template` appends or prepends steps to a
pipeline, runs debug traces, and compiles the pipeline into a shell command
string.

This wrapper validates every argument before the standard library is reached, so
a caller gets a clear :class:`TypeError` or :class:`ValueError` instead of an
opaque failure from the standard library.  It re-exports the useful constants
and the :class:`Template` class, adds ``is_available`` to detect when the
interpreter ships the module, and normalizes the API.

.. note::

   The :mod:`pipes` module was deprecated in Python 3.11 and removed in Python
   3.13 as part of :pep:`594`.  The import below degrades gracefully: when the
   interpreter no longer ships the module, the helpers raise a
   :class:`RuntimeError` that names the missing module, while the helpers that
   need no standard library keep working.
"""

from __future__ import annotations

import warnings
from typing import Any, List

__all__ = [
    "FILEIN_FILEOUT",
    "FILEIN_STDOUT",
    "SINK",
    "SOURCE",
    "STDIN_FILEOUT",
    "STDIN_STDOUT",
    "Template",
    "create_template",
    "is_available",
    "make_pipeline",
    "quote",
    "quote_command",
    "step_kinds",
]

try:
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", DeprecationWarning)
        import pipes as _pipes
except ImportError:  # pragma: no cover - Python 3.13 removed the module
    _pipes = None  # type: ignore[assignment]

#: Step kind constants re-exported from the standard library.
FILEIN_FILEOUT = getattr(_pipes, "FILEIN_FILEOUT", "ff")
STDIN_FILEOUT = getattr(_pipes, "STDIN_FILEOUT", "-f")
FILEIN_STDOUT = getattr(_pipes, "FILEIN_STDOUT", "f-")
STDIN_STDOUT = getattr(_pipes, "STDIN_STDOUT", "--")
SOURCE = getattr(_pipes, "SOURCE", ".-")
SINK = getattr(_pipes, "SINK", "-.")

#: The kinds a pipeline step can have.
VALID_STEP_KINDS = (
    FILEIN_FILEOUT,
    STDIN_FILEOUT,
    FILEIN_STDOUT,
    STDIN_STDOUT,
    SOURCE,
    SINK,
)


def _pipes_module() -> Any:
    """Return the standard library ``pipes`` module.

    Returns:
        The imported :mod:`pipes` module.

    Raises:
        RuntimeError: If the interpreter no longer ships the ``pipes`` module.
    """
    if _pipes is None:  # pragma: no cover - Python 3.13 removed the module
        raise RuntimeError(
            "the standard library 'pipes' module was removed in Python 3.13; "
            "use the subprocess module to build pipelines instead"
        )
    return _pipes


def _require_str(value: Any, name: str) -> str:
    """Return *value* as a string, raising ``TypeError`` for other types."""
    if not isinstance(value, str):
        raise TypeError(f"{name} must be a str, got {type(value).__name__}")
    return value


def is_available() -> bool:
    """Return ``True`` when the standard library ships the ``pipes`` module."""
    return _pipes is not None


def quote(file: Any) -> str:
    """Return a shell-quoted version of *file*."""
    name = _require_str(file, "file")
    pipes_module = _pipes_module()
    return str(pipes_module.quote(name))


def quote_command(command: Any) -> str:
    """Return a shell-quoted version of *command*."""
    return quote(command)


def step_kinds() -> List[str]:
    """Return the valid kinds of pipeline steps."""
    return list(VALID_STEP_KINDS)


class _TemplateProxy:
    def __new__(cls, *args: Any, **kwargs: Any) -> Any:
        pipes_module = _pipes_module()
        return pipes_module.Template(*args, **kwargs)


# Re-export the standard library class
if _pipes is not None:
    Template = _pipes.Template  # type: ignore[misc,assignment]
else:
    Template = _TemplateProxy  # type: ignore[misc,assignment]


def create_template() -> Any:
    """Return a fresh pipeline template."""
    pipes_module = _pipes_module()
    return pipes_module.Template()


def make_pipeline(template: Any, infile: Any, outfile: Any) -> None:
    """Run a template as a pipeline."""
    _require_str(infile, "infile")
    _require_str(outfile, "outfile")
    pipes_module = _pipes_module()
    if not isinstance(template, pipes_module.Template):
        raise TypeError(f"template must be a pipes.Template, got {type(template).__name__}")
    pipes_module.Template.makepipeline(template, infile, outfile)
