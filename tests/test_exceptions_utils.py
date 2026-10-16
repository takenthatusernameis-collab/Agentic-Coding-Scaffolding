"""Tests for exceptions_utils module."""

import unittest

from exceptions_utils import (
    ConfigurationError,
    NotFoundError,
    PermissionError_,
    TimeoutError_,
    ValidationError,
    catch_and_wrap,
    get_error_details,
    is_instance_of_any,
)


class TestCustomExceptions(unittest.TestCase):
    def test_validation_error_default(self):
        err = ValidationError()
        self.assertIsInstance(err, ValueError)
        self.assertIsInstance(err, ValidationError)
        self.assertEqual(err.message, "Validation failed")
        self.assertIsNone(err.field)
        self.assertIsNone(err.value)

    def test_validation_error_with_details(self):
        err = ValidationError("Invalid email", field="email", value="not-an-email")
        self.assertEqual(err.message, "Invalid email")
        self.assertEqual(err.field, "email")
        self.assertEqual(err.value, "not-an-email")
        self.assertEqual(str(err), "Invalid email")

    def test_configuration_error(self):
        err = ConfigurationError("Missing config")
        self.assertIsInstance(err, Exception)
        self.assertEqual(str(err), "Missing config")

    def test_not_found_error(self):
        err = NotFoundError("User not found")
        self.assertIsInstance(err, Exception)
        self.assertEqual(str(err), "User not found")

    def test_permission_error_(self):
        err = PermissionError_("Access denied")
        self.assertIsInstance(err, Exception)
        self.assertEqual(str(err), "Access denied")

    def test_timeout_error_(self):
        err = TimeoutError_("Request timed out")
        self.assertIsInstance(err, Exception)
        self.assertEqual(str(err), "Request timed out")


class TestCatchAndWrap(unittest.TestCase):
    def test_successful_execution(self):
        result = catch_and_wrap(lambda: 42)
        self.assertEqual(result, 42)

    def test_wraps_exception_with_default(self):
        def fail():
            raise ValueError("oops")

        with self.assertRaises(Exception) as ctx:
            catch_and_wrap(fail)
        self.assertIsInstance(ctx.exception, Exception)
        not isinstance(ctx.exception, ValueError)

    def test_wraps_specific_exceptions_only(self):
        def fail():
            raise ValueError("oops")

        with self.assertRaises(Exception):
            catch_and_wrap(fail, exceptions=(ValueError,))

    def test_does_not_wrap_other_exceptions(self):
        def fail():
            raise TypeError("oops")

        with self.assertRaises(TypeError):
            catch_and_wrap(fail, exceptions=(ValueError,))

    def test_wraps_with_custom_exception(self):
        def fail():
            raise RuntimeError("bad")

        with self.assertRaises(ConfigurationError):
            catch_and_wrap(fail, exceptions=(RuntimeError,), wrap_with=ConfigurationError)

    def test_wraps_with_custom_message(self):
        def fail():
            raise RuntimeError("bad")

        with self.assertRaises(ConfigurationError) as ctx:
            catch_and_wrap(
                fail,
                exceptions=(RuntimeError,),
                wrap_with=ConfigurationError,
                message="Config failed",
            )
        self.assertEqual(str(ctx.exception), "Config failed")

    def test_preserves_cause(self):
        def fail():
            raise RuntimeError("original")

        try:
            catch_and_wrap(fail, exceptions=(RuntimeError,), wrap_with=ValidationError)
        except ValidationError as e:
            self.assertIsNotNone(e.__cause__)
            self.assertIsInstance(e.__cause__, RuntimeError)


class TestGetErrorDetails(unittest.TestCase):
    def test_get_error_details(self):
        try:
            raise ValueError("test error")
        except ValueError as e:
            details = get_error_details(e)
            self.assertEqual(details["type"], "ValueError")
            self.assertEqual(details["message"], "test error")
            self.assertIn("traceback", details)
            self.assertIsInstance(details["traceback"], str)


class TestIsInstanceOfAny(unittest.TestCase):
    def test_matches_single_type(self):
        self.assertTrue(is_instance_of_any(ValueError("x"), (ValueError,)))
        self.assertFalse(is_instance_of_any(TypeError("x"), (ValueError,)))

    def test_matches_multiple_types(self):
        self.assertTrue(is_instance_of_any(ValueError("x"), (ValueError, TypeError)))
        self.assertTrue(is_instance_of_any(TypeError("x"), (ValueError, TypeError)))
        self.assertFalse(is_instance_of_any(RuntimeError("x"), (ValueError, TypeError)))

    def test_handles_non_exceptions(self):
        self.assertFalse(is_instance_of_any("not an exception", (ValueError,)))


if __name__ == "__main__":
    unittest.main()
