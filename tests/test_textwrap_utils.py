import textwrap

import textwrap_utils


def test_wrap_text():
    lines = textwrap_utils.wrap_text("hello world", width=5)
    assert lines == textwrap.wrap("hello world", width=5)


def test_shorten_text():
    assert textwrap_utils.shorten_text("hello world", width=8) == "hello..."


def test_dedent_text():
    assert textwrap_utils.dedent_text("    a\n    b") == "a\nb"


def test_indent_text():
    assert textwrap_utils.indent_text("a\nb", "> ") == "> a\n> b"


def test_fill_text():
    assert textwrap_utils.fill_text("hello world", width=5) == textwrap.fill("hello world", width=5)


def test_validation():
    for f in (textwrap_utils.wrap_text, textwrap_utils.fill_text):
        try:
            f(123)
        except TypeError:
            pass
        else:
            raise AssertionError("TypeError expected")
