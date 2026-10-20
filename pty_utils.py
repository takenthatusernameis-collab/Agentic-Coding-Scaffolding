"""Pseudo-terminal utilities wrapping the standard library :mod:`pty` module.

The :mod:`pty` module opens a pseudo-terminal, forks a process onto it, and
runs a program with the pseudo-terminal as its controlling terminal.  A
program that drives a child process therefore reads and writes the terminal
of the child instead of a pipe.

This wrapper validates every argument before the standard library is reached,
so a caller gets a clear :class:`TypeError` or :class:`ValueError` instead of
an opaque failure from the C layer.  It returns values in a consistent form:
the result of :func:`fork` is a :class:`ForkResult` named tuple with stable
field names, and :func:`master_open` always returns the name of the device
before its file descriptor.

.. note::

   The :mod:`pty` module only exists on Unix-like platforms.  The import
   below degrades gracefully: when the interpreter does not ship the module,
   the helpers that talk to the operating system raise a
   :class:`RuntimeError` that names the missing module, while the pure
   helpers keep working.

The standard library deprecated :func:`pty.master_open` and
:func:`pty.slave_open` in Python 3.12, because the pseudo-terminal of the
host is opened with :func:`os.openpty` and :func:`os.ttyname` instead.  The
wrapper never calls the deprecated functions, so it works on every supported
interpreter without raising a :class:`DeprecationWarning`.
"""

from __future__ import annotations

import os
from collections.abc import Sequence
from typing import Any, Callable, NamedTuple

try:
    import pty as _pty
except ImportError:  # pragma: no cover - the module is Unix-only
    _pty = None  # type: ignore[assignment]


__all__: list[str] = [
    "CHILD",
    "ForkResult",
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
#: The value :func:`fork` reports to the child process.
CHILD: int = 0


class ForkResult(NamedTuple):
    """The result of :func:`fork`.

    Attributes:
        pid: The process identifier of the child process, or zero in the
            child process itself.
        master_fd: The file descriptor of the master end of the new
            pseudo-terminal.
    """

    pid: int
    master_fd: int


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


def openpty() -> tuple[int, int]:
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


def open_terminal() -> tuple[int, int]:
    """Open a new pseudo-terminal pair.

    This is an alias of :func:`openpty` that spells out the purpose of the
    helper.

    Returns:
        A pair ``(master_fd, slave_fd)``.

    Raises:
        RuntimeError: If the interpreter does not ship the ``pty`` module.
        OSError: If the operating system fails to allocate a pseudo-terminal.
    """
    return openpty()


def master_open() -> tuple[str, int]:
    """Open a pseudo-terminal and return the name of the slave device.

    The standard library function of the same name returns the file
    descriptor before the name, and it is deprecated since Python 3.12.  This
    helper returns the name first and the file descriptor second, and it never
    calls the deprecated function.

    Returns:
        A pair ``(slave_name, master_fd)`` where *slave_name* is the path of
        the slave device and *master_fd* is the file descriptor of the master
        end.

    Raises:
        RuntimeError: If the interpreter does not ship the ``pty`` module.
        OSError: If the operating system fails to allocate a pseudo-terminal.
    """
    master_fd, slave_fd = openpty()
    try:
        name = os.ttyname(slave_fd)
    finally:
        os.close(slave_fd)
    return name, master_fd


def slave_open(tty_name: str) -> int:
    """Open the slave end of a pseudo-terminal by name.

    Args:
        tty_name: The name of the slave device, as returned by
            :func:`master_open` or by :func:`os.ttyname`.

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
    _pty_module()
    return int(os.open(tty_name, os.O_RDWR | getattr(os, "O_NOCTTY", 0)))


def fork() -> ForkResult:
    """Fork a process and give it a new pseudo-terminal.

    The child process becomes the session leader of the new pseudo-terminal,
    so it has a controlling terminal of its own.

    Returns:
        A :class:`ForkResult` named tuple with the process identifier of the
        child and the file descriptor of the master end of the new
        pseudo-terminal.  The process identifier is zero in the child
        process itself.

    Raises:
        RuntimeError: If the interpreter does not ship the ``pty`` module.
        OSError: If the fork fails.
    """
    pid, master_fd = _pty_module().fork()
    return ForkResult(int(pid), int(master_fd))


def _read(fd: int) -> bytes:
    """Read up to a kilobyte from *fd* and return empty bytes at the end."""
    try:
        return os.read(fd, 1024)
    except OSError:
        return b""


def spawn(
    argv: Sequence[str],
    master_read: Callable[[int], bytes] | None = None,
    stdin_read: Callable[[int], bytes] | None = None,
) -> int:
    """Run a program with a pseudo-terminal as its controlling terminal.

    The helper waits for the program to finish and returns its exit status,
    so it blocks until the child process ends.

    Args:
        argv: The command line of the program, as a sequence of strings.  The
            first element is the program and the rest are its arguments.
        master_read: The callable that reads the master end of the
            pseudo-terminal.  The default reads a kilobyte at a time.
        stdin_read: The callable that reads the standard input.  The default
            reads a kilobyte at a time.

    Returns:
        The exit status of the program.

    Raises:
        TypeError: If *argv* is not a sequence of strings, or if one of the
            callables is not callable.
        ValueError: If *argv* is empty.
        RuntimeError: If the interpreter does not ship the ``pty`` module.
        OSError: If the program cannot be started.
    """
    if isinstance(argv, (str, bytes)):
        raise TypeError("argv must be a sequence of str, got str")
    if not isinstance(argv, Sequence):
        raise TypeError(f"argv must be a sequence, got {type(argv).__name__}")
    argv = list(argv)
    if len(argv) == 0:
        raise ValueError("argv must not be empty")
    for index, argument in enumerate(argv):
        if not isinstance(argument, str):
            raise TypeError(
                f"argv[{index}] must be a str, got {type(argument).__name__}"
            )
    for name, callback in (("master_read", master_read), ("stdin_read", stdin_read)):
        if callback is not None and not callable(callback):
            raise TypeError(f"{name} must be callable, got {type(callback).__name__}")
    pty_mod = _pty_module()
    if master_read is None and stdin_read is None:
        return int(pty_mod.spawn(argv))
    return int(pty_mod.spawn(argv, master_read or _read, stdin_read or _read))
