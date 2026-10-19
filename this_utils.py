"""Utilities for the Zen of Python (wrapping :mod:`this`).

This module exposes the well-known ``this`` module — which prints the Zen of
Python — as a small, consistent utility surface. The ``this`` module itself
has no public API beyond the ``this`` function, so the wrapper simply
re-exports it and provides a couple of helpers around the underlying
translation table.
"""

import this as _this

# The Zen of Python, as a single string.
zen_of_python = _this.s

# The ROT13 translation table used to encode the Zen.
translation_table = _this.d

# The index of the key used in the cipher.
cipher_index = getattr(_this, "c", 97)


def this():
    """Return the ``this`` module's ``this`` callable.

    The ``this`` module historically exposed a ``this`` function that prints
    the Zen of Python. On modern Python it is not always present, so this
    helper returns ``None`` when it is unavailable.
    """
    return getattr(_this, "this", None)


def print_zen():
    """Print the Zen of Python to standard output."""
    print(_this.s)
