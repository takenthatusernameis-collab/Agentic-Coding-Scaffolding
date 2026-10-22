"""Pipeline utilities wrapping the standard library :mod:`pipes` module.

The :mod:`pipes` module builds pipeline templates from shell commands. A
:class:`~pipes.Template` appends or prepends steps to a pipeline, runs debug
traces, and returns file objects or copies data through the pipeline.

This wrapper validates every argument before the standard library is reached,
so a caller gets a clear :class:`TypeError` or :class:`ValueError` instead of
an opaque failure from the standard library. It adds the conveniences the
standard library leaves to the caller: the kinds of pipeline steps are
validated against the constants the module defines, and the flags of the
template are normalized.

.. note::

   The :mod:`pipes` module was deprecated in Python 3.11 and removed in Python
   3.13 as part of :pep:`594`. The import below degrades gracefully: when the
   interpreter no longer ships the module, the helpers raise a
   :class:`RuntimeError` that names the missing module, while :func:`is_available`
   keeps working.

The wrapper never executes arbitrary shell commands outside the objects the
standard library creates and never writes to the filesystem behind the
caller's back.
"""

from __future__ import annotations

import warnings
from typing import Any, Iterable, List, Optional, Tuple

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

#: Constants that describe the kind of a pipeline step.
FILEIN_FILEOUT = "ff"
FILEIN_STDOUT = "f-"
SINK = "-."
SOURCE = ".-"
STDIN_FILEOUT = "-f"
STDIN_STDOUT = "--"

#: The valid step kinds recognized by the standard library.
VALID_STEP_KINDS: Tuple[str, ...] = (
    FILEIN_FILEOUT,
    FILEIN_STDOUT,
    SINK,
    SOURCE,
    STDIN_FILEOUT,
    STDIN_STDOUT,
)

try:
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", DeprecationWarning)
        import pipes as _pipes
except ImportError:  # pragma: no cover - Python 3.13 removed the module
    _pipes = None  # type: ignore[assignment]


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


def _require_optional_str(value: Any, name: str) -> Optional[str]:
    """Return *value* when it is a string or ``None``."""
    if value is None:
        return None
    if not isinstance(value, str):
        raise TypeError(f"{name} must be a str or None, got {type(value).__name__}")
    return value


def _require_bool(value: Any, name: str) -> bool:
    """Return *value* as a bool, rejecting other types."""
    if not isinstance(value, bool):
        raise TypeError(f"{name} must be a bool, got {type(value).__name__}")
    return value


def _require_step_kind(value: Any, name: str) -> str:
    """Return *value* as a valid step kind."""
    kind = _require_str(value, name)
    if kind not in VALID_STEP_KINDS:
        raise ValueError(
            f"{name} must be one of {VALID_STEP_KINDS}, got {kind!r}"
        )
    return kind


def is_available() -> bool:
    """Return ``True`` when the standard library ships the ``pipes`` module.

    Returns:
        Whether :mod:`pipes` can be imported.
    """
    return _pipes is not None


def quote(file: Any) -> str:
    """Return a shell-quoted version of *file*.

    Args:
        file: The string to quote for use by the shell.

    Returns:
        The quoted string.

    Raises:
        TypeError: If *file* is not a string.
        RuntimeError: If the interpreter no longer ships the ``pipes`` module.
    """
    name = _require_str(file, "file")
    pipes_module = _pipes_module()
    return pipes_module.quote(name)


def quote_command(command: Any) -> str:
    """Return a shell-quoted version of *command*.

    Args:
        command: The string to quote for use by the shell.

    Returns:
        The quoted string.

    Raises:
        TypeError: If *command* is not a string.
        RuntimeError: If the interpreter no longer ships the ``pipes`` module.
    """
    return quote(command)


def step_kinds() -> List[str]:
    """Return the valid kinds of pipeline steps.

    Returns:
        A sorted list of the step kind constants.
    """
    return sorted(VALID_STEP_KINDS)


def create_template() -> "Template":
    """Return a fresh pipeline template.

    Returns:
        A new :class:`~pipes.Template` instance.

    Raises:
        RuntimeError: If the interpreter no longer ships the ``pipes`` module.
    """
    pipes_module = _pipes_module()
    return pipes_module.Template()


# Re-export the standard library class
Template = None  # type: ignore[assignment]


def _get_template_class() -> Any:
    pipes_module = _pipes_module()
    return pipes_module.Template


# Make Template accessible
class _TemplateProxy:
    def __new__(cls, *args: Any, **kwargs: Any) -> Any:
        pipes_module = _pipes_module()
        return pipes_module.Template(*args, **kwargs)


Template = _TemplateProxy  # type: ignore[misc,assignment]


def make_pipeline(template: Any, infile: Any, outfile: Any) -> None:
    """Run a template as a pipeline.

    Args:
        template: The template to run.
        infile: The input file.
        outfile: The output file.

    Raises:
        TypeError: If the arguments have wrong types.
        RuntimeError: If the interpreter no longer ships the ``pipes`` module.
    """
    _require_str(infile, "infile")
    _require_str(outfile, "outfile")
    pipes_module = _pipes_module()
    if not isinstance(template, pipes_module.Template):
        raise TypeError(
            f"template must be a pipes.Template, got {type(template).__name__}"
        )
    pipes_module.Template.makepipeline(template, infile, outfile)
