"""File control utilities wrapping the standard library :mod:`fcntl` module.

The :mod:`fcntl` module controls the behaviour of an open file descriptor.  A
program places an advisory lock on a file with :func:`fcntl.flock` or with
:func:`fcntl.lockf`, and it performs the other control operations with
:func:`fcntl.fcntl` and :func:`fcntl.ioctl`.

This wrapper validates every argument before the standard library is reached,
so a caller gets a clear :class:`TypeError` or :class:`ValueError` instead of
an opaque failure from the C layer.  It adds conveniences the standard
library does not offer: the lock modes are addressed by name, the descriptor
flags and the file status flags are read and written with dedicated helpers, a
file descriptor is duplicated with a single call, and :func:`file_lock` locks a
file for the duration of a block of code.

.. note::

   The :mod:`fcntl` module only exists on Unix-like platforms.  The import
   below degrades gracefully: when the interpreter does not ship the module,
   the helpers raise a :class:`RuntimeError` that names the missing module,
   while the pure helpers keep working.

The locks are advisory.  A program that does not ask for a lock ignores the
locks of the other programs, and a lock is released as soon as the file
descriptor is closed.
"""

from __future__ import annotations

import os
from contextlib import contextmanager
from typing import Any, Dict, Iterator

try:
    import fcntl as _fcntl
except ImportError:  # pragma: no cover - the module is Unix-only
    _fcntl = None  # type: ignore[assignment]


def _constant(name: str, fallback: int) -> int:
    """Return the standard library constant *name*, or *fallback*.

    Args:
        name: The name of the constant in the standard library module.
        fallback: The value to use when the interpreter does not provide the
            constant.

    Returns:
        The value of the constant.
    """
    if _fcntl is None:
        return fallback
    value = getattr(_fcntl, name, fallback)
    return value if isinstance(value, int) else fallback


#: Acquire a shared lock.
LOCK_SH: int = _constant("LOCK_SH", 1)
#: Acquire an exclusive lock.
LOCK_EX: int = _constant("LOCK_EX", 2)
#: Do not block when the lock cannot be acquired.
LOCK_NB: int = _constant("LOCK_NB", 4)
#: Release a lock.
LOCK_UN: int = _constant("LOCK_UN", 8)

#: Read the flags of a file descriptor.
F_GETFD: int = _constant("F_GETFD", 1)
#: Write the flags of a file descriptor.
F_SETFD: int = _constant("F_SETFD", 2)
#: Read the status flags of an open file.
F_GETFL: int = _constant("F_GETFL", 3)
#: Write the status flags of an open file.
F_SETFL: int = _constant("F_SETFL", 4)
#: Duplicate a file descriptor.
F_DUPFD: int = _constant("F_DUPFD", 0)
#: Duplicate a file descriptor and mark the copy as close on exec.
F_DUPFD_CLOEXEC: int = _constant("F_DUPFD_CLOEXEC", 1030)
#: Close the file descriptor when the process executes a new program.
FD_CLOEXEC: int = _constant("FD_CLOEXEC", 1)

#: A read lock on a region of a file.
F_RDLCK: int = _constant("F_RDLCK", 0)
#: A write lock on a region of a file.
F_WRLCK: int = _constant("F_WRLCK", 1)
#: No lock on a region of a file.
F_UNLCK: int = _constant("F_UNLCK", 2)
#: Read the lock that blocks a region of a file.
F_GETLK: int = _constant("F_GETLK", 5)
#: Write a lock on a region of a file without blocking.
F_SETLK: int = _constant("F_SETLK", 6)
#: Write a lock on a region of a file and wait for it.
F_SETLKW: int = _constant("F_SETLKW", 7)

#: Take a write lock on a region of a file and wait for it.
F_LOCK: int = 0
#: Take a write lock on a region of a file without waiting for it.
F_TLOCK: int = 1
#: Release the lock on a region of a file.
F_ULOCK: int = 2

#: The names of the lock modes of :func:`lock_kind`.
_LOCK_MODES: Dict[str, int] = {
    "shared": LOCK_SH,
    "exclusive": LOCK_EX,
    "unlock": LOCK_UN,
}


__all__: list[str] = [
    "F_DUPFD",
    "F_DUPFD_CLOEXEC",
    "F_GETFD",
    "F_GETFL",
    "F_GETLK",
    "F_LOCK",
    "F_RDLCK",
    "F_SETFD",
    "F_SETFL",
    "F_SETLK",
    "F_SETLKW",
    "F_TLOCK",
    "F_ULOCK",
    "F_UNLCK",
    "F_WRLCK",
    "FD_CLOEXEC",
    "LOCK_EX",
    "LOCK_NB",
    "LOCK_SH",
    "LOCK_UN",
    "control",
    "duplicate_fd",
    "file_lock",
    "flock",
    "get_descriptor_flags",
    "get_file_status_flags",
    "ioctl",
    "is_available",
    "is_cloexec",
    "lock_kind",
    "lock_modes",
    "lockf",
    "set_descriptor_flags",
    "set_file_status_flags",
    "unlock",
]


def _fcntl_module() -> Any:
    """Return the standard library ``fcntl`` module.

    Raises:
        RuntimeError: If the interpreter does not ship the ``fcntl`` module.
    """
    if _fcntl is None:
        raise RuntimeError("the standard library module 'fcntl' is not available")
    return _fcntl


def is_available() -> bool:
    """Return ``True`` if the ``fcntl`` module is available."""
    return _fcntl is not None


def _validate_fd(fd: int) -> int:
    """Return *fd* when it is a valid file descriptor.

    Args:
        fd: The file descriptor to validate.

    Returns:
        The validated file descriptor.

    Raises:
        TypeError: If *fd* is not an int.
        ValueError: If *fd* is negative.
    """
    if isinstance(fd, bool) or not isinstance(fd, int):
        raise TypeError(f"fd must be an int, got {type(fd).__name__}")
    if fd < 0:
        raise ValueError(f"fd must not be negative, got {fd}")
    return fd


def _validate_operation(operation: int) -> int:
    """Return *operation* when it is a known lock operation.

    Args:
        operation: The lock operation to validate.

    Returns:
        The validated lock operation.

    Raises:
        TypeError: If *operation* is not an int.
        ValueError: If *operation* is not a known lock operation.
    """
    if isinstance(operation, bool) or not isinstance(operation, int):
        raise TypeError(f"operation must be an int, got {type(operation).__name__}")
    known = LOCK_SH | LOCK_EX | LOCK_UN | LOCK_NB
    if operation & ~known:
        raise ValueError(f"operation has unknown bits, got {operation}")
    modes = [mode for mode in (LOCK_SH, LOCK_EX, LOCK_UN) if operation & mode]
    if len(modes) != 1:
        raise ValueError(
            "operation must be exactly one of LOCK_SH, LOCK_EX, and LOCK_UN, "
            f"got {operation}"
        )
    return operation


def _validate_command(command: int) -> int:
    """Return *command* when it is a known record lock command.

    Args:
        command: The record lock command to validate.

    Returns:
        The validated record lock command.

    Raises:
        TypeError: If *command* is not an int.
        ValueError: If *command* is not a known record lock command.
    """
    if isinstance(command, bool) or not isinstance(command, int):
        raise TypeError(f"command must be an int, got {type(command).__name__}")
    if command not in (F_LOCK, F_TLOCK, F_ULOCK):
        raise ValueError(
            f"command must be F_LOCK, F_TLOCK, or F_ULOCK, got {command}"
        )
    return command


def _validate_offset(value: int, name: str) -> int:
    """Return *value* when it is a usable offset.

    Args:
        value: The offset to validate.
        name: The name of the argument, used in the error messages.

    Returns:
        The validated offset.

    Raises:
        TypeError: If *value* is not an int.
    """
    if isinstance(value, bool) or not isinstance(value, int):
        raise TypeError(f"{name} must be an int, got {type(value).__name__}")
    return value


def _host_lockf_command(command: int) -> int:
    """Return the command the host expects for a record lock command.

    The standard library changed the commands of :func:`fcntl.lockf` in
    Python 3.14.  The older interpreters expect the ``F_LOCK``,
    ``F_TLOCK``, and ``F_ULOCK`` commands, while the newer ones expect the
    ``LOCK_EX``, ``LOCK_EX | LOCK_NB``, and ``LOCK_UN`` commands of the
    advisory locks.  The wrapper always speaks the older dialect and
    translates it here.

    Args:
        command: The record lock command of the wrapper.

    Returns:
        The command the standard library of the host understands.

    Raises:
        RuntimeError: If the interpreter does not ship the ``fcntl`` module.
    """
    module = _fcntl_module()
    if hasattr(module, "F_LOCK"):
        return command
    if command == F_LOCK:
        return LOCK_EX
    if command == F_TLOCK:
        return LOCK_EX | LOCK_NB
    return LOCK_UN


def flock(fd: int, operation: int) -> None:
    """Place an advisory lock on the file behind *fd*.

    The lock is a whole file lock.  A shared lock lets the other programs
    read the file, an exclusive lock keeps them out, and both are released
    with :data:`LOCK_UN`.

    Args:
        fd: The file descriptor of the file to lock.
        operation: The lock operation.  One of :data:`LOCK_SH`,
            :data:`LOCK_EX`, or :data:`LOCK_UN`, optionally combined with
            :data:`LOCK_NB` to avoid blocking.

    Raises:
        TypeError: If *fd* or *operation* has the wrong type.
        ValueError: If *fd* is negative or *operation* is not a known lock
            operation.
        RuntimeError: If the interpreter does not ship the ``fcntl`` module.
        OSError: If the lock cannot be acquired.
    """
    _validate_fd(fd)
    _validate_operation(operation)
    module = _fcntl_module()
    module.flock(fd, operation)


def unlock(fd: int) -> None:
    """Release the advisory lock of the file behind *fd*.

    Args:
        fd: The file descriptor of the locked file.

    Raises:
        TypeError: If *fd* is not an int.
        ValueError: If *fd* is negative.
        RuntimeError: If the interpreter does not ship the ``fcntl`` module.
        OSError: If the lock cannot be released.
    """
    flock(fd, LOCK_UN)


def lockf(
    fd: int,
    command: int,
    length: int = 0,
    start: int = 0,
    whence: int = os.SEEK_SET,
) -> None:
    """Place an advisory lock on a region of the file behind *fd*.

    The lock is a record lock.  It covers the *length* bytes that begin at
    *start*, relative to *whence*.  A length of zero covers the region up to
    the end of the file.

    Args:
        fd: The file descriptor of the file to lock.
        command: The lock command.  :data:`F_LOCK` takes a write lock and
            waits for it, :data:`F_TLOCK` takes a write lock without waiting
            for it, and :data:`F_ULOCK` releases the lock.
        length: The number of bytes to lock.
        start: The offset of the first byte of the locked region.
        whence: The reference point of *start*.  One of :data:`os.SEEK_SET`,
            :data:`os.SEEK_CUR`, or :data:`os.SEEK_END`.

    Raises:
        TypeError: If an argument has the wrong type.
        ValueError: If *fd* is negative, *command* is not a known record lock
            command, or *whence* is not a known reference point.
        RuntimeError: If the interpreter does not ship the ``fcntl`` module.
        OSError: If the lock cannot be acquired.
    """
    _validate_fd(fd)
    _validate_command(command)
    _validate_offset(length, "length")
    _validate_offset(start, "start")
    if isinstance(whence, bool) or not isinstance(whence, int):
        raise TypeError(f"whence must be an int, got {type(whence).__name__}")
    if whence not in (os.SEEK_SET, os.SEEK_CUR, os.SEEK_END):
        raise ValueError(
            "whence must be os.SEEK_SET, os.SEEK_CUR, or os.SEEK_END, "
            f"got {whence}"
        )
    module = _fcntl_module()
    module.lockf(fd, _host_lockf_command(command), length, start, whence)


def control(fd: int, cmd: int, arg: int | bytes = 0) -> int | bytes:
    """Perform the control operation *cmd* on the file behind *fd*.

    The command and the argument depend on the platform.  The constants of
    the standard library, such as :data:`F_GETFD` and :data:`F_SETFD`, name
    the usual operations.

    Args:
        fd: The file descriptor to control.
        cmd: The control operation to perform.
        arg: The argument of the operation.  An integer for the operations
            that take a number, and a byte string for the operations that
            take a buffer.

    Returns:
        The result of the operation.

    Raises:
        TypeError: If an argument has the wrong type.
        ValueError: If *fd* is negative.
        RuntimeError: If the interpreter does not ship the ``fcntl`` module.
        OSError: If the operation fails.
    """
    _validate_fd(fd)
    if isinstance(cmd, bool) or not isinstance(cmd, int):
        raise TypeError(f"cmd must be an int, got {type(cmd).__name__}")
    if isinstance(arg, bool) or not isinstance(arg, (int, bytes, bytearray)):
        raise TypeError(f"arg must be an int or bytes, got {type(arg).__name__}")
    module = _fcntl_module()
    if isinstance(arg, bytearray):
        arg = bytes(arg)
    result: int | bytes = module.fcntl(fd, cmd, arg)
    return result


def ioctl(fd: int, request: int, arg: int = 0) -> int:
    """Perform the device control operation *request* on the file behind *fd*.

    Args:
        fd: The file descriptor to control.
        request: The device specific request to perform.
        arg: The argument of the request.

    Returns:
        The result of the operation.

    Raises:
        TypeError: If an argument has the wrong type.
        ValueError: If *fd* is negative.
        RuntimeError: If the interpreter does not ship the ``fcntl`` module.
        OSError: If the operation fails.
    """
    _validate_fd(fd)
    if isinstance(request, bool) or not isinstance(request, int):
        raise TypeError(f"request must be an int, got {type(request).__name__}")
    if isinstance(arg, bool) or not isinstance(arg, int):
        raise TypeError(f"arg must be an int, got {type(arg).__name__}")
    module = _fcntl_module()
    return int(module.ioctl(fd, request, arg))


def get_descriptor_flags(fd: int) -> int:
    """Return the flags of the file descriptor *fd*.

    Args:
        fd: The file descriptor to read.

    Returns:
        The flags of the file descriptor, such as :data:`FD_CLOEXEC`.

    Raises:
        TypeError: If *fd* is not an int.
        ValueError: If *fd* is negative.
        RuntimeError: If the interpreter does not ship the ``fcntl`` module.
        OSError: If the flags cannot be read.
    """
    _validate_fd(fd)
    module = _fcntl_module()
    return int(module.fcntl(fd, F_GETFD))


def set_descriptor_flags(fd: int, flags: int) -> None:
    """Write the flags of the file descriptor *fd*.

    Args:
        fd: The file descriptor to write.
        flags: The flags to write, such as :data:`FD_CLOEXEC`.

    Raises:
        TypeError: If an argument has the wrong type.
        ValueError: If *fd* is negative.
        RuntimeError: If the interpreter does not ship the ``fcntl`` module.
        OSError: If the flags cannot be written.
    """
    _validate_fd(fd)
    if isinstance(flags, bool) or not isinstance(flags, int):
        raise TypeError(f"flags must be an int, got {type(flags).__name__}")
    if flags < 0:
        raise ValueError(f"flags must not be negative, got {flags}")
    module = _fcntl_module()
    module.fcntl(fd, F_SETFD, flags)


def get_file_status_flags(fd: int) -> int:
    """Return the status flags of the open file behind *fd*.

    Args:
        fd: The file descriptor of the open file.

    Returns:
        The status flags of the open file, such as ``os.O_APPEND``.

    Raises:
        TypeError: If *fd* is not an int.
        ValueError: If *fd* is negative.
        RuntimeError: If the interpreter does not ship the ``fcntl`` module.
        OSError: If the flags cannot be read.
    """
    _validate_fd(fd)
    module = _fcntl_module()
    return int(module.fcntl(fd, F_GETFL))


def set_file_status_flags(fd: int, flags: int) -> None:
    """Write the status flags of the open file behind *fd*.

    Args:
        fd: The file descriptor of the open file.
        flags: The status flags to write, such as ``os.O_APPEND``.

    Raises:
        TypeError: If an argument has the wrong type.
        ValueError: If *fd* is negative.
        RuntimeError: If the interpreter does not ship the ``fcntl`` module.
        OSError: If the flags cannot be written.
    """
    _validate_fd(fd)
    if isinstance(flags, bool) or not isinstance(flags, int):
        raise TypeError(f"flags must be an int, got {type(flags).__name__}")
    if flags < 0:
        raise ValueError(f"flags must not be negative, got {flags}")
    module = _fcntl_module()
    module.fcntl(fd, F_SETFL, flags)


def duplicate_fd(fd: int, minimum: int = 0, inheritable: bool = False) -> int:
    """Return a copy of the file descriptor *fd*.

    Args:
        fd: The file descriptor to copy.
        minimum: The lowest file descriptor the copy may receive.
        inheritable: Whether the copy stays open when the process executes a
            new program.  The copy is close on exec by default.

    Returns:
        The new file descriptor.

    Raises:
        TypeError: If an argument has the wrong type.
        ValueError: If *fd* or *minimum* is negative.
        RuntimeError: If the interpreter does not ship the ``fcntl`` module.
        OSError: If the file descriptor cannot be copied.
    """
    _validate_fd(fd)
    _validate_offset(minimum, "minimum")
    if minimum < 0:
        raise ValueError(f"minimum must not be negative, got {minimum}")
    if not isinstance(inheritable, bool):
        raise TypeError(f"inheritable must be a bool, got {type(inheritable).__name__}")
    module = _fcntl_module()
    command = F_DUPFD if inheritable else F_DUPFD_CLOEXEC
    return int(module.fcntl(fd, command, minimum))


def is_cloexec(fd: int) -> bool:
    """Return ``True`` if the file descriptor *fd* is close on exec.

    Args:
        fd: The file descriptor to read.

    Returns:
        ``True`` if the file descriptor is closed when the process executes a
        new program.

    Raises:
        TypeError: If *fd* is not an int.
        ValueError: If *fd* is negative.
        RuntimeError: If the interpreter does not ship the ``fcntl`` module.
        OSError: If the flags cannot be read.
    """
    return bool(get_descriptor_flags(fd) & FD_CLOEXEC)


def lock_modes() -> Dict[str, int]:
    """Return the lock modes of the wrapper, keyed by their name.

    Returns:
        A dictionary that maps the name of a lock mode to its operation,
        such as ``"exclusive"`` to :data:`LOCK_EX`.
    """
    return dict(_LOCK_MODES)


def lock_kind(name: str, blocking: bool = True) -> int:
    """Return the lock operation of the named mode.

    Args:
        name: The name of the mode.  One of ``"shared"``, ``"exclusive"``,
            or ``"unlock"``.
        blocking: Whether the operation waits for the lock.  A non blocking
            operation is combined with :data:`LOCK_NB`.

    Returns:
        The lock operation of the mode.

    Raises:
        TypeError: If *name* is not a str or *blocking* is not a bool.
        ValueError: If *name* is not a known lock mode.
    """
    if not isinstance(name, str):
        raise TypeError(f"name must be a str, got {type(name).__name__}")
    if not isinstance(blocking, bool):
        raise TypeError(f"blocking must be a bool, got {type(blocking).__name__}")
    key = name.strip().lower()
    if key not in _LOCK_MODES:
        raise ValueError(
            f"name must be one of {sorted(_LOCK_MODES)}, got {name!r}"
        )
    operation = _LOCK_MODES[key]
    if not blocking:
        operation |= LOCK_NB
    return operation


@contextmanager
def file_lock(
    path: str,
    mode: str = "exclusive",
    blocking: bool = True,
    create: bool = True,
) -> Iterator[int]:
    """Lock the file at *path* for the duration of the block.

    The file is opened, locked, and unlocked again when the block ends.  The
    file descriptor is closed as well, which releases the lock.

    Args:
        path: The path of the file to lock.
        mode: The name of the lock mode.  One of ``"shared"``,
            ``"exclusive"``, or ``"unlock"``.
        blocking: Whether the lock waits for the other programs.  A non
            blocking lock raises an :class:`OSError` instead of waiting.
        create: Whether the file is created when it does not exist.

    Yields:
        The file descriptor of the locked file.

    Raises:
        TypeError: If an argument has the wrong type.
        ValueError: If *mode* is not a known lock mode.
        RuntimeError: If the interpreter does not ship the ``fcntl`` module.
        OSError: If the file cannot be opened or locked.
    """
    operation = lock_kind(mode, blocking)
    if not isinstance(path, str):
        raise TypeError(f"path must be a str, got {type(path).__name__}")
    if not isinstance(create, bool):
        raise TypeError(f"create must be a bool, got {type(create).__name__}")
    flags = os.O_RDWR | (os.O_CREAT if create else 0)
    fd = os.open(path, flags, 0o666)
    try:
        flock(fd, operation)
        try:
            yield fd
        finally:
            try:
                unlock(fd)
            except OSError:  # pragma: no cover - the descriptor is already closed
                pass
    finally:
        os.close(fd)
