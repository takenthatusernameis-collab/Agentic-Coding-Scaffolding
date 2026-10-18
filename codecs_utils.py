"""Utilities for codec registration and encoding/decoding (wrapping :mod:`codecs`)."""

from __future__ import annotations

import codecs as _codecs


def encode(obj, encoding="utf-8", errors="strict"):
    """Encode *obj* using *encoding*."""
    return _codecs.encode(obj, encoding, errors)


def decode(obj, encoding="utf-8", errors="strict"):
    """Decode *obj* using *encoding*."""
    return _codecs.decode(obj, encoding, errors)


def lookup(encoding):
    """Look up a codec by *encoding* name."""
    return _codecs.lookup(encoding)


def getencoder(encoding):
    """Return the encoder function for *encoding*."""
    return _codecs.getencoder(encoding)


def getdecoder(encoding):
    """Return the decoder function for *encoding*."""
    return _codecs.getdecoder(encoding)


def getincrementalencoder(encoding, errors="strict"):
    """Return an incremental encoder for *encoding*."""
    return _codecs.getincrementalencoder(encoding)(errors)


def getincrementaldecoder(encoding, errors="strict"):
    """Return an incremental decoder for *encoding*."""
    return _codecs.getincrementaldecoder(encoding)(errors)


def getreader(encoding):
    """Return a StreamReader for *encoding*."""
    return _codecs.getreader(encoding)


def getwriter(encoding):
    """Return a StreamWriter for *encoding*."""
    return _codecs.getwriter(encoding)


def open(filename, mode="r", encoding=None, errors="strict", buffering=-1, newline=None):
    """Open a file with the given encoding."""
    return _codecs.open(filename, mode, encoding, errors, buffering, newline)


def register(search_function):
    """Register a codec search function."""
    return _codecs.register(search_function)


def register_error(name, error_handler):
    """Register an error handler under *name*."""
    return _codecs.register_error(name, error_handler)


def lookup_error(name):
    """Look up an error handler by *name*."""
    return _codecs.lookup_error(name)


__all__ = [
    "encode",
    "decode",
    "lookup",
    "getencoder",
    "getdecoder",
    "getincrementalencoder",
    "getincrementaldecoder",
    "getreader",
    "getwriter",
    "open",
    "register",
    "register_error",
    "lookup_error",
]
