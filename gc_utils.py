"""Utilities wrapping the standard library ``gc`` module."""

import gc

__all__ = [
    "collect",
    "disable",
    "enable",
    "get_count",
    "get_debug",
    "get_objects",
    "get_referents",
    "get_referrers",
    "get_stats",
    "get_threshold",
    "is_tracked",
    "is_finalized",
    "isenabled",
    "set_debug",
    "set_threshold",
]


def enable() -> None:
    gc.enable()


def disable() -> None:
    gc.disable()


def isenabled() -> bool:
    return gc.isenabled()


def collect(*, generation: int = 2) -> int:
    return gc.collect(generation)


def get_count() -> tuple:
    return gc.get_count()


def get_objects() -> list:
    return gc.get_objects()


def get_referents(*objs: object) -> list:
    return gc.get_referents(*objs)


def get_referrers(*objs: object) -> list:
    return gc.get_referrers(*objs)


def get_stats() -> list:
    return gc.get_stats()


def set_debug(flags: int) -> None:
    gc.set_debug(flags)


def get_debug() -> int:
    return gc.get_debug()


def set_threshold(threshold0: int, threshold1: int = 0, threshold2: int = 0) -> None:
    if threshold1 == 0 and threshold2 == 0:
        gc.set_threshold(threshold0)
    else:
        gc.set_threshold(threshold0, threshold1, threshold2)


def get_threshold() -> tuple:
    return gc.get_threshold()


def is_tracked(obj: object) -> bool:
    """Return True if *obj* is tracked by the garbage collector.

    The garbage collector only tracks containers (lists, dicts, instances,
    ...) that can contain or reference other objects; simple atomic objects
    such as integers and strings are never tracked.

    Args:
        obj: The object to inspect.

    Returns:
        True when the object is tracked by the GC, False otherwise.

    Examples:
        >>> is_tracked([1, 2, 3])
        True
        >>> is_tracked(42)
        False
        >>> is_tracked("hello")
        False
    """
    return gc.is_tracked(obj)


def is_finalized(obj: object) -> bool:
    """Return True if *obj* has already been finalized by the GC.

    An object is finalized when its ``__del__`` (if any) has been called
    during a collection pass and the object is no longer reachable.

    Args:
        obj: The object to inspect.

    Returns:
        True when the object has been finalized, False otherwise.

    Examples:
        >>> is_finalized(42)
        False
    """
    return gc.is_finalized(obj)
