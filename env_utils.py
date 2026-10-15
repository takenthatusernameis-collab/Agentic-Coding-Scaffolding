"""Environment variable utility functions for reading, writing, and parsing values.

This module provides a small, consistent API around :mod:`os` environment
variables, including typed accessors (``int``, ``float``, ``bool``) and helpers
for required variables, defaults, and prefix-based grouping.
"""

import os
from typing import Dict, List, Optional

__all__: List[str] = [
    "ensure_env",
    "get_env",
    "get_env_bool",
    "get_env_float",
    "get_env_int",
    "get_env_required",
    "prefix_env",
    "set_env",
    "unset_env",
]

_TRUE_VALUES = frozenset({"1", "true", "yes", "y", "on", "t"})
_FALSE_VALUES = frozenset({"0", "false", "no", "n", "off", "f", ""})


def get_env(key: str, default: Optional[str] = None) -> Optional[str]:
    """Return the value of an environment variable, or ``default`` if unset.

    Args:
        key: The name of the environment variable.
        default: The value to return if the variable is not set. Defaults to ``None``.

    Returns:
        The environment variable value as a string, or ``default`` if unset.

    Raises:
        TypeError: If ``key`` is not a string.

    Example:
        >>> import os
        >>> os.environ.pop("MISSING_VAR", None)
        >>> get_env("MISSING_VAR", "fallback")
        'fallback'
    """
    if not isinstance(key, str):
        raise TypeError("key must be a string")
    return os.environ.get(key, default)


def get_env_required(key: str) -> str:
    """Return the value of a required environment variable.

    Args:
        key: The name of the environment variable.

    Returns:
        The environment variable value as a string.

    Raises:
        TypeError: If ``key`` is not a string.
        KeyError: If the environment variable is not set.

    Example:
        >>> import os
        >>> os.environ["MY_VAR"] = "hello"
        >>> get_env_required("MY_VAR")
        'hello'
    """
    if not isinstance(key, str):
        raise TypeError("key must be a string")
    value = os.environ.get(key)
    if value is None:
        raise KeyError(f"Required environment variable not set: {key}")
    return value


def get_env_int(key: str, default: Optional[int] = None) -> Optional[int]:
    """Return an environment variable parsed as an integer.

    Args:
        key: The name of the environment variable.
        default: The value to return if the variable is not set. Defaults to ``None``.

    Returns:
        The environment variable value as an integer, or ``default`` if unset.

    Raises:
        TypeError: If ``key`` is not a string.
        ValueError: If the variable is set but cannot be parsed as an integer.

    Example:
        >>> import os
        >>> os.environ["PORT"] = "8080"
        >>> get_env_int("PORT")
        8080
    """
    if not isinstance(key, str):
        raise TypeError("key must be a string")
    value = os.environ.get(key)
    if value is None:
        return default
    try:
        return int(value)
    except ValueError:
        raise ValueError(
            f"Environment variable {key!r} is not a valid integer: {value!r}"
        ) from None


def get_env_float(key: str, default: Optional[float] = None) -> Optional[float]:
    """Return an environment variable parsed as a floating-point number.

    Args:
        key: The name of the environment variable.
        default: The value to return if the variable is not set. Defaults to ``None``.

    Returns:
        The environment variable value as a float, or ``default`` if unset.

    Raises:
        TypeError: If ``key`` is not a string.
        ValueError: If the variable is set but cannot be parsed as a float.

    Example:
        >>> import os
        >>> os.environ["RATIO"] = "3.14"
        >>> get_env_float("RATIO")
        3.14
    """
    if not isinstance(key, str):
        raise TypeError("key must be a string")
    value = os.environ.get(key)
    if value is None:
        return default
    try:
        return float(value)
    except ValueError:
        raise ValueError(f"Environment variable {key!r} is not a valid float: {value!r}") from None


def get_env_bool(key: str, default: Optional[bool] = None) -> Optional[bool]:
    """Return an environment variable parsed as a boolean.

    The following case-insensitive values are recognized as ``True``:
    ``"1"``, ``"true"``, ``"yes"``, ``"y"``, ``"on"``, ``"t"``.

    The following case-insensitive values are recognized as ``False``:
    ``"0"``, ``"false"``, ``"no"``, ``"n"``, ``"off"``, ``"f"``, ``""``.

    Args:
        key: The name of the environment variable.
        default: The value to return if the variable is not set. Defaults to ``None``.

    Returns:
        The environment variable value as a boolean, or ``default`` if unset.

    Raises:
        TypeError: If ``key`` is not a string.
        ValueError: If the variable is set but is not a recognized boolean string.

    Example:
        >>> import os
        >>> os.environ["DEBUG"] = "true"
        >>> get_env_bool("DEBUG")
        True
    """
    if not isinstance(key, str):
        raise TypeError("key must be a string")
    value = os.environ.get(key)
    if value is None:
        return default
    lowered = value.strip().lower()
    if lowered in _TRUE_VALUES:
        return True
    if lowered in _FALSE_VALUES:
        return False
    raise ValueError(f"Environment variable {key!r} is not a valid boolean: {value!r}")


def set_env(key: str, value: object) -> None:
    """Set an environment variable to the string representation of ``value``.

    Args:
        key: The name of the environment variable.
        value: The value to set. Non-string values are converted via ``str()``.

    Raises:
        TypeError: If ``key`` is not a string.
        ValueError: If ``key`` is empty or contains ``=``.
    """
    if not isinstance(key, str):
        raise TypeError("key must be a string")
    if not key:
        raise ValueError("key must not be empty")
    if "=" in key:
        raise ValueError("key must not contain '='")
    os.environ[key] = str(value)


def ensure_env(key: str, default: str) -> str:
    """Ensure an environment variable is set, populating it with ``default`` if missing.

    If the variable is already set, its current value is returned unchanged.
    Otherwise ``default`` is set and returned.

    Args:
        key: The name of the environment variable.
        default: The value to use (and set) if the variable is not already set.

    Returns:
        The current value of the environment variable.

    Raises:
        TypeError: If ``key`` or ``default`` is not a string.
        ValueError: If ``key`` is empty or contains ``=``.

    Example:
        >>> import os
        >>> os.environ.pop("NEW_VAR", None)
        >>> ensure_env("NEW_VAR", "default")
        'default'
    """
    if not isinstance(key, str):
        raise TypeError("key must be a string")
    if not isinstance(default, str):
        raise TypeError("default must be a string")
    value = os.environ.get(key)
    if value is None:
        set_env(key, default)
        return default
    return value


def unset_env(key: str) -> bool:
    """Unset (remove) an environment variable.

    Args:
        key: The name of the environment variable.

    Returns:
        ``True`` if the variable was present and removed, ``False`` if it was not set.

    Raises:
        TypeError: If ``key`` is not a string.
    """
    if not isinstance(key, str):
        raise TypeError("key must be a string")
    return os.environ.pop(key, None) is not None


def prefix_env(prefix: str) -> Dict[str, str]:
    """Return all environment variables whose names start with ``prefix``.

    Args:
        prefix: The prefix to filter environment variable names by.

    Returns:
        A dictionary mapping matching variable names to their values.

    Raises:
        TypeError: If ``prefix`` is not a string.

    Example:
        >>> import os
        >>> os.environ["APP_DEBUG"] = "1"
        >>> prefix_env("APP_")
        {'APP_DEBUG': '1'}
    """
    if not isinstance(prefix, str):
        raise TypeError("prefix must be a string")
    return {k: v for k, v in os.environ.items() if k.startswith(prefix)}
