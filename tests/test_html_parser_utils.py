"""Tests for html_parser_utils."""

from html_parser_utils import HTMLParser, parse_html, strip_tags


def test_strip_tags_basic() -> None:
    html = "<p>Hello <b>World</b>!</p>"
    assert strip_tags(html) == "Hello World!"


def test_strip_tags_none() -> None:
    assert strip_tags(None) == ""


def test_strip_tags_no_tags() -> None:
    assert strip_tags("plain text") == "plain text"


def test_parse_html_with_custom_handlers() -> None:
    tags = []

    def handle_starttag(tag: str, attrs: list) -> None:
        tags.append(("start", tag))

    def handle_endtag(tag: str) -> None:
        tags.append(("end", tag))

    parser = parse_html(
        "<div>Hi</div>",
        handle_starttag=handle_starttag,
        handle_endtag=handle_endtag,
    )
    assert isinstance(parser, HTMLParser)
    assert ("start", "div") in tags
    assert ("end", "div") in tags


def test_parse_html_default() -> None:
    parser = parse_html("<span>test</span>")
    assert isinstance(parser, HTMLParser)
