"""Tests for sysconfig_utils module."""

import re
import sysconfig
import unittest

import sysconfig_utils


class TestGetConfigVars(unittest.TestCase):
    """Verify access to the interpreter configuration variables."""

    def test_get_config_vars_returns_mapping(self):
        variables = sysconfig_utils.get_config_vars()
        self.assertIsInstance(variables, dict)
        self.assertTrue(variables)

    def test_get_config_vars_contains_prefix(self):
        variables = sysconfig_utils.get_config_vars()
        self.assertIn("prefix", variables)
        self.assertIn("exec_prefix", variables)

    def test_get_config_vars_returns_a_copy(self):
        variables = sysconfig_utils.get_config_vars()
        variables["prefix"] = "/mutated"
        self.assertNotEqual(sysconfig_utils.get_config_vars()["prefix"], "/mutated")

    def test_get_config_var_of_known_name(self):
        self.assertEqual(
            sysconfig_utils.get_config_var("prefix"),
            sysconfig.get_config_var("prefix"),
        )

    def test_get_config_var_of_unknown_name(self):
        self.assertIsNone(sysconfig_utils.get_config_var("definitely-not-a-variable"))

    def test_get_config_var_requires_string(self):
        with self.assertRaises(TypeError):
            sysconfig_utils.get_config_var(1)  # type: ignore[arg-type]

    def test_has_config_var(self):
        self.assertTrue(sysconfig_utils.has_config_var("prefix"))
        self.assertFalse(sysconfig_utils.has_config_var("definitely-not-a-variable"))

    def test_has_config_var_requires_string(self):
        with self.assertRaises(TypeError):
            sysconfig_utils.has_config_var(None)  # type: ignore[arg-type]

    def test_list_config_var_names(self):
        names = sysconfig_utils.list_config_var_names()
        self.assertIsInstance(names, list)
        self.assertIn("prefix", names)
        self.assertEqual(names, sorted(names))

    def test_list_config_var_names_matches_config_vars(self):
        self.assertEqual(
            sysconfig_utils.list_config_var_names(),
            sorted(sysconfig_utils.get_config_vars()),
        )


class TestGetPaths(unittest.TestCase):
    """Verify access to the interpreter installation paths."""

    def test_get_paths_returns_mapping(self):
        paths = sysconfig_utils.get_paths()
        self.assertIsInstance(paths, dict)
        self.assertTrue(paths)

    def test_get_paths_contains_known_names(self):
        paths = sysconfig_utils.get_paths()
        for name in ("stdlib", "platstdlib", "purelib", "platlib", "include", "scripts"):
            self.assertIn(name, paths)

    def test_get_paths_without_expansion_keeps_placeholders(self):
        paths = sysconfig_utils.get_paths(expand=False)
        self.assertTrue(any("{" in value for value in paths.values()))

    def test_get_paths_with_expansion_resolves_placeholders(self):
        paths = sysconfig_utils.get_paths(expand=True)
        self.assertFalse(any("{" in value for value in paths.values()))

    def test_get_paths_supports_every_scheme(self):
        for scheme in sysconfig_utils.get_scheme_names():
            with self.subTest(scheme=scheme):
                paths = sysconfig_utils.get_paths(scheme=scheme)
                self.assertIn("purelib", paths)

    def test_get_paths_rejects_unknown_scheme(self):
        with self.assertRaises(KeyError):
            sysconfig_utils.get_paths(scheme="definitely-not-a-scheme")

    def test_get_paths_rejects_bad_types(self):
        with self.assertRaises(TypeError):
            sysconfig_utils.get_paths(scheme=1)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            sysconfig_utils.get_paths(vars=["prefix"])  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            sysconfig_utils.get_paths(expand="yes")  # type: ignore[arg-type]


class TestGetPath(unittest.TestCase):
    """Verify lookup of a single installation path."""

    def test_get_path_returns_string(self):
        self.assertIsInstance(sysconfig_utils.get_path("purelib"), str)

    def test_get_path_matches_get_paths(self):
        paths = sysconfig_utils.get_paths()
        self.assertEqual(sysconfig_utils.get_path("purelib"), paths["purelib"])

    def test_get_path_of_unknown_name(self):
        with self.assertRaises(KeyError):
            sysconfig_utils.get_path("definitely-not-a-path")

    def test_get_path_requires_string(self):
        with self.assertRaises(TypeError):
            sysconfig_utils.get_path(None)  # type: ignore[arg-type]

    def test_get_path_rejects_bad_types(self):
        with self.assertRaises(TypeError):
            sysconfig_utils.get_path("purelib", scheme=1)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            sysconfig_utils.get_path("purelib", vars="prefix")  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            sysconfig_utils.get_path("purelib", expand=1)  # type: ignore[arg-type]


class TestInterpreterMetadata(unittest.TestCase):
    """Verify the interpreter metadata helpers."""

    def test_get_platform(self):
        platform = sysconfig_utils.get_platform()
        self.assertIsInstance(platform, str)
        self.assertTrue(platform)

    def test_get_python_version(self):
        version = sysconfig_utils.get_python_version()
        self.assertIsInstance(version, str)
        self.assertTrue(re.fullmatch(r"\d+\.\d+", version))

    def test_get_default_scheme(self):
        scheme = sysconfig_utils.get_default_scheme()
        self.assertIsInstance(scheme, str)
        self.assertIn(scheme, sysconfig_utils.get_scheme_names())

    def test_get_scheme_names(self):
        names = sysconfig_utils.get_scheme_names()
        self.assertIsInstance(names, tuple)
        self.assertTrue(names)
        self.assertIn("posix_prefix", names)

    def test_is_python_build(self):
        self.assertIsInstance(sysconfig_utils.is_python_build(), bool)

    def test_get_config_h_filename(self):
        filename = sysconfig_utils.get_config_h_filename()
        self.assertIsInstance(filename, str)
        self.assertTrue(filename)

    def test_get_makefile_filename(self):
        filename = sysconfig_utils.get_makefile_filename()
        self.assertIsInstance(filename, str)
        self.assertTrue(filename)


class TestGetPreferredScheme(unittest.TestCase):
    """Verify resolution of the preferred installation scheme."""

    def test_get_preferred_scheme_for_installation_types(self):
        for installation_type in ("prefix", "home", "user"):
            with self.subTest(installation_type=installation_type):
                scheme = sysconfig_utils.get_preferred_scheme(installation_type)
                self.assertIsInstance(scheme, str)
                self.assertTrue(scheme)

    def test_get_preferred_scheme_prefix_matches_default(self):
        self.assertEqual(
            sysconfig_utils.get_preferred_scheme("prefix"),
            sysconfig_utils.get_default_scheme(),
        )

    def test_get_preferred_scheme_of_unknown_type(self):
        with self.assertRaises(KeyError):
            sysconfig_utils.get_preferred_scheme("definitely-not-a-type")

    def test_get_preferred_scheme_requires_string(self):
        with self.assertRaises(TypeError):
            sysconfig_utils.get_preferred_scheme(None)  # type: ignore[arg-type]


if __name__ == "__main__":
    unittest.main()
