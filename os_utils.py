"""Operating system utility functions.

This module provides helpers for inspecting the operating system and
environment using only the Python standard library.
"""

from __future__ import annotations

import os
import platform
import shutil
from typing import Any, Dict, Optional

__all__: list[str] = [
    "expand_path",
    "find_executable",
    "get_cpu_count",
    "get_disk_usage",
    "get_platform_info",
    "get_user_home",
    "get_username",
    "is_executable",
]


def get_platform_info() -> Dict[str, Any]:
    """Return a dictionary describing the current platform.

    Returns:
        Dictionary with keys ``system``, ``release``, ``version``,
        ``machine``, ``processor``, ``python_version``, and
        ``python_implementation``.
    """
    return {
        "system": platform.system(),
        "release": platform.release(),
        "version": platform.version(),
        "machine": platform.machine(),
        "processor": platform.processor(),
        "python_version": platform.python_version(),
        "python_implementation": platform.python_implementation(),
    }


def get_cpu_count() -> int:
    """Return the number of CPUs available on the system.

    Returns:
        The number of CPUs, or ``1`` if it cannot be determined.
    """
    count = os.cpu_count()
    return count if count is not None else 1


def get_disk_usage(path: str = "/") -> Dict[str, int]:
    """Return disk usage statistics for ``path``.

    Args:
        path: Filesystem path to query (default: ``"/"``).

    Returns:
        Dictionary with keys ``total``, ``used``, ``free``, and ``percent``.

    Raises:
        TypeError: If ``path`` is not a string.
        FileNotFoundError: If ``path`` does not exist.
    """
    if not isinstance(path, str):
        raise TypeError("path must be a string")
    if not os.path.exists(path):
        raise FileNotFoundError(f"Path does not exist: {path}")
    usage = shutil.disk_usage(path)
    total = usage.total
    used = usage.used
    free = usage.free
    percent = int(round((used / total) * 100)) if total else 0
    return {
        "total": total,
        "used": used,
        "free": free,
        "percent": percent,
    }


def get_user_home() -> str:
    """Return the current user's home directory."""
    return os.path.expanduser("~")


def get_username() -> str:
    """Return the current user's login name."""
    try:
        return os.getlogin()
    except OSError:
        return os.environ.get("USER", os.environ.get("USERNAME", ""))


def find_executable(name: str) -> Optional[str]:
    """Return the full path to an executable named ``name`` on ``PATH``.

    Args:
        name: Name of the executable to locate.

    Returns:
        The full path to the executable, or ``None`` if not found.

    Raises:
        TypeError: If ``name`` is not a string.
    """
    if not isinstance(name, str):
        raise TypeError("name must be a string")
    return shutil.which(name)


def expand_path(path: str) -> str:
    """Expand ``~`` and environment variables in ``path`` and make it absolute.

    Args:
        path: Path to expand.

    Returns:
        The expanded, absolute path.

    Raises:
        TypeError: If ``path`` is not a string.
    """
    if not isinstance(path, str):
        raise TypeError("path must be a string")
    expanded = os.path.expanduser(path)
    expanded = os.path.expandvars(expanded)
    return os.path.abspath(expanded)


def is_executable(path: str) -> bool:
    """Return ``True`` if ``path`` exists and is executable.

    Args:
        path: Path to check.

    Returns:
        ``True`` if the path exists and is executable, ``False`` otherwise.

    Raises:
        TypeError: If ``path`` is not a string.
    """
    if not isinstance(path, str):
        raise TypeError("path must be a string")
    return os.path.isfile(path) and os.access(path, os.X_OK)


if __name__ == "__main__":
    import json

    print(json.dumps(get_platform_info(), indent=2))
