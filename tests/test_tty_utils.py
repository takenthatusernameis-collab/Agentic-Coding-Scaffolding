import termios
import unittest

from tty_utils import cfmakecbreak, cfmakeraw, setcbreak, setraw


class TestTtyUtils(unittest.TestCase):
    def test_cfmakeraw(self):
        mode = [0, 0, 0, 0, 0, 0, list(termios.tcgetattr(0)[6])] if False else None
        # Build a minimal mode list mimicking termios structure
        mode = [0] * 7
        mode[6] = [0] * termios.NCCS
        result = cfmakeraw(mode)
        self.assertIsNone(result)

    def test_cfmakecbreak(self):
        mode = [0] * 7
        mode[6] = [0] * termios.NCCS
        result = cfmakecbreak(mode)
        self.assertIsNone(result)

    def test_setraw_callable(self):
        self.assertTrue(callable(setraw))

    def test_setcbreak_callable(self):
        self.assertTrue(callable(setcbreak))


if __name__ == "__main__":
    unittest.main()
