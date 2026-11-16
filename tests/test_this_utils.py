"""Tests for this_utils."""

import io
import this as _this
import unittest
from contextlib import redirect_stdout

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


def test_decode_returns_str():
    assert isinstance(this_utils.decode("Gur Mra bs Clguba"), str)


def test_decode_round_trip():
    encoded = "gur mra bs clguba"
    assert "the zen of python" in this_utils.decode(encoded)


class TestPrintZen(unittest.TestCase):
    def test_print_zen_outputs_zen(self) -> None:
        buffer = io.StringIO()
        with redirect_stdout(buffer):
            this_utils.print_zen()
        self.assertEqual(buffer.getvalue(), this_utils.decode(_this.s) + "\n")

    def test_print_zen_is_decoded(self) -> None:
        buffer = io.StringIO()
        with redirect_stdout(buffer):
            this_utils.print_zen()
        self.assertIn("The Zen of Python", buffer.getvalue())
        self.assertIn("Beautiful is better", buffer.getvalue())

    def test_print_zen_is_not_encoded(self) -> None:
        buffer = io.StringIO()
        with redirect_stdout(buffer):
            this_utils.print_zen()
        self.assertNotIn("Gur Mra bs Clguba", buffer.getvalue())


if __name__ == "__main__":
    unittest.main()
