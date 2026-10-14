import io
import unittest
from unittest.mock import patch

from hello import main


class TestHello(unittest.TestCase):
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_main_prints_hello_world(self, mock_stdout):
        main()
        self.assertEqual(mock_stdout.getvalue().strip(), "Hello, World!")

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_main_prints_hello_alice(self, mock_stdout):
        main("Alice")
        self.assertEqual(mock_stdout.getvalue().strip(), "Hello, Alice!")

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_main_prints_hello_with_custom_name(self, mock_stdout):
        main("Bob")
        self.assertEqual(mock_stdout.getvalue().strip(), "Hello, Bob!")


if __name__ == '__main__':
    unittest.main()
