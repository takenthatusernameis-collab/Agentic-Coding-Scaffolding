"""Threading utility functions wrapping the standard library 'threading' module."""

from __future__ import annotations

import threading
from typing import Any, Callable, Optional

__all__: list[str] = [
    "ThreadCreate",
    "thread_start",
    "thread_join",
    "thread_is_alive",
    "thread_name",
    "thread_ident",
    "thread_daemon",
    "thread_set_daemon",
    "LockCreate",
    "lock_acquire",
    "lock_release",
    "lock_locked",
    "RLockCreate",
    "rlock_acquire",
    "rlock_release",
    "SemaphoreCreate",
    "semaphore_acquire",
    "semaphore_release",
    "EventCreate",
    "event_set",
    "event_clear",
    "event_is_set",
    "event_wait",
    "ConditionCreate",
    "condition_acquire",
    "condition_release",
    "condition_wait",
    "condition_notify",
    "condition_notify_all",
    "TimerCreate",
    "timer_start",
    "timer_cancel",
    "BarrierCreate",
    "barrier_wait",
    "barrier_reset",
    "barrier_abort",
    "barrier_parties",
    "barrier_broken",
    "current_thread",
    "active_count",
    "enumerate_threads",
    "main_thread",
]


def ThreadCreate(
    target: Optional[Callable[..., Any]] = None,
    args: tuple = (),
    kwargs: Optional[dict[str, Any]] = None,
    name: Optional[str] = None,
    daemon: Optional[bool] = None,
) -> threading.Thread:
    return threading.Thread(
        target=target, args=args, kwargs=kwargs or {}, name=name, daemon=daemon
    )


def thread_start(t: threading.Thread) -> None:
    t.start()


def thread_join(t: threading.Thread, timeout: Optional[float] = None) -> None:
    t.join(timeout)


def thread_is_alive(t: threading.Thread) -> bool:
    return t.is_alive()


def thread_name(t: threading.Thread) -> str:
    return t.name


def thread_ident(t: threading.Thread) -> Optional[int]:
    return t.ident


def thread_daemon(t: threading.Thread) -> bool:
    return bool(t.daemon)


def thread_set_daemon(t: threading.Thread, daemon: bool) -> None:
    t.daemon = daemon


def LockCreate() -> threading.Lock:
    return threading.Lock()


def lock_acquire(lock: threading.Lock, blocking: bool = True, timeout: float = -1) -> bool:
    return lock.acquire(blocking=blocking, timeout=timeout)


def lock_release(lock: threading.Lock) -> None:
    lock.release()


def lock_locked(lock: threading.Lock) -> bool:
    return lock.locked()


def RLockCreate() -> threading.RLock:
    return threading.RLock()


def rlock_acquire(rlock: threading.RLock, blocking: bool = True, timeout: float = -1) -> bool:
    return rlock.acquire(blocking=blocking, timeout=timeout)


def rlock_release(rlock: threading.RLock) -> None:
    rlock.release()


def SemaphoreCreate(value: int = 1) -> threading.Semaphore:
    return threading.Semaphore(value)


def semaphore_acquire(
    sem: threading.Semaphore, blocking: bool = True, timeout: Optional[float] = None
) -> bool:
    return sem.acquire(blocking=blocking, timeout=timeout if timeout is not None else -1)


def semaphore_release(sem: threading.Semaphore) -> None:
    sem.release()


def EventCreate() -> threading.Event:
    return threading.Event()


def event_set(e: threading.Event) -> None:
    e.set()


def event_clear(e: threading.Event) -> None:
    e.clear()


def event_is_set(e: threading.Event) -> bool:
    return e.is_set()


def event_wait(e: threading.Event, timeout: Optional[float] = None) -> bool:
    return e.wait(timeout)


def ConditionCreate(lock: Any = None) -> threading.Condition:
    return threading.Condition(lock) if lock is not None else threading.Condition()


def condition_acquire(c: threading.Condition, blocking: bool = True, timeout: float = -1) -> bool:
    return c.acquire(blocking=blocking, timeout=timeout)


def condition_release(c: threading.Condition) -> None:
    c.release()


def condition_wait(c: threading.Condition, timeout: Optional[float] = None) -> bool:
    return c.wait(timeout)


def condition_notify(c: threading.Condition, n: int = 1) -> None:
    c.notify(n)


def condition_notify_all(c: threading.Condition) -> None:
    c.notify_all()


def TimerCreate(
    interval: float,
    function: Callable[..., Any],
    args: tuple = (),
    kwargs: Optional[dict[str, Any]] = None,
) -> threading.Timer:
    return threading.Timer(interval, function, args=args, kwargs=kwargs or {})


def timer_start(t: threading.Timer) -> None:
    t.start()


def timer_cancel(t: threading.Timer) -> None:
    t.cancel()


def BarrierCreate(
    parties: int,
    action: Optional[Callable[[], Any]] = None,
    timeout: Optional[float] = None,
) -> threading.Barrier:
    return threading.Barrier(parties, action=action, timeout=timeout)


def barrier_wait(b: threading.Barrier, timeout: Optional[float] = None) -> int:
    return b.wait(timeout)


def barrier_reset(b: threading.Barrier) -> None:
    b.reset()


def barrier_abort(b: threading.Barrier) -> None:
    b.abort()


def barrier_parties(b: threading.Barrier) -> int:
    return b.parties


def barrier_broken(b: threading.Barrier) -> bool:
    return b.broken


def current_thread() -> threading.Thread:
    return threading.current_thread()


def active_count() -> int:
    return threading.active_count()


def enumerate_threads() -> list[threading.Thread]:
    return threading.enumerate()


def main_thread() -> threading.Thread:
    return threading.main_thread()
