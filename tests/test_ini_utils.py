import tempfile
import unittest
from pathlib import Path

from ini_utils import (
    get_config_value,
    get_section,
    has_section,
    list_sections,
    load_config,
    merge_configs,
    save_config,
    set_config_value,
)


class TestLoadConfig(unittest.TestCase):
    """Test the load_config function."""

    def test_load_valid_ini(self):
        """Test loading a valid INI configuration file."""
        content = """[database]
host = localhost
port = 5432

[debug]
enabled = true
"""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".ini", delete=False) as f:
            f.write(content)
            temp_path = f.name

        try:
            loaded = load_config(temp_path)
            self.assertEqual(
                loaded,
                {
                    "database": {"host": "localhost", "port": "5432"},
                    "debug": {"enabled": "true"},
                },
            )
        finally:
            Path(temp_path).unlink()

    def test_load_file_not_found(self):
        """Test loading a non-existent file raises FileNotFoundError."""
        with self.assertRaises(FileNotFoundError):
            load_config("/non/existent/file.ini")

    def test_load_with_path_object(self):
        """Test loading works with Path objects."""
        content = "[section]\nkey = value\n"
        with tempfile.NamedTemporaryFile(mode="w", suffix=".ini", delete=False) as f:
            f.write(content)
            temp_path = Path(f.name)

        try:
            loaded = load_config(temp_path)
            self.assertEqual(loaded, {"section": {"key": "value"}})
        finally:
            temp_path.unlink()

    def test_load_ignores_default_section(self):
        """Test that the DEFAULT section is not included in results."""
        content = """[DEFAULT]
host = localhost

[database]
host = 127.0.0.1
port = 5432
"""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".ini", delete=False) as f:
            f.write(content)
            temp_path = f.name

        try:
            loaded = load_config(temp_path)
            self.assertNotIn("DEFAULT", loaded)
            self.assertEqual(loaded["database"]["host"], "127.0.0.1")
        finally:
            Path(temp_path).unlink()


class TestSaveConfig(unittest.TestCase):
    """Test the save_config function."""

    def test_save_and_load_roundtrip(self):
        """Test saving and loading preserves data."""
        original_config = {
            "database": {"host": "localhost", "port": "5432"},
            "debug": {"enabled": "true"},
        }

        with tempfile.NamedTemporaryFile(mode="w", suffix=".ini", delete=False) as f:
            temp_path = f.name

        try:
            save_config(original_config, temp_path)
            loaded_config = load_config(temp_path)
            self.assertEqual(loaded_config, original_config)
        finally:
            Path(temp_path).unlink()

    def test_save_creates_directories(self):
        """Test that save_config creates parent directories if needed."""
        config = {"section": {"key": "value"}}

        with tempfile.TemporaryDirectory() as tmp_dir:
            nested_path = Path(tmp_dir) / "nested" / "deep" / "config.ini"

            self.assertFalse(nested_path.parent.exists())

            save_config(config, nested_path)

            self.assertTrue(nested_path.exists())
            loaded = load_config(nested_path)
            self.assertEqual(loaded, config)

    def test_save_invalid_config_type(self):
        """Test that saving non-dict config raises TypeError."""
        with tempfile.NamedTemporaryFile(suffix=".ini", delete=False) as f:
            temp_path = f.name

        try:
            with self.assertRaises(TypeError):
                save_config(["not", "a", "dict"], temp_path)
        finally:
            Path(temp_path).unlink()

    def test_save_invalid_section_type(self):
        """Test that saving a section with non-dict values raises TypeError."""
        with tempfile.NamedTemporaryFile(suffix=".ini", delete=False) as f:
            temp_path = f.name

        try:
            with self.assertRaises(TypeError):
                save_config({"section": ["not", "a", "dict"]}, temp_path)
        finally:
            Path(temp_path).unlink()


class TestGetConfigValue(unittest.TestCase):
    """Test the get_config_value function."""

    def setUp(self):
        """Set up test configuration."""
        self.config = {
            "database": {"host": "localhost", "port": "5432"},
            "debug": {"enabled": "true"},
        }

    def test_get_existing_value(self):
        """Test getting an existing configuration value."""
        self.assertEqual(get_config_value(self.config, "database.host"), "localhost")
        self.assertEqual(get_config_value(self.config, "database.port"), "5432")
        self.assertEqual(get_config_value(self.config, "debug.enabled"), "true")

    def test_get_missing_key_returns_default(self):
        """Test that missing keys return the default value."""
        self.assertIsNone(get_config_value(self.config, "database.hostname"))
        self.assertEqual(
            get_config_value(self.config, "database.hostname", "default"), "default"
        )

    def test_get_missing_section_returns_default(self):
        """Test that missing sections return the default value."""
        self.assertIsNone(get_config_value(self.config, "missing.host"))
        self.assertEqual(
            get_config_value(self.config, "missing.host", "default"), "default"
        )

    def test_get_with_non_dict_config(self):
        """Test getting value from non-dict config returns default."""
        self.assertEqual(get_config_value("not a dict", "section.key", "default"), "default")
        self.assertIsNone(get_config_value([], "section.key"))

    def test_get_with_invalid_key_path(self):
        """Test that malformed key paths return the default value."""
        self.assertIsNone(get_config_value(self.config, "noseparator"))
        self.assertIsNone(get_config_value(self.config, "a.b.c"))


class TestSetConfigValue(unittest.TestCase):
    """Test the set_config_value function."""

    def test_set_new_section_and_key(self):
        """Test setting a value in a new section."""
        config = {}
        set_config_value(config, "database.host", "localhost")
        self.assertEqual(config, {"database": {"host": "localhost"}})

    def test_set_overwrites_existing(self):
        """Test that setting overwrites existing values."""
        config = {"database": {"host": "localhost"}}
        set_config_value(config, "database.host", "127.0.0.1")
        self.assertEqual(config["database"]["host"], "127.0.0.1")

    def test_set_adds_key_to_existing_section(self):
        """Test adding a key to an existing section."""
        config = {"database": {"host": "localhost"}}
        set_config_value(config, "database.port", "5432")
        self.assertEqual(config, {"database": {"host": "localhost", "port": "5432"}})

    def test_set_invalid_config_type(self):
        """Test that setting value in non-dict config raises TypeError."""
        with self.assertRaises(TypeError):
            set_config_value(["not", "a", "dict"], "section.key", "value")

    def test_set_invalid_key_path(self):
        """Test that malformed key paths raise ValueError."""
        with self.assertRaises(ValueError):
            set_config_value({}, "noseparator", "value")
        with self.assertRaises(ValueError):
            set_config_value({}, "a.b.c", "value")


class TestMergeConfigs(unittest.TestCase):
    """Test the merge_configs function."""

    def test_merge_simple_dicts(self):
        """Test merging simple configurations."""
        base = {"database": {"host": "localhost", "port": "5432"}}
        override = {"database": {"port": "5433"}, "debug": {"enabled": "true"}}
        expected = {
            "database": {"host": "localhost", "port": "5433"},
            "debug": {"enabled": "true"},
        }
        self.assertEqual(merge_configs(base, override), expected)

    def test_merge_preserves_base_when_no_override(self):
        """Test that base values are preserved when not overridden."""
        base = {"database": {"host": "localhost", "port": "5432"}}
        override = {"database": {"user": "admin"}}
        expected = {"database": {"host": "localhost", "port": "5432", "user": "admin"}}
        self.assertEqual(merge_configs(base, override), expected)

    def test_merge_with_empty_dicts(self):
        """Test merging with empty dictionaries."""
        base = {"database": {"host": "localhost"}}
        override = {}
        self.assertEqual(merge_configs(base, override), base)

        base = {}
        override = {"debug": {"enabled": "true"}}
        self.assertEqual(merge_configs(base, override), override)

        base = {}
        override = {}
        self.assertEqual(merge_configs(base, override), {})

    def test_merge_invalid_types(self):
        """Test that merging invalid types raises TypeError."""
        with self.assertRaises(TypeError):
            merge_configs("not a dict", {"a": {}})
        with self.assertRaises(TypeError):
            merge_configs({"a": {}}, "not a dict")
        with self.assertRaises(TypeError):
            merge_configs({"a": ["not", "dict"]}, {"b": {}})
        with self.assertRaises(TypeError):
            merge_configs({"a": {}}, {"b": ["not", "dict"]})


class TestListSections(unittest.TestCase):
    """Test the list_sections function."""

    def test_list_sections(self):
        """Test listing section names."""
        config = {"database": {}, "debug": {}, "logging": {}}
        self.assertEqual(sorted(list_sections(config)), ["database", "debug", "logging"])

    def test_list_sections_empty(self):
        """Test listing sections of an empty config."""
        self.assertEqual(list_sections({}), [])


class TestHasSection(unittest.TestCase):
    """Test the has_section function."""

    def test_has_section(self):
        """Test checking for section existence."""
        config = {"database": {"host": "localhost"}}
        self.assertTrue(has_section(config, "database"))
        self.assertFalse(has_section(config, "missing"))


class TestGetSection(unittest.TestCase):
    """Test the get_section function."""

    def test_get_section(self):
        """Test getting a section's key/value map."""
        config = {"database": {"host": "localhost", "port": "5432"}}
        self.assertEqual(get_section(config, "database"), {"host": "localhost", "port": "5432"})

    def test_get_missing_section(self):
        """Test getting a missing section returns an empty dict."""
        self.assertEqual(get_section({}, "missing"), {})

    def test_get_section_returns_copy(self):
        """Test that the returned dict is a copy."""
        config = {"database": {"host": "localhost"}}
        section = get_section(config, "database")
        section["host"] = "changed"
        self.assertEqual(config["database"]["host"], "localhost")


if __name__ == "__main__":
    unittest.main()
