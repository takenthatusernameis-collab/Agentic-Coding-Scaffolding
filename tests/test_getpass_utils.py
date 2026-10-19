import getpass
import unittest

from getpass_utils import getpass as _getpass
from getpass_utils import getuser


class TestGetpassUtils(unittest.TestCase):
    def test_getuser(self):
        self.assertIsInstance(getuser(), str)
        self.assertEqual(getuser(), getpass.getuser())

    def test_getpass_callable(self):
        self.assertTrue(callable(_getpass))


if __name__ == "__main__":
    unittest.main()
