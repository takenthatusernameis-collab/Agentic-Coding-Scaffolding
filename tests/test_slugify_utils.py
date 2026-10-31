"""Tests for slugify_utils."""

from slugify_utils import deslugify, is_slug, slugify


def test_slugify_basic():
    assert slugify("Hello World") == "hello-world"


def test_slugify_accents():
    assert slugify("Cafe Resume") == "cafe-resume"


def test_slugify_custom_separator():
    assert slugify("Hello World", "_") == "hello_world"


def test_slugify_invalid_text():
    try:
        slugify(123)  # type: ignore[arg-type]
    except TypeError:
        pass
    else:
        raise AssertionError("expected TypeError")


def test_is_slug():
    assert is_slug("hello-world")
    assert not is_slug("Hello World")
    assert not is_slug("")


def test_deslugify():
    assert deslugify("hello-world") == "Hello World"
    assert deslugify("hello_world", "_") == "Hello World"


def test_deslugify_invalid():
    try:
        deslugify(123)  # type: ignore[arg-type]
    except TypeError:
        pass
    else:
        raise AssertionError("expected TypeError")
