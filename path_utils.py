"""Path manipulation utilities for working with filesystem paths."""

from __future__ import annotations

import os
from pathlib import Path, PurePath
from typing import List, Union

__all__: List[str] = [
    "join_path",
    "normalize_path",
    "get_absolute_path",
    "get_relative_path",
    "get_parent_dir",
    "get_file_name",
    "get_file_stem",
    "get_file_extension",
    "change_extension",
    "is_absolute",
    "get_path_components",
    "get_common_path",
    "ensure_extension",
]


def join_path(*parts: Union[str, Path]) -> str:
    """Join path components into a single path string.

    Args:
        *parts: Path components to join.

    Returns:
        The joined path as a string.

    Examples:
        >>> join_path("a", "b", "c")
        'a/b/c'
        >>> join_path("/usr", "local", "bin")
        '/usr/local/bin'
    """
    return str(Path(*[str(p) for p in parts]))


def normalize_path(path: Union[str, Path]) -> str:
    """Normalize a path by resolving redundant separators and relative components.

    Unlike :func:`get_absolute_path`, this does not resolve the path against the
    current working directory; it only collapses redundant separators and ``..``
    / ``.`` components.

    Args:
        path: The path to normalize.

    Returns:
        The normalized path as a string.

    Examples:
        >>> normalize_path("a//b/../c")
        'a/c'
        >>> normalize_path("/usr/./local//bin")
        '/usr/local/bin'
    """
    parts: List[str] = []
    is_absolute = PurePath(path).is_absolute()
    for part in PurePath(path).parts:
        if part == os.sep and is_absolute:
            # Root separator is handled by the prefix below.
            continue
        if part in (".", ".."):
            if part == "..":
                if parts and parts[-1] != "..":
                    parts.pop()
                elif not is_absolute:
                    parts.append("..")
            continue
        parts.append(part)
    if not parts:
        return os.sep if is_absolute else "."
    if is_absolute:
        return os.sep + os.sep.join(parts)
    return os.sep.join(parts)


def get_absolute_path(path: Union[str, Path]) -> str:
    """Return the absolute version of a path.

    Args:
        path: The path to convert.

    Returns:
        The absolute path as a string.

    Examples:
        >>> isinstance(get_absolute_path("foo"), str)
        True
    """
    return str(Path(path).absolute())


def get_relative_path(path: Union[str, Path], start: Union[str, Path] = ".") -> str:
    """Return a path relative to a starting directory.

    Args:
        path: The target path.
        start: The base directory (default: current directory).

    Returns:
        The relative path as a string.

    Raises:
        ValueError: If the path is not relative to the start directory.

    Examples:
        >>> get_relative_path("/usr/local/bin", "/usr")
        'local/bin'
    """
    return str(Path(path).relative_to(Path(start)))


def get_parent_dir(path: Union[str, Path]) -> str:
    """Return the parent directory of a path.

    Args:
        path: The file or directory path.

    Returns:
        The parent directory as a string.

    Examples:
        >>> get_parent_dir("/usr/local/bin/python")
        '/usr/local/bin'
        >>> get_parent_dir("file.txt")
        '.'
    """
    return str(Path(path).parent)


def get_file_name(path: Union[str, Path]) -> str:
    """Return the file name (last component) of a path.

    Args:
        path: The file or directory path.

    Returns:
        The file name as a string.

    Examples:
        >>> get_file_name("/usr/local/bin/python")
        'python'
        >>> get_file_name("archive.tar.gz")
        'archive.tar.gz'
    """
    return Path(path).name


def get_file_stem(path: Union[str, Path]) -> str:
    """Return the file name without its final extension.

    Args:
        path: The file path.

    Returns:
        The file stem as a string.

    Examples:
        >>> get_file_stem("/usr/local/script.py")
        'script'
        >>> get_file_stem("archive.tar.gz")
        'archive.tar'
    """
    return Path(path).stem


def get_file_extension(path: Union[str, Path]) -> str:
    """Return the file extension (including the leading dot) of a path.

    Args:
        path: The file path.

    Returns:
        The file extension as a string, or an empty string if none.

    Examples:
        >>> get_file_extension("script.py")
        '.py'
        >>> get_file_extension("Makefile")
        ''
        >>> get_file_extension("archive.tar.gz")
        '.gz'
    """
    return Path(path).suffix


def change_extension(path: Union[str, Path], extension: str) -> str:
    """Return a path with the file extension replaced.

    The new extension should include the leading dot if desired.

    Args:
        path: The file path.
        extension: The new extension (with or without leading dot).

    Returns:
        The path with the new extension as a string.

    Examples:
        >>> change_extension("script.py", ".txt")
        'script.txt'
        >>> change_extension("image.png", "jpg")
        'image.jpg'
    """
    if extension and not extension.startswith("."):
        extension = "." + extension
    return str(Path(path).with_suffix(extension))


def is_absolute(path: Union[str, Path]) -> bool:
    """Return True if the path is absolute.

    Args:
        path: The path to check.

    Returns:
        True if the path is absolute, False otherwise.

    Examples:
        >>> is_absolute("/usr/local/bin")
        True
        >>> is_absolute("relative/path")
        False
    """
    return Path(path).is_absolute()


def get_path_components(path: Union[str, Path]) -> List[str]:
    """Split a path into its individual components.

    Args:
        path: The path to split.

    Returns:
        A list of path component strings.

    Examples:
        >>> get_path_components("/usr/local/bin")
        ['/', 'usr', 'local', 'bin']
        >>> get_path_components("a/b/c")
        ['a', 'b', 'c']
    """
    parts = Path(path).parts
    return [str(p) for p in parts]


def get_common_path(*paths: Union[str, Path]) -> str:
    """Return the longest common path prefix of the given paths.

    Args:
        *paths: Two or more paths to compare.

    Returns:
        The common path prefix as a string.

    Raises:
        ValueError: If fewer than two paths are provided.

    Examples:
        >>> get_common_path("/a/b/c", "/a/b/d")
        '/a/b'
        >>> get_common_path("x/y/z", "x/y/w")
        'x/y'
    """
    if len(paths) < 2:
        raise ValueError("At least two paths are required")
    resolved = [Path(p).parts for p in paths]
    common: List[str] = []
    for parts in zip(*resolved):
        if all(part == parts[0] for part in parts):
            common.append(parts[0])
        else:
            break
    if not common:
        return ""
    return str(PurePath(*common))


def ensure_extension(path: Union[str, Path], extension: str) -> str:
    """Ensure a path has the given extension, adding it if missing.

    The extension should include the leading dot if desired.

    Args:
        path: The file path.
        extension: The required extension.

    Returns:
        The path with the extension guaranteed as a string.

    Examples:
        >>> ensure_extension("script.py", ".py")
        'script.py'
        >>> ensure_extension("script", ".py")
        'script.py'
        >>> ensure_extension("image.png", ".py")
        'image.png.py'
    """
    if not extension.startswith("."):
        extension = "." + extension
    current = Path(path).suffix
    if current == extension:
        return str(path)
    return str(Path(path).with_name(Path(path).name + extension))
