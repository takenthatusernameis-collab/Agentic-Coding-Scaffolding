"""Utilities for Python interactive console support (wrapping :mod:`code`)."""

import code as _code


def interact(banner=None, readfunc=None, local=None, exitmsg=None):
    """Run an interactive console (wrapping ``code.interact``)."""
    return _code.interact(banner=banner, readfunc=readfunc, local=local, exitmsg=exitmsg)


def compile_command(source, filename="<input>", symbol="single"):
    """Compile a command (wrapping ``code.compile_command``)."""
    if not isinstance(source, str):
        raise TypeError("source must be a str")
    return _code.compile_command(source, filename=filename, symbol=symbol)


def console_class():
    """Return the ``InteractiveConsole`` class."""
    return _code.InteractiveConsole


def interpreter_class():
    """Return the ``InteractiveInterpreter`` class."""
    return _code.InteractiveInterpreter
