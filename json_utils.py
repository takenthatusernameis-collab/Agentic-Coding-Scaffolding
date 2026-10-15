"""JSON utility functions."""

import json
from typing import Any


def read_json(path: str) -> Any:
    """Read JSON data from a file."""
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def write_json(path: str, data: Any, indent: int = 4, ensure_ascii: bool = False) -> None:
    """Write JSON data to a file."""
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=indent, ensure_ascii=ensure_ascii)


def load_json_string(s: str) -> Any:
    """Parse JSON from a string."""
    return json.loads(s)


def dump_json_string(data: Any, indent: int = 4, ensure_ascii: bool = False) -> str:
    """Serialize data to JSON string."""
    return json.dumps(data, indent=indent, ensure_ascii=ensure_ascii)


def is_valid_json(s: str) -> bool:
    """Check if a string is valid JSON."""
    try:
        json.loads(s)
        return True
    except (json.JSONDecodeError, TypeError):
        return False


def pretty_print_json(data: Any, indent: int = 4) -> str:
    """Return a pretty-printed JSON string."""
    return json.dumps(data, indent=indent, ensure_ascii=False, sort_keys=False)
