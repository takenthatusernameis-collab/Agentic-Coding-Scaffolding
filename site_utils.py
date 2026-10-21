"""Site configuration and user-site directory utilities.

This module provides helpers for inspecting the Python site configuration
using only the standard library ``site`` module.
"""

from __future__ import annotations

import site
from typing import List

__all__: list[str] = [
    "get_site_packages",
    "get_user_base",
    "get_user_site_packages",
    "is_user_site_enabled",
]


def get_site_packages() -> List[str]:
    """Return the list of site-packages directories.

    Returns:
        A list of absolute directory paths.
    """
    return list(site.getsitepackages())


def get_user_base() -> str:
    """Return the base directory for user-specific installations.

    Returns:
        The absolute path to the user base directory.
    """
    return site.getuserbase()


def get_user_site_packages() -> str:
    """Return the user site-packages directory.

    Returns:
        The absolute path to the user site-packages directory.
    """
    return site.getusersitepackages()


def is_user_site_enabled() -> bool:
    """Return whether user site-packages are enabled.

    Returns:
        ``True`` when user site-packages are enabled, ``False`` otherwise.
    """
    return bool(site.ENABLE_USER_SITE)
