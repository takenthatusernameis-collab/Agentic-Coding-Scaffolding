"""Utilities for working with Python abstract syntax trees (wrapping :mod:`ast`)."""

import ast as _ast


def parse(source, filename="<unknown>", mode="exec"):
    if not isinstance(source, str):
        raise TypeError("source must be a str")
    if not isinstance(filename, str):
        raise TypeError("filename must be a str")
    if mode not in ("exec", "eval", "single"):
        raise ValueError("mode must be one of 'exec', 'eval', 'single'")
    return _ast.parse(source, filename=filename, mode=mode)


def unparse(node):
    return _ast.unparse(node)


def dump(node, annotate_fields=True, include_attributes=False, indent=None):
    return _ast.dump(
        node,
        annotate_fields=annotate_fields,
        include_attributes=include_attributes,
        indent=indent,
    )


def literal_eval(node_or_string):
    return _ast.literal_eval(node_or_string)


def get_docstring(node, clean=True):
    return _ast.get_docstring(node, clean=clean)


def walk(node):
    return list(_ast.walk(node))


def iter_fields(node):
    return list(_ast.iter_fields(node))


def iter_child_nodes(node):
    return list(_ast.iter_child_nodes(node))


def find_all(node, node_type):
    result = [n for n in _ast.walk(node) if isinstance(n, node_type)]
    return result


def fix_missing_locations(node):
    return _ast.fix_missing_locations(node)


def increment_lineno(node, n=1):
    if not isinstance(n, int):
        raise TypeError("n must be an int")
    return _ast.increment_lineno(node, n=n)


def copy_location(new_node, old_node):
    return _ast.copy_location(new_node, old_node)


def node_to_string(node):
    return _ast.unparse(node)
