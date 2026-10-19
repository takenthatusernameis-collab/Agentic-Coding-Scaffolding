import os
import sys
import tempfile
import unittest

from pkgutil_utils import (
    extend_path,
    find_spec,
    get_data,
    iter_importers,
    iter_modules,
    read_text,
    resolve_name,
    walk_packages,
)


class TestPkgutilUtils(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.pkg = os.path.join(self.tmp, "samplepkg")
        os.makedirs(self.pkg)
        with open(os.path.join(self.pkg, "__init__.py"), "w") as f:
            f.write("VALUE = 42\n")
        with open(os.path.join(self.pkg, "data.txt"), "w") as f:
            f.write("payload")
        with open(os.path.join(self.pkg, "mod.py"), "w") as f:
            f.write("X = 1\n")
        sub = os.path.join(self.pkg, "sub")
        os.makedirs(sub)
        with open(os.path.join(sub, "__init__.py"), "w") as f:
            f.write("")
        with open(os.path.join(sub, "leaf.py"), "w") as f:
            f.write("Y = 2\n")

    def tearDown(self):
        sys.path.remove(self.tmp) if self.tmp in sys.path else None

    def test_iter_modules_finds_modules_and_packages(self):
        found = dict(iter_modules([self.tmp]))
        self.assertEqual(found, {"samplepkg": True})
        children = dict(iter_modules([self.pkg]))
        self.assertIn("mod", children)
        self.assertFalse(children["mod"])
        self.assertIn("sub", children)
        self.assertTrue(children["sub"])

    def test_iter_modules_applies_prefix(self):
        found = dict(iter_modules([self.tmp], prefix="pkg."))
        self.assertEqual(found, {"pkg.samplepkg": True})

    def test_iter_modules_rejects_string_path(self):
        with self.assertRaises(TypeError):
            iter_modules(self.tmp)

    def test_iter_modules_rejects_non_string_entries(self):
        with self.assertRaises(TypeError):
            iter_modules([1])

    def test_iter_modules_rejects_non_string_prefix(self):
        with self.assertRaises(TypeError):
            iter_modules([self.pkg], prefix=5)


    def test_walk_packages_finds_nested_modules(self):
        names = dict(walk_packages([self.pkg], prefix="samplepkg."))
        self.assertIn("samplepkg.mod", names)
        self.assertIn("samplepkg.sub", names)
        self.assertIn("samplepkg.sub.leaf", names)
        self.assertTrue(names["samplepkg.sub"])

    def test_walk_packages_rejects_non_callable_onerror(self):
        with self.assertRaises(TypeError):
            walk_packages([self.pkg], onerror="nope")

    def test_get_data_reads_bytes(self):
        sys.path.insert(0, self.tmp)
        try:
            data = get_data("samplepkg", "data.txt")
        finally:
            sys.path.remove(self.tmp)
        self.assertEqual(data, b"payload")

    def test_get_data_type_errors(self):
        with self.assertRaises(TypeError):
            get_data(1, "data.txt")
        with self.assertRaises(TypeError):
            get_data("samplepkg", 2)

    def test_read_text_decodes_contents(self):
        sys.path.insert(0, self.tmp)
        try:
            text = read_text("samplepkg", "data.txt")
        finally:
            sys.path.remove(self.tmp)
        self.assertEqual(text, "payload")

    def test_read_text_rejects_non_string_encoding(self):
        with self.assertRaises(TypeError):
            read_text("samplepkg", "data.txt", encoding=1)

    def test_resolve_name_returns_module(self):
        module = resolve_name("json")
        self.assertEqual(module.__name__, "json")

    def test_resolve_name_type_error(self):
        with self.assertRaises(TypeError):
            resolve_name(None)

    def test_iter_importers_returns_finders(self):
        importers = iter_importers("json")
        self.assertIsInstance(importers, list)
        self.assertTrue(len(importers) > 0)

    def test_iter_importers_type_error(self):
        with self.assertRaises(TypeError):
            iter_importers(1)

    def test_extend_path_returns_list(self):
        result = extend_path([self.tmp], "samplepkg")
        self.assertIsInstance(result, list)
        self.assertIn(self.tmp, result)

    def test_extend_path_type_errors(self):
        with self.assertRaises(TypeError):
            extend_path("not-a-list", "samplepkg")
        with self.assertRaises(TypeError):
            extend_path([], 1)

    def test_find_spec_returns_spec(self):
        spec = find_spec("json")
        self.assertIsNotNone(spec)
        self.assertEqual(spec.name, "json")

    def test_find_spec_type_error(self):
        with self.assertRaises(TypeError):
            find_spec(1)


if __name__ == "__main__":
    unittest.main()
