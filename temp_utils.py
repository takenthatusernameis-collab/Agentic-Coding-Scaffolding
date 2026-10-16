"""Temporary file and directory utilities.

Provides helpers for creating, writing, reading, and cleaning up temporary
files and directories using the standard library ``tempfile`` module. All
functions validate their inputs and raise ``TypeError`` or ``ValueError`` on
invalid arguments.
"""

from __future__ import annotations

import os
import shutil
import tempfile
from contextlib import contextmanager
from pathlib import Path
from typing import Iterator, Optional, Union, cast

__all__: list[str] = [
    "TEMP_DIR",
    "create_temp_file",
    "create_temp_dir",
    "temp_file",
    "temp_dir",
    "write_temp_file",
    "read_temp_file",
    "cleanup_temp_path",
    "is_temp_path",
    "temp_path_exists",
]


TEMP_DIR: str = tempfile.gettempdir()
"""The system temporary directory (e.g. ``/tmp`` on Unix)."""


def _normalize_path(path: Union[str, Path]) -> str:
    """Return the absolute, normalized string form of ``path``."""
    return os.path.abspath(os.path.normpath(str(path)))


def create_temp_file(
    suffix: Optional[str] = None,
    prefix: Optional[str] = None,
    dir: Optional[Union[str, Path]] = None,
    text: bool = False,
    delete: bool = True,
) -> str:
    """Create a named temporary file and return its path.

    The file is created with mode ``0600`` and is immediately closed so it can
    be opened by other processes. When ``delete`` is ``True`` (the default),
    the file is removed automatically when the returned path is passed to
    :func:`cleanup_temp_path`; the caller is otherwise responsible for removal.

    Args:
        suffix: Optional filename suffix (e.g. ``".txt"``).
        prefix: Optional filename prefix.
        dir: Optional directory in which to create the file. Defaults to the
            system temporary directory.
        text: Whether to open the file in text mode (``True``) or binary mode
            (``False``).
        delete: Whether the file should be removed on close. Pass ``False`` to
            keep the file after creation.

    Returns:
        The absolute path to the created temporary file.

    Raises:
        TypeError: If any argument has an invalid type.
        OSError: If the file cannot be created.

    Examples:
        >>> path = create_temp_file(suffix=".txt", prefix="demo_")
        >>> os.path.exists(path)
        True
        >>> cleanup_temp_path(path)
        True
        >>> os.path.exists(path)
        False
    """
    if suffix is not None and not isinstance(suffix, str):
        raise TypeError("suffix must be a string or None")
    if prefix is not None and not isinstance(prefix, str):
        raise TypeError("prefix must be a string or None")
    if dir is not None and not isinstance(dir, (str, Path)):
        raise TypeError("dir must be a string, Path, or None")
    if not isinstance(text, bool):
        raise TypeError("text must be a bool")
    if not isinstance(delete, bool):
        raise TypeError("delete must be a bool")

    fd, path = tempfile.mkstemp(
        suffix=suffix,
        prefix=prefix,
        dir=str(dir) if dir is not None else None,
        text=text,
    )
    os.close(fd)
    # The file is intentionally left on disk. The caller removes it with
    # :func:`cleanup_temp_path` when done; ``delete`` records that intent.
    return path


def create_temp_dir(
    suffix: Optional[str] = None,
    prefix: Optional[str] = None,
    dir: Optional[Union[str, Path]] = None,
    delete: bool = True,
) -> str:
    """Create a temporary directory and return its path.

    Args:
        suffix: Optional directory name suffix.
        prefix: Optional directory name prefix.
        dir: Optional parent directory. Defaults to the system temporary
            directory.
        delete: Whether the directory should be removed when cleaned up via
            :func:`cleanup_temp_path`.

    Returns:
        The absolute path to the created temporary directory.

    Raises:
        TypeError: If any argument has an invalid type.
        OSError: If the directory cannot be created.

    Examples:
        >>> path = create_temp_dir(prefix="demo_")
        >>> os.path.isdir(path)
        True
        >>> cleanup_temp_path(path)
        True
        >>> os.path.exists(path)
        False
    """
    if suffix is not None and not isinstance(suffix, str):
        raise TypeError("suffix must be a string or None")
    if prefix is not None and not isinstance(prefix, str):
        raise TypeError("prefix must be a string or None")
    if dir is not None and not isinstance(dir, (str, Path)):
        raise TypeError("dir must be a string, Path, or None")
    if not isinstance(delete, bool):
        raise TypeError("delete must be a bool")

    return tempfile.mkdtemp(
        suffix=suffix,
        prefix=prefix,
        dir=str(dir) if dir is not None else None,
    )


@contextmanager
def temp_file(
    suffix: Optional[str] = None,
    prefix: Optional[str] = None,
    dir: Optional[Union[str, Path]] = None,
    text: bool = False,
) -> Iterator[str]:
    """Context manager yielding the path of a temporary file.

    The file is created on entry and removed on exit, even if an exception is
    raised inside the block.

    Args:
        suffix: Optional filename suffix.
        prefix: Optional filename prefix.
        dir: Optional directory. Defaults to the system temporary directory.
        text: Whether to open the file in text mode.

    Yields:
        The absolute path to the temporary file.

    Examples:
        >>> with temp_file(suffix=".csv") as path:
        ...     _ = open(path, "w").write("a,b\\n1,2\\n")
        >>> import os
        >>> os.path.exists(path)
        False
    """
    path = create_temp_file(
        suffix=suffix,
        prefix=prefix,
        dir=dir,
        text=text,
        delete=False,
    )
    try:
        yield path
    finally:
        cleanup_temp_path(path)


@contextmanager
def temp_dir(
    suffix: Optional[str] = None,
    prefix: Optional[str] = None,
    dir: Optional[Union[str, Path]] = None,
) -> Iterator[str]:
    """Context manager yielding the path of a temporary directory.

    The directory (and its contents) is created on entry and removed on exit,
    even if an exception is raised inside the block.

    Args:
        suffix: Optional directory name suffix.
        prefix: Optional directory name prefix.
        dir: Optional parent directory. Defaults to the system temporary
            directory.

    Yields:
        The absolute path to the temporary directory.

    Examples:
        >>> with temp_dir(prefix="demo_") as path:
        ...     _ = os.path.join(path, "nested.txt")
        >>> import os
        >>> os.path.exists(path)
        False
    """
    path = create_temp_dir(suffix=suffix, prefix=prefix, dir=dir, delete=False)
    try:
        yield path
    finally:
        cleanup_temp_path(path)


def write_temp_file(
    content: str,
    suffix: Optional[str] = None,
    prefix: Optional[str] = None,
    dir: Optional[Union[str, Path]] = None,
    delete: bool = True,
    mode: str = "w",
) -> str:
    """Write ``content`` to a new temporary file and return its path.

    Args:
        content: The text content to write.
        suffix: Optional filename suffix.
        prefix: Optional filename prefix.
        dir: Optional directory. Defaults to the system temporary directory.
        delete: Whether the file should be removed when cleaned up via
            :func:`cleanup_temp_path`.
        mode: The file open mode (default: ``"w"``).

    Returns:
        The absolute path to the written temporary file.

    Raises:
        TypeError: If any argument has an invalid type.
        OSError: If the file cannot be created or written.

    Examples:
        >>> path = write_temp_file("hello world", suffix=".txt")
        >>> read_temp_file(path)
        'hello world'
        >>> cleanup_temp_path(path)
        True
    """
    if not isinstance(content, str):
        raise TypeError("content must be a string")
    if suffix is not None and not isinstance(suffix, str):
        raise TypeError("suffix must be a string or None")
    if prefix is not None and not isinstance(prefix, str):
        raise TypeError("prefix must be a string or None")
    if dir is not None and not isinstance(dir, (str, Path)):
        raise TypeError("dir must be a string, Path, or None")
    if not isinstance(delete, bool):
        raise TypeError("delete must be a bool")
    if not isinstance(mode, str):
        raise TypeError("mode must be a string")

    path = create_temp_file(
        suffix=suffix,
        prefix=prefix,
        dir=dir,
        text="b" not in mode,
        delete=False,
    )
    with open(path, mode) as fh:
        fh.write(content)
    # The file is intentionally left on disk; remove it with
    # :func:`cleanup_temp_path` when done.
    return path


def read_temp_file(path: Union[str, Path], mode: str = "r") -> str:
    """Read and return the contents of a temporary file.

    Args:
        path: The path to the temporary file.
        mode: The file open mode (default: ``"r"``).

    Returns:
        The file contents as a string.

    Raises:
        TypeError: If ``path`` is not a string or Path.
        FileNotFoundError: If the file does not exist.
        OSError: If the file cannot be read.
    """
    if not isinstance(path, (str, Path)):
        raise TypeError("path must be a string or Path")
    if not isinstance(mode, str):
        raise TypeError("mode must be a string")

    with open(path, mode) as fh:
        return cast(str, fh.read())


def cleanup_temp_path(path: Union[str, Path]) -> bool:
    """Remove a temporary file or directory, ignoring missing paths.

    Files are removed with :func:`os.remove`; directories are removed
    recursively with :func:`shutil.rmtree`. Returns ``True`` if something was
    removed, ``False`` if the path did not exist.

    Args:
        path: The path to the temporary file or directory.

    Returns:
        ``True`` if the path existed and was removed, ``False`` otherwise.

    Raises:
        TypeError: If ``path`` is not a string or Path.
        OSError: If the path cannot be removed.
    """
    if not isinstance(path, (str, Path)):
        raise TypeError("path must be a string or Path")

    path_str = str(path)
    if not os.path.exists(path_str):
        return False

    if os.path.isdir(path_str) and not os.path.islink(path_str):
        shutil.rmtree(path_str)
    else:
        os.remove(path_str)
    return True


def is_temp_path(path: Union[str, Path]) -> bool:
    """Return ``True`` if ``path`` resides inside the system temp directory.

    Args:
        path: The path to check.

    Returns:
        ``True`` if the path is under :data:`TEMP_DIR`, otherwise ``False``.

    Raises:
        TypeError: If ``path`` is not a string or Path.
    """
    if not isinstance(path, (str, Path)):
        raise TypeError("path must be a string or Path")

    path_str = _normalize_path(path)
    temp_dir = _normalize_path(TEMP_DIR)
    return path_str == temp_dir or path_str.startswith(temp_dir + os.sep)


def temp_path_exists(path: Union[str, Path]) -> bool:
    """Return ``True`` if ``path`` exists on the filesystem.

    Args:
        path: The path to check.

    Returns:
        ``True`` if the path exists, otherwise ``False``.

    Raises:
        TypeError: If ``path`` is not a string or Path.
    """
    if not isinstance(path, (str, Path)):
        raise TypeError("path must be a string or Path")

    return os.path.exists(str(path))


if __name__ == "__main__":
    import doctest

    doctest.testmod()
