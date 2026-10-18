"""Circuit breaker utilities.

This module provides a :class:`CircuitBreaker` implementing the circuit breaker
resilience pattern, which wraps an operation and short-circuits calls once a
configurable failure threshold is reached. The circuit cycles through three
states:

* ``CLOSED`` — calls execute normally; failures increment the failure counter.
* ``OPEN`` — calls are rejected immediately with :class:`CircuitOpenError`.
* ``HALF_OPEN`` — a single trial call is allowed after the recovery timeout;
  success closes the circuit, failure re-opens it.

All state transitions are thread-safe. A circuit breaker is useful for failing
fast against a flaky downstream dependency instead of repeatedly waiting on
timeouts, giving the dependency time to recover.
"""

from __future__ import annotations

import threading
import time
from typing import Any, Callable, Optional, Tuple, TypeVar, Union

T = TypeVar("T")


class CircuitOpenError(RuntimeError):
    """Raised when an operation is rejected because the circuit is open."""


class CircuitBreaker:
    """A thread-safe circuit breaker that short-circuits failing operations.

    Args:
        failure_threshold: Number of consecutive failures required to open the
            circuit. Must be at least 1.
        recovery_timeout: Seconds to wait before allowing a recovery trial call
            once the circuit is open. Must be greater than 0.
        expected_exception: An exception class, or tuple of exception classes,
            that count as failures. Any other exception propagates and is not
            counted.

    Raises:
        TypeError: If ``failure_threshold`` is not an integer,
            ``recovery_timeout`` is not a number, or ``expected_exception`` is
            not an exception class or tuple of exception classes.
        ValueError: If ``failure_threshold`` is less than 1 or
            ``recovery_timeout`` is not greater than 0.
    """

    CLOSED = "closed"
    OPEN = "open"
    HALF_OPEN = "half_open"

    def __init__(
        self,
        failure_threshold: int = 5,
        recovery_timeout: float = 30.0,
        expected_exception: Union[type[BaseException], Tuple[type[BaseException], ...]] = Exception,
    ) -> None:
        if isinstance(failure_threshold, bool) or not isinstance(failure_threshold, int):
            raise TypeError("failure_threshold must be an integer")
        if failure_threshold < 1:
            raise ValueError("failure_threshold must be at least 1")
        if isinstance(recovery_timeout, bool) or not isinstance(recovery_timeout, (int, float)):
            raise TypeError("recovery_timeout must be a number")
        if recovery_timeout <= 0:
            raise ValueError("recovery_timeout must be greater than 0")

        if isinstance(expected_exception, type):
            expected_exceptions: Tuple[type[BaseException], ...] = (expected_exception,)
        elif isinstance(expected_exception, tuple) and all(
            isinstance(exc, type) for exc in expected_exception
        ):
            expected_exceptions = expected_exception
        else:
            raise TypeError(
                "expected_exception must be an exception class or a tuple of exception classes"
            )

        self._failure_threshold = failure_threshold
        self._recovery_timeout = float(recovery_timeout)
        self._expected_exceptions = expected_exceptions
        self._lock = threading.Lock()
        self._state = self.CLOSED
        self._failures = 0
        self._opened_at: Optional[float] = None
        self._half_open_trial = False

    @property
    def state(self) -> str:
        """Return the current circuit state (``closed``, ``open``, ``half_open``)."""
        with self._lock:
            self._maybe_transition()
            return self._state

    @property
    def failures(self) -> int:
        """Return the current consecutive failure count."""
        with self._lock:
            return self._failures

    @property
    def failure_threshold(self) -> int:
        """Return the failure threshold used to open the circuit."""
        return self._failure_threshold

    @property
    def recovery_timeout(self) -> float:
        """Return the recovery timeout in seconds."""
        return self._recovery_timeout

    def _maybe_transition(self) -> None:
        """Move an open circuit to half-open once the recovery timeout elapses."""
        if (
            self._state == self.OPEN
            and self._opened_at is not None
            and time.monotonic() - self._opened_at >= self._recovery_timeout
        ):
            self._state = self.HALF_OPEN

    def _record_failure(self) -> None:
        """Record a failed call, opening or re-opening the circuit as needed."""
        self._failures += 1
        if self._state == self.HALF_OPEN or self._failures >= self._failure_threshold:
            self._state = self.OPEN
            self._opened_at = time.monotonic()

    def _record_success(self) -> None:
        """Record a successful call, closing the circuit."""
        self._failures = 0
        self._opened_at = None
        self._state = self.CLOSED

    def can_execute(self) -> bool:
        """Return whether a call would be allowed right now.

        An open circuit that has not yet reached its recovery timeout reports
        ``False``; once the timeout elapses the circuit moves to half-open and
        reports ``True`` for a single trial call.
        """
        with self._lock:
            self._maybe_transition()
            if self._state == self.HALF_OPEN and self._half_open_trial:
                return False
            return self._state != self.OPEN

    def call(self, func: Callable[..., T], *args: Any, **kwargs: Any) -> T:
        """Execute ``func`` through the circuit breaker.

        Args:
            func: The callable to execute.
            *args: Positional arguments forwarded to ``func``.
            **kwargs: Keyword arguments forwarded to ``func``.

        Returns:
            The return value of ``func``.

        Raises:
            TypeError: If ``func`` is not callable.
            CircuitOpenError: If the circuit is open, or if a half-open trial
                call is already in progress.
        """
        if not callable(func):
            raise TypeError("func must be callable")

        with self._lock:
            self._maybe_transition()
            if self._state == self.OPEN:
                remaining = self._recovery_timeout
                if self._opened_at is not None:
                    remaining = max(
                        0.0, self._recovery_timeout - (time.monotonic() - self._opened_at)
                    )
                raise CircuitOpenError(f"circuit breaker is open; retry in {remaining:.2f} seconds")
            if self._state == self.HALF_OPEN:
                if self._half_open_trial:
                    raise CircuitOpenError(
                        "circuit breaker is half-open; a trial call is in progress"
                    )
                self._half_open_trial = True

        try:
            result = func(*args, **kwargs)
        except self._expected_exceptions:
            with self._lock:
                self._record_failure()
                self._half_open_trial = False
            raise
        else:
            with self._lock:
                self._record_success()
                self._half_open_trial = False
            return result

    def reset(self) -> None:
        """Reset the circuit to the closed state with zero failures."""
        with self._lock:
            self._state = self.CLOSED
            self._failures = 0
            self._opened_at = None
            self._half_open_trial = False
