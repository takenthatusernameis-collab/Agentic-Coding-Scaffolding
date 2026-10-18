"""Utilities for pathname pattern expansion (wrapping :mod:`glob`)."""

import glob as _glob


def glob_pattern(pattern, *, root_dir=None, dir_fd=None, recursive=False):
    if not isinstance(pattern, str):
        raise TypeError("pattern must be a str")
    return _glob.glob(pattern, root_dir=root_dir, dir_fd=dir_fd, recursive=recursive)


def iglob(pattern, *, root_dir=None, dir_fd=None, recursive=False):
    if not isinstance(pattern, str):
        raise TypeError("pattern must be a str")
    return _glob.iglob(pattern, root_dir=root_dir, dir_fd=dir_fd, recursive=recursive)


def escape(pathname):
    if not isinstance(pathname, str):
        raise TypeError("pathname must be a str")
    return _glob.escape(pathname)


def has_magic(pathname):
    if not isinstance(pathname, str):
        raise TypeError("pathname must be a str")
    return _glob.has_magic(pathname)