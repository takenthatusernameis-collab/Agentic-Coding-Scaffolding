"""Tests for the contract-audit tool."""

import importlib.util
import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TOOL = ROOT / "tools" / "audit_contracts.py"


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

    def test_a_syntax_error_marks_the_file_unparseable(self):
        issues, ok = audit_contracts.audit_source("def f(:\n", "m.py")
        self.assertFalse(ok)
        self.assertEqual(issues, [])


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


if __name__ == "__main__":
    unittest.main()
