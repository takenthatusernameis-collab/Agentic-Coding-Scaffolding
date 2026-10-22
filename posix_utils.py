"""POSIX interface utilities wrapping the standard library :mod:`posix` module.

The :mod:`posix` module exposes the low level system calls of a Unix like
operating system.  It opens and closes file descriptors, reads and writes
bytes, inspects the metadata of a file, creates links, asks the kernel for
the limits of the system, and reports the scheduling policy of a process.

This wrapper validates every argument before the standard library is reached,
so a caller gets a clear :class:`TypeError` or :class:`ValueError` instead of
an opaque failure from the C layer.  It adds the conveniences the standard
library leaves to the caller: a descriptor is read until the requested number
of bytes arrived and written until every byte left, a directory is created
together with its parents, a path is removed whatever it is, the metadata of a
file is returned as one record, the scheduling policy is reported by name, and
a wait status is turned into a readable sentence.

.. note::

   The :mod:`posix` module only exists on Unix like platforms.  The import
   below degrades gracefully: when the interpreter does not ship the module,
   the helpers raise a :class:`RuntimeError` that names the missing module,
   while :func:`is_available` keeps working.

The wrapper never forks a process, never replaces the current process, and
never touches a path it was not given.
"""

from __future__ import annotations

import os
import signal
import stat
from typing import Any, Dict, List, NamedTuple, Optional, Sequence, Set, Tuple, Union

__all__ = [
    "DeviceNumber",
    "FileInfo",
    "ProcessTimes",
    "SchedulerParameters",
    "SystemName",
    "affinity_mask",
    "change_mode",
    "change_owner",
    "close_fd",
    "cpu_count",
    "create_directory",
    "create_hard_link",
    "create_pipe",
    "create_symbolic_link",
    "delete_file",
    "describe_wait_status",
    "device_number",
    "duplicate_fd",
    "duplicate_fd_to",
    "error_message",
    "exit_code_of",
    "file_info",
    "file_mode",
    "file_size",
    "is_available",
    "is_blocking",
    "is_executable",
    "is_inheritable",
    "is_readable",
    "is_terminal",
    "is_writable",
    "list_xattrs",
    "load_average",
    "login_name",
    "make_device",
    "open_fd",
    "path_accessible",
    "process_times",
    "read_at",
    "read_exactly",
    "read_fd",
    "read_symbolic_link",
    "read_xattr",
    "remove_directory",
    "remove_path",
    "remove_xattr",
    "rename_path",
    "scheduler_parameters",
    "scheduler_policy",
    "scheduler_policy_name",
    "scheduler_priorities",
    "seek_fd",
    "set_blocking",
    "set_inheritable",
    "set_umask",
    "sync_data",
    "sync_fd",
    "system_configuration",
    "system_limit",
    "system_limits",
    "terminal_device",
    "terminal_size",
    "truncate_fd",
    "uname",
    "write_all",
    "write_at",
    "write_fd",
    "write_xattr",
    "yield_cpu",
]

PathLike = Union[str, bytes, os.PathLike]

#: The names of the limits :func:`system_limits` reports by default.
DEFAULT_LIMIT_NAMES: Tuple[str, ...] = (
    "SC_ARG_MAX",
    "SC_CHILD_MAX",
    "SC_HOST_NAME_MAX",
    "SC_IOV_MAX",
    "SC_NGROUPS_MAX",
    "SC_NPROCESSORS",
    "SC_OPEN_MAX",
    "SC_PAGE_SIZE",
    "SC_SEM_NSEMS_MAX",
    "SC_STACK_SIZE",
    "SC_TTY_NAME_MAX",
)

#: The names of the scheduling policies the standard library defines.
SCHED_POLICIES: Dict[str, int] = {
    "SCHED_OTHER": 0,
    "SCHED_FIFO": 1,
    "SCHED_RR": 2,
    "SCHED_BATCH": 3,
    "SCHED_IDLE": 5,
    "SCHED_RESET_ON_FORK": 0x40000000,
}

try:
    import posix as _posix
except ImportError:  # pragma: no cover - the module is Unix only
    _posix = None  # type: ignore[assignment]


class SystemName(NamedTuple):
    """The identification of the running system."""

    system: str
    node: str
    release: str
    version: str
    machine: str


class FileInfo(NamedTuple):
    """The metadata of a file."""

    mode: int
    permissions: int
    size: int
    uid: int
    gid: int
    inode: int
    device: int
    hard_links: int
    atime: float
    mtime: float
    ctime: float
    is_directory: bool
    is_regular_file: bool
    is_symbolic_link: bool


class DeviceNumber(NamedTuple):
    """The major and minor number of a device."""

    major: int
    minor: int


class SchedulerParameters(NamedTuple):
    """The scheduling parameters of a process."""

    policy: str
    priority: int
    minimum_priority: int
    maximum_priority: int


class ProcessTimes(NamedTuple):
    """The times a process used the processor."""

    user: float
    system: float
    children_user: float
    children_system: float
    elapsed: float


def _posix_module() -> Any:
    """Return the standard library ``posix`` module.

    Returns:
        The imported :mod:`posix` module.

    Raises:
        RuntimeError: If the interpreter does not ship the ``posix`` module.
    """
    if _posix is None:  # pragma: no cover - the module is Unix only
        raise RuntimeError(
            "the standard library 'posix' module only exists on Unix like platforms; "
            "use the 'os' module for the calls that every platform provides"
        )
    return _posix


def _require_path(value: Any, name: str) -> Union[str, bytes]:
    """Return *value* as a path, raising ``TypeError`` for other types.

    Args:
        value: The value to check.
        name: The name of the argument, used in the error message.

    Returns:
        The value as a path.

    Raises:
        TypeError: If *value* is not a path.
    """
    if isinstance(value, (str, bytes)):
        return value
    if isinstance(value, os.PathLike):
        result = os.fspath(value)
        if isinstance(result, (str, bytes)):
            return result
    raise TypeError(f"{name} must be a path, got {type(value).__name__}")


def _require_fd(value: Any, name: str) -> int:
    """Return *value* as a file descriptor, raising ``TypeError`` or ``ValueError``.

    Args:
        value: The value to check.
        name: The name of the argument, used in the error message.

    Returns:
        The value as a file descriptor.

    Raises:
        TypeError: If *value* is not an int (or is a bool).
        ValueError: If *value* is negative.
    """
    if isinstance(value, bool) or not isinstance(value, int):
        raise TypeError(f"{name} must be an int, got {type(value).__name__}")
    if value < 0:
        raise ValueError(f"{name} must not be negative, got {value}")
    return value


def _require_count(value: Any, name: str) -> int:
    """Return *value* as a non negative number of bytes.

    Args:
        value: The value to check.
        name: The name of the argument, used in the error message.

    Returns:
        The value as an int.

    Raises:
        TypeError: If *value* is not an int (or is a bool).
        ValueError: If *value* is negative.
    """
    if isinstance(value, bool) or not isinstance(value, int):
        raise TypeError(f"{name} must be an int, got {type(value).__name__}")
    if value < 0:
        raise ValueError(f"{name} must not be negative, got {value}")
    return value


def _require_text(value: Any, name: str) -> str:
    """Return *value* as text, raising ``TypeError`` for other types.

    Args:
        value: The value to check.
        name: The name of the argument, used in the error message.

    Returns:
        The value as text.

    Raises:
        TypeError: If *value* is not a string.
    """
    if not isinstance(value, str):
        raise TypeError(f"{name} must be a str, got {type(value).__name__}")
    return value


def _require_bytes(value: Any, name: str) -> bytes:
    """Return *value* as bytes, raising ``TypeError`` for other types.

    Args:
        value: The value to check.
        name: The name of the argument, used in the error message.

    Returns:
        The value as bytes.

    Raises:
        TypeError: If *value* is not bytes-like.
    """
    if isinstance(value, bytes):
        return value
    if isinstance(value, (bytearray, memoryview)):
        return bytes(value)
    raise TypeError(f"{name} must be bytes, got {type(value).__name__}")


def _require_mode(value: Any, name: str) -> int:
    """Return *value* as a file mode, raising ``TypeError`` or ``ValueError``.

    Args:
        value: The value to check.
        name: The name of the argument, used in the error message.

    Returns:
        The value as a file mode.

    Raises:
        TypeError: If *value* is not an int (or is a bool).
        ValueError: If *value* is negative or holds bits outside the mode.
    """
    if isinstance(value, bool) or not isinstance(value, int):
        raise TypeError(f"{name} must be an int, got {type(value).__name__}")
    if value < 0:
        raise ValueError(f"{name} must not be negative, got {value}")
    if value & ~0o7777:
        raise ValueError(f"{name} must only hold the bits of a file mode, got {value}")
    return value


def _require_pid(value: Any, name: str) -> int:
    """Return *value* as a process identifier.

    Args:
        value: The value to check.
        name: The name of the argument, used in the error message.

    Returns:
        The value as a process identifier.

    Raises:
        TypeError: If *value* is not an int (or is a bool).
        ValueError: If *value* is negative.
    """
    if isinstance(value, bool) or not isinstance(value, int):
        raise TypeError(f"{name} must be an int, got {type(value).__name__}")
    if value < 0:
        raise ValueError(f"{name} must not be negative, got {value}")
    return value


def is_available() -> bool:
    """Return ``True`` if the interpreter ships the ``posix`` module.

    Returns:
        ``True`` when the standard library module could be imported.
    """
    return _posix is not None


def uname() -> SystemName:
    """Return the identification of the running system.

    Returns:
        The system, the node, the release, the version, and the machine.

    Raises:
        RuntimeError: If the interpreter does not ship the ``posix`` module.
    """
    module = _posix_module()
    result = module.uname()
    return SystemName(
        system=str(result.sysname),
        node=str(result.nodename),
        release=str(result.release),
        version=str(result.version),
        machine=str(result.machine),
    )


def cpu_count() -> Optional[int]:
    """Return the number of the processors of the system.

    Returns:
        The number of the processors, or ``None`` when the system does not
        report it.

    Raises:
        RuntimeError: If the interpreter does not ship the ``posix`` module.
    """
    module = _posix_module()
    count = module.cpu_count()
    return None if count is None else int(count)


def load_average() -> Tuple[float, float, float]:
    """Return the load average of the system.

    Returns:
        The load average over one, five, and fifteen minutes.

    Raises:
        RuntimeError: If the interpreter does not ship the ``posix`` module.
    """
    module = _posix_module()
    one, five, fifteen = module.getloadavg()
    return (float(one), float(five), float(fifteen))


def process_times() -> ProcessTimes:
    """Return the times the process used the processor.

    Returns:
        The user, the system, the children user, the children system, and the
        elapsed time.

    Raises:
        RuntimeError: If the interpreter does not ship the ``posix`` module.
    """
    module = _posix_module()
    result = module.times()
    return ProcessTimes(
        user=float(result.user),
        system=float(result.system),
        children_user=float(result.children_user),
        children_system=float(result.children_system),
        elapsed=float(result.elapsed),
    )


def system_limit(name: str) -> int:
    """Return the value of a limit of the system.

    Args:
        name: The name of the limit, such as ``"SC_PAGE_SIZE"``.

    Returns:
        The value of the limit.

    Raises:
        TypeError: If *name* is not a string.
        ValueError: If the interpreter does not know the limit.
        RuntimeError: If the interpreter does not ship the ``posix`` module.
    """
    module = _posix_module()
    _require_text(name, "name")
    names = getattr(module, "sysconf_names", {})
    if name not in names:
        raise ValueError(f"unknown system limit {name!r}")
    return int(module.sysconf(names[name]))


def system_limits(names: Optional[Sequence[str]] = None) -> Dict[str, int]:
    """Return the values of the limits of the system.

    Args:
        names: The names of the limits to report.  When it is ``None`` the
            limits of :data:`DEFAULT_LIMIT_NAMES` the interpreter knows are
            reported.

    Returns:
        The values of the limits, keyed by their name.

    Raises:
        TypeError: If *names* is not a sequence of strings.
        ValueError: If a name is not a limit the interpreter knows.
        RuntimeError: If the interpreter does not ship the ``posix`` module.
    """
    module = _posix_module()
    if names is None:
        available = getattr(module, "sysconf_names", {})
        selected = [name for name in DEFAULT_LIMIT_NAMES if name in available]
    else:
        if isinstance(names, (str, bytes)) or not isinstance(names, (list, tuple)):
            raise TypeError("names must be a sequence of strings")
        selected = []
        for name in names:
            _require_text(name, "name")
            selected.append(name)
    limits: Dict[str, int] = {}
    for name in selected:
        limits[name] = system_limit(name)
    return limits


def system_configuration(name: str) -> str:
    """Return the value of a configuration string of the system.

    Args:
        name: The name of the configuration, such as ``"CS_PATH"``.

    Returns:
        The value of the configuration.

    Raises:
        TypeError: If *name* is not a string.
        ValueError: If the interpreter does not know the configuration.
        RuntimeError: If the interpreter does not ship the ``posix`` module.
    """
    module = _posix_module()
    _require_text(name, "name")
    names = getattr(module, "confstr_names", {})
    if name not in names:
        raise ValueError(f"unknown system configuration {name!r}")
    return str(module.confstr(name))


def login_name() -> Optional[str]:
    """Return the name of the user that logged in.

    The standard library raises :exc:`OSError` when the process has no
    controlling terminal, which is the normal case of a service.

    Returns:
        The name of the user, or ``None`` when the system does not report it.

    Raises:
        RuntimeError: If the interpreter does not ship the ``posix`` module.
    """
    module = _posix_module()
    try:
        name = module.getlogin()
    except OSError:
        return None
    return str(name)


def terminal_device() -> str:
    """Return the path of the controlling terminal of the system.

    Returns:
        The path of the terminal.

    Raises:
        RuntimeError: If the interpreter does not ship the ``posix`` module.
    """
    module = _posix_module()
    return str(module.ctermid())


def open_fd(path: PathLike, flags: int, mode: int = 0o777) -> int:
    """Open a path and return the file descriptor of the open file.

    Args:
        path: The path of the file.
        flags: The flags of the open, such as :data:`os.O_RDONLY` combined
            with :data:`os.O_CREAT`.
        mode: The permissions of a file that is created.

    Returns:
        The file descriptor of the open file.

    Raises:
        TypeError: If *path* is not a path, or if *flags* or *mode* are not
            ints.
        ValueError: If *mode* holds bits outside the file mode.
        RuntimeError: If the interpreter does not ship the ``posix`` module.
    """
    module = _posix_module()
    location = _require_path(path, "path")
    if isinstance(flags, bool) or not isinstance(flags, int):
        raise TypeError(f"flags must be an int, got {type(flags).__name__}")
    permissions = _require_mode(mode, "mode")
    return int(module.open(location, flags, permissions))


def close_fd(fd: int) -> None:
    """Close a file descriptor.

    Args:
        fd: The file descriptor.

    Raises:
        TypeError: If *fd* is not an int.
        ValueError: If *fd* is negative.
        RuntimeError: If the interpreter does not ship the ``posix`` module.
    """
    module = _posix_module()
    descriptor = _require_fd(fd, "fd")
    module.close(descriptor)


def read_fd(fd: int, size: int) -> bytes:
    """Read up to *size* bytes from a file descriptor.

    A single read returns fewer bytes than requested when the file ends or
    when the descriptor is a pipe and no more data is ready.

    Args:
        fd: The file descriptor.
        size: The number of bytes to read.

    Returns:
        The bytes that were read, empty at the end of the file.

    Raises:
        TypeError: If *fd* or *size* are not ints.
        ValueError: If *fd* or *size* are negative.
        RuntimeError: If the interpreter does not ship the ``posix`` module.
    """
    module = _posix_module()
    descriptor = _require_fd(fd, "fd")
    count = _require_count(size, "size")
    return bytes(module.read(descriptor, count))


def read_exactly(fd: int, size: int) -> bytes:
    """Read exactly *size* bytes from a file descriptor.

    The descriptor is read until the requested number of bytes arrived, so a
    short read of a pipe does not lose the rest of the data.

    Args:
        fd: The file descriptor.
        size: The number of bytes to read.

    Returns:
        The bytes that were read.

    Raises:
        EOFError: If the file ends before *size* bytes were read.
        TypeError: If *fd* or *size* are not ints.
        ValueError: If *fd* or *size* are negative.
        RuntimeError: If the interpreter does not ship the ``posix`` module.
    """
    module = _posix_module()
    descriptor = _require_fd(fd, "fd")
    count = _require_count(size, "size")
    chunks: List[bytes] = []
    received = 0
    while received < count:
        chunk = bytes(module.read(descriptor, count - received))
        if not chunk:
            raise EOFError(
                f"expected {count} bytes but the file ended after {received} bytes"
            )
        chunks.append(chunk)
        received += len(chunk)
    return b"".join(chunks)


def write_fd(fd: int, data: bytes) -> int:
    """Write bytes to a file descriptor.

    A single write may write fewer bytes than requested, which the caller has
    to handle.  Use :func:`write_all` to write every byte.

    Args:
        fd: The file descriptor.
        data: The bytes to write.

    Returns:
        The number of bytes that were written.

    Raises:
        TypeError: If *fd* is not an int or *data* is not bytes-like.
        ValueError: If *fd* is negative.
        RuntimeError: If the interpreter does not ship the ``posix`` module.
    """
    module = _posix_module()
    descriptor = _require_fd(fd, "fd")
    payload = _require_bytes(data, "data")
    return int(module.write(descriptor, payload))


def write_all(fd: int, data: bytes) -> int:
    """Write every byte to a file descriptor.

    The descriptor is written until the whole payload left, so a short write
    of a pipe does not lose the rest of the data.

    Args:
        fd: The file descriptor.
        data: The bytes to write.

    Returns:
        The number of bytes that were written.

    Raises:
        TypeError: If *fd* is not an int or *data* is not bytes-like.
        ValueError: If *fd* is negative.
        RuntimeError: If the interpreter does not ship the ``posix`` module.
    """
    module = _posix_module()
    descriptor = _require_fd(fd, "fd")
    payload = _require_bytes(data, "data")
    written = 0
    while written < len(payload):
        count = int(module.write(descriptor, payload[written:]))
        if count <= 0:
            raise OSError(f"wrote {written} of {len(payload)} bytes before the write stopped")
        written += count
    return written


def seek_fd(fd: int, offset: int, whence: int = os.SEEK_SET) -> int:
    """Move the position of a file descriptor.

    Args:
        fd: The file descriptor.
        offset: The offset of the new position.
        whence: The origin of the offset: :data:`os.SEEK_SET`,
            :data:`os.SEEK_CUR`, or :data:`os.SEEK_END`.

    Returns:
        The new position of the descriptor.

    Raises:
        TypeError: If *fd*, *offset*, or *whence* are not ints.
        ValueError: If *fd* is negative or *whence* is not a known origin.
        RuntimeError: If the interpreter does not ship the ``posix`` module.
    """
    module = _posix_module()
    descriptor = _require_fd(fd, "fd")
    if isinstance(offset, bool) or not isinstance(offset, int):
        raise TypeError(f"offset must be an int, got {type(offset).__name__}")
    if isinstance(whence, bool) or not isinstance(whence, int):
        raise TypeError(f"whence must be an int, got {type(whence).__name__}")
    if whence not in (os.SEEK_SET, os.SEEK_CUR, os.SEEK_END):
        raise ValueError(
            "whence must be one of os.SEEK_SET, os.SEEK_CUR, os.SEEK_END, "
            f"got {whence}"
        )
    return int(module.lseek(descriptor, offset, whence))


def read_at(fd: int, size: int, offset: int) -> bytes:
    """Read bytes from a file descriptor at a given offset.

    The position of the descriptor is not changed.

    Args:
        fd: The file descriptor.
        size: The number of bytes to read.
        offset: The offset the read starts at.

    Returns:
        The bytes that were read, empty past the end of the file.

    Raises:
        TypeError: If *fd*, *size*, or *offset* are not ints.
        ValueError: If *fd* is negative or *size* is negative.
        RuntimeError: If the interpreter does not ship the ``posix`` module.
    """
    module = _posix_module()
    descriptor = _require_fd(fd, "fd")
    count = _require_count(size, "size")
    if isinstance(offset, bool) or not isinstance(offset, int):
        raise TypeError(f"offset must be an int, got {type(offset).__name__}")
    return bytes(module.pread(descriptor, count, offset))


def write_at(fd: int, data: bytes, offset: int) -> int:
    """Write bytes to a file descriptor at a given offset.

    The position of the descriptor is not changed.

    Args:
        fd: The file descriptor.
        data: The bytes to write.
        offset: The offset the write starts at.

    Returns:
        The number of bytes that were written.

    Raises:
        TypeError: If *fd* or *offset* are not ints, or *data* is not
            bytes-like.
        ValueError: If *fd* is negative.
        RuntimeError: If the interpreter does not ship the ``posix`` module.
    """
    module = _posix_module()
    descriptor = _require_fd(fd, "fd")
    payload = _require_bytes(data, "data")
    if isinstance(offset, bool) or not isinstance(offset, int):
        raise TypeError(f"offset must be an int, got {type(offset).__name__}")
    return int(module.pwrite(descriptor, payload, offset))


def duplicate_fd(fd: int) -> int:
    """Duplicate a file descriptor.

    The copy shares the file offset and the status flags with the original,
    and it is closed when the process executes a new program.

    Args:
        fd: The file descriptor.

    Returns:
        The file descriptor of the copy.

    Raises:
        TypeError: If *fd* is not an int.
        ValueError: If *fd* is negative.
        RuntimeError: If the interpreter does not ship the ``posix`` module.
    """
    module = _posix_module()
    descriptor = _require_fd(fd, "fd")
    return int(module.dup(descriptor))


def duplicate_fd_to(fd: int, target: int) -> int:
    """Duplicate a file descriptor onto another one.

    Args:
        fd: The file descriptor.
        target: The file descriptor the copy is written to.  It is closed
            first when it is open.

    Returns:
        The file descriptor of the copy.

    Raises:
        TypeError: If *fd* or *target* are not ints.
        ValueError: If *fd* or *target* are negative.
        RuntimeError: If the interpreter does not ship the ``posix`` module.
    """
    module = _posix_module()
    descriptor = _require_fd(fd, "fd")
    replacement = _require_fd(target, "target")
    return int(module.dup2(descriptor, replacement))


def create_pipe(nonblocking: bool = False) -> Tuple[int, int]:
    """Create a pipe and return the descriptors of its two ends.

    Args:
        nonblocking: Whether the ends of the pipe are opened in the
            non-blocking mode.

    Returns:
        The descriptor of the reading end and the descriptor of the writing
        end.

    Raises:
        TypeError: If *nonblocking* is not a bool.
        RuntimeError: If the interpreter does not ship the ``posix`` module.
    """
    module = _posix_module()
    if not isinstance(nonblocking, bool):
        raise TypeError(f"nonblocking must be a bool, got {type(nonblocking).__name__}")
    if nonblocking and hasattr(module, "pipe2"):
        flags = os.O_CLOEXEC | os.O_NONBLOCK
        read_fd, write_fd = module.pipe2(flags)
        return (int(read_fd), int(write_fd))
    read_fd, write_fd = module.pipe()
    return (int(read_fd), int(write_fd))


def is_terminal(fd: int) -> bool:
    """Return ``True`` if the descriptor is connected to a terminal.

    Args:
        fd: The file descriptor.

    Returns:
        ``True`` when the descriptor is a terminal.

    Raises:
        TypeError: If *fd* is not an int.
        ValueError: If *fd* is negative.
        RuntimeError: If the interpreter does not ship the ``posix`` module.
    """
    module = _posix_module()
    descriptor = _require_fd(fd, "fd")
    return bool(module.isatty(descriptor))


def is_blocking(fd: int) -> bool:
    """Return ``True`` if the descriptor is in the blocking mode.

    Args:
        fd: The file descriptor.

    Returns:
        ``True`` when the descriptor blocks.

    Raises:
        TypeError: If *fd* is not an int.
        ValueError: If *fd* is negative.
        RuntimeError: If the interpreter does not ship the ``posix`` module.
    """
    module = _posix_module()
    descriptor = _require_fd(fd, "fd")
    return bool(module.get_blocking(descriptor))


def set_blocking(fd: int, blocking: bool = True) -> None:
    """Set the blocking mode of a file descriptor.

    Args:
        fd: The file descriptor.
        blocking: Whether the descriptor blocks.

    Raises:
        TypeError: If *fd* is not an int or *blocking* is not a bool.
        ValueError: If *fd* is negative.
        RuntimeError: If the interpreter does not ship the ``posix`` module.
    """
    module = _posix_module()
    descriptor = _require_fd(fd, "fd")
    if not isinstance(blocking, bool):
        raise TypeError(f"blocking must be a bool, got {type(blocking).__name__}")
    module.set_blocking(descriptor, blocking)


def is_inheritable(fd: int) -> bool:
    """Return ``True`` if the descriptor survives the execution of a program.

    Args:
        fd: The file descriptor.

    Returns:
        ``True`` when the descriptor is inheritable.

    Raises:
        TypeError: If *fd* is not an int.
        ValueError: If *fd* is negative.
        RuntimeError: If the interpreter does not ship the ``posix`` module.
    """
    module = _posix_module()
    descriptor = _require_fd(fd, "fd")
    return bool(module.get_inheritable(descriptor))


def set_inheritable(fd: int, inheritable: bool = True) -> None:
    """Set whether the descriptor survives the execution of a program.

    Args:
        fd: The file descriptor.
        inheritable: Whether the descriptor is inheritable.

    Raises:
        TypeError: If *fd* is not an int or *inheritable* is not a bool.
        ValueError: If *fd* is negative.
        RuntimeError: If the interpreter does not ship the ``posix`` module.
    """
    module = _posix_module()
    descriptor = _require_fd(fd, "fd")
    if not isinstance(inheritable, bool):
        raise TypeError(f"inheritable must be a bool, got {type(inheritable).__name__}")
    module.set_inheritable(descriptor, inheritable)


def sync_fd(fd: int) -> None:
    """Write the file behind a descriptor to the storage device.

    Args:
        fd: The file descriptor.

    Raises:
        TypeError: If *fd* is not an int.
        ValueError: If *fd* is negative.
        RuntimeError: If the interpreter does not ship the ``posix`` module.
    """
    module = _posix_module()
    descriptor = _require_fd(fd, "fd")
    module.fsync(descriptor)


def sync_data(fd: int) -> None:
    """Write the data of a file behind a descriptor to the storage device.

    Unlike :func:`sync_fd` the metadata of the file is not written.

    Args:
        fd: The file descriptor.

    Raises:
        TypeError: If *fd* is not an int.
        ValueError: If *fd* is negative.
        RuntimeError: If the interpreter does not ship the ``posix`` module.
    """
    module = _posix_module()
    descriptor = _require_fd(fd, "fd")
    module.fdatasync(descriptor)


def truncate_fd(fd: int, length: int) -> None:
    """Set the length of the file behind a descriptor.

    Args:
        fd: The file descriptor.
        length: The new length of the file in bytes.

    Raises:
        TypeError: If *fd* or *length* are not ints.
        ValueError: If *fd* or *length* are negative.
        RuntimeError: If the interpreter does not ship the ``posix`` module.
    """
    module = _posix_module()
    descriptor = _require_fd(fd, "fd")
    size = _require_count(length, "length")
    module.ftruncate(descriptor, size)


def terminal_size(fd: int = 1) -> Tuple[int, int]:
    """Return the size of the terminal behind a descriptor.

    Args:
        fd: The file descriptor of the terminal.

    Returns:
        The number of the columns and the number of the lines.

    Raises:
        OSError: If the descriptor is not connected to a terminal.
        TypeError: If *fd* is not an int.
        ValueError: If *fd* is negative.
        RuntimeError: If the interpreter does not ship the ``posix`` module.
    """
    module = _posix_module()
    descriptor = _require_fd(fd, "fd")
    size = module.get_terminal_size(descriptor)
    return (int(size.columns), int(size.lines))


def file_info(path: PathLike, follow_symlinks: bool = True) -> FileInfo:
    """Return the metadata of a file as one record.

    Args:
        path: The path of the file.
        follow_symlinks: Whether a symbolic link is resolved.  When it is
            ``False`` the link itself is described.

    Returns:
        The metadata of the file.

    Raises:
        TypeError: If *path* is not a path or *follow_symlinks* is not a bool.
        RuntimeError: If the interpreter does not ship the ``posix`` module.
    """
    module = _posix_module()
    location = _require_path(path, "path")
    if not isinstance(follow_symlinks, bool):
        raise TypeError(
            f"follow_symlinks must be a bool, got {type(follow_symlinks).__name__}"
        )
    result = module.stat(location) if follow_symlinks else module.lstat(location)
    mode = int(result.st_mode)
    return FileInfo(
        mode=mode,
        permissions=stat.S_IMODE(mode),
        size=int(result.st_size),
        uid=int(result.st_uid),
        gid=int(result.st_gid),
        inode=int(result.st_ino),
        device=int(result.st_dev),
        hard_links=int(result.st_nlink),
        atime=float(result.st_atime),
        mtime=float(result.st_mtime),
        ctime=float(result.st_ctime),
        is_directory=stat.S_ISDIR(mode),
        is_regular_file=stat.S_ISREG(mode),
        is_symbolic_link=stat.S_ISLNK(mode),
    )


def file_mode(path: PathLike) -> int:
    """Return the permissions of a file.

    Args:
        path: The path of the file.

    Returns:
        The permission bits of the file.

    Raises:
        TypeError: If *path* is not a path.
        RuntimeError: If the interpreter does not ship the ``posix`` module.
    """
    module = _posix_module()
    location = _require_path(path, "path")
    return stat.S_IMODE(int(module.stat(location).st_mode))


def file_size(path: PathLike) -> int:
    """Return the size of a file in bytes.

    Args:
        path: The path of the file.

    Returns:
        The size of the file in bytes.

    Raises:
        TypeError: If *path* is not a path.
        RuntimeError: If the interpreter does not ship the ``posix`` module.
    """
    module = _posix_module()
    location = _require_path(path, "path")
    return int(module.stat(location).st_size)


def device_number(path: PathLike) -> DeviceNumber:
    """Return the major and minor number of the device behind a file.

    Args:
        path: The path of the file.

    Returns:
        The major and the minor number of the device.

    Raises:
        TypeError: If *path* is not a path.
        RuntimeError: If the interpreter does not ship the ``posix`` module.
    """
    module = _posix_module()
    location = _require_path(path, "path")
    device = int(module.stat(location).st_dev)
    return DeviceNumber(major=int(module.major(device)), minor=int(module.minor(device)))


def make_device(major: int, minor: int) -> int:
    """Return the device number of a major and a minor number.

    Args:
        major: The major number of the device.
        minor: The minor number of the device.

    Returns:
        The device number.

    Raises:
        TypeError: If *major* or *minor* are not ints.
        ValueError: If *major* or *minor* are negative.
        RuntimeError: If the interpreter does not ship the ``posix`` module.
    """
    module = _posix_module()
    major_number = _require_count(major, "major")
    minor_number = _require_count(minor, "minor")
    return int(module.makedev(major_number, minor_number))


def path_accessible(path: PathLike, mode: int = os.F_OK) -> bool:
    """Return ``True`` if the path can be used in the given way.

    Args:
        path: The path of the file.
        mode: :data:`os.F_OK` when the existence of the path is checked,
            :data:`os.R_OK` when it is checked for reading, :data:`os.W_OK`
            for writing, and :data:`os.X_OK` for execution.

    Returns:
        ``True`` when the path can be used in the given way.

    Raises:
        TypeError: If *path* is not a path or *mode* is not an int.
        ValueError: If *mode* is not a known access mode.
        RuntimeError: If the interpreter does not ship the ``posix`` module.
    """
    module = _posix_module()
    location = _require_path(path, "path")
    if isinstance(mode, bool) or not isinstance(mode, int):
        raise TypeError(f"mode must be an int, got {type(mode).__name__}")
    if mode not in (os.F_OK, os.R_OK, os.W_OK, os.X_OK):
        raise ValueError(
            "mode must be one of os.F_OK, os.R_OK, os.W_OK, os.X_OK, " f"got {mode}"
        )
    return bool(module.access(location, mode))


def is_readable(path: PathLike) -> bool:
    """Return ``True`` if the path can be read.

    Args:
        path: The path of the file.

    Returns:
        ``True`` when the path can be read.

    Raises:
        TypeError: If *path* is not a path.
        RuntimeError: If the interpreter does not ship the ``posix`` module.
    """
    return path_accessible(path, os.R_OK)


def is_writable(path: PathLike) -> bool:
    """Return ``True`` if the path can be written.

    Args:
        path: The path of the file.

    Returns:
        ``True`` when the path can be written.

    Raises:
        TypeError: If *path* is not a path.
        RuntimeError: If the interpreter does not ship the ``posix`` module.
    """
    return path_accessible(path, os.W_OK)


def is_executable(path: PathLike) -> bool:
    """Return ``True`` if the path can be executed.

    Args:
        path: The path of the file.

    Returns:
        ``True`` when the path can be executed.

    Raises:
        TypeError: If *path* is not a path.
        RuntimeError: If the interpreter does not ship the ``posix`` module.
    """
    return path_accessible(path, os.X_OK)


def create_directory(
    path: PathLike, mode: int = 0o777, parents: bool = False, exist_ok: bool = False
) -> None:
    """Create a directory.

    Args:
        path: The path of the directory.
        mode: The permissions of the directory.
        parents: Whether the missing parents of the directory are created.
        exist_ok: Whether an existing directory is accepted.

    Raises:
        FileExistsError: If the directory exists and *exist_ok* is ``False``.
        NotADirectoryError: If a parent of the directory is not a directory.
        TypeError: If *path* is not a path, or if the other arguments have the
            wrong type.
        ValueError: If *mode* holds bits outside the file mode.
        RuntimeError: If the interpreter does not ship the ``posix`` module.
    """
    module = _posix_module()
    location = _require_path(path, "path")
    permissions = _require_mode(mode, "mode")
    if not isinstance(parents, bool):
        raise TypeError(f"parents must be a bool, got {type(parents).__name__}")
    if not isinstance(exist_ok, bool):
        raise TypeError(f"exist_ok must be a bool, got {type(exist_ok).__name__}")
    if not parents:
        try:
            module.mkdir(location, permissions)
        except FileExistsError:
            if not exist_ok:
                raise
        return
    parent = os.path.dirname(location)
    if parent and parent != location:
        create_directory(parent, permissions, parents=True, exist_ok=True)
    try:
        module.mkdir(location, permissions)
    except FileExistsError:
        if not exist_ok:
            raise


def remove_directory(path: PathLike) -> None:
    """Remove an empty directory.

    Args:
        path: The path of the directory.

    Raises:
        TypeError: If *path* is not a path.
        RuntimeError: If the interpreter does not ship the ``posix`` module.
    """
    module = _posix_module()
    location = _require_path(path, "path")
    module.rmdir(location)


def delete_file(path: PathLike) -> None:
    """Remove a file or a symbolic link.

    Args:
        path: The path of the file.

    Raises:
        TypeError: If *path* is not a path.
        RuntimeError: If the interpreter does not ship the ``posix`` module.
    """
    module = _posix_module()
    location = _require_path(path, "path")
    module.unlink(location)


def remove_path(path: PathLike) -> None:
    """Remove a path whatever it is.

    A symbolic link is removed instead of the file it points to, a file is
    removed, and an empty directory is removed.

    Args:
        path: The path to remove.

    Raises:
        FileNotFoundError: If the path does not exist.
        TypeError: If *path* is not a path.
        RuntimeError: If the interpreter does not ship the ``posix`` module.
    """
    module = _posix_module()
    location = _require_path(path, "path")
    result = module.lstat(location)
    if stat.S_ISDIR(int(result.st_mode)):
        module.rmdir(location)
    else:
        module.unlink(location)


def rename_path(source: PathLike, target: PathLike) -> None:
    """Move a path to another one.

    Args:
        source: The path that is moved.
        target: The path it is moved to.

    Raises:
        TypeError: If *source* or *target* are not paths.
        RuntimeError: If the interpreter does not ship the ``posix`` module.
    """
    module = _posix_module()
    old = _require_path(source, "source")
    new = _require_path(target, "target")
    module.rename(old, new)


def create_hard_link(source: PathLike, target: PathLike) -> None:
    """Create a hard link to a file.

    Args:
        source: The path of the existing file.
        target: The path of the link that is created.

    Raises:
        TypeError: If *source* or *target* are not paths.
        RuntimeError: If the interpreter does not ship the ``posix`` module.
    """
    module = _posix_module()
    existing = _require_path(source, "source")
    link = _require_path(target, "target")
    module.link(existing, link)


def create_symbolic_link(source: PathLike, target: PathLike) -> None:
    """Create a symbolic link to a path.

    Args:
        source: The path the link points to.
        target: The path of the link that is created.

    Raises:
        TypeError: If *source* or *target* are not paths.
        RuntimeError: If the interpreter does not ship the ``posix`` module.
    """
    module = _posix_module()
    destination = _require_path(source, "source")
    link = _require_path(target, "target")
    module.symlink(destination, link)


def read_symbolic_link(path: PathLike) -> str:
    """Return the path a symbolic link points to.

    Args:
        path: The path of the symbolic link.

    Returns:
        The path the link points to.

    Raises:
        TypeError: If *path* is not a path.
        RuntimeError: If the interpreter does not ship the ``posix`` module.
    """
    module = _posix_module()
    location = _require_path(path, "path")
    return os.fsdecode(module.readlink(location))


def change_mode(path: PathLike, mode: int) -> None:
    """Set the permissions of a path.

    Args:
        path: The path of the file.
        mode: The permission bits of the file.

    Raises:
        TypeError: If *path* is not a path or *mode* is not an int.
        ValueError: If *mode* is negative or holds bits outside the file mode.
        RuntimeError: If the interpreter does not ship the ``posix`` module.
    """
    module = _posix_module()
    location = _require_path(path, "path")
    permissions = _require_mode(mode, "mode")
    module.chmod(location, permissions)


def change_owner(path: PathLike, uid: int, gid: int) -> None:
    """Set the owner and the group of a path.

    Args:
        path: The path of the file.
        uid: The user identifier of the new owner, or ``-1`` to keep it.
        gid: The group identifier of the new group, or ``-1`` to keep it.

    Raises:
        TypeError: If *path* is not a path or the identifiers are not ints.
        ValueError: If an identifier is smaller than ``-1``.
        RuntimeError: If the interpreter does not ship the ``posix`` module.
    """
    module = _posix_module()
    location = _require_path(path, "path")
    if isinstance(uid, bool) or not isinstance(uid, int):
        raise TypeError(f"uid must be an int, got {type(uid).__name__}")
    if isinstance(gid, bool) or not isinstance(gid, int):
        raise TypeError(f"gid must be an int, got {type(gid).__name__}")
    if uid < -1:
        raise ValueError(f"uid must not be smaller than -1, got {uid}")
    if gid < -1:
        raise ValueError(f"gid must not be smaller than -1, got {gid}")
    module.chown(location, uid, gid)


def set_umask(mask: int) -> int:
    """Set the mask of the permissions of the files that are created.

    Args:
        mask: The mask of the permissions.

    Returns:
        The mask that was set before.

    Raises:
        TypeError: If *mask* is not an int.
        ValueError: If *mask* is negative or holds bits outside the file mode.
        RuntimeError: If the interpreter does not ship the ``posix`` module.
    """
    module = _posix_module()
    permissions = _require_mode(mask, "mask")
    return int(module.umask(permissions))


def read_xattr(path: PathLike, name: str, follow_symlinks: bool = True) -> bytes:
    """Return the value of an extended attribute of a path.

    Args:
        path: The path of the file.
        name: The name of the attribute.
        follow_symlinks: Whether a symbolic link is resolved.

    Returns:
        The value of the attribute.

    Raises:
        TypeError: If *path* is not a path, *name* is not a string, or
            *follow_symlinks* is not a bool.
        RuntimeError: If the interpreter does not ship the ``posix`` module.
    """
    module = _posix_module()
    location = _require_path(path, "path")
    _require_text(name, "name")
    if not isinstance(follow_symlinks, bool):
        raise TypeError(
            f"follow_symlinks must be a bool, got {type(follow_symlinks).__name__}"
        )
    return bytes(module.getxattr(location, name, follow_symlinks=follow_symlinks))


def write_xattr(
    path: PathLike, name: str, value: bytes, follow_symlinks: bool = True
) -> None:
    """Set the value of an extended attribute of a path.

    Args:
        path: The path of the file.
        name: The name of the attribute.
        value: The value of the attribute.
        follow_symlinks: Whether a symbolic link is resolved.

    Raises:
        TypeError: If *path* is not a path, *name* is not a string, *value* is
            not bytes-like, or *follow_symlinks* is not a bool.
        RuntimeError: If the interpreter does not ship the ``posix`` module.
    """
    module = _posix_module()
    location = _require_path(path, "path")
    _require_text(name, "name")
    payload = _require_bytes(value, "value")
    if not isinstance(follow_symlinks, bool):
        raise TypeError(
            f"follow_symlinks must be a bool, got {type(follow_symlinks).__name__}"
        )
    module.setxattr(location, name, payload, follow_symlinks=follow_symlinks)


def list_xattrs(path: PathLike, follow_symlinks: bool = True) -> List[str]:
    """Return the names of the extended attributes of a path.

    Args:
        path: The path of the file.
        follow_symlinks: Whether a symbolic link is resolved.

    Returns:
        The names of the attributes.

    Raises:
        TypeError: If *path* is not a path or *follow_symlinks* is not a bool.
        RuntimeError: If the interpreter does not ship the ``posix`` module.
    """
    module = _posix_module()
    location = _require_path(path, "path")
    if not isinstance(follow_symlinks, bool):
        raise TypeError(
            f"follow_symlinks must be a bool, got {type(follow_symlinks).__name__}"
        )
    return [str(item) for item in module.listxattr(location, follow_symlinks=follow_symlinks)]


def remove_xattr(path: PathLike, name: str, follow_symlinks: bool = True) -> None:
    """Remove an extended attribute of a path.

    Args:
        path: The path of the file.
        name: The name of the attribute.
        follow_symlinks: Whether a symbolic link is resolved.

    Raises:
        TypeError: If *path* is not a path, *name* is not a string, or
            *follow_symlinks* is not a bool.
        RuntimeError: If the interpreter does not ship the ``posix`` module.
    """
    module = _posix_module()
    location = _require_path(path, "path")
    _require_text(name, "name")
    if not isinstance(follow_symlinks, bool):
        raise TypeError(
            f"follow_symlinks must be a bool, got {type(follow_symlinks).__name__}"
        )
    module.removexattr(location, name, follow_symlinks=follow_symlinks)


def scheduler_policy(pid: int = 0) -> int:
    """Return the scheduling policy of a process.

    Args:
        pid: The identifier of the process, or ``0`` for the current one.

    Returns:
        The value of the policy, such as :data:`SCHED_POLICIES`.

    Raises:
        TypeError: If *pid* is not an int.
        ValueError: If *pid* is negative.
        RuntimeError: If the interpreter does not ship the ``posix`` module.
    """
    module = _posix_module()
    process = _require_pid(pid, "pid")
    return int(module.sched_getscheduler(process))


def scheduler_policy_name(pid: int = 0) -> str:
    """Return the name of the scheduling policy of a process.

    Args:
        pid: The identifier of the process, or ``0`` for the current one.

    Returns:
        The name of the policy, such as ``"SCHED_OTHER"``, or ``"SCHED_<value>"``
        when the policy is not one the standard library names.

    Raises:
        TypeError: If *pid* is not an int.
        ValueError: If *pid* is negative.
        RuntimeError: If the interpreter does not ship the ``posix`` module.
    """
    policy = scheduler_policy(pid)
    for name, value in SCHED_POLICIES.items():
        if value == policy:
            return name
    return f"SCHED_{policy}"


def scheduler_priorities(policy: int) -> Tuple[int, int]:
    """Return the lowest and the highest priority of a scheduling policy.

    Args:
        policy: The value of the policy, such as :data:`SCHED_POLICIES`.

    Returns:
        The lowest and the highest priority of the policy.

    Raises:
        TypeError: If *policy* is not an int.
        ValueError: If *policy* is negative.
        RuntimeError: If the interpreter does not ship the ``posix`` module.
    """
    module = _posix_module()
    if isinstance(policy, bool) or not isinstance(policy, int):
        raise TypeError(f"policy must be an int, got {type(policy).__name__}")
    if policy < 0:
        raise ValueError(f"policy must not be negative, got {policy}")
    lowest = int(module.sched_get_priority_min(policy))
    highest = int(module.sched_get_priority_max(policy))
    return (lowest, highest)


def scheduler_parameters(pid: int = 0) -> SchedulerParameters:
    """Return the scheduling parameters of a process.

    Args:
        pid: The identifier of the process, or ``0`` for the current one.

    Returns:
        The name of the policy, its priority, and the lowest and the highest
        priority of the policy.

    Raises:
        TypeError: If *pid* is not an int.
        ValueError: If *pid* is negative.
        RuntimeError: If the interpreter does not ship the ``posix`` module.
    """
    module = _posix_module()
    process = _require_pid(pid, "pid")
    parameters = module.sched_getparam(process)
    priority = int(parameters.sched_priority)
    policy = int(module.sched_getscheduler(process))
    lowest = int(module.sched_get_priority_min(policy))
    highest = int(module.sched_get_priority_max(policy))
    return SchedulerParameters(
        policy=scheduler_policy_name(process),
        priority=priority,
        minimum_priority=lowest,
        maximum_priority=highest,
    )


def affinity_mask(pid: int = 0) -> Set[int]:
    """Return the processors a process may run on.

    Args:
        pid: The identifier of the process, or ``0`` for the current one.

    Returns:
        The identifiers of the processors.

    Raises:
        TypeError: If *pid* is not an int.
        ValueError: If *pid* is negative.
        RuntimeError: If the interpreter does not ship the ``posix`` module.
    """
    module = _posix_module()
    process = _require_pid(pid, "pid")
    return {int(item) for item in module.sched_getaffinity(process)}


def yield_cpu() -> None:
    """Give up the rest of the time slice of the processor.

    Raises:
        RuntimeError: If the interpreter does not ship the ``posix`` module.
    """
    module = _posix_module()
    module.sched_yield()


def exit_code_of(status: int) -> int:
    """Return the exit code of a wait status.

    Args:
        status: The status the standard library reported for a process.

    Returns:
        The exit code of the process.

    Raises:
        TypeError: If *status* is not an int.
        ValueError: If *status* is negative.
        RuntimeError: If the interpreter does not ship the ``posix`` module.
    """
    module = _posix_module()
    if isinstance(status, bool) or not isinstance(status, int):
        raise TypeError(f"status must be an int, got {type(status).__name__}")
    if status < 0:
        raise ValueError(f"status must not be negative, got {status}")
    return int(module.waitstatus_to_exitcode(status))


def describe_wait_status(status: int) -> str:
    """Return a readable description of a wait status.

    Args:
        status: The status the standard library reported for a process.

    Returns:
        A sentence that names what happened to the process.

    Raises:
        TypeError: If *status* is not an int.
        ValueError: If *status* is negative.
        RuntimeError: If the interpreter does not ship the ``posix`` module.
    """
    module = _posix_module()
    if isinstance(status, bool) or not isinstance(status, int):
        raise TypeError(f"status must be an int, got {type(status).__name__}")
    if status < 0:
        raise ValueError(f"status must not be negative, got {status}")
    if module.WIFEXITED(status):
        return f"exited with code {module.WEXITSTATUS(status)}"
    if module.WIFSIGNALED(status):
        return f"terminated by signal {_signal_name(module.WTERMSIG(status))}"
    if module.WIFSTOPPED(status):
        return f"stopped by signal {_signal_name(module.WSTOPSIG(status))}"
    if module.WIFCONTINUED(status):
        return "continued"
    return f"unknown wait status {status}"


def _signal_name(number: int) -> str:
    """Return the name of a signal number.

    Args:
        number: The number of the signal.

    Returns:
        The name of the signal, or ``"signal <number>"`` when the signal is
        not one the standard library names.
    """
    try:
        return signal.Signals(number).name
    except ValueError:
        return f"signal {number}"


def error_message(code: int) -> str:
    """Return the message of an error number.

    Args:
        code: The number of the error.

    Returns:
        The message of the error.

    Raises:
        TypeError: If *code* is not an int.
        RuntimeError: If the interpreter does not ship the ``posix`` module.
    """
    module = _posix_module()
    if isinstance(code, bool) or not isinstance(code, int):
        raise TypeError(f"code must be an int, got {type(code).__name__}")
    return str(module.strerror(code))
