"""Tests for env_utils module."""

import os
import unittest
from unittest import mock

from env_utils import (
    ensure_env,
    get_env,
    get_env_bool,
    get_env_float,
    get_env_int,
    get_env_required,
    prefix_env,
    set_env,
    unset_env,
)


class TestGetEnv(unittest.TestCase):
    def test_returns_value_when_set(self) -> None:
        with mock.patch.dict(os.environ, {"MY_VAR": "value"}, clear=True):
            self.assertEqual(get_env("MY_VAR"), "value")

    def test_returns_default_when_unset(self) -> None:
        with mock.patch.dict(os.environ, {}, clear=True):
            self.assertIsNone(get_env("MISSING"))
            self.assertEqual(get_env("MISSING", "fallback"), "fallback")

    def test_returns_empty_string_when_set_empty(self) -> None:
        with mock.patch.dict(os.environ, {"EMPTY_VAR": ""}, clear=True):
            self.assertEqual(get_env("EMPTY_VAR"), "")

    def test_non_string_key_raises(self) -> None:
        with self.assertRaises(TypeError):
            get_env(123)  # type: ignore[arg-type]


class TestGetEnvRequired(unittest.TestCase):
    def test_returns_value_when_set(self) -> None:
        with mock.patch.dict(os.environ, {"REQUIRED_VAR": "abc"}, clear=True):
            self.assertEqual(get_env_required("REQUIRED_VAR"), "abc")

    def test_raises_when_unset(self) -> None:
        with mock.patch.dict(os.environ, {}, clear=True):
            with self.assertRaises(KeyError):
                get_env_required("MISSING_REQUIRED")

    def test_error_message_contains_key(self) -> None:
        with mock.patch.dict(os.environ, {}, clear=True):
            with self.assertRaises(KeyError) as ctx:
                get_env_required("MISSING_REQUIRED")
            self.assertIn("MISSING_REQUIRED", str(ctx.exception))

    def test_non_string_key_raises(self) -> None:
        with self.assertRaises(TypeError):
            get_env_required(123)  # type: ignore[arg-type]


class TestGetEnvInt(unittest.TestCase):
    def test_returns_int_when_valid(self) -> None:
        with mock.patch.dict(os.environ, {"PORT": "8080"}, clear=True):
            self.assertEqual(get_env_int("PORT"), 8080)

    def test_returns_default_when_unset(self) -> None:
        with mock.patch.dict(os.environ, {}, clear=True):
            self.assertEqual(get_env_int("MISSING", 42), 42)
            self.assertIsNone(get_env_int("MISSING"))

    def test_raises_when_invalid(self) -> None:
        with mock.patch.dict(os.environ, {"PORT": "not-a-number"}, clear=True):
            with self.assertRaises(ValueError):
                get_env_int("PORT")

    def test_handles_negative(self) -> None:
        with mock.patch.dict(os.environ, {"OFFSET": "-5"}, clear=True):
            self.assertEqual(get_env_int("OFFSET"), -5)

    def test_non_string_key_raises(self) -> None:
        with self.assertRaises(TypeError):
            get_env_int(123)  # type: ignore[arg-type]


class TestGetEnvFloat(unittest.TestCase):
    def test_returns_float_when_valid(self) -> None:
        with mock.patch.dict(os.environ, {"RATIO": "3.14"}, clear=True):
            result = get_env_float("RATIO")
            assert result is not None
            self.assertAlmostEqual(result, 3.14)

    def test_returns_int_as_float(self) -> None:
        with mock.patch.dict(os.environ, {"COUNT": "10"}, clear=True):
            result = get_env_float("COUNT")
            assert result is not None
            self.assertEqual(result, 10.0)

    def test_returns_default_when_unset(self) -> None:
        with mock.patch.dict(os.environ, {}, clear=True):
            self.assertIsNone(get_env_float("MISSING"))
            result = get_env_float("MISSING", 1.5)
            assert result is not None
            self.assertAlmostEqual(result, 1.5)

    def test_raises_when_invalid(self) -> None:
        with mock.patch.dict(os.environ, {"RATE": "abc"}, clear=True):
            with self.assertRaises(ValueError):
                get_env_float("RATE")

    def test_non_string_key_raises(self) -> None:
        with self.assertRaises(TypeError):
            get_env_float(123)  # type: ignore[arg-type]


class TestGetEnvBool(unittest.TestCase):
    def test_true_values(self) -> None:
        for val in ["1", "true", "TRUE", "Yes", "on", "Y", "t"]:
            with mock.patch.dict(os.environ, {"FLAG": val}, clear=True):
                self.assertIs(get_env_bool("FLAG"), True, f"{val!r} should be True")

    def test_false_values(self) -> None:
        for val in ["0", "false", "NO", "off", "f", "", "  "]:
            with mock.patch.dict(os.environ, {"FLAG": val}, clear=True):
                self.assertIs(get_env_bool("FLAG"), False, f"{val!r} should be False")

    def test_returns_default_when_unset(self) -> None:
        with mock.patch.dict(os.environ, {}, clear=True):
            self.assertIs(get_env_bool("MISSING", True), True)
            self.assertIs(get_env_bool("MISSING", False), False)
            self.assertIsNone(get_env_bool("MISSING"))

    def test_raises_when_invalid(self) -> None:
        with mock.patch.dict(os.environ, {"FLAG": "maybe"}, clear=True):
            with self.assertRaises(ValueError):
                get_env_bool("FLAG")

    def test_non_string_key_raises(self) -> None:
        with self.assertRaises(TypeError):
            get_env_bool(123)  # type: ignore[arg-type]


class TestSetEnv(unittest.TestCase):
    def test_sets_string_value(self) -> None:
        with mock.patch.dict(os.environ, {}, clear=True):
            set_env("KEY", "value")
            self.assertEqual(os.environ["KEY"], "value")

    def test_converts_non_string_value(self) -> None:
        with mock.patch.dict(os.environ, {}, clear=True):
            set_env("COUNT", 42)
            self.assertEqual(os.environ["COUNT"], "42")

    def test_overwrites_existing(self) -> None:
        with mock.patch.dict(os.environ, {"KEY": "old"}, clear=True):
            set_env("KEY", "new")
            self.assertEqual(os.environ["KEY"], "new")

    def test_rejects_non_string_key(self) -> None:
        with self.assertRaises(TypeError):
            set_env(123, "value")  # type: ignore[arg-type]

    def test_rejects_empty_key(self) -> None:
        with self.assertRaises(ValueError):
            set_env("", "value")

    def test_rejects_key_with_equals(self) -> None:
        with self.assertRaises(ValueError):
            set_env("KEY=VAL", "value")


class TestEnsureEnv(unittest.TestCase):
    def test_sets_default_when_missing(self) -> None:
        with mock.patch.dict(os.environ, {}, clear=True):
            result = ensure_env("NEW_VAR", "default")
            self.assertEqual(result, "default")
            self.assertEqual(os.environ["NEW_VAR"], "default")

    def test_preserves_existing_value(self) -> None:
        with mock.patch.dict(os.environ, {"EXISTING": "old"}, clear=True):
            result = ensure_env("EXISTING", "new")
            self.assertEqual(result, "old")
            self.assertEqual(os.environ["EXISTING"], "old")

    def test_rejects_non_string_key(self) -> None:
        with self.assertRaises(TypeError):
            ensure_env(123, "default")  # type: ignore[arg-type]

    def test_rejects_non_string_default(self) -> None:
        with self.assertRaises(TypeError):
            ensure_env("NEW_VAR", 42)  # type: ignore[arg-type]

    def test_rejects_empty_key(self) -> None:
        with self.assertRaises(ValueError):
            ensure_env("", "default")


class TestUnsetEnv(unittest.TestCase):
    def test_removes_existing(self) -> None:
        with mock.patch.dict(os.environ, {"TO_REMOVE": "x"}, clear=True):
            self.assertTrue(unset_env("TO_REMOVE"))
            self.assertNotIn("TO_REMOVE", os.environ)

    def test_returns_false_when_not_set(self) -> None:
        with mock.patch.dict(os.environ, {}, clear=True):
            self.assertFalse(unset_env("MISSING"))
            self.assertFalse(unset_env("MISSING"))

    def test_non_string_key_raises(self) -> None:
        with self.assertRaises(TypeError):
            unset_env(123)  # type: ignore[arg-type]


class TestPrefixEnv(unittest.TestCase):
    def test_returns_filtered_vars(self) -> None:
        env = {"APP_DEBUG": "1", "APP_HOST": "x", "PATH": "/bin"}
        with mock.patch.dict(os.environ, env, clear=False):
            result = prefix_env("APP_")
            self.assertEqual(result, {"APP_DEBUG": "1", "APP_HOST": "x"})

    def test_empty_prefix_returns_all(self) -> None:
        env = {"A": "1", "B": "2"}
        with mock.patch.dict(os.environ, env, clear=False):
            result = prefix_env("")
            self.assertIn("A", result)
            self.assertIn("B", result)

    def test_no_matches_returns_empty(self) -> None:
        with mock.patch.dict(os.environ, {}, clear=True):
            self.assertEqual(prefix_env("NOPE_"), {})

    def test_non_string_prefix_raises(self) -> None:
        with self.assertRaises(TypeError):
            prefix_env(123)  # type: ignore[arg-type]


if __name__ == "__main__":
    unittest.main()
