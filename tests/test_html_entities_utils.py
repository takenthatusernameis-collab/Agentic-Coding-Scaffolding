"""Tests for html_entities_utils."""

from html_entities_utils import (
    codepoint_to_name,
    decode_entity,
    get_entity_by_name,
    name_to_codepoint,
    unescape_entity,
)


def test_name_to_codepoint() -> None:
    assert name_to_codepoint("amp") == ord("&")
    assert name_to_codepoint("lt") == ord("<")
    assert get_entity_by_name("gt") == ord(">")


def test_codepoint_to_name() -> None:
    assert codepoint_to_name(ord("&")) == "amp"


def test_decode_entity() -> None:
    assert decode_entity("nbsp") == "\xa0"
    assert unescape_entity("copy") is not None
