"""Tests for site_utils."""

import os
import site
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

import site_utils
from site_utils import (
    add_site_dir,
    add_site_packages,
    add_user_site_packages,
    check_enable_user_site,
    get_enable_user_site,
    get_site_packages,
    get_site_prefixes,
    get_user_base,
    get_user_site_packages,
    is_user_site_enabled,
    make_path,
    remove_duplicate_paths,
)


class TestModuleContract(unittest.TestCase):
    """Verify the contract of the module."""

    def test_all_is_sorted_and_unique(self):
        self.assertEqual(site_utils.__all__, sorted(set(site_utils.__all__)))

    def test_every_name_exists(self):
        for name in site_utils.__all__:
            self.assertTrue(hasattr(site_utils, name), name)

    def test_the_helpers_read_the_standard_library(self):
        self.assertEqual(get_site_packages(), list(site.getsitepackages()))
        self.assertEqual(get_site_prefixes(), list(site.PREFIXES))
        self.assertEqual(get_user_base(), site.getuserbase())
        self.assertEqual(get_user_site_packages(), site.getusersitepackages())
        self.assertEqual(get_enable_user_site(), site.ENABLE_USER_SITE)
        self.assertEqual(is_user_site_enabled(), bool(site.ENABLE_USER_SITE))
        self.assertEqual(check_enable_user_site(), site.check_enableusersite())


class TestSitePackages(unittest.TestCase):
    """Verify the helpers that report the global site directories."""

    def test_get_site_packages_matches_the_standard_library(self):
        self.assertEqual(get_site_packages(), list(site.getsitepackages()))

    def test_get_site_packages_accepts_prefixes(self):
        self.assertEqual(get_site_packages(["/nowhere"]), list(site.getsitepackages(["/nowhere"])))

    def test_get_site_packages_rejects_a_single_string(self):
        with self.assertRaises(TypeError):
            get_site_packages("/nowhere")

    def test_get_site_packages_rejects_a_bad_container(self):
        with self.assertRaises(TypeError):
            get_site_packages(42)

    def test_get_site_packages_rejects_a_bad_entry(self):
        with self.assertRaises(TypeError):
            get_site_packages([42])

    def test_get_site_prefixes_matches_the_standard_library(self):
        self.assertEqual(get_site_prefixes(), list(site.PREFIXES))


class TestUserSite(unittest.TestCase):
    """Verify the helpers that report the settings of the user site."""

    def test_get_user_base_matches_the_standard_library(self):
        self.assertEqual(get_user_base(), site.getuserbase())

    def test_get_user_site_packages_matches_the_standard_library(self):
        self.assertEqual(get_user_site_packages(), site.getusersitepackages())

    def test_get_enable_user_site_matches_the_standard_library(self):
        self.assertEqual(get_enable_user_site(), site.ENABLE_USER_SITE)

    def test_is_user_site_enabled_matches_the_standard_library(self):
        self.assertEqual(is_user_site_enabled(), bool(site.ENABLE_USER_SITE))

    def test_check_enable_user_site_matches_the_standard_library(self):
        self.assertEqual(check_enable_user_site(), site.check_enableusersite())

    def test_check_enable_user_site_reports_a_state(self):
        self.assertIn(check_enable_user_site(), (True, False, None))


class TestPathHelpers(unittest.TestCase):
    """Verify the helpers that work on the paths of the search path."""

    def test_make_path_joins_the_segments(self):
        expected = os.path.join(os.getcwd(), "alpha", "beta")
        self.assertEqual(make_path("alpha", "beta"), (expected, os.path.normcase(expected)))

    def test_make_path_accepts_a_single_segment(self):
        expected = os.path.abspath("alpha")
        self.assertEqual(make_path("alpha"), (expected, os.path.normcase(expected)))

    def test_make_path_rejects_a_bad_segment(self):
        with self.assertRaises(TypeError):
            make_path("alpha", 42)

    def test_make_path_rejects_an_empty_call(self):
        with self.assertRaises(ValueError):
            make_path()

    def test_remove_duplicate_paths_removes_the_duplicates(self):
        with mock.patch.object(sys, "path", ["/one", "/two", "/one"]):
            known = remove_duplicate_paths()
            self.assertEqual(sys.path, ["/one", "/two"])
        self.assertIn(os.path.normcase("/one"), known)
        self.assertIn(os.path.normcase("/two"), known)

    def test_remove_duplicate_paths_forwards_to_the_standard_library(self):
        with mock.patch.object(
            site_utils._site, "removeduppaths", return_value={"/one"}
        ) as patched:
            self.assertEqual(remove_duplicate_paths(), {"/one"})
            patched.assert_called_once_with()


class TestSearchPath(unittest.TestCase):
    """Verify the helpers that add directories to the search path."""

    def test_add_site_dir_adds_the_directory(self):
        with tempfile.TemporaryDirectory() as directory:
            with mock.patch.object(sys, "path", []):
                known = set()
                result = add_site_dir(directory, known)
                self.assertIs(result, known)
                self.assertIn(os.path.normcase(os.path.abspath(directory)), known)
                self.assertIn(os.path.abspath(directory), sys.path)

    def test_add_site_dir_processes_the_pth_files(self):
        with tempfile.TemporaryDirectory() as directory:
            Path(directory, "extra.pth").write_text("import sys\n")
            with mock.patch.object(sys, "path", []):
                known = set()
                add_site_dir(directory, known)
            self.assertIn(os.path.normcase(os.path.abspath(directory)), known)

    def test_add_site_dir_derives_the_known_paths_from_the_process(self):
        with tempfile.TemporaryDirectory() as directory:
            with mock.patch.object(sys, "path", []):
                result = add_site_dir(directory)
                self.assertIsNone(result)
                self.assertIn(os.path.abspath(directory), sys.path)

    def test_add_site_dir_rejects_a_bad_directory(self):
        with self.assertRaises(TypeError):
            add_site_dir(42, set())

    def test_add_site_dir_rejects_an_empty_directory(self):
        with self.assertRaises(ValueError):
            add_site_dir("", set())

    def test_add_site_dir_rejects_a_bad_known_paths(self):
        with self.assertRaises(TypeError):
            add_site_dir("/nowhere", "not a set")
        with self.assertRaises(TypeError):
            add_site_dir("/nowhere", {42})

    def test_add_site_packages_adds_the_global_directories(self):
        with mock.patch.object(sys, "path", []):
            known = set()
            result = add_site_packages(known)
            self.assertIs(result, known)
            for directory in get_site_packages():
                if os.path.isdir(directory):
                    self.assertIn(os.path.normcase(os.path.abspath(directory)), result)

    def test_add_site_packages_accepts_prefixes(self):
        with mock.patch.object(sys, "path", []):
            known = set()
            add_site_packages(known, ["/nowhere"])
        self.assertEqual(known, set())

    def test_add_site_packages_rejects_a_bad_known_paths(self):
        with self.assertRaises(TypeError):
            add_site_packages("not a set")

    def test_add_site_packages_rejects_a_bad_prefix(self):
        with self.assertRaises(TypeError):
            add_site_packages(set(), "/nowhere")

    def test_add_user_site_packages_reports_the_known_paths(self):
        with mock.patch.object(sys, "path", []):
            known = set()
            result = add_user_site_packages(known)
            self.assertIs(result, known)
            user_site = get_user_site_packages()
            if is_user_site_enabled() and user_site and os.path.isdir(user_site):
                self.assertIn(os.path.normcase(user_site), result)

    def test_add_user_site_packages_rejects_a_bad_known_paths(self):
        with self.assertRaises(TypeError):
            add_user_site_packages("not a set")


if __name__ == "__main__":
    unittest.main()
