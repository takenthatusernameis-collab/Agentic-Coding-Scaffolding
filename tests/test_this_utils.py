"""Tests for this_utils."""

import this as _this

import this_utils


def test_zen_of_python_is_string():
    assert isinstance(this_utils.zen_of_python, str)
    assert this_utils.zen_of_python == _this.s


def test_translation_table_is_dict():
    assert isinstance(this_utils.translation_table, dict)
    assert this_utils.translation_table == _this.d


def test_cipher_index_is_int():
    assert isinstance(this_utils.cipher_index, int)
    assert this_utils.cipher_index == _this.c


def test_this_returns_callable_or_none():
    result = this_utils.this()
    # The `this` function is not always exposed; accept either.
    assert result is None or callable(result)


def test_print_zen(capsys):
    this_utils.print_zen()
    out = capsys.readouterr().out
    # The Zen is ROT13-encoded in the stdlib module; the encoded header is
    # "Gur Mra bs Clguba" for "The Zen of Python".
    assert "Gur Mra bs Clguba" in out
