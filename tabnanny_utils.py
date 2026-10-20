"""Utilities for detecting ambiguous indentation (wrapping :mod:`tabnanny`)."""

from __future__ import annotations

import os as _os
import tabnanny as _tabnanny
from tabnanny import NannyNag as NannyNag


def check(path):
    """Check *path* (file or directory) for ambiguous indentation."""
    if not isinstance(path, (str, bytes, _os.PathLike)):
        raise TypeError("path must be a path-like object")
    return _tabnanny.check(path)


def process_tokens(tokens):
    """Process *tokens* and raise :class:`NannyNag` on ambiguous indentation."""
    return _tabnanny.process_tokens(tokens)


__all__ = ["NannyNag", "check", "process_tokens"]
