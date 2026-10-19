import codeop
import unittest

from codeop_utils import CommandCompiler, Compile, compile_command


class TestCodeopUtils(unittest.TestCase):
    def test_compile_command_complete(self):
        code = compile_command("1 + 2")
        self.assertIsNotNone(code)

    def test_compile_command_incomplete(self):
        code = compile_command("def f():")
        self.assertIsNone(code)

    def test_compile_command_syntax_error(self):
        with self.assertRaises(SyntaxError):
            compile_command("def f()")

    def test_command_compiler(self):
        cc = CommandCompiler()
        code = cc("x = 1")
        self.assertIsNotNone(code)

    def test_compile_alias(self):
        self.assertIs(Compile, codeop.Compile)


if __name__ == "__main__":
    unittest.main()
