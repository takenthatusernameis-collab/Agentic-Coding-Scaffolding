"""Utilities for terminal control (wrapping :mod:`tty`)."""

import tty as _tty


def cfmakeraw(mode):
    return _tty.cfmakeraw(mode)


def cfmakecbreak(mode):
    return _tty.cfmakecbreak(mode)


def setraw(fd, when=None):
    if when is None:
        return _tty.setraw(fd)
    return _tty.setraw(fd, when)


def setcbreak(fd, when=None):
    if when is None:
        return _tty.setcbreak(fd)
    return _tty.setcbreak(fd, when)
