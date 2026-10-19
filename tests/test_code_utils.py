import unittest

import code_utils


class TestCodeUtils(unittest.TestCase):
    def test_compile_command(self):
        self.assertIsNotNone(code_utils.compile_command("x = 1"))

    def test_compile_command_invalid(self):
        self.assertIsNone(code_utils.compile_command("def foo("))

    def test_console_class(self):
        self.assertTrue(callable(code_utils.console_class()))

    def test_interpreter_class(self):
        self.assertTrue(callable(code_utils.interpreter_class()))

    def test_type_error(self):
        with self.assertRaises(TypeError):
            code_utils.compile_command(123)


if __name__ == "__main__":
    unittest.main()
