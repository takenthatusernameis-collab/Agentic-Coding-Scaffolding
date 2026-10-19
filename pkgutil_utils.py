"""Utilities for package and module discovery (wrapping :mod:`pkgutil`).

This module provides a small, validated layer over the standard library
``pkgutil`` module for locating modules inside packages, reading package data
files, and resolving importable names. All functions validate their inputs and
raise ``TypeError`` on invalid arguments.
"""

from __future__ import annotations

import importlib.util
import pkgutil
from typing import Any, Callable, Sequence

__all__ = [
    "iter_modules",
    "walk_packages",
    "get_data",
    "read_text",
    "resolve_name",
    "iter_importers",
    "extend_path",
    "find_spec",
]


def _validate_path(path: Sequence[str] | None) -> list[str] | None:
    """Validate and normalize a sequence of search directories.

    Args:
        path: Optional sequence of directory paths to search.

    Returns:
        A list of directory paths, or None when *path* is None.

    Raises:
        TypeError: If *path* is not None and not a sequence of strings.
    """
    if path is None:
        return None
    if isinstance(path, (str, bytes)):
        raise TypeError("path must be a sequence of strings, not a single string")
    if not isinstance(path, Sequence):
        raise TypeError("path must be a sequence of strings")
    for entry in path:
        if not isinstance(entry, str):
            raise TypeError("path entries must be strings")
    return list(path)


def _validate_prefix(prefix: str) -> str:
    """Validate a module name prefix.

    Args:
        prefix: Prefix prepended to discovered module names.

    Returns:
        The validated prefix.

    Raises:
        TypeError: If *prefix* is not a string.
    """
    if not isinstance(prefix, str):
        raise TypeError("prefix must be a str")
    return prefix


def iter_modules(
    path: Sequence[str] | None = None, prefix: str = ""
) -> list[tuple[str, bool]]:
    """List the modules found in *path*.

    Args:
        path: Optional sequence of directories to search. When None the
            current ``sys.path`` is searched.
        prefix: Prefix prepended to every discovered module name.

    Returns:
        A list of ``(name, is_package)`` tuples.

    Raises:
        TypeError: If *path* is not a sequence of strings or *prefix* is not
            a string.
    """
    directories = _validate_path(path)
    _validate_prefix(prefix)
    return [(info.name, info.ispkg) for info in pkgutil.iter_modules(directories, prefix)]


def walk_packages(
    path: Sequence[str] | None = None,
    prefix: str = "",
    onerror: Callable[[str], None] | None = None,
) -> list[tuple[str, bool]]:
    """Recursively list the modules and sub-packages found in *path*.

    Args:
        path: Optional sequence of directories to search. When None the
            current ``sys.path`` is searched.
        prefix: Prefix prepended to every discovered module name.
        onerror: Optional callable invoked with the name of a package that
            could not be imported.

    Returns:
        A list of ``(name, is_package)`` tuples for every discovered module.

    Raises:
        TypeError: If *path* is not a sequence of strings, *prefix* is not a
            string, or *onerror* is not callable.
    """
    directories = _validate_path(path)
    _validate_prefix(prefix)
    if onerror is not None and not callable(onerror):
        raise TypeError("onerror must be callable")
    found = pkgutil.walk_packages(directories, prefix, onerror)
    return [(info.name, info.ispkg) for info in found]


def get_data(package: str, resource: str) -> bytes:
    """Read a data file shipped inside *package*.

    Args:
        package: Name of the package that contains the resource.
        resource: Name of the resource file inside the package.

    Returns:
        The raw bytes of the resource.

    Raises:
        TypeError: If *package* or *resource* is not a string.
        OSError: If the resource cannot be found.
    """
    if not isinstance(package, str):
        raise TypeError("package must be a str")
    if not isinstance(resource, str):
        raise TypeError("resource must be a str")
    data = pkgutil.get_data(package, resource)
    if data is None:
        raise OSError(f"resource {resource!r} not found in package {package!r}")
    return data


def read_text(
    package: str, resource: str, encoding: str = "utf-8", errors: str = "strict"
) -> str:
    """Read a data file shipped inside *package* and decode it as text.

    Args:
        package: Name of the package that contains the resource.
        resource: Name of the resource file inside the package.
        encoding: Text encoding used to decode the resource.
        errors: Error handling scheme used when decoding fails.

    Returns:
        The decoded contents of the resource.

    Raises:
        TypeError: If any argument is not a string.
        OSError: If the resource cannot be found.
        UnicodeDecodeError: If the resource cannot be decoded.
    """
    if not isinstance(encoding, str):
        raise TypeError("encoding must be a str")
    if not isinstance(errors, str):
        raise TypeError("errors must be a str")
    return get_data(package, resource).decode(encoding, errors)


def resolve_name(name: str) -> Any:
    """Resolve a dotted name to the module or attribute it refers to.

    Args:
        name: Dotted module name, optionally with a ``:attr`` suffix.

    Returns:
        The resolved object, usually a module.

    Raises:
        TypeError: If *name* is not a string.
        ValueError: If *name* is not a valid dotted name.
        ImportError: If the name cannot be imported.
    """
    if not isinstance(name, str):
        raise TypeError("name must be a str")
    return pkgutil.resolve_name(name)


def iter_importers(fullname: str = "") -> list[Any]:
    """Return the meta path finders that would be consulted for *fullname*.

    Args:
        fullname: Fully qualified module name to find importers for.

    Returns:
        A list of importer objects, in the order they are consulted.

    Raises:
        TypeError: If *fullname* is not a string.
    """
    if not isinstance(fullname, str):
        raise TypeError("fullname must be a str")
    return list(pkgutil.iter_importers(fullname))


def extend_path(path: list[str], name: str) -> list[str]:
    """Extend a package ``__path__`` with the directories of a namespace package.

    Args:
        path: Existing package path entries.
        name: Name of the package being extended.

    Returns:
        The extended list of package path entries.

    Raises:
        TypeError: If *path* is not a list of strings or *name* is not a
            string.
    """
    if not isinstance(path, list) or not all(isinstance(entry, str) for entry in path):
        raise TypeError("path must be a list of strings")
    if not isinstance(name, str):
        raise TypeError("name must be a str")
    return pkgutil.extend_path(path, name)


def find_spec(name: str) -> Any:
    """Return the import spec for the module named *name*.

    This replaces the deprecated :func:`pkgutil.get_loader` helper and
    returns ``None`` when the module cannot be found.

    Args:
        name: Name of the module to look up.

    Returns:
        The module spec, or None when the module cannot be found.

    Raises:
        TypeError: If *name* is not a string.
    """
    if not isinstance(name, str):
        raise TypeError("name must be a str")
    return importlib.util.find_spec(name)
