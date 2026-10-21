"""Tests for ensurepip_utils.

The tests never install anything: the standard library is patched whenever the
wrapper reaches it, so the suite installs no package, writes no file, and
never reaches the network.
"""

import io
import unittest
from contextlib import redirect_stderr, redirect_stdout
from unittest.mock import patch

import ensurepip_utils

try:
    import ensurepip as _standard_ensurepip
except ImportError:  # pragma: no cover - a distribution can remove the package
    _standard_ensurepip = None  # type: ignore[assignment]


class TestModuleContract(unittest.TestCase):
    """Verify the contract of the module."""

    def test_all_is_sorted_and_unique(self):
        self.assertEqual(ensurepip_utils.__all__, sorted(set(ensurepip_utils.__all__)))

    def test_every_name_exists(self):
        for name in ensurepip_utils.__all__:
            self.assertTrue(hasattr(ensurepip_utils, name), name)

    def test_is_available_reports_a_bool(self):
        self.assertIsInstance(ensurepip_utils.is_available(), bool)

    def test_is_available_matches_the_standard_library(self):
        self.assertEqual(ensurepip_utils.is_available(), _standard_ensurepip is not None)


class TestInspection(unittest.TestCase):
    """Verify the helpers that report what the interpreter carries."""

    def setUp(self):
        if _standard_ensurepip is None:
            self.skipTest("ensurepip package not available")

    def test_the_version_of_pip_is_reported_as_text(self):
        version = ensurepip_utils.pip_version()
        self.assertIsInstance(version, str)
        self.assertTrue(version)

    def test_the_version_matches_the_standard_library(self):
        self.assertEqual(ensurepip_utils.pip_version(), str(_standard_ensurepip.version()))

    def test_the_wheel_is_a_wheel_when_one_is_found(self):
        wheel = ensurepip_utils.bundled_wheel()
        if wheel is None:
            self.skipTest("the interpreter carries no wheel of pip")
        self.assertTrue(wheel.endswith(".whl"), wheel)

    def test_the_presence_of_pip_is_reported_as_a_bool(self):
        self.assertIsInstance(ensurepip_utils.is_pip_installed(), bool)

    def test_the_presence_of_pip_is_not_guessed(self):
        with patch("ensurepip_utils.importlib.util.find_spec", return_value=None):
            self.assertFalse(ensurepip_utils.is_pip_installed())
        with patch("ensurepip_utils.importlib.util.find_spec", return_value=object()):
            self.assertTrue(ensurepip_utils.is_pip_installed())


class TestValidation(unittest.TestCase):
    """Verify the validation of the arguments.

    The arguments are validated before the standard library is reached, so the
    same error is raised on an interpreter that removed the package.
    """

    def setUp(self):
        patcher = patch("ensurepip_utils._ensurepip")
        self.module = patcher.start()
        self.addCleanup(patcher.stop)

    def test_the_flags_must_be_booleans(self):
        for flag in ("upgrade", "user", "altinstall", "default_pip"):
            with self.assertRaises(TypeError):
                ensurepip_utils.bootstrap(**{flag: "yes"})
        self.module.bootstrap.assert_not_called()

    def test_the_root_must_be_a_path(self):
        with self.assertRaises(TypeError):
            ensurepip_utils.bootstrap(root=42)
        self.module.bootstrap.assert_not_called()

    def test_the_root_must_not_be_empty(self):
        with self.assertRaises(ValueError):
            ensurepip_utils.bootstrap(root="")
        self.module.bootstrap.assert_not_called()

    def test_the_verbosity_must_be_an_integer(self):
        with self.assertRaises(TypeError):
            ensurepip_utils.bootstrap(verbosity="2")
        with self.assertRaises(TypeError):
            ensurepip_utils.bootstrap(verbosity=True)
        self.module.bootstrap.assert_not_called()

    def test_the_verbosity_must_not_be_negative(self):
        with self.assertRaises(ValueError):
            ensurepip_utils.bootstrap(verbosity=-1)
        self.module.bootstrap.assert_not_called()

    def test_the_arguments_of_the_command_line_must_be_a_sequence(self):
        with self.assertRaises(TypeError):
            ensurepip_utils.run_cli("--version")
        self.module.bootstrap.assert_not_called()


class TestBootstrap(unittest.TestCase):
    """Verify the helper that installs the bundled pip."""

    def setUp(self):
        patcher = patch("ensurepip_utils._ensurepip")
        self.module = patcher.start()
        self.addCleanup(patcher.stop)
        self.module.version.return_value = "24.0"

    def test_the_options_are_handed_to_the_standard_library(self):
        ensurepip_utils.bootstrap()
        self.module.bootstrap.assert_called_once_with(
            root=None,
            upgrade=False,
            user=False,
            altinstall=False,
            default_pip=False,
            verbosity=0,
        )

    def test_the_options_are_handed_over_as_given(self):
        ensurepip_utils.bootstrap(
            root="/tmp/root",
            upgrade=True,
            user=True,
            altinstall=True,
            default_pip=True,
            verbosity=2,
        )
        self.module.bootstrap.assert_called_once_with(
            root="/tmp/root",
            upgrade=True,
            user=True,
            altinstall=True,
            default_pip=True,
            verbosity=2,
        )

    def test_the_record_holds_the_installation(self):
        result = ensurepip_utils.bootstrap(root="/tmp/root", upgrade=True, verbosity=1)
        self.assertEqual(result.pip_version, "24.0")
        self.assertEqual(result.root, "/tmp/root")
        self.assertTrue(result.upgrade)
        self.assertFalse(result.user)
        self.assertFalse(result.altinstall)
        self.assertFalse(result.default_pip)
        self.assertEqual(result.verbosity, 1)

    def test_the_record_holds_the_running_environment(self):
        result = ensurepip_utils.bootstrap()
        self.assertIsNone(result.root)

    def test_a_path_is_accepted_as_the_root(self):
        import pathlib

        ensurepip_utils.bootstrap(root=pathlib.Path("/tmp/root"))
        self.module.bootstrap.assert_called_once_with(
            root="/tmp/root",
            upgrade=False,
            user=False,
            altinstall=False,
            default_pip=False,
            verbosity=0,
        )


class TestCommandLine(unittest.TestCase):
    """Verify the command line interface of the wrapper."""

    def setUp(self):
        patcher = patch("ensurepip_utils._ensurepip")
        self.module = patcher.start()
        self.addCleanup(patcher.stop)
        self.module.version.return_value = "24.0"

    def test_the_version_is_reported(self):
        output = io.StringIO()
        with redirect_stdout(output):
            code = ensurepip_utils.run_cli(["--version"])
        self.assertEqual(code, 0)
        self.assertIn("24.0", output.getvalue())
        self.module.bootstrap.assert_not_called()

    def test_an_unknown_option_is_reported(self):
        errors = io.StringIO()
        with redirect_stderr(errors):
            code = ensurepip_utils.run_cli(["--unknown"])
        self.assertEqual(code, 2)
        self.assertTrue(errors.getvalue())
        self.module.bootstrap.assert_not_called()

    def test_the_options_are_handed_to_the_standard_library(self):
        code = ensurepip_utils.run_cli(["--upgrade", "--user", "--altinstall", "-v"])
        self.assertEqual(code, 0)
        self.module.bootstrap.assert_called_once_with(
            root=None,
            upgrade=True,
            user=True,
            altinstall=True,
            default_pip=False,
            verbosity=1,
        )

    def test_the_root_is_handed_to_the_standard_library(self):
        code = ensurepip_utils.run_cli(["--root", "/tmp/root", "--default-pip"])
        self.assertEqual(code, 0)
        self.module.bootstrap.assert_called_once_with(
            root="/tmp/root",
            upgrade=False,
            user=False,
            altinstall=False,
            default_pip=True,
            verbosity=0,
        )


class TestDegradation(unittest.TestCase):
    """Verify the behaviour on an interpreter that removed the package."""

    def setUp(self):
        patcher = patch("ensurepip_utils._ensurepip", None)
        patcher.start()
        self.addCleanup(patcher.stop)

    def test_the_helpers_report_the_missing_package(self):
        with self.assertRaises(RuntimeError):
            ensurepip_utils.pip_version()
        with self.assertRaises(RuntimeError):
            ensurepip_utils.bundled_wheel()
        with self.assertRaises(RuntimeError):
            ensurepip_utils.bootstrap()
        with self.assertRaises(RuntimeError):
            ensurepip_utils.run_cli([])

    def test_the_presence_of_pip_is_still_reported(self):
        self.assertIsInstance(ensurepip_utils.is_pip_installed(), bool)


if __name__ == "__main__":
    unittest.main()
