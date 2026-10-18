import unittest

from http_utils import (
    HTTP_CLIENT_ERROR,
    HTTP_INFORMATIONAL,
    HTTP_REDIRECTION,
    HTTP_SERVER_ERROR,
    HTTP_SUCCESS,
    is_client_error,
    is_error,
    is_informational,
    is_redirection,
    is_server_error,
    is_success,
    status_code_category,
    status_message,
)


class TestStatusCodeCategory(unittest.TestCase):
    def test_informational(self):
        self.assertEqual(status_code_category(100), HTTP_INFORMATIONAL)
        self.assertEqual(status_code_category(199), HTTP_INFORMATIONAL)

    def test_success(self):
        self.assertEqual(status_code_category(200), HTTP_SUCCESS)
        self.assertEqual(status_code_category(299), HTTP_SUCCESS)

    def test_redirection(self):
        self.assertEqual(status_code_category(300), HTTP_REDIRECTION)
        self.assertEqual(status_code_category(399), HTTP_REDIRECTION)

    def test_client_error(self):
        self.assertEqual(status_code_category(400), HTTP_CLIENT_ERROR)
        self.assertEqual(status_code_category(499), HTTP_CLIENT_ERROR)

    def test_server_error(self):
        self.assertEqual(status_code_category(500), HTTP_SERVER_ERROR)
        self.assertEqual(status_code_category(599), HTTP_SERVER_ERROR)


class TestStatusMessage(unittest.TestCase):
    def test_known_codes(self):
        self.assertEqual(status_message(200), "OK")
        self.assertEqual(status_message(201), "Created")
        self.assertEqual(status_message(404), "Not Found")
        self.assertEqual(status_message(500), "Internal Server Error")
        self.assertEqual(status_message(418), "I'm a teapot")

    def test_unknown_code_returns_none(self):
        self.assertIsNone(status_message(999))
        self.assertIsNone(status_message(0))


class TestBooleanChecks(unittest.TestCase):
    def test_is_informational(self):
        self.assertTrue(is_informational(100))
        self.assertFalse(is_informational(200))

    def test_is_success(self):
        self.assertTrue(is_success(200))
        self.assertTrue(is_success(204))
        self.assertFalse(is_success(300))

    def test_is_redirection(self):
        self.assertTrue(is_redirection(301))
        self.assertTrue(is_redirection(308))
        self.assertFalse(is_redirection(200))

    def test_is_client_error(self):
        self.assertTrue(is_client_error(400))
        self.assertTrue(is_client_error(404))
        self.assertFalse(is_client_error(500))

    def test_is_server_error(self):
        self.assertTrue(is_server_error(500))
        self.assertTrue(is_server_error(503))
        self.assertFalse(is_server_error(400))

    def test_is_error(self):
        self.assertTrue(is_error(400))
        self.assertTrue(is_error(500))
        self.assertFalse(is_error(200))
        self.assertFalse(is_error(300))


if __name__ == "__main__":
    unittest.main()
