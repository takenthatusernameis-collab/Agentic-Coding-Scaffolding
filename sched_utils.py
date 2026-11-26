"""Utilities wrapping the standard library ``sched`` module."""

import math
import sched
import time

__all__ = [
    "cancel",
    "empty",
    "enter",
    "enterabs",
    "queue",
    "run",
    "scheduler",
]


def scheduler(timefunc=time.monotonic, delayfunc=time.sleep) -> sched.scheduler:
    return sched.scheduler(timefunc, delayfunc)


def enter(s, delay, priority, action, *argument, **kwargs):
    if isinstance(delay, bool) or not isinstance(delay, (int, float)):
        raise TypeError(f"delay must be a number, got {type(delay).__name__}")
    if not math.isfinite(delay):
        raise ValueError(f"delay must be finite, got {delay!r}")
    if delay < 0:
        raise ValueError(f"delay must be non-negative, got {delay}")
    return s.enter(delay, priority, action, argument, kwargs)


def enterabs(s, time, priority, action, *argument, **kwargs):
    if isinstance(time, bool) or not isinstance(time, (int, float)):
        raise TypeError(f"time must be a number, got {type(time).__name__}")
    if not math.isfinite(time):
        raise ValueError(f"time must be finite, got {time!r}")
    return s.enterabs(time, priority, action, argument, kwargs)


def cancel(s: sched.scheduler, event: sched.Event) -> None:
    s.cancel(event)


def empty(s: sched.scheduler) -> bool:
    return s.empty()


def run(s: sched.scheduler, blocking: bool = True) -> None:
    s.run(blocking)


def queue(s: sched.scheduler) -> list:
    return s.queue
