"""Tests for configparser_utils."""

import os
import tempfile
import unittest

from configparser_utils import (
    DEFAULTSECT,
    BasicInterpolation,
    ConfigParser,
    Error,
    ExtendedInterpolation,
    NoOptionError,
    NoSectionError,
    ParsingError,
    RawConfigParser,
    get_options,
    get_sections,
    load_config,
    read_files,
    save_config,
    write_config,
)


class TestLoadSave(unittest.TestCase):
    def test_load_config_basic(self):
        with tempfile.TemporaryDirectory() as d:
            path = os.path.join(d, "test.ini")
            with open(path, "w", encoding="utf-8") as f:
                f.write("[section1]\nkey1 = value1\nkey2 = value2\n\n[section2]\nkey3 = value3\n")
            config = load_config(path)
            self.assertIn("section1", config)
            self.assertEqual(config["section1"]["key1"], "value1")
            self.assertEqual(config["section1"]["key2"], "value2")
            self.assertIn("section2", config)
            self.assertEqual(config["section2"]["key3"], "value3")

    def test_load_config_file_not_found(self):
        with self.assertRaises(FileNotFoundError):
            load_config("/nonexistent/file.ini")

    def test_load_config_type_error(self):
        with self.assertRaises(TypeError):
            load_config(123)  # type: ignore[arg-type]

    def test_save_config_basic(self):
        with tempfile.TemporaryDirectory() as d:
            path = os.path.join(d, "test.ini")
            config = {"section1": {"key1": "value1", "key2": 42}, "section2": {"key3": "value3"}}
            save_config(config, path)
            self.assertTrue(os.path.exists(path))
            loaded = load_config(path)
            self.assertEqual(loaded["section1"]["key1"], "value1")
            self.assertEqual(loaded["section1"]["key2"], "42")

    def test_save_config_type_error_config(self):
        with self.assertRaises(TypeError):
            save_config("not_a_dict", "path.ini")  # type: ignore[arg-type]

    def test_save_config_type_error_section(self):
        with self.assertRaises(TypeError):
            save_config({"section": "not_a_dict"}, "path.ini")  # type: ignore[arg-type]

    def test_save_config_type_error_path(self):
        with self.assertRaises(TypeError):
            save_config({}, 123)  # type: ignore[arg-type]


class TestParserHelpers(unittest.TestCase):
    def test_get_sections(self):
        parser = ConfigParser()
        parser.add_section("sec1")
        parser.add_section("sec2")
        sections = get_sections(parser)
        self.assertIn("sec1", sections)
        self.assertIn("sec2", sections)

    def test_get_sections_type_error(self):
        with self.assertRaises(TypeError):
            get_sections("not_parser")  # type: ignore[arg-type]

    def test_get_options(self):
        parser = ConfigParser()
        parser.add_section("sec1")
        parser.set("sec1", "opt1", "val1")
        parser.set("sec1", "opt2", "val2")
        options = get_options(parser, "sec1")
        self.assertIn("opt1", options)
        self.assertIn("opt2", options)

    def test_get_options_type_error(self):
        with self.assertRaises(TypeError):
            get_options("not_parser", "sec1")  # type: ignore[arg-type]


class TestFileOperations(unittest.TestCase):
    def test_read_files(self):
        with tempfile.TemporaryDirectory() as d:
            path1 = os.path.join(d, "test1.ini")
            path2 = os.path.join(d, "test2.ini")
            with open(path1, "w", encoding="utf-8") as f:
                f.write("[sec1]\na=1\n")
            with open(path2, "w", encoding="utf-8") as f:
                f.write("[sec2]\nb=2\n")
            result = read_files([path1, path2])
            self.assertTrue(any(os.path.basename(r) == "test1.ini" for r in result))
            self.assertTrue(any(os.path.basename(r) == "test2.ini" for r in result))

    def test_write_config(self):
        with tempfile.TemporaryDirectory() as d:
            path = os.path.join(d, "output.ini")
            parser = ConfigParser()
            parser.add_section("test")
            parser.set("test", "key", "value")
            write_config(parser, path)
            self.assertTrue(os.path.exists(path))
            loaded = load_config(path)
            self.assertEqual(loaded["test"]["key"], "value")

    def test_write_config_type_error(self):
        with self.assertRaises(TypeError):
            write_config("not_parser", "path.ini")  # type: ignore[arg-type]


class TestExports(unittest.TestCase):
    def test_classes_and_constants_exist(self):
        self.assertIsNotNone(ConfigParser)
        self.assertIsNotNone(RawConfigParser)
        self.assertIsNotNone(BasicInterpolation)
        self.assertIsNotNone(ExtendedInterpolation)
        self.assertEqual(DEFAULTSECT, "DEFAULT")


class TestExceptions(unittest.TestCase):
    def test_exceptions_exist(self):
        self.assertTrue(issubclass(Error, Exception))
        self.assertTrue(issubclass(NoSectionError, Error))
        self.assertTrue(issubclass(NoOptionError, Error))
        self.assertTrue(issubclass(ParsingError, Error))


if __name__ == "__main__":
    unittest.main()
