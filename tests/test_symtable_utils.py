"""Tests for symtable_utils module."""

import os
import tempfile
import unittest

import symtable_utils

SAMPLE = '''
import os
from pathlib import Path

CONSTANT = 1


def outer(first, second=2):
    local_value = first + second

    def inner():
        return local_value

    return inner


class Base:
    attribute = 0

    def method(self):
        return self.attribute
'''


class TestBuildSymbolTable(unittest.TestCase):
    def test_returns_module_scope(self):
        table = symtable_utils.build_symbol_table(SAMPLE, "sample.py")
        self.assertEqual(symtable_utils.scope_type(table), "module")

    def test_default_filename_and_compile_type(self):
        table = symtable_utils.build_symbol_table("value = 1")
        self.assertEqual(symtable_utils.scope_type(table), "module")
        self.assertEqual(symtable_utils.scope_identifiers(table), ["value"])

    def test_scope_identifiers_lists_bindings(self):
        table = symtable_utils.build_symbol_table(SAMPLE, "sample.py")
        identifiers = symtable_utils.scope_identifiers(table)
        for name in ("os", "Path", "CONSTANT", "outer", "Base"):
            self.assertIn(name, identifiers)

    def test_eval_compile_type(self):
        table = symtable_utils.build_symbol_table("1 + 2", "<eval>", "eval")
        self.assertEqual(symtable_utils.scope_type(table), "module")

    def test_single_compile_type(self):
        table = symtable_utils.build_symbol_table("value = 1", "<single>", "single")
        self.assertEqual(symtable_utils.scope_type(table), "module")

    def test_code_must_be_string(self):
        with self.assertRaises(TypeError):
            symtable_utils.build_symbol_table(123)  # type: ignore[arg-type]

    def test_filename_must_be_string(self):
        with self.assertRaises(TypeError):
            symtable_utils.build_symbol_table("x = 1", 5)  # type: ignore[arg-type]

    def test_compile_type_must_be_string(self):
        with self.assertRaises(TypeError):
            symtable_utils.build_symbol_table("x = 1", "<s>", 1)  # type: ignore[arg-type]

    def test_unknown_compile_type_raises_value_error(self):
        with self.assertRaises(ValueError):
            symtable_utils.build_symbol_table("x = 1", "<s>", "module")

    def test_syntax_error_propagates(self):
        with self.assertRaises(SyntaxError):
            symtable_utils.build_symbol_table("def broken(:")


class TestLookupSymbolTable(unittest.TestCase):
    def test_lookup_known_module(self):
        table = symtable_utils.lookup_symbol_table("json")
        self.assertEqual(symtable_utils.scope_type(table), "module")
        self.assertIn("JSONDecoder", symtable_utils.scope_identifiers(table))

    def test_lookup_with_explicit_filename(self):
        with tempfile.TemporaryDirectory() as directory:
            path = os.path.join(directory, "explicit_module.py")
            with open(path, "w", encoding="utf-8") as handle:
                handle.write("EXPLICIT = 1\n")
            table = symtable_utils.lookup_symbol_table("json", filename=path)
        self.assertIn("EXPLICIT", symtable_utils.scope_identifiers(table))

    def test_lookup_unknown_module_raises_import_error(self):
        with self.assertRaises(ImportError):
            symtable_utils.lookup_symbol_table("module_that_does_not_exist_xyz")

    def test_lookup_name_must_be_string(self):
        with self.assertRaises(TypeError):
            symtable_utils.lookup_symbol_table(None)  # type: ignore[arg-type]

    def test_lookup_empty_name_raises_value_error(self):
        with self.assertRaises(ValueError):
            symtable_utils.lookup_symbol_table("")

    def test_lookup_filename_must_be_string(self):
        with self.assertRaises(TypeError):
            symtable_utils.lookup_symbol_table("json", filename=1)  # type: ignore[arg-type]

    def test_lookup_missing_file_raises_os_error(self):
        with self.assertRaises(OSError):
            symtable_utils.lookup_symbol_table("json", filename="/nonexistent/module.py")


class TestScopeInspection(unittest.TestCase):
    def setUp(self):
        self.table = symtable_utils.build_symbol_table(SAMPLE, "sample.py")

    def test_scope_type_rejects_non_table(self):
        with self.assertRaises(TypeError):
            symtable_utils.scope_type("not-a-table")  # type: ignore[arg-type]

    def test_scope_identifiers_rejects_non_table(self):
        with self.assertRaises(TypeError):
            symtable_utils.scope_identifiers(None)  # type: ignore[arg-type]

    def test_child_scopes_lists_nested_scopes(self):
        children = symtable_utils.child_scopes(self.table)
        names = [child.get_name() for child in children]
        self.assertIn("outer", names)
        self.assertIn("Base", names)

    def test_child_scopes_rejects_non_table(self):
        with self.assertRaises(TypeError):
            symtable_utils.child_scopes(1)  # type: ignore[arg-type]

    def test_iter_scopes_walks_depth_first(self):
        paths = [path for path, _ in symtable_utils.iter_scopes(self.table)]
        self.assertIn((), paths)
        self.assertIn(("outer",), paths)
        self.assertIn(("outer", "inner"), paths)
        self.assertIn(("Base",), paths)
        self.assertIn(("Base", "method"), paths)

    def test_iter_scopes_rejects_non_table(self):
        with self.assertRaises(TypeError):
            list(symtable_utils.iter_scopes(None))  # type: ignore[arg-type]

    def test_find_scope_returns_matching_scope(self):
        found = symtable_utils.find_scope(self.table, "inner")
        self.assertIsNotNone(found)
        self.assertEqual(found.get_name(), "inner")
        self.assertEqual(found.get_type(), "function")

    def test_find_scope_returns_none_when_missing(self):
        self.assertIsNone(symtable_utils.find_scope(self.table, "absent"))

    def test_find_scope_rejects_non_string_name(self):
        with self.assertRaises(TypeError):
            symtable_utils.find_scope(self.table, 5)  # type: ignore[arg-type]

    def test_find_scope_rejects_non_table(self):
        with self.assertRaises(TypeError):
            symtable_utils.find_scope("not-a-table", "inner")  # type: ignore[arg-type]

    def test_describe_scope_reports_metadata(self):
        described = symtable_utils.describe_scope(self.table)
        self.assertEqual(described["type"], "module")
        self.assertEqual(described["name"], "top")
        self.assertIsInstance(described["lineno"], int)
        self.assertIn("CONSTANT", described["identifiers"])
        self.assertIn("outer", described["children"])

    def test_describe_scope_rejects_non_table(self):
        with self.assertRaises(TypeError):
            symtable_utils.describe_scope(object())  # type: ignore[arg-type]


class TestSymbolInfo(unittest.TestCase):
    def setUp(self):
        self.table = symtable_utils.build_symbol_table(SAMPLE, "sample.py")

    def test_symbol_info_reports_name_and_flags(self):
        info = symtable_utils.symbol_info(self.table, "CONSTANT")
        self.assertEqual(info["name"], "CONSTANT")
        self.assertTrue(info["is_global"])
        self.assertTrue(info["is_assigned"])
        self.assertFalse(info["is_imported"])

    def test_symbol_info_reports_imported_symbol(self):
        info = symtable_utils.symbol_info(self.table, "os")
        self.assertTrue(info["is_imported"])
        self.assertFalse(info["is_parameter"])

    def test_symbol_info_raises_key_error_when_missing(self):
        with self.assertRaises(KeyError):
            symtable_utils.symbol_info(self.table, "missing_name")

    def test_symbol_info_rejects_non_table(self):
        with self.assertRaises(TypeError):
            symtable_utils.symbol_info(None, "CONSTANT")  # type: ignore[arg-type]

    def test_symbol_info_rejects_non_string_name(self):
        with self.assertRaises(TypeError):
            symtable_utils.symbol_info(self.table, 5)  # type: ignore[arg-type]

    def test_symbol_flags_rejects_non_symbol(self):
        with self.assertRaises(TypeError):
            symtable_utils.symbol_flags("not-a-symbol")  # type: ignore[arg-type]

    def test_symbol_flags_covers_every_predicate(self):
        flags = symtable_utils.symbol_flags(self.table.lookup("CONSTANT"))
        for name in (
            "is_global",
            "is_local",
            "is_free",
            "is_nonlocal",
            "is_parameter",
            "is_imported",
            "is_assigned",
            "is_referenced",
            "is_namespace",
            "is_declared_global",
            "is_declared_nonlocal",
        ):
            self.assertIn(name, flags)
            self.assertIsInstance(flags[name], bool)

    def test_namespace_names_of_class_scope(self):
        names = symtable_utils.namespace_names(self.table.lookup("Base"))
        self.assertIn("attribute", names)
        self.assertIn("method", names)

    def test_namespace_names_returns_empty_for_plain_name(self):
        self.assertEqual(symtable_utils.namespace_names(self.table.lookup("CONSTANT")), [])

    def test_namespace_names_rejects_non_symbol(self):
        with self.assertRaises(TypeError):
            symtable_utils.namespace_names(None)  # type: ignore[arg-type]


class TestNameCollectors(unittest.TestCase):
    def setUp(self):
        self.table = symtable_utils.build_symbol_table(SAMPLE, "sample.py")

    def test_global_names(self):
        names = symtable_utils.global_names(self.table)
        self.assertIn("CONSTANT", names)
        self.assertIn("outer", names)

    def test_local_names_at_module_scope(self):
        names = symtable_utils.local_names(self.table)
        self.assertIn("CONSTANT", names)

    def test_imported_names(self):
        names = symtable_utils.imported_names(self.table)
        self.assertEqual(sorted(names), ["Path", "os"])

    def test_assigned_names(self):
        names = symtable_utils.assigned_names(self.table)
        self.assertIn("CONSTANT", names)
        self.assertNotIn("os", names)

    def test_parameter_names_of_function_scope(self):
        outer = symtable_utils.find_scope(self.table, "outer")
        self.assertEqual(sorted(symtable_utils.parameter_names(outer)), ["first", "second"])

    def test_free_variables_of_nested_scope(self):
        inner = symtable_utils.find_scope(self.table, "inner")
        self.assertEqual(symtable_utils.free_variables(inner), ["local_value"])

    def test_referenced_names_of_function_scope(self):
        outer = symtable_utils.find_scope(self.table, "outer")
        self.assertIn("first", symtable_utils.referenced_names(outer))

    def test_nonlocal_names_empty_by_default(self):
        self.assertEqual(symtable_utils.nonlocal_names(self.table), [])

    def test_nonlocal_names_detects_declaration(self):
        table = symtable_utils.build_symbol_table(
            "def outer():\n"
            "    value = 1\n"
            "    def inner():\n"
            "        nonlocal value\n"
            "        value = 2\n",
            "nonlocal.py",
        )
        inner = symtable_utils.find_scope(table, "inner")
        self.assertEqual(symtable_utils.nonlocal_names(inner), ["value"])

    def test_collectors_reject_non_table(self):
        for collector in (
            symtable_utils.global_names,
            symtable_utils.local_names,
            symtable_utils.parameter_names,
            symtable_utils.imported_names,
            symtable_utils.assigned_names,
            symtable_utils.referenced_names,
            symtable_utils.nonlocal_names,
            symtable_utils.free_variables,
        ):
            with self.subTest(collector=collector.__name__):
                with self.assertRaises(TypeError):
                    collector(None)  # type: ignore[arg-type]


class TestCompileTypes(unittest.TestCase):
    def test_compile_types_constant(self):
        self.assertEqual(
            symtable_utils.COMPILE_TYPES,
            ("exec", "eval", "single"),
        )


class TestModuleSurface(unittest.TestCase):
    def test_public_names_are_exported(self):
        for name in symtable_utils.__all__:
            with self.subTest(name=name):
                self.assertTrue(hasattr(symtable_utils, name))

    def test_all_entries_are_unique(self):
        self.assertEqual(len(symtable_utils.__all__), len(set(symtable_utils.__all__)))

    def test_reads_source_from_disk(self):
        with tempfile.TemporaryDirectory() as directory:
            path = os.path.join(directory, "module_under_test.py")
            with open(path, "w", encoding="utf-8") as handle:
                handle.write("MARKER = 42\n")
            with open(path, encoding="utf-8") as handle:
                source = handle.read()
            table = symtable_utils.build_symbol_table(source, path)
        self.assertIn("MARKER", symtable_utils.scope_identifiers(table))


if __name__ == "__main__":
    unittest.main()
