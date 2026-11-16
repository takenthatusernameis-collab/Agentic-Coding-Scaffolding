"""TOML utility functions (wraps stdlib tomllib)."""

from typing import Any

import tomllib  # type: ignore[import-not-found]

__all__ = [
    "is_valid_toml",
    "load_toml_string",
    "read_toml",
]


def read_toml(path: str) -> Any:
    """Read TOML data from a file."""
    with open(path, "rb") as f:
        return tomllib.load(f)


def load_toml_string(s: str) -> Any:
    """Parse TOML from a string."""
    return tomllib.loads(s)


def is_valid_toml(s: str) -> bool:
    """Check if a string is valid TOML.

    Args:
        s: The string to validate.

    Returns:
        ``True`` if *s* parses as TOML, ``False`` otherwise. Non-string input
        is not valid TOML and returns ``False`` rather than raising, so the
        predicate stays total the way ``duration_utils.is_valid_duration`` is.

    Examples:
        >>> is_valid_toml('key = "val"')
        True
        >>> is_valid_toml("key =")
        False
        >>> is_valid_toml(123)  # type: ignore[arg-type]
        False
    """
    if not isinstance(s, str):
        return False
    try:
        tomllib.loads(s)
        return True
    except tomllib.TOMLDecodeError:
        return False
    except (TypeError, ValueError):
        return False
