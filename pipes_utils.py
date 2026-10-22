"""Pipeline template utilities wrapping the standard library :mod:`pipes` module.

The :mod:`pipes` module builds conversion pipeline templates: objects that chain
one or more shell commands together, piping the output of one step into the input
of the next while taking care of temporary files for steps that require real
files.

This wrapper exposes validated helpers for building, inspecting, and running
pipeline templates, plus the step kind constants and a shell-quoting helper.

.. note::

   The :mod:`pipes` module is deprecated and slated for removal in Python 3.13.
   The import below degrades gracefully: when the interpreter no longer ships the
   module, the helpers raise a :class:`RuntimeError`, while :func:`is_available`
   reports whether the interpreter still ships it.

The helpers never spawn a shell behind the caller's back.  Running a template
through :func:`copy_file` is the only helper that executes a shell command, and it
does so through the standard library exactly as :mod:`pipes` does.
"""

from __future__ import annotations

import os
import warnings
from typing import Any, Optional, Union

__all__ = [
    "FILEIN_FILEOUT",
    "FILEIN_STDOUT",
    "SINK",
    "SOURCE",
    "STDIN_FILEOUT",
    "STDIN_STDOUT",
    "Template",
    "append_step",
    "build_pipeline",
    "clone_template",
    "copy_file",
    "create_template",
    "is_available",
    "makepipeline",
    "open_for_reading",
    "open_for_writing",
    "open_template",
    "prepend_step",
    "quote_command",
    "reset_template",
    "set_debug",
    "update_debug",
]

#: Step kind: the command reads from a file and writes to a file.
FILEIN_FILEOUT = "ff"
#: Step kind: the command reads standard input and writes to a file.
STDIN_FILEOUT = "-f"
#: Step kind: the command reads from a file and writes standard output.
FILEIN_STDOUT = "f-"
#: Step kind: the command reads standard input and writes standard output.
STDIN_STDOUT = "--"
#: Step kind: the command must be first and writes standard output.
SOURCE = ".-"
#: Step kind: the command must be last and reads standard input.
SINK = "-."

#: Every step kind the standard library accepts.
STEP_KINDS = [
    FILEIN_FILEOUT,
    STDIN_FILEOUT,
    FILEIN_STDOUT,
    STDIN_STDOUT,
    SOURCE,
    SINK,
]

try:
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", DeprecationWarning)
        import pipes as _pipes
except ImportError:  # pragma: no cover - Python 3.13 removed the module
    _pipes = None  # type: ignore[assignment]

if _pipes is not None:
    Template = _pipes.Template  # type: ignore[assignment]
else:
    Template = None  # type: ignore[assignment]


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
            "use shlex and subprocess directly instead"
        )
    return _pipes


def _require_str(value: Any, name: str) -> str:
    """Return *value* as a string, raising ``TypeError`` for other types."""
    if isinstance(value, str):
        return value
    raise TypeError(f"{name} must be str, got {type(value).__name__}")


def _require_bool(value: Any, name: str) -> bool:
    """Return *value* as a bool, rejecting other types including ints."""
    if isinstance(value, bool):
        return value
    raise TypeError(f"{name} must be bool, got {type(value).__name__}")


def _require_kind(value: Any, name: str) -> str:
    """Return *value* when it is a recognized step kind."""
    kind = _require_str(value, name)
    if kind not in STEP_KINDS:
        raise ValueError(f"{name} must be one of {STEP_KINDS!r}, got {kind!r}")
    return kind


PathLike = Union[str, "os.PathLike[str]"]


def _require_path(value: Any, name: str) -> str:
    """Return *value* as a filesystem path string."""
    if isinstance(value, str):
        return value
    if isinstance(value, os.PathLike):
        return os.fspath(value)  # type: ignore[no-any-return]
    raise TypeError(f"{name} must be str or os.PathLike, got {type(value).__name__}")


def _require_mode(value: Any, name: str) -> str:
    """Return *value* when it is a valid open mode."""
    mode = _require_str(value, name)
    if mode not in ("r", "w"):
        raise ValueError(f"{name} must be 'r' or 'w', got {mode!r}")
    return mode


def is_available() -> bool:
    """Return ``True`` when the interpreter still ships the ``pipes`` module.

    Returns:
        ``True`` when :mod:`pipes` can be imported, otherwise ``False``.
    """
    return _pipes is not None


def create_template() -> Any:
    """Return a fresh pipeline template.

    Returns:
        A new :class:`pipes.Template` with no conversion steps.

    Raises:
        RuntimeError: If the interpreter no longer ships the ``pipes`` module.
    """
    return _pipes_module().Template()


def reset_template(template: Any) -> None:
    """Restore *template* to its initial state, removing every step.

    Args:
        template: The pipeline template to reset.

    Raises:
        TypeError: If *template* is not a pipeline template.
        RuntimeError: If the interpreter no longer ships the ``pipes`` module.
    """
    module = _pipes_module()
    if not isinstance(template, module.Template):
        raise TypeError(f"template must be a pipes.Template, got {type(template).__name__}")
    template.reset()


def clone_template(template: Any) -> Any:
    """Return a new pipeline template identical to *template*.

    Args:
        template: The pipeline template to copy.

    Returns:
        A new :class:`pipes.Template` with the same steps and debugging flag.

    Raises:
        TypeError: If *template* is not a pipeline template.
        RuntimeError: If the interpreter no longer ships the ``pipes`` module.
    """
    module = _pipes_module()
    if not isinstance(template, module.Template):
        raise TypeError(f"template must be a pipes.Template, got {type(template).__name__}")
    return template.clone()


def set_debug(template: Any, flag: bool) -> None:
    """Turn debugging on or off for *template*.

    Args:
        template: The pipeline template to configure.
        flag: ``True`` to print each pipeline command before running it.

    Raises:
        TypeError: If *template* is not a pipeline template or *flag* is not a bool.
        RuntimeError: If the interpreter no longer ships the ``pipes`` module.
    """
    module = _pipes_module()
    if not isinstance(template, module.Template):
        raise TypeError(f"template must be a pipes.Template, got {type(template).__name__}")
    template.debug(_require_bool(flag, "flag"))


update_debug = set_debug


def append_step(template: Any, cmd: str, kind: str) -> None:
    """Add a conversion step at the end of *template*.

    Args:
        template: The pipeline template to extend.
        cmd: The shell command to run.
        kind: One of the step kind constants, describing how the command reads
            its input and writes its output.

    Raises:
        TypeError: If *template* is not a pipeline template, *cmd* is not a
            string, or *kind* is not a string.
        ValueError: If *kind* is not a recognized step kind or the step cannot
            be appended.
        RuntimeError: If the interpreter no longer ships the ``pipes`` module.
    """
    module = _pipes_module()
    if not isinstance(template, module.Template):
        raise TypeError(f"template must be a pipes.Template, got {type(template).__name__}")
    template.append(_require_str(cmd, "cmd"), _require_kind(kind, "kind"))


def prepend_step(template: Any, cmd: str, kind: str) -> None:
    """Add a conversion step at the front of *template*.

    Args:
        template: The pipeline template to extend.
        cmd: The shell command to run.
        kind: One of the step kind constants, describing how the command reads
            its input and writes its output.

    Raises:
        TypeError: If *template* is not a pipeline template, *cmd* is not a
            string, or *kind* is not a string.
        ValueError: If *kind* is not a recognized step kind or the step cannot
            be prepended.
        RuntimeError: If the interpreter no longer ships the ``pipes`` module.
    """
    module = _pipes_module()
    if not isinstance(template, module.Template):
        raise TypeError(f"template must be a pipes.Template, got {type(template).__name__}")
    template.prepend(_require_str(cmd, "cmd"), _require_kind(kind, "kind"))


def open_template(template: Any, file: Union[str, "os.PathLike[str]"], mode: str) -> Any:
    """Open *file* for reading or writing through *template*.

    Args:
        template: The pipeline template to use.
        file: The path of the file to open.
        mode: Either ``'r'`` to read or ``'w'`` to write.

    Returns:
        A file-like object open for reading or writing through the pipeline.

    Raises:
        TypeError: If *template* is not a pipeline template or *file* is not a
            path.
        ValueError: If *mode* is not ``'r'`` or ``'w'``.
        RuntimeError: If the interpreter no longer ships the ``pipes`` module.
    """
    module = _pipes_module()
    if not isinstance(template, module.Template):
        raise TypeError(f"template must be a pipes.Template, got {type(template).__name__}")
    return template.open(_require_path(file, "file"), _require_mode(mode, "mode"))


def open_for_reading(template: Any, file: Union[str, "os.PathLike[str]"]) -> Any:
    """Open *file* for reading through *template*.

    Args:
        template: The pipeline template to use.
        file: The path of the file to read.

    Returns:
        A file-like object open for reading through the pipeline.

    Raises:
        TypeError: If *template* is not a pipeline template or *file* is not a path.
        RuntimeError: If the interpreter no longer ships the ``pipes`` module.
    """
    return open_template(template, file, "r")


def open_for_writing(template: Any, file: Union[str, "os.PathLike[str]"]) -> Any:
    """Open *file* for writing through *template*.

    Args:
        template: The pipeline template to use.
        file: The path of the file to write.

    Returns:
        A file-like object open for writing through the pipeline.

    Raises:
        TypeError: If *template* is not a pipeline template or *file* is not a path.
        RuntimeError: If the interpreter no longer ships the ``pipes`` module.
    """
    return open_template(template, file, "w")


def copy_file(template: Any, infile: Union[str, "os.PathLike[str]"], outfile: Union[str, "os.PathLike[str]"]) -> int:
    """Convert *infile* to *outfile* through *template* and return the exit status.

    Args:
        template: The pipeline template to use.
        infile: The path of the file to read.
        outfile: The path of the file to write.

    Returns:
        The exit status of the conversion pipeline.

    Raises:
        TypeError: If *template* is not a pipeline template or a path is not a path.
        RuntimeError: If the interpreter no longer ships the ``pipes`` module.
    """
    module = _pipes_module()
    if not isinstance(template, module.Template):
        raise TypeError(f"template must be a pipes.Template, got {type(template).__name__}")
    return template.copy(_require_path(infile, "infile"), _require_path(outfile, "outfile"))


def build_pipeline(
    template: Any,
    infile: Union[str, "os.PathLike[str]"],
    outfile: Union[str, "os.PathLike[str]"],
) -> str:
    """Return the shell command string that converts *infile* to *outfile*.

    Args:
        template: The pipeline template to use.
        infile: The path of the file to read.
        outfile: The path of the file to write.

    Returns:
        The shell command string for the conversion pipeline.

    Raises:
        TypeError: If *template* is not a pipeline template or a path is not a path.
        RuntimeError: If the interpreter no longer ships the ``pipes`` module.
    """
    module = _pipes_module()
    if not isinstance(template, module.Template):
        raise TypeError(f"template must be a pipes.Template, got {type(template).__name__}")
    return template.makepipeline(_require_path(infile, "infile"), _require_path(outfile, "outfile"))


def quote_command(text: str) -> str:
    """Return *text* quoted so it can be embedded safely in a shell command.

    Args:
        text: The text to quote.

    Returns:
        The shell-quoted form of *text*.

    Raises:
        TypeError: If *text* is not a string.
    """
    return _pipes_module().quote(_require_str(text, "text"))
