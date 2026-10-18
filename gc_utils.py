"""Utilities wrapping the standard library ``gc`` module."""

import gc


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
