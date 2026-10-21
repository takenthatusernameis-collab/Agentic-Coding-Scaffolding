"""Tests for venv_utils."""

import contextlib
import io
import os
import sys
import tempfile
import unittest
import venv
from typing import Any, Dict

import venv_utils
from venv_utils import (
    EnvBuilder,
    activation_scripts,
    create_environment,
    describe_environment,
    environment_paths,
    environment_python,
    find_environments,
    is_environment,
    read_configuration,
    run_cli,
)


class ModuleTestCase(unittest.TestCase):
    """Provide a temporary directory for the tests that need one."""

    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = self.temporary.name

    def write_configuration(self, directory: str, body: str) -> str:
        """Write a configuration file into a directory and return the directory."""
        os.makedirs(directory, exist_ok=True)
        with open(os.path.join(directory, "pyvenv.cfg"), "w", encoding="utf-8") as stream:
            stream.write(body)
        return directory

    def create(self, name: str = "demo", **kwargs: Any) -> Dict[str, Any]:
        """Create an environment in the temporary directory and return its report."""
        return create_environment(os.path.join(self.root, name), **kwargs)


class TestModuleContract(unittest.TestCase):
    """Verify the contract of the module."""

    def test_all_is_sorted_and_unique(self):
        self.assertEqual(venv_utils.__all__, sorted(set(venv_utils.__all__)))

    def test_every_name_exists(self):
        for name in venv_utils.__all__:
            self.assertTrue(hasattr(venv_utils, name), name)

    def test_the_module_reexports_the_builder_of_the_standard_library(self):
        self.assertIs(EnvBuilder, venv.EnvBuilder)


class TestConfiguration(ModuleTestCase):
    """Verify the helpers that read the configuration of an environment."""

    def test_is_environment_reports_an_environment(self):
        directory = self.write_configuration(
            os.path.join(self.root, "env"), "home = /usr/bin\nversion = 3.12.3\n"
        )
        self.assertTrue(is_environment(directory))

    def test_is_environment_reports_a_plain_directory(self):
        self.assertFalse(is_environment(self.root))

    def test_is_environment_rejects_a_bad_directory(self):
        with self.assertRaises(TypeError):
            is_environment(42)
        with self.assertRaises(ValueError):
            is_environment("")

    def test_read_configuration_returns_the_settings(self):
        directory = self.write_configuration(
            os.path.join(self.root, "env"),
            "home = /usr/bin\ninclude-system-site-packages = false\nversion = 3.12.3\n",
        )
        configuration = read_configuration(directory)
        self.assertEqual(configuration["home"], "/usr/bin")
        self.assertEqual(configuration["include-system-site-packages"], "false")
        self.assertEqual(configuration["version"], "3.12.3")

    def test_read_configuration_strips_the_quotes_of_the_prompt(self):
        directory = self.write_configuration(os.path.join(self.root, "env"), "prompt = 'my env'\n")
        self.assertEqual(read_configuration(directory)["prompt"], "my env")

    def test_read_configuration_ignores_comments_and_blank_lines(self):
        directory = self.write_configuration(
            os.path.join(self.root, "env"), "# a comment\n\nhome = /usr/bin\n"
        )
        self.assertEqual(read_configuration(directory), {"home": "/usr/bin"})

    def test_read_configuration_ignores_a_line_without_a_setting(self):
        directory = self.write_configuration(
            os.path.join(self.root, "env"), "home = /usr/bin\nnonsense\n"
        )
        self.assertEqual(read_configuration(directory), {"home": "/usr/bin"})

    def test_read_configuration_rejects_a_plain_directory(self):
        with self.assertRaises(ValueError):
            read_configuration(self.root)

    def test_read_configuration_rejects_a_bad_directory(self):
        with self.assertRaises(TypeError):
            read_configuration(42)
        with self.assertRaises(ValueError):
            read_configuration("")


class TestPaths(ModuleTestCase):
    """Verify the helpers that report the directories of an environment."""

    def test_environment_paths_holds_the_directories_of_the_standard_library(self):
        paths = environment_paths(os.path.join(self.root, "env"))
        self.assertIn("scripts", paths)
        self.assertIn("purelib", paths)
        self.assertIn("include", paths)
        for path in paths.values():
            self.assertTrue(path.startswith(self.root))

    def test_environment_paths_places_the_scripts_inside_the_environment(self):
        paths = environment_paths(os.path.join(self.root, "env"))
        self.assertTrue(paths["scripts"].startswith(os.path.join(self.root, "env")))

    def test_environment_paths_rejects_a_bad_directory(self):
        with self.assertRaises(TypeError):
            environment_paths(42)
        with self.assertRaises(ValueError):
            environment_paths("")

    def test_environment_python_finds_the_interpreter_of_an_environment(self):
        report = self.create()
        python = environment_python(report["directory"])
        self.assertTrue(os.path.exists(python))
        self.assertIn("python", os.path.basename(python))

    def test_environment_python_falls_back_to_a_path_for_a_missing_interpreter(self):
        python = environment_python(os.path.join(self.root, "nowhere"))
        self.assertTrue(python.startswith(self.root))
        self.assertFalse(os.path.exists(python))

    def test_activation_scripts_lists_the_scripts_of_an_environment(self):
        report = self.create()
        scripts = activation_scripts(report["directory"])
        self.assertTrue(scripts)
        for script in scripts:
            self.assertTrue(os.path.exists(script))

    def test_activation_scripts_is_empty_for_a_plain_directory(self):
        self.assertEqual(activation_scripts(self.root), [])

    def test_activation_scripts_rejects_a_bad_directory(self):
        with self.assertRaises(TypeError):
            activation_scripts(42)


class TestCreation(ModuleTestCase):
    """Verify the helper that creates a virtual environment."""

    def test_create_environment_creates_the_environment(self):
        report = self.create()
        self.assertTrue(os.path.isdir(report["directory"]))
        self.assertTrue(is_environment(report["directory"]))

    def test_create_environment_describes_the_environment(self):
        report = self.create()
        self.assertEqual(report["directory"], os.path.join(self.root, "demo"))
        self.assertIn("configuration", report)
        self.assertIn("paths", report)
        self.assertIn("python", report)

    def test_create_environment_records_the_version_of_the_interpreter(self):
        report = self.create()
        version = report["configuration"]["version"]
        self.assertEqual(version, ".".join(str(part) for part in sys.version_info[:3]))

    def test_create_environment_hides_the_packages_of_the_system(self):
        report = self.create()
        self.assertEqual(report["configuration"]["include-system-site-packages"], "false")

    def test_create_environment_can_show_the_packages_of_the_system(self):
        report = self.create(name="shared", system_site_packages=True)
        self.assertEqual(report["configuration"]["include-system-site-packages"], "true")

    def test_create_environment_records_the_prompt(self):
        report = self.create(prompt="my env")
        self.assertEqual(report["configuration"]["prompt"], "my env")

    def test_create_environment_names_the_prompt_after_the_directory(self):
        report = self.create(name="named")
        self.assertNotIn("prompt", report["configuration"])

    def test_create_environment_creates_the_directories_of_the_environment(self):
        report = self.create()
        for name in ("scripts", "purelib", "include"):
            self.assertTrue(os.path.isdir(report["paths"][name]), name)

    def test_create_environment_records_the_command_that_created_it(self):
        report = self.create()
        command = report["configuration"]["command"]
        self.assertIn("-m venv", command)
        self.assertIn(report["directory"], command)

    def test_create_environment_creates_an_interpreter(self):
        report = self.create()
        python = report["python"]
        self.assertTrue(os.path.exists(python))
        self.assertTrue(os.access(python, os.X_OK))

    def test_create_environment_clears_the_directory_when_asked(self):
        target = os.path.join(self.root, "old")
        os.makedirs(target)
        with open(os.path.join(target, "leftover.txt"), "w", encoding="utf-8") as stream:
            stream.write("left over")
        create_environment(target, clear=True)
        self.assertFalse(os.path.exists(os.path.join(target, "leftover.txt")))

    def test_create_environment_keeps_the_directory_when_not_clearing(self):
        target = os.path.join(self.root, "old")
        os.makedirs(target)
        with open(os.path.join(target, "leftover.txt"), "w", encoding="utf-8") as stream:
            stream.write("left over")
        create_environment(target)
        self.assertTrue(os.path.exists(os.path.join(target, "leftover.txt")))

    def test_create_environment_rejects_a_bad_directory(self):
        with self.assertRaises(TypeError):
            create_environment(42)
        with self.assertRaises(ValueError):
            create_environment("")

    def test_create_environment_rejects_a_bad_flag(self):
        with self.assertRaises(TypeError):
            create_environment(os.path.join(self.root, "demo"), with_pip="yes")
        with self.assertRaises(TypeError):
            create_environment(os.path.join(self.root, "demo"), clear=1)
        with self.assertRaises(TypeError):
            create_environment(os.path.join(self.root, "demo"), upgrade="yes")
        with self.assertRaises(TypeError):
            create_environment(os.path.join(self.root, "demo"), system_site_packages="yes")

    def test_create_environment_rejects_a_bad_symlink_flag(self):
        with self.assertRaises(TypeError):
            create_environment(os.path.join(self.root, "demo"), symlinks="yes")

    def test_create_environment_rejects_a_bad_prompt(self):
        with self.assertRaises(TypeError):
            create_environment(os.path.join(self.root, "demo"), prompt=42)
        with self.assertRaises(ValueError):
            create_environment(os.path.join(self.root, "demo"), prompt="  ")


class TestDescription(ModuleTestCase):
    """Verify the helper that describes an existing environment."""

    def test_describe_environment_reports_the_environment(self):
        report = self.create()
        described = describe_environment(report["directory"])
        self.assertEqual(described["directory"], report["directory"])
        self.assertEqual(described["configuration"], report["configuration"])
        self.assertEqual(described["paths"], report["paths"])

    def test_describe_environment_rejects_a_plain_directory(self):
        with self.assertRaises(ValueError):
            describe_environment(self.root)

    def test_describe_environment_rejects_a_bad_directory(self):
        with self.assertRaises(TypeError):
            describe_environment(42)


class TestDiscovery(ModuleTestCase):
    """Verify the helper that finds the environments of a directory tree."""

    def test_find_environments_finds_an_environment(self):
        report = self.create()
        self.assertEqual(find_environments(self.root), [report["directory"]])

    def test_find_environments_finds_the_environments_of_a_tree(self):
        first = self.create(name="first")
        second = self.create(name="second")
        found = find_environments(self.root)
        self.assertEqual(found, sorted([first["directory"], second["directory"]]))

    def test_find_environments_reports_the_root_itself(self):
        report = self.create()
        self.assertEqual(find_environments(report["directory"]), [report["directory"]])

    def test_find_environments_respects_the_depth(self):
        nested = os.path.join(self.root, "one", "two")
        report = create_environment(nested)
        self.assertEqual(find_environments(self.root, max_depth=1), [])
        self.assertEqual(find_environments(self.root, max_depth=2), [report["directory"]])

    def test_find_environments_is_empty_for_a_plain_tree(self):
        self.assertEqual(find_environments(self.root), [])

    def test_find_environments_rejects_a_bad_depth(self):
        with self.assertRaises(TypeError):
            find_environments(self.root, max_depth="deep")
        with self.assertRaises(ValueError):
            find_environments(self.root, max_depth=-1)

    def test_find_environments_rejects_a_bad_root(self):
        with self.assertRaises(TypeError):
            find_environments(42)


class TestCommandLine(ModuleTestCase):
    """Verify the helper that runs the command line interface of the standard library."""

    def test_run_cli_creates_an_environment(self):
        target = os.path.join(self.root, "cli")
        self.assertEqual(run_cli(["--without-pip", target]), 0)
        self.assertTrue(is_environment(target))

    def test_run_cli_reports_a_bad_argument(self):
        stream = io.StringIO()
        with contextlib.redirect_stderr(stream):
            code = run_cli(["--nowhere"])
        self.assertNotEqual(code, 0)

    def test_run_cli_rejects_a_bad_argument_list(self):
        with self.assertRaises(TypeError):
            run_cli("--nowhere")
        with self.assertRaises(TypeError):
            run_cli([42])


class TestStandardLibrary(unittest.TestCase):
    """Verify that the wrapper agrees with the standard library."""

    def test_the_builder_of_the_standard_library_is_reexported(self):
        self.assertIs(venv_utils.EnvBuilder, venv.EnvBuilder)

    def test_the_wrapper_uses_the_builder_of_the_standard_library(self):
        self.assertTrue(issubclass(venv_utils.EnvBuilder, venv.EnvBuilder))


if __name__ == "__main__":
    unittest.main()
