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

    def test_is_complete(self):
        self.assertTrue(code_utils.is_complete("x = 1"))

    def test_is_complete_incomplete(self):
        self.assertFalse(code_utils.is_complete("def foo("))

    def test_is_complete_invalid(self):
        self.assertFalse(code_utils.is_complete("def foo(:"))

    def test_is_complete_type_error(self):
        with self.assertRaises(TypeError):
            code_utils.is_complete(123)


if __name__ == "__main__":
    unittest.main()
