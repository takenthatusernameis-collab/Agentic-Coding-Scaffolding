"""Site configuration utilities wrapping the standard library :mod:`site` module.

The :mod:`site` module is imported by the interpreter at startup to configure
the module search path.  It knows the directories the interpreter looks for
packages in, the directory a user installs packages into, and it adds the site
directories of a virtual environment to the search path.

This wrapper validates every argument before the standard library is reached,
so a caller gets a clear :class:`TypeError` or :class:`ValueError` instead of
an opaque failure.  The settings of the standard library are read through the
helpers of this module, so a caller never has to reach into the module to read
them, and the tri-state of the user site setting is reported as the standard
library reports it.

The helpers that change the search path of the interpreter work on
:data:`sys.path` of the process, so a program that calls one of them changes
where its own imports are looked up.  The tests of the project replace
:data:`sys.path` with a copy, so the suite never changes the search path of
the process that runs it.
"""

from __future__ import annotations

import site as _site
from typing import List, Optional, Sequence, Set, Tuple

__all__: list[str] = [
    "add_site_dir",
    "add_site_packages",
    "add_user_site_packages",
    "check_enable_user_site",
    "get_enable_user_site",
    "get_site_packages",
    "get_site_prefixes",
    "get_user_base",
    "get_user_site_packages",
    "is_user_site_enabled",
    "make_path",
    "remove_duplicate_paths",
]


def _require_str(value: object, name: str) -> str:
    if not isinstance(value, str):
        raise TypeError(f"{name} must be a str, got {type(value).__name__}")
    return value


def _require_non_empty_str(value: object, name: str) -> str:
    text = _require_str(value, name)
    if not text:
        raise ValueError(f"{name} must not be empty")
    return text


def _require_optional_prefixes(value: object, name: str) -> Optional[List[str]]:
    """Return the prefixes as a list, or ``None`` when no prefixes are given."""
    if value is None:
        return None
    if isinstance(value, (str, bytes)):
        raise TypeError(f"{name} must be a sequence of strings, not a single string")
    if not isinstance(value, (list, tuple)):
        raise TypeError(f"{name} must be a list or a tuple, got {type(value).__name__}")
    for entry in value:
        if not isinstance(entry, str):
            raise TypeError(f"{name} entries must be strings, got {type(entry).__name__}")
    return list(value)


def _require_known_paths(value: object, name: str) -> Set[str]:
    """Return the set of known paths unchanged, so the standard library can fill it."""
    if not isinstance(value, set):
        raise TypeError(f"{name} must be a set of strings, got {type(value).__name__}")
    for entry in value:
        if not isinstance(entry, str):
            raise TypeError(f"{name} entries must be strings, got {type(entry).__name__}")
    return value


def get_site_packages(prefixes: Optional[Sequence[str]] = None) -> List[str]:
    """Return the global site-packages directories of the interpreter.

    Args:
        prefixes: The installation prefixes the directories are looked up in.
            The prefixes of the interpreter are used when it is ``None``.

    Returns:
        The absolute paths of the site-packages directories.
    """
    resolved = _require_optional_prefixes(prefixes, "prefixes")
    return list(_site.getsitepackages(resolved))


def get_site_prefixes() -> List[str]:
    """Return the installation prefixes of the interpreter.

    Returns:
        The prefixes the site-packages directories are looked up in.
    """
    return list(_site.PREFIXES)


def get_user_base() -> Optional[str]:
    """Return the base directory a user installs packages below.

    Returns:
        The absolute path of the user base directory, or ``None`` on the
        platforms that have no home directory.
    """
    return _site.getuserbase()


def get_user_site_packages() -> Optional[str]:
    """Return the site-packages directory of the user.

    Returns:
        The absolute path of the user site-packages directory, or ``None`` on
        the platforms that have no home directory.
    """
    return _site.getusersitepackages()


def get_enable_user_site() -> Optional[bool]:
    """Return the user site setting of the interpreter.

    Returns:
        ``True`` when the user site directory is used, ``False`` when it is
        disabled, and ``None`` when the interpreter has not decided yet.
    """
    return _site.ENABLE_USER_SITE


def is_user_site_enabled() -> bool:
    """Return whether the user site directory is used by the interpreter.

    Returns:
        ``True`` when the user site directory is used, ``False`` otherwise.
    """
    return bool(_site.ENABLE_USER_SITE)


def check_enable_user_site() -> Optional[bool]:
    """Check whether the user site directory is safe to use.

    The standard library disables the user site directory when the process
    runs with a different effective user than the real one, and when the
    interpreter was started with the ``-s`` flag.

    Returns:
        ``True`` when the user site directory is safe to use, ``False`` when
        it is disabled by the user, and ``None`` when it is disabled for
        security reasons.
    """
    return _site.check_enableusersite()


def make_path(*paths: str) -> Tuple[str, str]:
    """Join the given paths and report them in absolute and normalized form.

    Args:
        paths: The path segments that are joined.

    Returns:
        The absolute path of the joined segments and its normalized form, the
        way the standard library stores the paths of the search path.
    """
    if not paths:
        raise ValueError("paths must not be empty")
    segments = [_require_str(path, "paths entries") for path in paths]
    return _site.makepath(*segments)


def remove_duplicate_paths() -> Set[str]:
    """Remove the duplicates of the search path and make its entries absolute.

    The search path of the process is changed in place, the way the standard
    library changes it.

    Returns:
        The normalized paths that are known to the search path.
    """
    return _site.removeduppaths()


def add_site_dir(sitedir: str, known_paths: Optional[Set[str]] = None) -> Optional[Set[str]]:
    """Add a directory to the search path and process the files it holds.

    The files with the ``.pth`` suffix of the directory are processed, the way
    the standard library processes them.  The search path of the process is
    changed in place.

    Args:
        sitedir: The directory that is added to the search path.
        known_paths: The paths that are known to the search path.  The paths
            of the search path of the process are used when it is ``None``.

    Returns:
        The paths that are known to the search path, or ``None`` when they
        were derived from the search path of the process.
    """
    directory = _require_non_empty_str(sitedir, "sitedir")
    if known_paths is None:
        _site.addsitedir(directory, None)
        return None
    known = _require_known_paths(known_paths, "known_paths")
    _site.addsitedir(directory, known)
    return known


def add_site_packages(
    known_paths: Set[str],
    prefixes: Optional[Sequence[str]] = None,
) -> Set[str]:
    """Add the global site-packages directories to the search path.

    The search path of the process is changed in place, the way the standard
    library changes it.

    Args:
        known_paths: The paths that are known to the search path.
        prefixes: The installation prefixes the directories are looked up in.
            The prefixes of the interpreter are used when it is ``None``.

    Returns:
        The paths that are known to the search path.
    """
    known = _require_known_paths(known_paths, "known_paths")
    resolved = _require_optional_prefixes(prefixes, "prefixes")
    return _site.addsitepackages(known, resolved)


def add_user_site_packages(known_paths: Set[str]) -> Set[str]:
    """Add the site-packages directory of the user to the search path.

    The directory is only added when the interpreter uses the user site
    directory and the directory exists.  The search path of the process is
    changed in place, the way the standard library changes it.

    Args:
        known_paths: The paths that are known to the search path.

    Returns:
        The paths that are known to the search path.
    """
    known = _require_known_paths(known_paths, "known_paths")
    return _site.addusersitepackages(known)
