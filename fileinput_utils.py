"""Utility functions wrapping the stdlib fileinput module."""

import fileinput
from typing import Any, Iterable, List, Optional


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


def filenames(files: Optional[Iterable[str]] = None) -> List[str]:
    names: List[str] = []
    with fileinput.input(files=files) as f:
        for line in f:
            if fileinput.isfirstline():
                names.append(fileinput.filename())
    return names
