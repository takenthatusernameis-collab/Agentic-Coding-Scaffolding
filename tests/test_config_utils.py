import json
import tempfile
import unittest
from pathlib import Path

from config_utils import get_config_value, load_config, merge_configs, save_config, set_config_value


class TestLoadConfig(unittest.TestCase):
    """Test the load_config function."""

    def test_load_valid_json(self):
        """Test loading a valid JSON configuration file."""
        config_data = {"key": "value", "number": 42, "nested": {"inner": "data"}}

        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(config_data, f)
            temp_path = f.name

        try:
            loaded = load_config(temp_path)
            self.assertEqual(loaded, config_data)
        finally:
            Path(temp_path).unlink()

    def test_load_file_not_found(self):
        """Test loading a non-existent file raises FileNotFoundError."""
        with self.assertRaises(FileNotFoundError):
            load_config("/non/existent/file.json")

    def test_load_invalid_json(self):
        """Test loading invalid JSON raises json.JSONDecodeError."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            f.write('{"invalid": json}')  # Missing quotes around json
            temp_path = f.name

        try:
            with self.assertRaises(json.JSONDecodeError):
                load_config(temp_path)
        finally:
            Path(temp_path).unlink()

    def test_load_valid_but_not_dict(self):
        """Test loading valid JSON that is not a dictionary raises TypeError."""
        for invalid_json in ['[1, 2, 3]', '"string"', '42', 'true', 'null']:
            with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
                f.write(invalid_json)
                temp_path = f.name

            try:
                with self.assertRaises(TypeError):
                    load_config(temp_path)
            finally:
                Path(temp_path).unlink()

    def test_load_with_path_object(self):
        """Test loading works with Path objects."""
        config_data = {"test": "value"}

        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(config_data, f)
            temp_path = Path(f.name)

        try:
            loaded = load_config(temp_path)
            self.assertEqual(loaded, config_data)
        finally:
            temp_path.unlink()


class TestSaveConfig(unittest.TestCase):
    """Test the save_config function."""

    def test_save_and_load_roundtrip(self):
        """Test saving and loading preserves data."""
        original_config = {
            "database": {
                "host": "localhost",
                "port": 5432,
                "credentials": {
                    "username": "admin",
                    "password": "secret"
                }
            },
            "debug": True,
            "tags": ["production", "web"]
        }

        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            temp_path = f.name

        try:
            save_config(original_config, temp_path)
            loaded_config = load_config(temp_path)
            self.assertEqual(loaded_config, original_config)
        finally:
            Path(temp_path).unlink()

    def test_save_creates_directories(self):
        """Test that save_config creates parent directories if needed."""
        config = {"test": "value"}

        with tempfile.TemporaryDirectory() as tmp_dir:
            nested_path = Path(tmp_dir) / "nested" / "deep" / "config.json"

            # Directory should not exist yet
            self.assertFalse(nested_path.parent.exists())

            save_config(config, nested_path)

            # Directory and file should now exist
            self.assertTrue(nested_path.exists())
            self.assertTrue(nested_path.parent.exists())

            loaded = load_config(nested_path)
            self.assertEqual(loaded, config)

    def test_save_invalid_config_type(self):
        """Test that saving non-dict config raises TypeError."""
        with tempfile.NamedTemporaryFile(suffix='.json', delete=False) as f:
            temp_path = f.name

        try:
            with self.assertRaises(TypeError):
                save_config(["not", "a", "dict"], temp_path)
        finally:
            Path(temp_path).unlink()

    def test_save_custom_indent(self):
        """Test saving with custom indentation."""
        config = {"key": "value"}

        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            temp_path = f.name

        try:
            save_config(config, temp_path, indent=4)

            with open(temp_path, 'r') as f:
                content = f.read()

            # Should contain indentation
            self.assertIn('    "key": "value"', content)
        finally:
            Path(temp_path).unlink()


class TestGetConfigValue(unittest.TestCase):
    """Test the get_config_value function."""

    def setUp(self):
        """Set up test configuration."""
        self.config = {
            "database": {
                "host": "localhost",
                "port": 5432,
                "credentials": {
                    "username": "admin",
                    "password": "secret"
                }
            },
            "debug": True,
            "tags": ["production", "web"],
            "simple_value": 42
        }

    def test_get_top_level_value(self):
        """Test getting a top-level configuration value."""
        self.assertEqual(get_config_value(self.config, "debug"), True)
        self.assertEqual(get_config_value(self.config, "simple_value"), 42)

    def test_get_nested_value(self):
        """Test getting a nested configuration value."""
        self.assertEqual(get_config_value(self.config, "database.host"), "localhost")
        self.assertEqual(get_config_value(self.config, "database.port"), 5432)
        self.assertEqual(
            get_config_value(self.config, "database.credentials.username"),
            "admin"
        )

    def test_get_missing_key_returns_default(self):
        """Test that missing keys return the default value."""
        self.assertIsNone(get_config_value(self.config, "missing_key"))
        self.assertEqual(get_config_value(self.config, "missing_key", "default"), "default")
        self.assertEqual(get_config_value(self.config, "database.missing", 999), 999)

    def test_get_value_via_nested_missing_parent(self):
        """Test getting a value when an intermediate parent is missing."""
        self.assertIsNone(get_config_value(self.config, "missing.parent.child"))
        self.assertEqual(
            get_config_value(self.config, "missing.parent.child", "found"),
            "found"
        )

    def test_get_with_custom_separator(self):
        """Test using a custom separator."""
        config = {"a": {"b": {"c": {"d": "value"}}}}
        self.assertEqual(get_config_value(config, "a/b/c/d", separator="/"), "value")

    def test_get_with_non_dict_config(self):
        """Test getting value from non-dict config returns default."""
        self.assertEqual(get_config_value("not a dict", "key", "default"), "default")
        self.assertEqual(get_config_value([], "key", "default"), "default")
        self.assertEqual(get_config_value(42, "key", "default"), "default")
        # Also test that it returns None when no default provided
        self.assertIsNone(get_config_value("not a dict", "key"))
        self.assertIsNone(get_config_value([], "key"))
        self.assertIsNone(get_config_value(42, "key"))


class TestSetConfigValue(unittest.TestCase):
    """Test the set_config_value function."""

    def test_set_top_level_value(self):
        """Test setting a top-level configuration value."""
        config = {}
        set_config_value(config, "new_key", "new_value")
        self.assertEqual(config["new_key"], "new_value")

    def test_set_nested_value(self):
        """Test setting a nested configuration value."""
        config = {}
        set_config_value(config, "database.host", "localhost")
        set_config_value(config, "database.port", 5432)

        expected = {"database": {"host": "localhost", "port": 5432}}
        self.assertEqual(config, expected)

    def test_set_overwrites_existing(self):
        """Test that setting overwrites existing values."""
        config = {"key": "old_value"}
        set_config_value(config, "key", "new_value")
        self.assertEqual(config["key"], "new_value")

    def test_set_creates_intermediate_dicts(self):
        """Test that intermediate dictionaries are created as needed."""
        config = {"existing": "value"}
        set_config_value(config, "new.nested.path", "final")

        expected = {
            "existing": "value",
            "new": {
                "nested": {
                    "path": "final"
                }
            }
        }
        self.assertEqual(config, expected)

    def test_set_with_custom_separator(self):
        """Test using a custom separator."""
        config = {}
        set_config_value(config, "a/b/c", "value", separator="/")
        expected = {"a": {"b": {"c": "value"}}}
        self.assertEqual(config, expected)

    def test_set_invalid_config_type(self):
        """Test that setting value in non-dict config raises TypeError."""
        with self.assertRaises(TypeError):
            set_config_value(["not", "a", "dict"], "key", "value")

        with self.assertRaises(TypeError):
            set_config_value("string", "key", "value")

        with self.assertRaises(TypeError):
            set_config_value(42, "key", "value")


class TestMergeConfigs(unittest.TestCase):
    """Test the merge_configs function."""

    def test_merge_simple_dicts(self):
        """Test merging simple flat dictionaries."""
        base = {"a": 1, "b": 2}
        override = {"b": 3, "c": 4}
        expected = {"a": 1, "b": 3, "c": 4}
        self.assertEqual(merge_configs(base, override), expected)

    def test_merge_nested_dicts(self):
        """Test merging nested dictionaries."""
        base = {
            "database": {
                "host": "localhost",
                "port": 5432
            },
            "debug": False
        }
        override = {
            "database": {
                "port": 5433,
                "credentials": {
                    "user": "admin"
                }
            },
            "debug": True
        }
        expected = {
            "database": {
                "host": "localhost",
                "port": 5433,
                "credentials": {
                    "user": "admin"
                }
            },
            "debug": True
        }
        self.assertEqual(merge_configs(base, override), expected)

    def test_merge_preserves_base_when_no_override(self):
        """Test that base values are preserved when not overridden."""
        base = {"a": 1, "b": {"x": 10}}
        override = {"b": {"y": 20}}
        expected = {"a": 1, "b": {"x": 10, "y": 20}}
        self.assertEqual(merge_configs(base, override), expected)

    def test_merge_with_empty_dicts(self):
        """Test merging with empty dictionaries."""
        base = {"a": 1}
        override = {}
        self.assertEqual(merge_configs(base, override), base)

        base = {}
        override = {"b": 2}
        self.assertEqual(merge_configs(base, override), override)

        base = {}
        override = {}
        self.assertEqual(merge_configs(base, override), {})

    def test_merge_invalid_types(self):
        """Test that merging invalid types raises TypeError."""
        with self.assertRaises(TypeError):
            merge_configs("not a dict", {"a": 1})

        with self.assertRaises(TypeError):
            merge_configs({"a": 1}, "not a dict")

        with self.assertRaises(TypeError):
            merge_configs(["a"], {"b": 2})


if __name__ == "__main__":
    unittest.main()
