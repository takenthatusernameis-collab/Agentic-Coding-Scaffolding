"""Utilities for command-line interpreter helpers (wrapping :mod:`cmd`)."""

import cmd as _cmd


class Cmd(_cmd.Cmd):
    """Thin subclass of :class:`cmd.Cmd` for convenience."""


def identchars():
    """Return the characters allowed in command names."""
    return _cmd.IDENTCHARS


def prompt_default():
    """Return the default prompt string."""
    return _cmd.PROMPT


def main():
    """Return the cmd module's ``main`` entry point if available."""
    return getattr(_cmd, "main", None)
