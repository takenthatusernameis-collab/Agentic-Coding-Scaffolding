"""Tests for tabnanny_utils."""

import io
import tempfile
import tokenize
import unittest

from tabnanny_utils import NannyNag, check, process_tokens


class TestTabnannyUtils(unittest.TestCase):
    """Verify the ambiguous indentation detection helpers of the wrapper."""

    def test_check_clean_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            src = tmp + "/clean.py"
            with open(src, "w") as handle:
                handle.write("x = 1\n")
            check(src)

    def test_process_tokens_raises_on_ambiguous(self):
        src = "def f():\n  x = 1\n\ty = 2\n"
        tokens = tokenize.generate_tokens(io.StringIO(src).readline)
        with self.assertRaises(NannyNag):
            process_tokens(tokens)

    def test_nannynag_attributes(self):
        nag = NannyNag(3, "msg", "line")
        self.assertEqual(nag.get_lineno(), 3)
        self.assertEqual(nag.get_msg(), "msg")
        self.assertEqual(nag.get_line(), "line")

    def test_check_rejects_non_path(self):
        with self.assertRaises(TypeError):
            check(123)  # type: ignore[arg-type]

    def test_process_tokens_rejects_non_iterable(self):
        with self.assertRaises(TypeError):
            process_tokens(123)  # type: ignore[arg-type]

    def test_all_is_sorted_and_unique(self):
        import tabnanny_utils

        self.assertIsNotNone(tabnanny_utils.__all__)
        self.assertEqual(
            len(tabnanny_utils.__all__), len(set(tabnanny_utils.__all__))
        )
        self.assertEqual(tabnanny_utils.__all__, sorted(tabnanny_utils.__all__))
        for name in tabnanny_utils.__all__:
            self.assertTrue(hasattr(tabnanny_utils, name), name)


if __name__ == "__main__":
    unittest.main()
