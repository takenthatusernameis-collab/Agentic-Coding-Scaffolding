"""Tests for config_schema module."""

import unittest

from config_schema import (
    ConfigSchema,
    ConfigValidationError,
    SchemaField,
    bool_validator,
    choices_validator,
    email_validator,
    float_validator,
    hostname_validator,
    int_validator,
    range_validator,
    regex_validator,
    str_validator,
    url_validator,
)


class TestSchemaFieldCoercion(unittest.TestCase):
    def test_int_validator_coerces_string(self):
        self.assertEqual(int_validator("42"), 42)
        self.assertEqual(int_validator(7), 7)
        self.assertEqual(int_validator(7.0), 7)

    def test_int_validator_rejects_bool(self):
        with self.assertRaises(TypeError):
            int_validator(True)

    def test_int_validator_rejects_non_whole_float(self):
        with self.assertRaises(ValueError):
            int_validator(3.5)

    def test_int_validator_rejects_bad_string(self):
        with self.assertRaises(ValueError):
            int_validator("not-a-number")

    def test_float_validator_coerces(self):
        self.assertEqual(float_validator("3.14"), 3.14)
        self.assertEqual(float_validator(7), 7.0)

    def test_float_validator_rejects_bool(self):
        with self.assertRaises(TypeError):
            float_validator(False)

    def test_str_validator_passthrough(self):
        self.assertEqual(str_validator("hello"), "hello")

    def test_str_validator_rejects_non_string(self):
        with self.assertRaises(TypeError):
            str_validator(123)

    def test_bool_validator_strings(self):
        self.assertTrue(bool_validator("true"))
        self.assertTrue(bool_validator("True"))
        self.assertTrue(bool_validator("1"))
        self.assertTrue(bool_validator("yes"))
        self.assertTrue(bool_validator("on"))
        self.assertFalse(bool_validator("false"))
        self.assertFalse(bool_validator("0"))
        self.assertFalse(bool_validator("no"))
        self.assertFalse(bool_validator("off"))

    def test_bool_validator_numbers(self):
        self.assertTrue(bool_validator(1))
        self.assertFalse(bool_validator(0))

    def test_bool_validator_rejects_bad_string(self):
        with self.assertRaises(ValueError):
            bool_validator("maybe")


class TestSchemaFieldValidators(unittest.TestCase):
    def test_email_validator(self):
        self.assertEqual(email_validator("user@example.com"), "user@example.com")
        with self.assertRaises(ValueError):
            email_validator("not-an-email")

    def test_hostname_validator(self):
        self.assertEqual(hostname_validator("example.com"), "example.com")
        self.assertEqual(hostname_validator("sub.example.com"), "sub.example.com")
        with self.assertRaises(ValueError):
            hostname_validator("-example.com")
        with self.assertRaises(ValueError):
            hostname_validator("example..com")

    def test_url_validator(self):
        self.assertEqual(url_validator("https://example.com/path"), "https://example.com/path")
        with self.assertRaises(ValueError):
            url_validator("example.com")
        with self.assertRaises(ValueError):
            url_validator("http://")

    def test_range_validator(self):
        validate = range_validator(1, 10)
        self.assertEqual(validate(5), 5)
        self.assertEqual(validate("7"), 7)
        with self.assertRaises(ValueError):
            validate(15)

    def test_range_validator_invalid_bounds(self):
        with self.assertRaises(ValueError):
            range_validator(10, 1)

    def test_choices_validator(self):
        validate = choices_validator("dev", "staging", "prod")
        self.assertEqual(validate("staging"), "staging")
        with self.assertRaises(ValueError):
            validate("production")

    def test_choices_validator_no_choices(self):
        with self.assertRaises(ValueError):
            choices_validator()

    def test_regex_validator(self):
        validate = regex_validator(r"^[A-Z]+$")
        self.assertEqual(validate("HELLO"), "HELLO")
        with self.assertRaises(ValueError):
            validate("hello")


class TestSchemaField(unittest.TestCase):
    def test_field_coerce_and_validate(self):
        field = SchemaField("port", int, default=8080)
        self.assertEqual(field.validate("9000"), 9000)
        self.assertEqual(field.validate(443), 443)

    def test_field_with_extra_validator(self):
        field = SchemaField("port", int, validator=range_validator(1, 65535))
        self.assertEqual(field.validate("8080"), 8080)
        with self.assertRaises(ValueError):
            field.validate(99999)

    def test_field_has_default(self):
        field = SchemaField("debug", bool, default=False)
        self.assertTrue(field.has_default)
        required = SchemaField("secret", str, required=True)
        self.assertFalse(required.has_default)

    def test_field_unsupported_type(self):
        with self.assertRaises(TypeError):
            SchemaField("x", list)

    def test_field_empty_name(self):
        with self.assertRaises(ValueError):
            SchemaField("", str)


class TestConfigSchemaValidate(unittest.TestCase):
    def setUp(self):
        self.schema = ConfigSchema([
            SchemaField("host", str, default="localhost"),
            SchemaField("port", int, default=8080, validator=range_validator(1, 65535)),
            SchemaField("debug", bool, default=False),
            SchemaField("secret", str, required=True),
        ])

    def test_validate_full_config(self):
        config = self.schema.validate({
            "host": "example.com",
            "port": "9000",
            "debug": "true",
            "secret": "s3cr3t",
        })
        self.assertEqual(config, {
            "host": "example.com",
            "port": 9000,
            "debug": True,
            "secret": "s3cr3t",
        })

    def test_validate_applies_defaults(self):
        config = self.schema.validate({"secret": "s3cr3t"})
        self.assertEqual(config["host"], "localhost")
        self.assertEqual(config["port"], 8080)
        self.assertEqual(config["debug"], False)
        self.assertEqual(config["secret"], "s3cr3t")

    def test_validate_missing_required_field(self):
        with self.assertRaises(ConfigValidationError):
            self.schema.validate({"host": "example.com"})

    def test_validate_rejects_non_dict(self):
        with self.assertRaises(TypeError):
            self.schema.validate("not a dict")  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            self.schema.validate([1, 2])  # type: ignore[arg-type]

    def test_validate_type_coercion_error(self):
        with self.assertRaises(ConfigValidationError):
            self.schema.validate({"secret": "x", "port": "not-a-number"})

    def test_validate_validation_error_wrapped(self):
        with self.assertRaises(ConfigValidationError):
            self.schema.validate({"secret": "x", "port": 99999})

    def test_validation_error_is_value_error(self):
        self.assertTrue(issubclass(ConfigValidationError, ValueError))

    def test_validate_unknown_keys_are_dropped(self):
        config = self.schema.validate({
            "secret": "x",
            "unknown": "ignored",
            "another": 1,
        })
        self.assertNotIn("unknown", config)
        self.assertNotIn("another", config)

    def test_parse_alias(self):
        config = {"secret": "x", "port": "3000"}
        self.assertEqual(self.schema.parse(config), self.schema.validate(config))

    def test_get(self):
        config = {"secret": "x", "port": "3000"}
        self.assertEqual(self.schema.get(config, "port"), 3000)
        self.assertEqual(self.schema.get(config, "host"), "localhost")
        self.assertEqual(self.schema.get(config, "missing", "fallback"), "fallback")
        self.assertEqual(self.schema.get(config, "not_a_field"), None)

    def test_field_names(self):
        self.assertEqual(
            sorted(self.schema.field_names()),
            ["debug", "host", "port", "secret"],
        )

    def test_required_and_optional_fields(self):
        self.assertEqual(self.schema.required_fields(), ["secret"])
        self.assertEqual(
            self.schema.optional_fields(),
            ["debug", "host", "port"],
        )


class TestConfigSchemaMerge(unittest.TestCase):
    def test_merge_combines_fields(self):
        base = ConfigSchema([SchemaField("a", str, default="x")])
        override = ConfigSchema([SchemaField("b", int, default=1)])
        merged = base.merge(override)
        self.assertEqual(sorted(merged.field_names()), ["a", "b"])

    def test_merge_overrides_existing_field(self):
        base = ConfigSchema([SchemaField("a", str, default="x")])
        override = ConfigSchema([SchemaField("a", int, default=7)])
        merged = base.merge(override)
        field = merged.fields["a"]
        self.assertIsInstance(field, SchemaField)
        self.assertEqual(field.type_, int)
        self.assertEqual(field.default, 7)

    def test_merge_returns_new_schema(self):
        base = ConfigSchema([SchemaField("a", str)])
        other = ConfigSchema([SchemaField("b", str)])
        merged = base.merge(other)
        self.assertIsNot(merged, base)
        self.assertEqual(len(base.fields), 1)
        self.assertEqual(len(merged.fields), 2)


if __name__ == "__main__":
    unittest.main()
