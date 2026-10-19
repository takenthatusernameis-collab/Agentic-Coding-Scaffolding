"""Utilities for running Python modules (wrapping :mod:`runpy`)."""

import runpy as _runpy


def run_module(mod_name, init_globals=None, run_name=None, alter_sys=False):
    if not isinstance(mod_name, str):
        raise TypeError("mod_name must be a str")
    return _runpy.run_module(
        mod_name, init_globals=init_globals, run_name=run_name, alter_sys=alter_sys
    )


def run_path(file_path, init_globals=None, run_name=None):
    if not isinstance(file_path, str):
        raise TypeError("file_path must be a str")
    return _runpy.run_path(file_path, init_globals=init_globals, run_name=run_name)
