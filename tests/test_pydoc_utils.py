"""Tests for pydoc_utils."""

import pydoc
import tempfile
import unittest
from pathlib import Path

import pydoc_utils
from pydoc_utils import (
    Doc,
    ErrorDuringImport,
    Helper,
    HTMLDoc,
    HTMLRepr,
    ModuleScanner,
    Repr,
    TextDoc,
    TextRepr,
    allmethods,
    apropos,
    classify_class_attrs,
    classname,
    cram,
    describe,
    doc,
    format_exception_only,
    getdoc,
    getpager,
    importfile,
    isdata,
    ispackage,
    ispath,
    locate,
    parentname,
    plain,
    render_doc,
    replace,
    resolve,
    safeimport,
    source_synopsis,
    splitdoc,
    stripid,
    synopsis,
    visiblename,
)


class _Example:
    """An example class used for documentation tests."""

    def example_method(self):
        """An example method."""


class TestModuleContract(unittest.TestCase):
    """Verify the public interface of the module."""

    def test_all_is_sorted_and_unique(self):
        self.assertEqual(len(pydoc_utils.__all__), len(set(pydoc_utils.__all__)))
        self.assertEqual(pydoc_utils.__all__, sorted(pydoc_utils.__all__))
        for name in pydoc_utils.__all__:
            self.assertTrue(hasattr(pydoc_utils, name), name)

    def test_the_classes_are_the_classes_of_the_standard_library(self):
        self.assertIs(Doc, pydoc.Doc)
        self.assertIs(HTMLDoc, pydoc.HTMLDoc)
        self.assertIs(HTMLRepr, pydoc.HTMLRepr)
        self.assertIs(Helper, pydoc.Helper)
        self.assertIs(ModuleScanner, pydoc.ModuleScanner)
        self.assertIs(Repr, pydoc.Repr)
        self.assertIs(TextDoc, pydoc.TextDoc)
        self.assertIs(TextRepr, pydoc.TextRepr)

    def test_the_error_is_the_error_of_the_standard_library(self):
        self.assertIs(ErrorDuringImport, pydoc.ErrorDuringImport)


class TestRendering(unittest.TestCase):
    """Verify the helpers that render documentation."""

    def test_render_doc_returns_a_string(self):
        found = render_doc(_Example)
        self.assertIsInstance(found, str)
        self.assertIn("Example", found)

    def test_render_doc_accepts_a_title(self):
        found = render_doc(_Example, title="Custom %s")
        self.assertTrue(found.startswith("Custom "))

    def test_render_doc_rejects_an_invalid_title(self):
        with self.assertRaises(TypeError):
            render_doc(_Example, title=123)  # type: ignore[arg-type]

    def test_render_doc_rejects_a_non_bool_forceload(self):
        with self.assertRaises(TypeError):
            render_doc(_Example, forceload="yes")  # type: ignore[arg-type]

    def test_render_doc_rejects_a_non_callable_renderer(self):
        with self.assertRaises(TypeError):
            render_doc(_Example, renderer=123)  # type: ignore[arg-type]

    def test_doc_returns_none(self):
        self.assertIsNone(doc(_Example))

    def test_doc_accepts_a_title(self):
        self.assertIsNone(doc(_Example, title="Custom %s"))

    def test_doc_rejects_an_invalid_title(self):
        with self.assertRaises(TypeError):
            doc(_Example, title=123)  # type: ignore[arg-type]

    def test_getdoc_returns_a_string(self):
        found = getdoc(_Example)
        self.assertIsInstance(found, str)

    def test_describe_returns_a_string(self):
        found = describe(_Example)
        self.assertIsInstance(found, str)


class TestResolution(unittest.TestCase):
    """Verify the helpers that locate and resolve objects."""

    def test_locate_finds_an_object(self):
        found = locate("pydoc.render_doc")
        self.assertEqual(found.__name__, "render_doc")

    def test_locate_rejects_a_non_string(self):
        with self.assertRaises(TypeError):
            locate(123)  # type: ignore[arg-type]

    def test_locate_rejects_a_non_bool_forceload(self):
        with self.assertRaises(TypeError):
            locate("pydoc.render_doc", forceload="yes")  # type: ignore[arg-type]

    def test_locate_of_an_unknown_name_returns_none(self):
        self.assertIsNone(locate("pydoc.does_not_exist"))

    def test_resolve_resolves_an_object(self):
        found = resolve(_Example)
        self.assertIs(found[0], _Example)

    def test_resolve_resolves_a_dotted_name(self):
        found = resolve("pydoc.render_doc")
        self.assertEqual(found[0].__name__, "render_doc")

    def test_resolve_rejects_a_non_bool_forceload(self):
        with self.assertRaises(TypeError):
            resolve(_Example, forceload="yes")  # type: ignore[arg-type]

    def test_safeimport_imports_a_module(self):
        found = safeimport("pydoc")
        self.assertEqual(found.__name__, "pydoc")

    def test_safeimport_returns_none_for_an_unknown_module(self):
        self.assertIsNone(safeimport("pydoc.does_not_exist"))

    def test_safeimport_rejects_a_non_string(self):
        with self.assertRaises(TypeError):
            safeimport(123)  # type: ignore[arg-type]

    def test_safeimport_rejects_a_non_bool_forceload(self):
        with self.assertRaises(TypeError):
            safeimport("pydoc", forceload="yes")  # type: ignore[arg-type]

    def test_safeimport_rejects_a_non_dict_cache(self):
        with self.assertRaises(TypeError):
            safeimport("pydoc", cache=[])  # type: ignore[arg-type]

    def test_importfile_imports_a_module_file(self):
        found = importfile(pydoc.__file__)
        self.assertEqual(found.__name__, "pydoc")

    def test_importfile_rejects_a_non_string(self):
        with self.assertRaises(TypeError):
            importfile(123)  # type: ignore[arg-type]


class TestIntrospection(unittest.TestCase):
    """Verify the helpers that introspect objects."""

    def test_classify_class_attrs_returns_a_list(self):
        found = classify_class_attrs(_Example)
        self.assertIsInstance(found, list)

    def test_classname_returns_the_qualified_name(self):
        found = classname(_Example, "anything")
        self.assertEqual(found, "test_pydoc_utils._Example")

    def test_classname_rejects_a_non_string_modname(self):
        with self.assertRaises(TypeError):
            classname(_Example, 123)  # type: ignore[arg-type]

    def test_parentname_returns_the_module_name(self):
        found = parentname(_Example, "anything")
        self.assertEqual(found, "test_pydoc_utils")

    def test_parentname_rejects_a_non_string_modname(self):
        with self.assertRaises(TypeError):
            parentname(_Example, 123)  # type: ignore[arg-type]

    def test_visiblename_reports_a_visible_name(self):
        self.assertTrue(visiblename("example_method"))
        self.assertFalse(visiblename("_private"))

    def test_visiblename_of_all_names(self):
        self.assertTrue(visiblename("_private", all_names=["_private"]))

    def test_visiblename_rejects_a_non_string(self):
        with self.assertRaises(TypeError):
            visiblename(123)  # type: ignore[arg-type]

    def test_visiblename_rejects_a_non_sequence_all_names(self):
        with self.assertRaises(TypeError):
            visiblename("name", all_names="yes")  # type: ignore[arg-type]

    def test_isdata_reports_a_data_object(self):
        self.assertTrue(isdata(42))

    def test_ispath_reports_a_path(self):
        self.assertTrue(ispath("/usr/bin/python"))
        self.assertFalse(ispath("not a path"))

    def test_ispackage_reports_a_package_directory(self):
        with tempfile.TemporaryDirectory() as directory:
            Path(directory, "__init__.py").write_text("", encoding="utf-8")
            self.assertTrue(ispackage(directory))

    def test_ispackage_rejects_a_non_string(self):
        with self.assertRaises(TypeError):
            ispackage(123)  # type: ignore[arg-type]


class TestAttributes(unittest.TestCase):
    """Verify the helpers that work with attributes."""

    def test_allmethods_returns_the_method_names(self):
        found = allmethods(_Example)
        self.assertIn("example_method", found)

    def test_allmethods_rejects_a_value_that_is_not_a_class(self):
        with self.assertRaises(TypeError):
            allmethods(42)  # type: ignore[arg-type]


class TestStrings(unittest.TestCase):
    """Verify the helpers that transform strings."""

    def test_splitdoc_splits_a_documentation_string(self):
        found = splitdoc("A summary.\n\nA section.")
        self.assertEqual(found, ("A summary.", "A section."))

    def test_splitdoc_rejects_a_non_string(self):
        with self.assertRaises(TypeError):
            splitdoc(123)  # type: ignore[arg-type]

    def test_stripid_returns_a_string(self):
        self.assertEqual(stripid("module.Class.method"), "module.Class.method")

    def test_stripid_rejects_a_non_string(self):
        with self.assertRaises(TypeError):
            stripid(123)  # type: ignore[arg-type]

    def test_replace_replaces_the_pairs(self):
        found = replace("hello world", "hello", "goodbye")
        self.assertEqual(found, "goodbye world")

    def test_replace_rejects_a_non_string(self):
        with self.assertRaises(TypeError):
            replace(123)  # type: ignore[arg-type]

    def test_replace_rejects_an_odd_number_of_strings(self):
        with self.assertRaises(TypeError):
            replace("text", "only")  # type: ignore[arg-type]

    def test_cram_shortens_a_text(self):
        self.assertEqual(cram("hello world", 5), "h...d")

    def test_cram_of_an_empty_maxlen(self):
        self.assertEqual(cram("hello world", 0), "...")

    def test_cram_rejects_a_non_string(self):
        with self.assertRaises(TypeError):
            cram(123, 5)  # type: ignore[arg-type]

    def test_cram_rejects_a_non_int_maxlen(self):
        with self.assertRaises(TypeError):
            cram("text", "5")  # type: ignore[arg-type]

    def test_cram_rejects_a_negative_maxlen(self):
        with self.assertRaises(ValueError):
            cram("text", -1)

    def test_plain_returns_plain_text(self):
        self.assertEqual(plain("hello"), "hello")

    def test_plain_rejects_a_non_string(self):
        with self.assertRaises(TypeError):
            plain(123)  # type: ignore[arg-type]


class TestSynopsis(unittest.TestCase):
    """Verify the helpers that read the synopsis of a module."""

    def test_synopsis_reads_the_synopsis_of_a_module(self):
        found = synopsis(pydoc.__file__)
        self.assertIsInstance(found, str)

    def test_synopsis_rejects_a_non_string(self):
        with self.assertRaises(TypeError):
            synopsis(123)  # type: ignore[arg-type]

    def test_synopsis_rejects_a_non_dict_cache(self):
        with self.assertRaises(TypeError):
            synopsis(pydoc.__file__, cache=[])  # type: ignore[arg-type]

    def test_source_synopsis_reads_the_synopsis_of_a_file(self):
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".py", delete=False, encoding="utf-8"
        ) as handle:
            handle.write('"""A sample module."""\n')
            path = handle.name
        try:
            with open(path, encoding="utf-8") as handle:
                found = source_synopsis(handle)
            self.assertIsInstance(found, str)
        finally:
            Path(path).unlink()

    def test_source_synopsis_rejects_a_value_that_is_not_file_like(self):
        with self.assertRaises(TypeError):
            source_synopsis(123)  # type: ignore[arg-type]


class TestExceptions(unittest.TestCase):
    """Verify the helpers that format exceptions."""

    def test_format_exception_only_formats_an_exception(self):
        try:
            raise ValueError("boom")
        except ValueError as exc:
            found = format_exception_only(ValueError, exc)
            self.assertIsInstance(found, list)
            self.assertEqual(found, ["ValueError: boom\n"])


class TestHelpers(unittest.TestCase):
    """Verify the remaining helpers."""

    def test_getpager_returns_a_pager_or_none(self):
        found = getpager()
        self.assertTrue(found is None or callable(found))

    def test_apropos_prints_a_summary(self):
        apropos("pydoc")


if __name__ == "__main__":
    unittest.main()
