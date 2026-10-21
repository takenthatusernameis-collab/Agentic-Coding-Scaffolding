"""Utilities wrapping the standard library ``nturl2path`` module."""

import nturl2path

__all__: list[str] = ["url2pathname", "pathname2url"]


def url2pathname(url: str) -> str:
    return nturl2path.url2pathname(url)


def pathname2url(path: str) -> str:
    return nturl2path.pathname2url(path)
