"""Utility functions wrapping the stdlib fileinput module."""

import fileinput
from typing import Any, Iterable, List, Optional

__all__ = [
    "count_lines",
    "has_lines",
    "filenames",
    "read_lines",
]


def read_lines(files: Optional[Iterable[str]] = None, **kwargs: Any) -> List[str]:
    lines: List[str] = []
    with fileinput.input(files=files, **kwargs) as f:
        for line in f:
            lines.append(line)
    return lines


def count_lines(files: Optional[Iterable[str]] = None) -> int:
    count = 0
    with fileinput.input(files=files) as f:
        for _ in f:
            count += 1
    return count



def has_lines(files: Optional[Iterable[str]] = None) -> bool:
    """Return True when the input contains at least one line."""
    return count_lines(files) > 0

def filenames(files: Optional[Iterable[str]] = None) -> List[str]:
    names: List[str] = []
    with fileinput.input(files=files) as f:
        for line in f:
            if fileinput.isfirstline():
                names.append(fileinput.filename())
    return names
