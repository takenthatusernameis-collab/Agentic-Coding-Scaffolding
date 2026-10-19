"""Utilities for secure password input (wrapping :mod:`getpass`)."""

import getpass as _getpass


def getpass(prompt="Password: ", stream=None):
    return _getpass.getpass(prompt, stream)


def getuser():
    return _getpass.getuser()
