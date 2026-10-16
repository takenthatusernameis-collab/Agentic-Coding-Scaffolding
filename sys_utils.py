"""Python runtime and system information utilities.

This module provides helpers for inspecting the Python interpreter and
runtime environment using only the standard library ``sys`` module.
It complements :mod:`os_utils`, which covers operating-system-level
information.
"""

from __future__ import annotations

import sys
from typing import Any, Dict, List, Optional

__all__: list[str] = [
    "get_argv",
    "get_executable",
    "get_frame_info",
    "get_platform",
    "get_path",
    "get_python_version",
    "get_python_version_string",
    "get_recursion_limit",
    "get_refcount",
    "get_stderr_encoding",
    "get_stdin_encoding",
    "get_stdout_encoding",
    "is_interactive",
    "set_recursion_limit",
]


def get_python_version() -> Dict[str, Any]:
    """Return the Python interpreter version as a dictionary.

    Returns:
        Dictionary with keys ``major``, ``minor``, ``micro``,
        ``releaselevel``, and ``serial``.
    """
    version_info = sys.version_info
    return {
        "major": version_info.major,
        "minor": version_info.minor,
        "micro": version_info.micro,
        "releaselevel": version_info.releaselevel,
        "serial": version_info.serial,
    }


def get_python_version_string() -> str:
    """Return the full Python version string.

    Returns:
        The version string (e.g. ``"3.11.0 (main, ...)"``).
    """
    return sys.version


def get_executable() -> str:
    """Return the absolute path of the Python executable.

    Returns:
        The path to the running Python interpreter executable.
    """
    return sys.executable


def get_argv() -> List[str]:
    """Return the command-line arguments passed to the script.

    Returns:
        A list of command-line arguments. The first element is the
        script name (or empty when run interactively).
    """
    return list(sys.argv)


def get_platform() -> str:
    """Return the platform identifier.

    Returns:
        The platform string (e.g. ``"linux"``, ``"darwin"``,
        ``"win32"``).
    """
    return sys.platform


def get_path() -> List[str]:
    """Return a copy of the module search path.

    Returns:
        A list of directory strings searched when importing modules.
    """
    return list(sys.path)


def get_recursion_limit() -> int:
    """Return the current maximum recursion depth.

    Returns:
        The current recursion limit as an integer.
    """
    return sys.getrecursionlimit()


def set_recursion_limit(limit: int) -> None:
    """Set the maximum recursion depth.

    Args:
        limit: The new recursion limit. Must be a positive integer.

    Raises:
        TypeError: If ``limit`` is not an integer.
        ValueError: If ``limit`` is less than or equal to 0.
    """
    if not isinstance(limit, int) or isinstance(limit, bool):
        raise TypeError("limit must be an integer")
    if limit <= 0:
        raise ValueError("limit must be greater than 0")
    sys.setrecursionlimit(limit)


def get_stdout_encoding() -> Optional[str]:
    """Return the encoding of the standard output stream.

    Returns:
        The encoding name (e.g. ``"utf-8"``), or ``None`` if unavailable.
    """
    stdout = getattr(sys, "stdout", None)
    if stdout is None:
        return None
    return getattr(stdout, "encoding", None)


def get_stderr_encoding() -> Optional[str]:
    """Return the encoding of the standard error stream.

    Returns:
        The encoding name (e.g. ``"utf-8"``), or ``None`` if unavailable.
    """
    stderr = getattr(sys, "stderr", None)
    if stderr is None:
        return None
    return getattr(stderr, "encoding", None)


def get_stdin_encoding() -> Optional[str]:
    """Return the encoding of the standard input stream.

    Returns:
        The encoding name (e.g. ``"utf-8"``), or ``None`` if unavailable.
    """
    stdin = getattr(sys, "stdin", None)
    if stdin is None:
        return None
    return getattr(stdin, "encoding", None)


def is_interactive() -> bool:
    """Return whether the interpreter is running in interactive mode.

    Returns:
        ``True`` when running in an interactive session, ``False``
        otherwise.
    """
    return hasattr(sys, "ps1") or hasattr(sys, "ps2")


def get_frame_info(depth: int = 0) -> Dict[str, Any]:
    """Return information about a stack frame.

    Args:
        depth: The number of frames to go back from the caller of this
            function. ``0`` refers to the caller of ``get_frame_info``.

    Returns:
        Dictionary with keys ``filename``, ``lineno``, ``function``,
        ``code_context``, and ``index``.

    Raises:
        TypeError: If ``depth`` is not an integer.
        ValueError: If ``depth`` is negative.
        IndexError: If ``depth`` is beyond the available call stack.
    """
    if not isinstance(depth, int) or isinstance(depth, bool):
        raise TypeError("depth must be an integer")
    if depth < 0:
        raise ValueError("depth must be non-negative")

    frame = sys._getframe(depth + 1)
    try:
        return {
            "filename": frame.f_code.co_filename,
            "lineno": frame.f_lineno,
            "function": frame.f_code.co_name,
            "code_context": None,
            "index": None,
        }
    finally:
        del frame


def get_refcount(obj: Any) -> int:
    """Return the reference count of an object.

    Args:
        obj: The object whose reference count should be retrieved.

    Returns:
        The reference count as an integer. Note that the count returned
        includes the temporary reference created by the call itself.
    """
    return sys.getrefcount(obj)
