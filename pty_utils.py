"""Pseudo-terminal utilities wrapping the standard library :mod:`pty` module.

The :mod:`pty` module handles the pseudo-terminal concept: starting another
process and being able to write to and read from its controlling terminal
programmatically.

This wrapper validates every argument before the standard library is reached,
so a caller gets a clear :class:`TypeError` or :class:`ValueError` instead of
an opaque failure from the C layer.  It returns values in a consistent form
and adds small conveniences on top of :func:`openpty`, :func:`fork`, and
:func:`spawn`.

.. note::

   The :mod:`pty` module only exists on Unix-like platforms.  The import
   below degrades gracefully: when the interpreter does not ship the module,
   the helpers raise a :class:`RuntimeError` that names the missing module,
   while the pure helpers keep working.
"""

from __future__ import annotations

import os
from typing import Any, Callable, List, Tuple, Union

try:
    import pty as _pty
except ImportError:  # pragma: no cover - the module is Unix-only
    _pty = None  # type: ignore[assignment]


__all__: list[str] = [
    "CHILD",
    "STDERR_FILENO",
    "STDIN_FILENO",
    "STDOUT_FILENO",
    "fork",
    "is_available",
    "master_open",
    "open_terminal",
    "openpty",
    "slave_open",
    "spawn",
]


#: File descriptor for stdin.
STDIN_FILENO: int = getattr(os, "STDIN_FILENO", 0)
#: File descriptor for stdout.
STDOUT_FILENO: int = getattr(os, "STDOUT_FILENO", 1)
#: File descriptor for stderr.
STDERR_FILENO: int = getattr(os, "STDERR_FILENO", 2)
#: A constant returned from :func:`fork` when the child process is running.
CHILD: int = getattr(os, "CHILD", 0)


def _pty_module() -> Any:
    """Return the standard library ``pty`` module.

    Raises:
        RuntimeError: If the interpreter does not ship the ``pty`` module.
    """
    if _pty is None:
        raise RuntimeError("the standard library module 'pty' is not available")
    return _pty


def is_available() -> bool:
    """Return ``True`` if the ``pty`` module is available."""
    return _pty is not None


def openpty() -> Tuple[int, int]:
    """Open a new pseudo-terminal pair.

    Returns:
        A pair ``(master_fd, slave_fd)`` where *master_fd* is the file
        descriptor of the master end and *slave_fd* is the file descriptor of
        the slave end.

    Raises:
        RuntimeError: If the interpreter does not ship the ``pty`` module.
        OSError: If the operating system fails to allocate a pseudo-terminal.
    """
    master_fd, slave_fd = _pty_module().openpty()
    return int(master_fd), int(slave_fd)


# Keep an alias matching the style of other wrappers.
open_terminal = openpty


def master_open() -> Tuple[str, int]:
    """Open a pseudo-terminal and return the master device and its name.

    Returns:
        A pair ``(master_name, master_fd)`` where *master_name* is the name of
        the master device and *master_fd* is its file descriptor.

    Raises:
        RuntimeError: If the interpreter does not ship the ``pty`` module.
        OSError: If the operating system fails to allocate a pseudo-terminal.
    """
    pty_mod = _pty_module()
    try:
        result = pty_mod.master_open()  # type: ignore[attr-defined]
    except AttributeError:
        master_fd, slave_fd = openpty()
        try:
            name = os.ttyname(slave_fd)
        except OSError:
            name = ""
        finally:
            try:
                os.close(slave_fd)
            except OSError:
                pass
        return name, master_fd
    if isinstance(result, tuple):
        if len(result) == 2:
            a, b = result
            # Python 3.x returns (fd, name); older versions may return (name, fd)
            if isinstance(a, int) and isinstance(b, str):
                return str(b), int(a)
            if isinstance(a, str) and isinstance(b, int):
                return str(a), int(b)
            # Try to be flexible
            if isinstance(a, int):
                return str(b), int(a)
            return str(a), int(b)
    raise RuntimeError("master_open() returned an unexpected value")


def slave_open(tty_name: str) -> int:
    """Open the slave end of a pseudo-terminal by name.

    Args:
        tty_name: The name of the slave device (as returned by
            :func:`master_open` or :func:`os.ttyname`).

    Returns:
        The file descriptor of the slave end.

    Raises:
        TypeError: If *tty_name* is not a string.
        ValueError: If *tty_name* is empty.
        RuntimeError: If the interpreter does not ship the ``pty`` module.
        OSError: If the operating system fails to open the device.
    """
    if not isinstance(tty_name, str):
        raise TypeError(f"tty_name must be a str, got {type(tty_name).__name__}")
    if tty_name == "":
        raise ValueError("tty_name must not be empty")
    try:
        fd = _pty_module().slave_open(tty_name)  # type: ignore[attr-defined]
    except AttributeError:
        fd = os.open(tty_name, os.O_RDWR)
    return int(fd)


def fork() -> Union[int, Tuple[int, ...]]:
    """Fork a process and connect the child's controlling terminal to a new
    pseudo-terminal.

    Returns:
        In some Python versions returns ``0`` in the child process and the
        process ID of the child in the parent process.  In other versions
        returns a tuple ``(pid, fd)`` as returned by the standard library.

    Raises:
        RuntimeError: If the interpreter does not ship the ``pty`` module.
        OSError: If the fork fails.
    """
    result = _pty_module().fork()
    if isinstance(result, tuple):
        return tuple(int(x) for x in result)
    return int(result)

def spawn(
    argv: List[str],
    master_read: Callable[[int], bytes] | None = None,
    stdin_read: Callable[[int], bytes] | None = None,
) -> int:
    """Spawn a process connected to its controlling terminal via a
    pseudo-terminal.

    Args:
        argv: The command line to execute as passed to :func:`os.execvp`.
        master_read: A callable used to read from the master end.  If omitted,
            the standard library's default is used.
        stdin_read: A callable used to read from stdin.  If omitted, the
            standard library's default is used.

    Returns:
        The exit status of the spawned process.

    Raises:
        TypeError: If *argv* is not a list of strings.
        ValueError: If *argv* is empty.
        RuntimeError: If the interpreter does not ship the ``pty`` module.
        OSError: If spawning the process fails.
    """
    if not isinstance(argv, list):
        raise TypeError(f"argv must be a list, got {type(argv).__name__}")
    if len(argv) == 0:
        raise ValueError("argv must not be empty")
    for i, arg in enumerate(argv):
        if not isinstance(arg, str):
            raise TypeError(
                f"argv[{i}] must be a str, got {type(arg).__name__}"
            )
    pty_mod = _pty_module()
    try:
        if master_read is None and stdin_read is None:
            return int(pty_mod.spawn(argv))
        return int(pty_mod.spawn(argv, master_read, stdin_read))
    except TypeError:
        try:
            return int(pty_mod.spawn(argv))
        except Exception:
            raise
