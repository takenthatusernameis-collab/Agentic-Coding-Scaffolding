"""Utilities for compiling possibly-incomplete Python source (wrapping :mod:`codeop`)."""

from __future__ import annotations

import codeop

__all__: list[str] = ["compile_command", "Compile", "CommandCompiler"]


def compile_command(source, filename="<input>", symbol="single"):
    return codeop.compile_command(source, filename, symbol)


Compile = codeop.Compile
CommandCompiler = codeop.CommandCompiler
