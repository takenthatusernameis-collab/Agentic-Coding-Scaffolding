import unittest
from unittest.mock import patch
import io
from hello import main


class TestHello(unittest.TestCase):
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_main_prints_hello_world(self, mock_stdout):
        main()
        self.assertEqual(mock_stdout.getvalue().strip(), "Hello, World!")


if __name__ == '__main__':
    unittest.main()