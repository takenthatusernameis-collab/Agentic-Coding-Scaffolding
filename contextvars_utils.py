"""Contextvars utility functions wrapping stdlib contextvars."""

from __future__ import annotations

import contextvars

__all__: list[str] = [
    "ContextVar",
    "Token",
    "copy_context",
    "Context",
]

ContextVar = contextvars.ContextVar
Token = contextvars.Token
Context = contextvars.Context


def copy_context() -> contextvars.Context:
    return contextvars.copy_context()
