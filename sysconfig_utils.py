"""Utilities for interpreter build configuration (wrapping :mod:`sysconfig`).

The :mod:`sysconfig` module exposes the configuration variables, installation
paths and schemes that describe how the running interpreter was built and where
it keeps its files. This wrapper exposes a small, validated surface over that
functionality so callers can look up build metadata, resolve installation
paths, and inspect the available installation schemes without repeating the
usual type checks.
"""

from __future__ import annotations

import sysconfig as _sysconfig
from typing import Any, Dict, List, Optional, Tuple, cast

__all__ = [
    "get_config_vars",
    "get_config_var",
    "has_config_var",
    "list_config_var_names",
    "get_paths",
    "get_path",
    "get_platform",
    "get_python_version",
    "get_default_scheme",
    "get_preferred_scheme",
    "get_scheme_names",
    "is_python_build",
    "get_config_h_filename",
    "get_makefile_filename",
]

# The installation types understood by :func:`get_preferred_scheme`.
_INSTALLATION_TYPES = ("prefix", "home", "user")


def _require_text(value: object, name: str) -> str:
    """Return *value* when it is a string, otherwise raise ``TypeError``."""
    if not isinstance(value, str):
        raise TypeError(f"{name} must be a string, got {type(value).__name__}")
    return value


def _require_optional_text(value: object, name: str) -> Optional[str]:
    """Return *value* when it is a string or ``None``, otherwise raise ``TypeError``."""
    if value is None:
        return None
    if not isinstance(value, str):
        raise TypeError(f"{name} must be a string or None, got {type(value).__name__}")
    return value


def _require_optional_mapping(value: object, name: str) -> Optional[Dict[str, Any]]:
    """Return *value* when it is a mapping or ``None``, otherwise raise ``TypeError``."""
    if value is None:
        return None
    if not isinstance(value, dict):
        raise TypeError(f"{name} must be a dict or None, got {type(value).__name__}")
    return value


def _require_flag(value: object, name: str) -> bool:
    """Return *value* when it is a boolean, otherwise raise ``TypeError``."""
    if not isinstance(value, bool):
        raise TypeError(f"{name} must be a bool, got {type(value).__name__}")
    return value


def get_config_vars() -> Dict[str, Any]:
    """Return the configuration variables of the running interpreter.

    The variables describe the build of the interpreter, such as the compiler
    used, the platform triplet and the installation prefixes.

    Returns:
        A mapping of configuration variable names to their values.
    """
    return dict(_sysconfig.get_config_vars())


def get_config_var(name: str) -> Any:
    """Return the configuration variable registered under *name*.

    Args:
        name: Name of the configuration variable, such as ``"CC"``.

    Returns:
        The value of the variable, or ``None`` when it is not defined.

    Raises:
        TypeError: If *name* is not a string.
    """
    key = _require_text(name, "name")
    return _sysconfig.get_config_var(key)


def has_config_var(name: str) -> bool:
    """Return ``True`` when the configuration variable *name* is defined.

    Args:
        name: Name of the configuration variable.

    Returns:
        ``True`` when the variable is known to the standard library.

    Raises:
        TypeError: If *name* is not a string.
    """
    key = _require_text(name, "name")
    return key in _sysconfig.get_config_vars()


def list_config_var_names() -> List[str]:
    """Return the sorted names of the known configuration variables."""
    return sorted(_sysconfig.get_config_vars())


def get_paths(
    scheme: Optional[str] = None,
    vars: Optional[Dict[str, Any]] = None,
    expand: bool = True,
) -> Dict[str, str]:
    """Return the installation paths of the running interpreter.

    Args:
        scheme: Installation scheme to describe, or ``None`` for the default.
        vars: Additional variables that override the discovered ones.
        expand: Whether to expand the ``{variable}`` placeholders of the scheme.

    Returns:
        A mapping of path names, such as ``"stdlib"``, to their values.

    Raises:
        TypeError: If any argument has an unsupported type.
        KeyError: If *scheme* is not a known installation scheme.
    """
    scheme_name = _require_optional_text(scheme, "scheme")
    overrides = _require_optional_mapping(vars, "vars")
    should_expand = _require_flag(expand, "expand")
    if scheme_name is None:
        scheme_name = _sysconfig.get_default_scheme()
    return dict(_sysconfig.get_paths(scheme_name, overrides, should_expand))


def get_path(
    name: str,
    scheme: Optional[str] = None,
    vars: Optional[Dict[str, Any]] = None,
    expand: bool = True,
) -> str:
    """Return the installation path registered under *name*.

    Args:
        name: Name of the path, such as ``"purelib"``.
        scheme: Installation scheme to describe, or ``None`` for the default.
        vars: Additional variables that override the discovered ones.
        expand: Whether to expand the ``{variable}`` placeholders of the scheme.

    Returns:
        The configured path.

    Raises:
        TypeError: If any argument has an unsupported type.
        KeyError: If *name* is not a known path name.
    """
    key = _require_text(name, "name")
    paths = get_paths(scheme, vars, expand)
    if key not in paths:
        raise KeyError(f"unknown path name: {key!r}")
    return paths[key]


def get_platform() -> str:
    """Return the platform string of the running interpreter."""
    return _sysconfig.get_platform()


def get_python_version() -> str:
    """Return the Python version as ``"major.minor"``."""
    return _sysconfig.get_python_version()


def get_default_scheme() -> str:
    """Return the default installation scheme of the current platform."""
    return _sysconfig.get_default_scheme()


def get_preferred_scheme(scheme: str) -> str:
    """Return the preferred installation scheme for the given installation type.

    The installation type is one of ``"prefix"``, ``"home"`` or ``"user"``.
    Interpreters that do not know an installation type fall back to the
    documented POSIX defaults.

    Args:
        scheme: Installation type to resolve.

    Returns:
        The name of the preferred installation scheme.

    Raises:
        TypeError: If *scheme* is not a string.
        KeyError: If *scheme* is not a known installation type.
    """
    key = _require_text(scheme, "scheme")
    try:
        preferred = cast(str, _sysconfig.get_preferred_scheme(cast(Any, key)))
    except (KeyError, ValueError):
        if key not in _INSTALLATION_TYPES:
            raise KeyError(f"unknown installation type: {key!r}") from None
        if key == "prefix":
            return _sysconfig.get_default_scheme()
        return "posix_home" if key == "home" else "posix_user"
    return preferred


def get_scheme_names() -> Tuple[str, ...]:
    """Return the names of the known installation schemes."""
    return tuple(_sysconfig.get_scheme_names())


def is_python_build() -> bool:
    """Return ``True`` when the interpreter was built from source locally."""
    return bool(_sysconfig.is_python_build())


def get_config_h_filename() -> str:
    """Return the path of the ``pyconfig.h`` header of the interpreter."""
    return _sysconfig.get_config_h_filename()


def get_makefile_filename() -> str:
    """Return the path of the ``Makefile`` used to build the interpreter."""
    return _sysconfig.get_makefile_filename()
