"""Utilities wrapping the standard library ``sched`` module."""

import sched
import time


def scheduler(timefunc=time.monotonic, delayfunc=time.sleep) -> sched.scheduler:
    return sched.scheduler(timefunc, delayfunc)


def enter(s, delay, priority, action, *argument, **kwargs):
    return s.enter(delay, priority, action, argument, kwargs)


def enterabs(s, time, priority, action, *argument, **kwargs):
    return s.enterabs(time, priority, action, argument, kwargs)


def cancel(s: sched.scheduler, event: sched.Event) -> None:
    s.cancel(event)


def empty(s: sched.scheduler) -> bool:
    return s.empty()


def run(s: sched.scheduler, blocking: bool = True) -> None:
    s.run(blocking)


def queue(s: sched.scheduler) -> list:
    return s.queue
