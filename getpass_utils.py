"""Utilities for secure password input (wrapping :mod:`getpass`)."""

import getpass as _getpass

__all__ = [
    "getpass",
    "getuser",
]



def getpass(prompt="Password: ", stream=None):
    return _getpass.getpass(prompt, stream)


def getuser():
    return _getpass.getuser()
