"""Utilities for the :mod:`antigravity` module."""

from __future__ import annotations

import antigravity as _antigravity

# Re-export the geohash function
geohash = _antigravity.geohash


def fly():
    """Open the XKCD comic about Python."""
    import webbrowser

    webbrowser.open("https://xkcd.com/353/")
    return "https://xkcd.com/353/"


def get_xkcd_url() -> str:
    """Return the URL of the XKCD comic about Python."""
    return "https://xkcd.com/353/"


__all__ = ["geohash", "fly", "get_xkcd_url"]
