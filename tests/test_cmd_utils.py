import unittest

import cmd_utils


class TestCmdUtils(unittest.TestCase):
    def test_cmd_class(self):
        self.assertTrue(issubclass(cmd_utils.Cmd, object))

    def test_identchars(self):
        self.assertIsInstance(cmd_utils.identchars(), str)

    def test_prompt_default(self):
        self.assertIsInstance(cmd_utils.prompt_default(), str)


if __name__ == "__main__":
    unittest.main()
