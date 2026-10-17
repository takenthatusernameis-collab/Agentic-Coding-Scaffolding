"""Difflib utility functions for sequence comparison and diffing."""

from __future__ import annotations

import difflib
from typing import Any, Sequence

__all__: list[str] = [
    "get_close_matches",
    "ratio",
    "unified_diff",
    "context_diff",
    "ndiff",
]


def get_close_matches(
    word: str,
    possibilities: Any,
    n: int = 3,
    cutoff: float = 0.6,
) -> list[str]:
    return difflib.get_close_matches(word, possibilities, n=n, cutoff=cutoff)


def ratio(a: str, b: str) -> float:
    return difflib.SequenceMatcher(None, a, b).ratio()


def unified_diff(
    a: Sequence[str],
    b: Sequence[str],
    fromfile: str = "",
    tofile: str = "",
    lineterm: str = "\n",
) -> list[str]:
    return list(difflib.unified_diff(a, b, fromfile=fromfile, tofile=tofile, lineterm=lineterm))


def context_diff(
    a: Sequence[str],
    b: Sequence[str],
    fromfile: str = "",
    tofile: str = "",
    lineterm: str = "\n",
) -> list[str]:
    return list(difflib.context_diff(a, b, fromfile=fromfile, tofile=tofile, lineterm=lineterm))


def ndiff(a: Sequence[str], b: Sequence[str], lineterm: str = "\n") -> list[str]:
    return list(difflib.ndiff(a, b))
