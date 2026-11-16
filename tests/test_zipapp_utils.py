"""Tests for zipapp utility functions."""

import os
import tempfile
import zipfile
from unittest import TestCase

import zipapp_utils


class TestZipappUtils(TestCase):
    def test_zipapp_error_exists(self):
        self.assertTrue(hasattr(zipapp_utils, "ZipAppError"))
        self.assertTrue(issubclass(zipapp_utils.ZipAppError, Exception))

    def test_create_archive_and_get_interpreter(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create a simple source directory
            src = os.path.join(tmpdir, "src")
            os.makedirs(src)
            with open(os.path.join(src, "__main__.py"), "w") as f:
                f.write("print('hello')\n")

            target = os.path.join(tmpdir, "app.pyz")
            zipapp_utils.create_archive(src, target)
            self.assertTrue(os.path.exists(target))

            # Get interpreter
            interp = zipapp_utils.get_interpreter(target)
            # Should return something like sys.executable or None depending
            self.assertIsInstance(interp, (str, type(None)))

    def test_create_zipapp_alias(self):
        self.assertEqual(zipapp_utils.create_zipapp, zipapp_utils.create_archive)

    def test_get_zipapp_interpreter_alias(self):
        self.assertEqual(zipapp_utils.get_zipapp_interpreter, zipapp_utils.get_interpreter)

    def test_is_zipapp_archive(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create a zipapp
            src = os.path.join(tmpdir, "src")
            os.makedirs(src)
            with open(os.path.join(src, "__main__.py"), "w") as f:
                f.write("print('hi')\n")
            target = os.path.join(tmpdir, "app.pyz")
            zipapp_utils.create_archive(src, target)
            self.assertTrue(zipapp_utils.is_zipapp_archive(target))

            # Create a regular zip
            zpath = os.path.join(tmpdir, "notapp.zip")
            with zipfile.ZipFile(zpath, "w") as z:
                z.writestr("test.txt", "hello")
            self.assertTrue(zipapp_utils.is_zipapp_archive(zpath))

            # Create a regular file
            fpath = os.path.join(tmpdir, "test.txt")
            with open(fpath, "w") as f:
                f.write("hello")
            self.assertFalse(zipapp_utils.is_zipapp_archive(fpath))

    def test_is_zipapp_archive_rejects_shebang_script(self):
        # A plain script that merely starts with a ``#!`` line is not a zipapp
        # archive: only the shebang is present, no ZIP content follows it.
        with tempfile.TemporaryDirectory() as tmpdir:
            script = os.path.join(tmpdir, "plain.py")
            with open(script, "w") as f:
                f.write("#!/usr/bin/env python\nprint('hi')\n")
            self.assertFalse(zipapp_utils.is_zipapp_archive(script))

    def test_is_zipapp_archive_accepts_shebang_zipapp(self):
        # A real zipapp with an interpreter line starts with ``#!`` and only
        # then holds the ZIP archive, so it is still detected.
        with tempfile.TemporaryDirectory() as tmpdir:
            src = os.path.join(tmpdir, "src")
            os.makedirs(src)
            with open(os.path.join(src, "__main__.py"), "w") as f:
                f.write("print('hi')\n")
            target = os.path.join(tmpdir, "app.pyz")
            zipapp_utils.create_archive(
                src, target, interpreter="/usr/bin/env python"
            )
            with open(target, "rb") as f:
                self.assertEqual(f.read(2), b"#!")
            self.assertTrue(zipapp_utils.is_zipapp_archive(target))
