"""Tests for the state-delta verification guard.

``tools/verify_state_delta.py`` records the HEAD at which the verification
battery last passed in ``.kilo/last_verified.checkpoint`` and skips the
battery when the working tree is clean and no source-relevant file has
changed since that checkpoint. These tests exercise the pure helpers, the
marker round-trip, and the command-line entry point without corrupting the
real checkpoint: the marker path is pointed at a temporary file for the
marker tests, and the real marker is backed up and restored around the
``main`` tests that advance it.
"""

import importlib.util
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TOOL = ROOT / "tools" / "verify_state_delta.py"

#: The real checkpoint marker. ``TestMarker`` points the module-level ``MARKER``
#: global at a temporary file for its tests; that mutation leaked into the other
#: classes because the global is shared state. Saving and restoring it here keeps
#: every class independent and order-independent.
_REAL_MARKER = ROOT / ".kilo" / "last_verified.checkpoint"


def load_tool():
    """Return the state-delta guard module loaded from its file path."""
    spec = importlib.util.spec_from_file_location("verify_state_delta", TOOL)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


verify_state_delta = load_tool()


class TestPathsAndGlobs(unittest.TestCase):
    """Verify the module's configured paths and source globs."""

    def test_the_marker_lives_under_kilo(self):
        self.assertEqual(
            verify_state_delta.MARKER, ROOT / ".kilo" / "last_verified.checkpoint"
        )

    def test_the_source_globs_cover_the_editable_surface(self):
        globs = set(verify_state_delta.SOURCE_GLOBS)
        for expected in (
            "*.py",
            "Makefile",
            "pyproject.toml",
            "scaffold.sh",
            ".kilo/command/scaffold-project.md",
        ):
            self.assertIn(expected, globs)


class TestMarker(unittest.TestCase):
    """Verify the checkpoint marker read/write round-trip.

    The module-level ``MARKER`` global is shared state, so every test that
    repoints it must restore the real marker afterwards; otherwise the
    mutation leaks into ``TestPathsAndGlobs`` and ``TestMain`` and breaks their
    assertions about where the marker lives.
    """

    def setUp(self):
        self._saved_marker = verify_state_delta.MARKER

    def tearDown(self):
        verify_state_delta.MARKER = self._saved_marker

    def test_read_returns_none_when_the_marker_is_absent(self):
        with tempfile.TemporaryDirectory() as tmp:
            marker = Path(tmp) / "last_verified.checkpoint"
            verify_state_delta.MARKER = marker
            self.assertIsNone(verify_state_delta.read_marker())

    def test_read_returns_none_for_malformed_json(self):
        with tempfile.TemporaryDirectory() as tmp:
            marker = Path(tmp) / "last_verified.checkpoint"
            marker.write_text("not json {")
            verify_state_delta.MARKER = marker
            self.assertIsNone(verify_state_delta.read_marker())

    def test_write_then_read_round_trips(self):
        with tempfile.TemporaryDirectory() as tmp:
            marker = Path(tmp) / "last_verified.checkpoint"
            verify_state_delta.MARKER = marker
            verify_state_delta.write_marker({"head": "deadbeef"})
            self.assertEqual(verify_state_delta.read_marker(), {"head": "deadbeef"})


class TestRepositoryState(unittest.TestCase):
    """Verify the helpers that read live repository state."""

    def test_working_tree_clean_returns_a_bool(self):
        self.assertIsInstance(verify_state_delta.working_tree_clean(), bool)

    def test_head_returns_a_non_empty_hex_sha(self):
        head = verify_state_delta.head()
        self.assertTrue(head)
        self.assertTrue(all(c in "0123456789abcdef" for c in head))

    def test_source_changed_since_head_is_false(self):
        # HEAD..HEAD is an empty diff, so no source-relevant file changed.
        self.assertFalse(verify_state_delta.source_changed_since(verify_state_delta.head()))


class TestMain(unittest.TestCase):
    """Verify the command-line entry point and the --full flag.

    The prior session found a genuine gap here: the tool documented
    ``python tools/verify_state_delta.py [--full]`` to force the battery and
    always advance the checkpoint, but ``__main__`` invoked ``main()`` with no
    arguments, so ``--full`` was silently ignored and the checkpoint could
    never advance to the current HEAD. The real marker is backed up and
    restored so the repository is left exactly as it was found.
    """

    def setUp(self):
        self._original_marker = (
            verify_state_delta.MARKER.read_text()
            if verify_state_delta.MARKER.is_file()
            else None
        )

    def tearDown(self):
        if self._original_marker is None:
            verify_state_delta.MARKER.unlink(missing_ok=True)
        else:
            verify_state_delta.MARKER.write_text(self._original_marker)

    def test_full_flag_runs_the_battery_and_advances_the_checkpoint(self):
        # ``--full`` must force the battery and record the current HEAD in the
        # marker, regardless of what the marker held before. The prior
        # assertion (that the marker *changed*) was brittle: when the marker
        # already equalled HEAD, ``--full`` legitimately re-records the same
        # value and the test failed on a green repository.
        rc = verify_state_delta.main(["--full"])
        self.assertEqual(rc, 0)
        after = verify_state_delta.read_marker()
        self.assertIsNotNone(after)
        self.assertEqual(after["head"], verify_state_delta.head())

    def test_skip_on_unchanged_state_when_marker_matches_head(self):
        # After --full the marker equals HEAD; a second run must skip the
        # battery rather than re-running it.
        verify_state_delta.main(["--full"])
        rc = verify_state_delta.main([])
        self.assertEqual(rc, 0)

    def test_battery_failure_returns_one_and_leaves_the_marker_untouched(self):
        original = verify_state_delta.read_marker()
        original_battery_ok = verify_state_delta.battery_ok
        verify_state_delta.battery_ok = lambda: False  # type: ignore[assignment]
        try:
            rc = verify_state_delta.main(["--full"])
        finally:
            verify_state_delta.battery_ok = original_battery_ok  # type: ignore[assignment]
        self.assertEqual(rc, 1)
        self.assertEqual(verify_state_delta.read_marker(), original)


class TestCommandLine(unittest.TestCase):
    """Verify the command-line interface of the guard."""

    def test_the_check_mode_reports_a_synchronised_repository(self):
        result = subprocess.run(
            [sys.executable, str(TOOL), "--full"],
            capture_output=True,
            text=True,
            timeout=180,
            check=False,
        )
        self.assertEqual(result.returncode, 0, msg=result.stdout + result.stderr)
        self.assertIn("Verification passed", result.stdout)


if __name__ == "__main__":
    unittest.main()
