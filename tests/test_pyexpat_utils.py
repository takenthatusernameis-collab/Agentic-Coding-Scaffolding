"""Tests for pyexpat_utils.

The tests never touch system files: every XML document is written to a
temporary directory the test owns.  The standard library is patched for the
validation and degradation tests, so the suite needs no network and no
filesystem outside its own temporary directories.
"""

import os
import tempfile
import unittest
from unittest import mock

import pyexpat_utils

try:
    import pyexpat as _pyexpat
except ImportError:  # pragma: no cover - pyexpat ships with every CPython
    _pyexpat = None  # type: ignore[assignment]


@unittest.skipUnless(pyexpat_utils.is_available(), "pyexpat module not available")
class TestModuleContract(unittest.TestCase):
    """Verify the contract of the module."""

    def test_all_is_sorted_and_unique(self):
        self.assertEqual(pyexpat_utils.__all__, sorted(set(pyexpat_utils.__all__)))

    def test_every_name_exists(self):
        for name in pyexpat_utils.__all__:
            self.assertTrue(hasattr(pyexpat_utils, name), name)

    def test_is_available_reports_a_bool(self):
        self.assertIsInstance(pyexpat_utils.is_available(), bool)

    def test_is_available_matches_the_standard_library(self):
        self.assertEqual(pyexpat_utils.is_available(), _pyexpat is not None)

    def test_expat_version_is_reported(self):
        self.assertIsInstance(pyexpat_utils.EXPAT_VERSION, str)
        self.assertNotEqual(pyexpat_utils.EXPAT_VERSION, "")

    def test_param_entity_parsing_constants_are_integers(self):
        self.assertIsInstance(pyexpat_utils.XML_PARAM_ENTITY_PARSING_ALWAYS, int)
        self.assertIsInstance(pyexpat_utils.XML_PARAM_ENTITY_PARSING_NEVER, int)
        self.assertIsInstance(pyexpat_utils.XML_PARAM_ENTITY_PARSING_UNLESS_STANDALONE, int)


@unittest.skipUnless(pyexpat_utils.is_available(), "pyexpat module not available")
class TestValidation(unittest.TestCase):
    """Verify the validation of the arguments.

    The arguments are validated before the standard library is reached, so the
    same error is raised on an interpreter that does not ship the module.
    """

    def setUp(self):
        patcher = mock.patch("pyexpat_utils._pyexpat")
        self.module = patcher.start()
        self.addCleanup(patcher.stop)

    def test_the_text_arguments_must_be_strings(self):
        parser = self.module.ParserCreate.return_value
        for call in (
            lambda: pyexpat_utils.parse(parser, 42),
            lambda: pyexpat_utils.parse_text(parser, 42),
            lambda: pyexpat_utils.set_base(parser, 42),
            lambda: pyexpat_utils.error_string("42"),
        ):
            with self.assertRaises(TypeError):
                call()

    def test_the_file_paths_must_be_paths(self):
        parser = self.module.ParserCreate.return_value
        with self.assertRaises(TypeError):
            pyexpat_utils.parse_file(parser, 42)

    def test_the_file_paths_must_not_be_empty(self):
        parser = self.module.ParserCreate.return_value
        with self.assertRaises(ValueError):
            pyexpat_utils.parse_file(parser, "")

    def test_the_buffer_size_must_be_positive(self):
        with self.assertRaises(ValueError):
            pyexpat_utils.create_parser(buffer_size=0)

    def test_the_handlers_must_be_callable(self):
        parser = self.module.ParserCreate.return_value
        for call in (
            lambda: pyexpat_utils.set_start_element_handler(parser, "handler"),
            lambda: pyexpat_utils.set_end_element_handler(parser, "handler"),
            lambda: pyexpat_utils.set_character_data_handler(parser, "handler"),
            lambda: pyexpat_utils.set_processing_instruction_handler(parser, "handler"),
        ):
            with self.assertRaises(TypeError):
                call()

    def test_the_standard_library_is_not_reached(self):
        parser = self.module.ParserCreate.return_value
        with self.assertRaises(TypeError):
            pyexpat_utils.parse(parser, 42)
        parser.Parse.assert_not_called()
        with self.assertRaises(TypeError):
            pyexpat_utils.parse_file(parser, 42)
        parser.ParseFile.assert_not_called()
        with self.assertRaises(TypeError):
            pyexpat_utils.set_start_element_handler(parser, "handler")
        self.assertNotEqual(parser.StartElementHandler, "handler")


@unittest.skipUnless(pyexpat_utils.is_available(), "pyexpat module not available")
class TestDegradation(unittest.TestCase):
    """Verify the behavior on an interpreter that does not ship the module."""

    def setUp(self):
        patcher = mock.patch("pyexpat_utils._pyexpat", None)
        patcher.start()
        self.addCleanup(patcher.stop)

    def test_parser_create_raises(self):
        with self.assertRaises(RuntimeError):
            pyexpat_utils.ParserCreate()

    def test_the_helpers_report_the_missing_module(self):
        for call in (
            lambda: pyexpat_utils.create_parser(),
            lambda: pyexpat_utils.error_string(1),
        ):
            with self.assertRaises(RuntimeError):
                call()

    def test_version_info_raises(self):
        with self.assertRaises(RuntimeError):
            pyexpat_utils.version_info()

    def test_is_available_reports_false(self):
        self.assertFalse(pyexpat_utils.is_available())


@unittest.skipUnless(pyexpat_utils.is_available(), "pyexpat module not available")
class TestParser(unittest.TestCase):
    """Verify the parser creation and parsing helpers."""

    def test_create_parser_returns_a_parser(self):
        parser = pyexpat_utils.create_parser()
        self.assertIsNotNone(parser)

    def test_create_parser_options_are_applied(self):
        parser = pyexpat_utils.create_parser(
            namespace_prefixes=True,
            ordered_attributes=True,
            specified_attributes=True,
            buffer_size=4096,
        )
        self.assertTrue(parser.namespace_prefixes)
        self.assertTrue(parser.ordered_attributes)
        self.assertTrue(parser.specified_attributes)
        self.assertEqual(parser.buffer_size, 4096)

    def test_parse_text_reports_well_formed_document(self):
        parser = pyexpat_utils.create_parser()
        result = pyexpat_utils.parse_text(parser, "<doc>text</doc>")
        self.assertEqual(result, 1)

    def test_parse_rejects_malformed_document(self):
        parser = pyexpat_utils.create_parser()
        with self.assertRaises(pyexpat_utils.ExpatError):
            pyexpat_utils.parse_text(parser, "<doc>unclosed")

    def test_error_position_reports_the_error(self):
        parser = pyexpat_utils.create_parser()
        with self.assertRaises(pyexpat_utils.ExpatError):
            pyexpat_utils.parse_text(parser, "<doc>unclosed")
        position = pyexpat_utils.error_position(parser)
        self.assertIsInstance(position.line, int)
        self.assertIsInstance(position.column, int)
        self.assertIsInstance(position.code, int)
        self.assertIsInstance(position.byte_index, int)

    def test_current_position_reports_the_position(self):
        parser = pyexpat_utils.create_parser()
        pyexpat_utils.parse_text(parser, "<doc>text</doc>")
        position = pyexpat_utils.current_position(parser)
        self.assertIsInstance(position.byte_index, int)
        self.assertIsInstance(position.line_number, int)
        self.assertIsInstance(position.column_number, int)


@unittest.skipUnless(pyexpat_utils.is_available(), "pyexpat module not available")
class TestFiles(unittest.TestCase):
    """Verify the helpers that parse files."""

    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)

    def test_parse_file_reads_a_well_formed_document(self):
        path = os.path.join(self.directory.name, "document.xml")
        with open(path, "w", encoding="utf-8") as handle:
            handle.write("<doc>text</doc>")
        parser = pyexpat_utils.create_parser()
        result = pyexpat_utils.parse_file(parser, path)
        self.assertEqual(result, 1)

    def test_parse_file_rejects_a_malformed_document(self):
        path = os.path.join(self.directory.name, "document.xml")
        with open(path, "w", encoding="utf-8") as handle:
            handle.write("<doc>unclosed")
        parser = pyexpat_utils.create_parser()
        with self.assertRaises(pyexpat_utils.ExpatError):
            pyexpat_utils.parse_file(parser, path)

    def test_parse_file_reports_a_missing_file(self):
        parser = pyexpat_utils.create_parser()
        missing = os.path.join(self.directory.name, "missing.xml")
        with self.assertRaises(OSError):
            pyexpat_utils.parse_file(parser, missing)


@unittest.skipUnless(pyexpat_utils.is_available(), "pyexpat module not available")
class TestHandlers(unittest.TestCase):
    """Verify the handler setters."""

    def test_start_and_end_element_handlers_are_set_and_removed(self):
        parser = pyexpat_utils.create_parser()
        started = []

        def start(name, attributes):
            started.append(name)

        def end(name):
            started.append(f"/{name}")

        pyexpat_utils.set_element_handlers(parser, start, end)
        pyexpat_utils.parse_text(parser, "<doc>text</doc>")
        self.assertEqual(started, ["doc", "/doc"])

        pyexpat_utils.set_start_element_handler(parser, None)
        pyexpat_utils.set_end_element_handler(parser, None)

    def test_character_data_handler_receives_text(self):
        parser = pyexpat_utils.create_parser()
        data = []

        def characters(text):
            data.append(text)

        pyexpat_utils.set_character_data_handler(parser, characters)
        pyexpat_utils.parse_text(parser, "<doc>hello world</doc>")
        self.assertEqual(data, ["hello world"])

    def test_processing_instruction_handler_receives_target_and_data(self):
        parser = pyexpat_utils.create_parser()
        instructions = []

        def instruction(target, data):
            instructions.append((target, data))

        pyexpat_utils.set_processing_instruction_handler(parser, instruction)
        pyexpat_utils.parse_text(parser, '<?target data?><doc/>')
        self.assertEqual(instructions, [("target", "data")])


@unittest.skipUnless(pyexpat_utils.is_available(), "pyexpat module not available")
class TestPositionAndBase(unittest.TestCase):
    """Verify the base and position helpers."""

    def test_get_base_and_set_base(self):
        parser = pyexpat_utils.create_parser()
        self.assertIsNone(pyexpat_utils.get_base(parser))
        base = pyexpat_utils.set_base(parser, "http://example.com/base/")
        self.assertEqual(base, "http://example.com/base/")
        self.assertEqual(pyexpat_utils.get_base(parser), "http://example.com/base/")

    def test_set_param_entity_parsing_returns_previous_value(self):
        parser = pyexpat_utils.create_parser()
        previous = pyexpat_utils.set_param_entity_parsing(
            parser,
            pyexpat_utils.XML_PARAM_ENTITY_PARSING_ALWAYS,
        )
        self.assertIsInstance(previous, int)


@unittest.skipUnless(pyexpat_utils.is_available(), "pyexpat module not available")
class TestAttributeMapping(unittest.TestCase):
    """Verify the attribute mapping helper."""

    def test_attributes_are_returned_as_a_mapping(self):
        parser = pyexpat_utils.create_parser()
        captured = {}

        def start(name, attributes):
            captured["attributes"] = attributes

        pyexpat_utils.set_start_element_handler(parser, start)
        pyexpat_utils.parse_text(parser, '<doc attr="value" other="2"/>')
        mapping = pyexpat_utils.attribute_mapping(captured["attributes"])
        self.assertEqual(mapping, {"attr": "value", "other": "2"})

    def test_attribute_mapping_rejects_non_mapping(self):
        with self.assertRaises(TypeError):
            pyexpat_utils.attribute_mapping("not-a-mapping")


if __name__ == "__main__":
    unittest.main()
