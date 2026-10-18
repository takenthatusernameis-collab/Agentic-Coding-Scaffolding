import ast
import unittest

from ast_utils import (
    copy_location,
    dump,
    find_all,
    fix_missing_locations,
    get_docstring,
    increment_lineno,
    iter_child_nodes,
    iter_fields,
    literal_eval,
    node_to_string,
    parse,
    unparse,
    walk,
)


class TestAstUtils(unittest.TestCase):
    def test_parse_exec(self):
        node = parse("x = 1")
        self.assertIsInstance(node, ast.Module)

    def test_parse_eval(self):
        node = parse("1 + 2", mode="eval")
        self.assertIsInstance(node, ast.Expression)

    def test_parse_type_error(self):
        with self.assertRaises(TypeError):
            parse(123)

    def test_parse_value_error(self):
        with self.assertRaises(ValueError):
            parse("x", mode="bad")

    def test_unparse(self):
        node = parse("x = 1")
        self.assertEqual(unparse(node).strip(), "x = 1")

    def test_dump(self):
        node = parse("x = 1")
        self.assertIn("Assign", dump(node))

    def test_literal_eval(self):
        self.assertEqual(literal_eval("[1, 2, 3]"), [1, 2, 3])

    def test_get_docstring(self):
        src = 'def f():\n    """doc"""\n    pass'
        node = parse(src)
        func = node.body[0]
        self.assertEqual(get_docstring(func), "doc")

    def test_walk(self):
        node = parse("x = 1")
        self.assertTrue(any(isinstance(n, ast.Assign) for n in walk(node)))

    def test_iter_fields(self):
        node = parse("x = 1")
        fields = iter_fields(node.body[0])
        self.assertTrue(any(k == "targets" for k, _ in fields))

    def test_iter_child_nodes(self):
        node = parse("x = 1")
        children = iter_child_nodes(node)
        self.assertTrue(len(children) >= 1)

    def test_find_all(self):
        node = parse("a = 1\nb = 2")
        assigns = find_all(node, ast.Assign)
        self.assertEqual(len(assigns), 2)

    def test_fix_missing_locations(self):
        node = parse("x = 1")
        self.assertIs(fix_missing_locations(node), node)

    def test_increment_lineno(self):
        node = parse("x = 1")
        new = increment_lineno(node, 2)
        self.assertIsNotNone(new)

    def test_increment_lineno_type_error(self):
        node = parse("x = 1")
        with self.assertRaises(TypeError):
            increment_lineno(node, "a")

    def test_copy_location(self):
        n1 = ast.Assign(targets=[ast.Name(id="x", ctx=ast.Store())], value=ast.Constant(value=1))
        n2 = ast.Assign(targets=[ast.Name(id="y", ctx=ast.Store())], value=ast.Constant(value=2))
        self.assertIs(copy_location(n1, n2), n1)

    def test_node_to_string(self):
        node = parse("x = 1")
        self.assertIn("x", node_to_string(node))


if __name__ == "__main__":
    unittest.main()
