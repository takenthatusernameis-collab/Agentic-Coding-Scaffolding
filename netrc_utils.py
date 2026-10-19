"""Netrc utility functions wrapping stdlib netrc."""

from __future__ import annotations

import netrc as _netrc

__all__: list[str] = [
    "netrc",
    "NetrcParseError",
]

netrc = _netrc.netrc
NetrcParseError = _netrc.NetrcParseError
"""Alias for the netrc class."""