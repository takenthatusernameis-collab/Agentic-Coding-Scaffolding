"""HTML parser utilities wrapping the standard library html.parser module.

Provides helpers for parsing HTML using HTMLParser with convenient wrappers.
"""

from __future__ import annotations

from html.parser import HTMLParser
from typing import Any, Callable, List, Optional, Union

__all__ = [
    "HTMLParser",
    "parse_html",
    "strip_tags",
]


class _TagStripper(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.reset()
        self.fed: List[str] = []

    def handle_data(self, data: str) -> None:
        self.fed.append(data)

    def get_data(self) -> str:
        return "".join(self.fed)


def strip_tags(html: Union[str, None]) -> str:
    """Remove all HTML tags from ``html`` and return the text content.

    Args:
        html: Input HTML string.

    Returns:
        Text content with tags removed.

    Raises:
        TypeError: If ``html`` is not a string or None.
    """
    if html is None:
        return ""
    if not isinstance(html, str):
        raise TypeError("html must be a string or None")
    s = _TagStripper()
    s.feed(html)
    s.close()
    return s.get_data()


def parse_html(
    html: str,
    *,
    handle_starttag: Optional[Callable[..., Any]] = None,
    handle_endtag: Optional[Callable[..., Any]] = None,
    handle_data: Optional[Callable[..., Any]] = None,
    handle_comment: Optional[Callable[..., Any]] = None,
    handle_entityref: Optional[Callable[..., Any]] = None,
    handle_charref: Optional[Callable[..., Any]] = None,
    handle_decl: Optional[Callable[..., Any]] = None,
    handle_pi: Optional[Callable[..., Any]] = None,
) -> HTMLParser:
    """Create and feed an HTMLParser with optional custom handlers.

    Args:
        html: HTML string to parse.
        handle_starttag: Optional callback for start tags.
        handle_endtag: Optional callback for end tags.
        handle_data: Optional callback for data.
        handle_comment: Optional callback for comments.
        handle_entityref: Optional callback for entity references.
        handle_charref: Optional callback for character references.
        handle_decl: Optional callback for declarations.
        handle_pi: Optional callback for processing instructions.

    Returns:
        The HTMLParser instance after feeding ``html``.

    Raises:
        TypeError: If ``html`` is not a string.
    """
    if not isinstance(html, str):
        raise TypeError("html must be a string")

    class CustomParser(HTMLParser):
        pass

    parser = CustomParser()
    if handle_starttag is not None:
        parser.handle_starttag = handle_starttag  # type: ignore[method-assign]
    if handle_endtag is not None:
        parser.handle_endtag = handle_endtag  # type: ignore[method-assign]
    if handle_data is not None:
        parser.handle_data = handle_data  # type: ignore[method-assign]
    if handle_comment is not None:
        parser.handle_comment = handle_comment  # type: ignore[method-assign]
    if handle_entityref is not None:
        parser.handle_entityref = handle_entityref  # type: ignore[method-assign]
    if handle_charref is not None:
        parser.handle_charref = handle_charref  # type: ignore[method-assign]
    if handle_decl is not None:
        parser.handle_decl = handle_decl  # type: ignore[method-assign]
    if handle_pi is not None:
        parser.handle_pi = handle_pi  # type: ignore[method-assign]

    parser.feed(html)
    parser.close()
    return parser
