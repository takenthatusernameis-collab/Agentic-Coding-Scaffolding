"""Gc utility functions wrapping the standard library 'gc' module."""

from __future__ import annotations

import gc
from typing import Any

__all__: list[str] = [
    "gc_collect",
    "gc_disable",
    "gc_enable",
    "gc_isenabled",
    "gc_get_threshold",
    "gc_set_threshold",
    "gc_get_count",
    "gc_get_objects",
]


def gc_collect(generation: int = 2) -> int:
    """Run a full garbage collection and return number of unreachable objects found."""
    return gc.collect(generation)


def gc_disable() -> None:
    """Disable automatic garbage collection."""
    gc.disable()


def gc_enable() -> None:
    """Enable automatic garbage collection."""
    gc.enable()


def gc_isenabled() -> bool:
    """Return True if automatic garbage collection is enabled."""
    return gc.isenabled()


def gc_get_threshold() -> tuple[int, int, int]:
    """Return the current garbage collection thresholds."""
    return gc.get_threshold()


def gc_set_threshold(threshold0: int, threshold1: int = 0, threshold2: int = 0) -> None:
    """Set the garbage collection thresholds."""
    gc.set_threshold(threshold0, threshold1, threshold2)


def gc_get_count() -> tuple[int, int, int]:
    """Return the current garbage collection counts."""
    return gc.get_count()


def gc_get_objects() -> list[Any]:
    """Return a list of all objects tracked by the collector."""
    return gc.get_objects()