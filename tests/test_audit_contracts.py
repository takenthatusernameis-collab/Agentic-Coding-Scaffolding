"""Tests for the contract-audit tool."""

import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TOOL = ROOT / "tools" / "audit_contracts.py"

#: A module whose documented exception is only raised one same-module helper
#: call below the audited function. Such a case is invisible at depth 0 and
#: detected at the default depth, which makes it a cheap probe for whether the
#: configured depth actually reaches the audit.
HELPER_RAISED_SOURCE = (
    "def require(x):\n"
    "    raise TypeError('bad')\n"
    "\n"
    "def f(x):\n"
    "    '''Summary.\n"
    "\n"
    "    Raises:\n"
    "        TypeError: If x is wrong.\n"
    "    '''\n"
    "    require(x)\n"
)


def load_tool():
    """Return the audit tool module loaded from its file path."""
    spec = importlib.util.spec_from_file_location("audit_contracts", TOOL)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


audit_contracts = load_tool()


class TestDocumentedRaises(unittest.TestCase):
    """Verify parsing of Raises: sections in docstrings."""

    def test_a_simple_raises_clause_is_parsed(self):
        doc = "Summary.\n\n    Raises:\n        TypeError: If x is wrong.\n"
        self.assertEqual(audit_contracts.documented_raises(doc), {"TypeError": 3})

    def test_a_multi_type_clause_is_parsed(self):
        doc = "Summary.\n\n    Raises:\n        TypeError, ValueError: If wrong.\n"
        parsed = audit_contracts.documented_raises(doc)
        self.assertEqual(set(parsed), {"TypeError", "ValueError"})

    def test_an_inline_raises_clause_is_parsed(self):
        doc = "Summary.\n\n    Raises: KeyError: If missing.\n"
        self.assertEqual(audit_contracts.documented_raises(doc), {"KeyError": 2})

    def test_a_section_after_raises_ends_the_block(self):
        doc = (
            "Summary.\n"
            "\n"
            "    Raises:\n"
            "        TypeError: If wrong.\n"
            "\n"
            "    Examples:\n"
            "        >>> 1\n"
            "        1\n"
        )
        self.assertEqual(audit_contracts.documented_raises(doc), {"TypeError": 3})

    def test_a_docstring_without_raises_returns_empty(self):
        self.assertEqual(audit_contracts.documented_raises("Just a summary."), {})
        self.assertEqual(audit_contracts.documented_raises(None), {})

    def test_a_lowercase_name_is_ignored(self):
        doc = "Summary.\n\n    Raises:\n        valueerror: lowercased.\n"
        self.assertEqual(audit_contracts.documented_raises(doc), {})

    def test_a_cross_reference_line_after_raises_is_not_an_exception(self):
        doc = (
            "Summary.\n"
            "\n"
            "    Raises:\n"
            "        AttributeError: If unsupported.\n"
            "\n"
            "    See :func:`ctypes.get_last_error`.\n"
        )
        self.assertEqual(audit_contracts.documented_raises(doc), {"AttributeError": 3})

    def test_a_doctest_after_raises_is_not_an_exception(self):
        doc = (
            "Summary.\n"
            "\n"
            "    Raises:\n"
            "        RuntimeError: If missing.\n"
            "\n"
            "    >>> has_topics()\n"
            "    True\n"
        )
        self.assertEqual(audit_contracts.documented_raises(doc), {"RuntimeError": 3})

    def test_a_wrapped_continuation_line_is_not_a_new_exception(self):
        doc = (
            "Summary.\n"
            "\n"
            "    Raises:\n"
            "        TypeError: If name is not a str or Path,\n"
            "            Path, or mode is not a str.\n"
            "        ValueError: If name is empty.\n"
        )
        parsed = audit_contracts.documented_raises(doc)
        self.assertEqual(set(parsed), {"TypeError", "ValueError"})


class TestDirectRaises(unittest.TestCase):
    """Verify extraction of raise statements from a function body."""

    def test_a_direct_raise_is_detected(self):
        tree = audit_contracts.ast.parse(
            "def f(x):\n"
            "    if x:\n"
            "        raise TypeError('bad')\n"
            "    return 1\n"
        )
        fn = tree.body[0]
        self.assertEqual(audit_contracts.direct_raises(fn), {"TypeError"})

    def test_a_raiser_in_a_helper_is_not_direct(self):
        tree = audit_contracts.ast.parse(
            "def f(x):\n"
            "    helper(x)\n"
        )
        fn = tree.body[0]
        self.assertEqual(audit_contracts.direct_raises(fn), set())

    def test_a_bare_raise_in_a_typed_except_handler_is_detected(self):
        tree = audit_contracts.ast.parse(
            "def f(x):\n"
            "    try:\n"
            "        x()\n"
            "    except ValueError:\n"
            "        raise\n"
        )
        fn = tree.body[0]
        self.assertEqual(audit_contracts.direct_raises(fn), {"ValueError"})

    def test_a_bare_raise_in_an_untyped_except_handler_is_ignored(self):
        tree = audit_contracts.ast.parse(
            "def f(x):\n"
            "    try:\n"
            "        x()\n"
            "    except:\n"
            "        raise\n"
        )
        fn = tree.body[0]
        self.assertEqual(audit_contracts.direct_raises(fn), set())

    def test_a_bare_raise_outside_a_handler_is_ignored(self):
        tree = audit_contracts.ast.parse(
            "def f(x):\n"
            "    raise\n"
        )
        fn = tree.body[0]
        self.assertEqual(audit_contracts.direct_raises(fn), set())

    def test_a_raise_of_the_bound_exception_name_resolves_to_the_handler_type(self):
        tree = audit_contracts.ast.parse(
            "def f(x):\n"
            "    try:\n"
            "        x()\n"
            "    except ValueError as exc:\n"
            "        raise exc\n"
        )
        fn = tree.body[0]
        self.assertEqual(audit_contracts.direct_raises(fn), {"ValueError"})

    def test_a_raise_of_the_bound_name_uses_the_handler_tuple_type(self):
        tree = audit_contracts.ast.parse(
            "def f(x):\n"
            "    try:\n"
            "        x()\n"
            "    except (ValueError, TypeError) as exc:\n"
            "        raise exc\n"
        )
        fn = tree.body[0]
        self.assertEqual(audit_contracts.direct_raises(fn), {"ValueError", "TypeError"})

    def test_a_raise_of_an_unrelated_name_is_treated_as_a_type(self):
        tree = audit_contracts.ast.parse(
            "def f(x):\n"
            "    raise err\n"
        )
        fn = tree.body[0]
        self.assertEqual(audit_contracts.direct_raises(fn), {"err"})


class TestRaisesClosure(unittest.TestCase):
    """Verify transitive raise detection through same-module helpers."""

    def test_a_helper_raise_is_followed(self):
        source = (
            "def helper(x):\n"
            "    raise ValueError('bad')\n"
            "\n"
            "def f(x):\n"
            "    helper(x)\n"
        )
        tree = audit_contracts.ast.parse(source)
        index = audit_contracts.build_index(tree)
        fn = index["f"]
        self.assertIn("ValueError", audit_contracts.raises_closure(fn, index, 3))

    def test_the_depth_bound_stops_the_traversal(self):
        source = (
            "def helper(x):\n"
            "    raise ValueError('bad')\n"
            "\n"
            "def f(x):\n"
            "    helper(x)\n"
        )
        tree = audit_contracts.ast.parse(source)
        index = audit_contracts.build_index(tree)
        fn = index["f"]
        self.assertEqual(audit_contracts.raises_closure(fn, index, 0), set())

    def test_a_cyclic_call_graph_terminates(self):
        source = (
            "def a():\n"
            "    b()\n"
            "\n"
            "def b():\n"
            "    a()\n"
        )
        tree = audit_contracts.ast.parse(source)
        index = audit_contracts.build_index(tree)
        fn = index["a"]
        self.assertEqual(audit_contracts.raises_closure(fn, index, 5), set())


class TestClassInitDelegation(unittest.TestCase):
    """Verify raises raised by a same-module class ``__init__`` are followed."""

    INIT_RAISES_SOURCE = (
        "class Widget:\n"
        "    def __init__(self, interval):\n"
        "        if interval <= 0:\n"
        "            raise ValueError('interval must be positive')\n"
        "\n"
        "def make(interval):\n"
        "    '''Summary.\n"
        "\n"
        "    Raises:\n"
        "        ValueError: If interval is not positive.\n"
        "    '''\n"
        "    return Widget(interval)\n"
    )

    def test_a_raise_in_a_same_module_class_init_is_followed(self):
        tree = audit_contracts.ast.parse(self.INIT_RAISES_SOURCE)
        index = audit_contracts.build_index(tree)
        fn = index["make"]
        self.assertIn("ValueError", audit_contracts.raises_closure(fn, index, 3))

    def test_delegated_class_init_raise_is_not_reported(self):
        issues, ok = audit_contracts.audit_source(self.INIT_RAISES_SOURCE, "m.py")
        self.assertTrue(ok)
        self.assertEqual(issues, [])

    def test_a_class_init_that_does_not_raise_is_still_reported(self):
        source = (
            "class Widget:\n"
            "    def __init__(self, value):\n"
            "        self.value = value\n"
            "\n"
            "def make(value):\n"
            "    '''Summary.\n"
            "\n"
            "    Raises:\n"
            "        TypeError: If value is wrong.\n"
            "    '''\n"
            "    return Widget(value)\n"
        )
        issues, ok = audit_contracts.audit_source(source, "m.py")
        self.assertTrue(ok)
        self.assertEqual([issue["exception"] for issue in issues], ["TypeError"])

    def test_a_class_without_init_is_treated_as_raising_nothing(self):
        source = (
            "class Widget:\n"
            "    pass\n"
            "\n"
            "def make(value):\n"
            "    '''Summary.\n"
            "\n"
            "    Raises:\n"
            "        TypeError: If value is wrong.\n"
            "    '''\n"
            "    return Widget()\n"
        )
        issues, ok = audit_contracts.audit_source(source, "m.py")
        self.assertTrue(ok)
        self.assertEqual([issue["exception"] for issue in issues], ["TypeError"])


class TestAuditSource(unittest.TestCase):
    """Verify the end-to-end audit over a source string."""

    def test_a_documented_but_unraised_exception_is_reported(self):
        source = (
            "def f(x):\n"
            "    '''Summary.\n"
            "\n"
            "    Raises:\n"
            "        TypeError: If x is wrong.\n"
            "    '''\n"
            "    return x\n"
        )
        issues, ok = audit_contracts.audit_source(source, "m.py")
        self.assertTrue(ok)
        self.assertEqual(len(issues), 1)
        self.assertEqual(issues[0]["function"], "f")
        self.assertEqual(issues[0]["exception"], "TypeError")

    def test_a_documented_and_raised_exception_is_not_reported(self):
        source = (
            "def f(x):\n"
            "    '''Summary.\n"
            "\n"
            "    Raises:\n"
            "        TypeError: If x is wrong.\n"
            "    '''\n"
            "    raise TypeError('bad')\n"
        )
        issues, ok = audit_contracts.audit_source(source, "m.py")
        self.assertTrue(ok)
        self.assertEqual(issues, [])

    def test_a_documented_exception_raised_via_a_bare_reraise_is_not_reported(self):
        source = (
            "def f(x):\n"
            "    '''Summary.\n"
            "\n"
            "    Raises:\n"
            "        ValueError: If x is wrong.\n"
            "    '''\n"
            "    try:\n"
            "        x()\n"
            "    except ValueError:\n"
            "        raise\n"
        )
        issues, ok = audit_contracts.audit_source(source, "m.py")
        self.assertTrue(ok)
        self.assertEqual(issues, [])

    def test_a_documented_exception_reraised_by_name_is_not_reported(self):
        source = (
            "def f(x):\n"
            "    '''Summary.\n"
            "\n"
            "    Raises:\n"
            "        ValueError: If x is wrong.\n"
            "    '''\n"
            "    try:\n"
            "        x()\n"
            "    except ValueError as exc:\n"
            "        raise exc\n"
        )
        issues, ok = audit_contracts.audit_source(source, "m.py")
        self.assertTrue(ok)
        self.assertEqual(issues, [])

    def test_a_documented_exception_raised_via_a_helper_is_not_reported(self):
        source = (
            "def require(x):\n"
            "    raise TypeError('bad')\n"
            "\n"
            "def f(x):\n"
            "    '''Summary.\n"
            "\n"
            "    Raises:\n"
            "        TypeError: If x is wrong.\n"
            "    '''\n"
            "    require(x)\n"
        )
        issues, ok = audit_contracts.audit_source(source, "m.py")
        self.assertTrue(ok)
        self.assertEqual(issues, [])

    def test_a_cross_reference_line_is_not_reported_as_an_exception(self):
        source = (
            "def f(x):\n"
            "    '''Summary.\n"
            "\n"
            "    Raises:\n"
            "        AttributeError: If unsupported.\n"
            "\n"
            "    See :func:`ctypes.get_last_error`.\n"
            "    '''\n"
            "    return x\n"
        )
        issues, ok = audit_contracts.audit_source(source, "m.py")
        self.assertTrue(ok)
        self.assertEqual([issue["exception"] for issue in issues], ["AttributeError"])

    def test_a_syntax_error_marks_the_file_unparseable(self):
        issues, ok = audit_contracts.audit_source("def f(:\n", "m.py")
        self.assertFalse(ok)
        self.assertEqual(issues, [])


class TestIgnoredRaises(unittest.TestCase):
    """Verify ``# audit-ignore:`` suppression of low-signal delegations."""

    def test_ignore_comment_on_the_raises_line_suppresses_the_type(self):
        source = (
            "def f(x):\n"
            "    '''Summary.\n"
            "\n"
            "    Raises:\n"
            "        OSError: If the file is missing.  # audit-ignore: OSError\n"
            "    '''\n"
            "    return open(x).read()\n"
        )
        issues, ok = audit_contracts.audit_source(source, "m.py")
        self.assertTrue(ok)
        self.assertEqual(issues, [])

    def test_ignore_comment_in_the_body_suppresses_the_type(self):
        source = (
            "def f(x):\n"
            "    '''Summary.\n"
            "\n"
            "    Raises:\n"
            "        ValueError: If x is wrong.\n"
            "    '''\n"
            "    return x.remove(1)  # audit-ignore: ValueError\n"
        )
        issues, ok = audit_contracts.audit_source(source, "m.py")
        self.assertTrue(ok)
        self.assertEqual(issues, [])

    def test_ignore_comment_lists_multiple_types(self):
        source = (
            "def f(x):\n"
            "    '''Summary.\n"
            "\n"
            "    Raises:\n"
            "        OSError: If the file is missing.\n"
            "        ValueError: If x is wrong.\n"
            "    '''\n"
            "    return x  # audit-ignore: OSError, ValueError\n"
        )
        issues, ok = audit_contracts.audit_source(source, "m.py")
        self.assertTrue(ok)
        self.assertEqual(issues, [])

    def test_ignore_comment_only_suppresses_the_named_type(self):
        source = (
            "def f(x):\n"
            "    '''Summary.\n"
            "\n"
            "    Raises:\n"
            "        OSError: If the file is missing.\n"
            "        TypeError: If x is wrong.\n"
            "    '''\n"
            "    return x  # audit-ignore: OSError\n"
        )
        issues, ok = audit_contracts.audit_source(source, "m.py")
        self.assertTrue(ok)
        self.assertEqual([issue["exception"] for issue in issues], ["TypeError"])

    def test_ignore_comment_does_not_leak_to_a_later_function(self):
        source = (
            "def f(x):\n"
            "    '''Summary.\n"
            "\n"
            "    Raises:\n"
            "        OSError: If the file is missing.  # audit-ignore: OSError\n"
            "    '''\n"
            "    return x\n"
            "\n"
            "def g(x):\n"
            "    '''Summary.\n"
            "\n"
            "    Raises:\n"
            "        OSError: If the file is missing.\n"
            "    '''\n"
            "    return x\n"
        )
        issues, ok = audit_contracts.audit_source(source, "m.py")
        self.assertTrue(ok)
        self.assertEqual([issue["function"] for issue in issues], ["g"])
        self.assertEqual([issue["exception"] for issue in issues], ["OSError"])

    def test_a_lowercase_ignore_name_is_ignored(self):
        source = (
            "def f(x):\n"
            "    '''Summary.\n"
            "\n"
            "    Raises:\n"
            "        OSError: If the file is missing.\n"
            "    '''\n"
            "    return x  # audit-ignore: oserror\n"
        )
        issues, ok = audit_contracts.audit_source(source, "m.py")
        self.assertTrue(ok)
        self.assertEqual([issue["exception"] for issue in issues], ["OSError"])

    def test_ignored_raises_returns_only_exception_like_names(self):
        source = (
            "def f(x):\n"
            "    return x  # audit-ignore: OSError, ValueError, not_a_type, 123\n"
        )
        fn = audit_contracts.ast.parse(source).body[0]
        self.assertEqual(
            audit_contracts.ignored_raises(source, fn),
            {"OSError", "ValueError"},
        )


class TestDepthPropagation(unittest.TestCase):
    """Verify the configured helper-call depth reaches the audit."""

    def test_audit_source_honours_a_zero_depth(self):
        issues, ok = audit_contracts.audit_source(
            HELPER_RAISED_SOURCE, "m.py", depth=0
        )
        self.assertTrue(ok)
        self.assertEqual([issue["exception"] for issue in issues], ["TypeError"])

    def test_audit_source_follows_helpers_at_the_default_depth(self):
        issues, ok = audit_contracts.audit_source(HELPER_RAISED_SOURCE, "m.py")
        self.assertTrue(ok)
        self.assertEqual(issues, [])

    def test_audit_paths_honours_the_depth(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "m.py"
            path.write_text(HELPER_RAISED_SOURCE)
            shallow, shallow_errors = audit_contracts.audit_paths([path], depth=0)
            deep, deep_errors = audit_contracts.audit_paths([path], depth=3)
        self.assertEqual(shallow_errors, [])
        self.assertEqual(deep_errors, [])
        self.assertEqual(len(shallow), 1)
        self.assertEqual(deep, [])


class TestFormatText(unittest.TestCase):
    """Verify the human-readable report."""

    def test_the_summary_line_counts_files_and_issues(self):
        issues = [
            {"path": "a.py", "line": 3, "function": "f", "exception": "TypeError"},
        ]
        report = audit_contracts.format_text(issues, scanned=1)
        self.assertIn("a.py:3: f: documents Raises: TypeError but never raises it", report)
        self.assertIn("Scanned 1 file(s); 1 potential contract issue(s).", report)


class TestCli(unittest.TestCase):
    """Verify the command-line entry point end-to-end."""

    def _run(self, *args: str) -> subprocess.CompletedProcess:
        return subprocess.run(
            [sys.executable, str(TOOL), *args],
            capture_output=True,
            text=True,
            cwd=str(ROOT),
        )

    def test_json_output_is_valid(self):
        result = self._run("--json", "case_utils.py")
        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(result.stdout)
        self.assertIn("scanned", payload)
        self.assertIn("issues", payload)

    def test_summary_output_lists_counts(self):
        result = self._run("--summary", "case_utils.py")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Scanned", result.stdout)

    def test_a_negative_depth_is_rejected(self):
        result = self._run("--depth", "-1", "case_utils.py")
        self.assertEqual(result.returncode, 2)
        self.assertIn("non-negative", result.stderr)

    def test_a_clean_file_reports_no_issues(self):
        result = self._run("--json", "case_utils.py")
        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["issues"], [])

    def test_the_depth_flag_changes_the_reported_issues(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "sample.py"
            path.write_text(HELPER_RAISED_SOURCE)
            default = self._run("--json", str(path))
            shallow = self._run("--json", "--depth", "0", str(path))
        self.assertEqual(default.returncode, 0, default.stderr)
        self.assertEqual(shallow.returncode, 0, shallow.stderr)
        self.assertEqual(json.loads(default.stdout)["issues"], [])
        self.assertEqual(len(json.loads(shallow.stdout)["issues"]), 1)


if __name__ == "__main__":
    unittest.main()
