"""Platform utilities (wrapping :mod:`platform`).

This module provides helpers for inspecting platform and Python implementation
details using the standard library :mod:`platform`. All functions validate
inputs and raise :class:`TypeError` or :class:`ValueError` for invalid
arguments where applicable.
"""

from __future__ import annotations

import platform
from typing import Any, Dict

__all__: list[str] = [
    "get_machine",
    "get_node",
    "get_platform",
    "get_processor",
    "get_python_build",
    "get_python_compiler",
    "get_python_implementation",
    "get_python_revision",
    "get_python_version",
    "get_python_version_tuple",
    "get_release",
    "get_system",
    "get_uname",
    "get_version",
    "platform_info",
]


def get_system() -> str:
    """Return the system name (e.g., 'Linux', 'Darwin', 'Windows')."""
    return platform.system()


def get_release() -> str:
    """Return the release name of the system."""
    return platform.release()


def get_version() -> str:
    """Return the system version string."""
    return platform.version()


def get_machine() -> str:
    """Return the machine type (e.g., 'x86_64')."""
    return platform.machine()


def get_processor() -> str:
    """Return the processor name (empty string if not available)."""
    return platform.processor()


def get_node() -> str:
    """Return the network name of the machine."""
    return platform.node()


def get_python_implementation() -> str:
    """Return the Python implementation name (e.g., 'CPython')."""
    return platform.python_implementation()


def get_python_version() -> str:
    """Return the Python version string."""
    return platform.python_version()


def get_python_version_tuple() -> tuple:
    """Return the Python version as a tuple (major, minor, patchlevel)."""
    return platform.python_version_tuple()


def get_python_build() -> tuple:
    """Return a tuple (build_number, build_date) for the Python build."""
    return platform.python_build()


def get_python_compiler() -> str:
    """Return the compiler used to build Python."""
    return platform.python_compiler()


def get_python_revision() -> str:
    """Return the Python revision."""
    return platform.python_revision()


def get_uname() -> platform.uname_result:
    """Return a uname_result tuple-like object with system info."""
    return platform.uname()


def get_platform(aliased: bool = False, terse: bool = False) -> str:
    """Return a single string identifying the platform.

    Args:
        aliased: If True, use aliases for platform names where applicable.
        terse: If True, return a more terse form.

    Returns:
        Platform string.

    Raises:
        TypeError: If arguments are not of the expected type.
    """
    if not isinstance(aliased, bool):
        raise TypeError("aliased must be a boolean")
    if not isinstance(terse, bool):
        raise TypeError("terse must be a boolean")
    return platform.platform(aliased=aliased, terse=terse)


def platform_info() -> Dict[str, Any]:
    """Return a dictionary with comprehensive platform information.

    Returns:
        Dictionary containing system, release, version, machine, processor,
        node, python implementation, python version, and uname details.
    """
    uname = platform.uname()
    return {
        "system": uname.system,
        "release": uname.release,
        "version": uname.version,
        "machine": uname.machine,
        "processor": uname.processor,
        "node": uname.node,
        "python_implementation": platform.python_implementation(),
        "python_version": platform.python_version(),
        "python_build": platform.python_build(),
        "python_compiler": platform.python_compiler(),
        "python_revision": platform.python_revision(),
    }
