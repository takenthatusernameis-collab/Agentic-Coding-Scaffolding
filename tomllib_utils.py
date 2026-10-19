"""TOML utility functions (wraps stdlib tomllib)."""

from typing import Any

import tomllib  # type: ignore[import-not-found]


def read_toml(path: str) -> Any:
    """Read TOML data from a file."""
    with open(path, "rb") as f:
        return tomllib.load(f)


def load_toml_string(s: str) -> Any:
    """Parse TOML from a string."""
    return tomllib.loads(s)


def is_valid_toml(s: str) -> bool:
    """Check if a string is valid TOML."""
    try:
        tomllib.loads(s)
        return True
    except tomllib.TOMLDecodeError:
        return False
    except (TypeError, ValueError):
        return False
