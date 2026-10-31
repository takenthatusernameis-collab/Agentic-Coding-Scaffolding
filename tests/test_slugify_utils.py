"""Tests for slugify_utils."""

from slugify_utils import deslugify, is_slug, slugify, truncate_slug


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


def test_truncate_slug_no_truncation():
    assert truncate_slug("hello-world", 100) == "hello-world"


def test_truncate_slug_basic():
    assert truncate_slug("hello-world-foo-bar", 12) == "hello..."


def test_truncate_slug_hard_cut():
    assert truncate_slug("abcdefghij", 5) == "ab..."


def test_truncate_slug_invalid_text():
    try:
        truncate_slug(123, 5)  # type: ignore[arg-type]
    except TypeError:
        pass
    else:
        raise AssertionError("expected TypeError")


def test_truncate_slug_invalid_max_length():
    try:
        truncate_slug("abc", -1)
    except ValueError:
        pass
    else:
        raise AssertionError("expected ValueError")


class TestSlugifyMany:
    def test_basic(self):
        from slugify_utils import slugify_many
        assert slugify_many(["Hello World", "Foo Bar"]) == ["hello-world", "foo-bar"]

    def test_type_error(self):
        import pytest
        from slugify_utils import slugify_many
        with pytest.raises(TypeError):
            slugify_many("nope")
