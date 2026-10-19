"""Tests for dis_utils module."""

import io
import unittest
from contextlib import redirect_stdout

from dis_utils import (
    Bytecode,
    code_info,
    dis,
    disassemble,
    disco,
    findlabels,
    findlinestarts,
    get_instructions,
    show_code,
)


def simple_func(x: int) -> int:
    return x + 1


class TestDisUtils(unittest.TestCase):
    def test_dis_outputs(self):
        buf = io.StringIO()
        with redirect_stdout(buf):
            dis(simple_func)
        self.assertIn("LOAD_FAST", buf.getvalue())

    def test_disassemble_outputs(self):
        buf = io.StringIO()
        with redirect_stdout(buf):
            disassemble(simple_func.__code__)
        self.assertIn("LOAD_FAST", buf.getvalue())

    def test_show_code_outputs(self):
        buf = io.StringIO()
        with redirect_stdout(buf):
            show_code(simple_func)
        output = buf.getvalue()
        self.assertIn("simple_func", output)

    def test_code_info_outputs(self):
        info = code_info(simple_func)
        self.assertIn("simple_func", info)

    def test_get_instructions_iterates(self):
        instrs = list(get_instructions(simple_func))
        self.assertTrue(len(instrs) > 0)

    def test_findlabels_and_findlinestarts(self):
        code = simple_func.__code__
        labels = findlabels(code.co_code)
        self.assertIsInstance(labels, list)
        linestarts = list(findlinestarts(code))
        self.assertIsInstance(linestarts, list)

    def test_bytecode_class(self):
        bc = Bytecode(simple_func)
        self.assertTrue(list(bc))

    def test_disco_no_args(self):
        try:
            disco()
        except Exception:
            pass


if __name__ == "__main__":
    unittest.main()
