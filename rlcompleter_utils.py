"""Utilities for interactive tab completion (wrapping :mod:`rlcompleter`)."""

from __future__ import annotations

import rlcompleter

__all__: list[str] = ["Completer", "complete"]


class Completer:
    """Wrapper around :class:`rlcompleter.Completer`."""

    def __init__(self, namespace: dict | None = None) -> None:
        if namespace is not None and not isinstance(namespace, dict):
            raise TypeError("namespace must be a dict or None")
        self._completer = rlcompleter.Completer(namespace)

    def complete(self, text: str, state: int) -> str | None:
        if not isinstance(text, str):
            raise TypeError("text must be a str")
        if not isinstance(state, int) or isinstance(state, bool):
            raise TypeError("state must be an int")
        return self._completer.complete(text, state)


def complete(text: str, state: int, namespace: dict | None = None) -> str | None:
    """Return the *state*-th completion for *text*."""
    if not isinstance(text, str):
        raise TypeError("text must be a str")
    if not isinstance(state, int) or isinstance(state, bool):
        raise TypeError("state must be an int")
    if namespace is not None and not isinstance(namespace, dict):
        raise TypeError("namespace must be a dict or None")
    return rlcompleter.Completer(namespace).complete(text, state)
