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
            "tools/*.py",
        ):
            self.assertIn(expected, globs)

    def test_the_source_globs_cover_the_templated_document_copies(self):
        # ``refresh_scaffold.py`` embeds these documents as templates and
        # ``tests.test_scaffold_sync`` asserts they stay in sync, so editing one
        # of them must invalidate the checkpoint instead of skipping the battery.
        spec = importlib.util.spec_from_file_location(
            "refresh_scaffold", ROOT / "tools" / "refresh_scaffold.py"
        )
        assert spec is not None and spec.loader is not None
        refresh_scaffold = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(refresh_scaffold)
        globs = set(verify_state_delta.SOURCE_GLOBS)
        for name in refresh_scaffold.TEMPLATED_COPIES:
            self.assertIn(name, globs, msg=name)

    def test_the_source_globs_are_relative_paths(self):
        # The globs are passed to ``git diff`` as pathspecs relative to the
        # repository root, so an absolute path would silently match nothing.
        for glob in verify_state_delta.SOURCE_GLOBS:
            self.assertFalse(glob.startswith("/"), msg=glob)

    def test_the_battery_includes_the_scaffold_sync_invariant(self):
        # ``make verify`` runs the scaffold-sync test; the state-delta guard must
        # not advance its checkpoint past a broken README/pyproject/scaffold
        # synchronization. Capture the battery's commands without executing them
        # by stubbing ``run`` for the duration of the call.
        captured: list[list[str]] = []
        original_run = verify_state_delta.run

        def fake_run(cmd: list[str], timeout: float = 30.0):
            captured.append(list(cmd))
            return subprocess.CompletedProcess(cmd, 0, "", "")

        verify_state_delta.run = fake_run  # type: ignore[assignment]
        try:
            ok = verify_state_delta.battery_ok()
        finally:
            verify_state_delta.run = original_run  # type: ignore[assignment]
        self.assertTrue(ok)
        joined = [" ".join(cmd) for cmd in captured]
        self.assertTrue(
            any("tests.test_scaffold_sync" in entry for entry in joined),
            msg=f"scaffold sync missing from battery: {joined}",
        )

    def test_the_battery_includes_the_doctest_suite(self):
        # The doctests are the executable specification of every module's
        # documented examples, and they are the only thing that executes them.
        # The battery previously omitted them, so a factually wrong example in a
        # docstring survived every session that ran ``make verify``: the doctest
        # suite failed while the battery stayed green and the checkpoint still
        # advanced. The battery must run the doctest suite so such a regression
        # blocks the checkpoint instead of being masked by it.
        captured: list[list[str]] = []
        original_run = verify_state_delta.run

        def fake_run(cmd: list[str], timeout: float = 30.0):
            captured.append(list(cmd))
            return subprocess.CompletedProcess(cmd, 0, "", "")

        verify_state_delta.run = fake_run  # type: ignore[assignment]
        try:
            ok = verify_state_delta.battery_ok()
        finally:
            verify_state_delta.run = original_run  # type: ignore[assignment]
        self.assertTrue(ok)
        joined = [" ".join(cmd) for cmd in captured]
        self.assertTrue(
            any("tests.test_doctests" in entry for entry in joined),
            msg=f"doctest suite missing from battery: {joined}",
        )

    def test_the_battery_fails_when_the_doctest_suite_fails(self):
        # A battery that merely lists the doctest suite is not enough: the
        # suite's exit status has to fail the battery, otherwise a broken
        # example still advances the checkpoint. Stub ``run`` so only the
        # doctest command reports failure.
        original_run = verify_state_delta.run

        def fake_run(cmd: list[str], timeout: float = 30.0):
            code = 1 if "tests.test_doctests" in " ".join(cmd) else 0
            return subprocess.CompletedProcess(cmd, code, "", "")

        verify_state_delta.run = fake_run  # type: ignore[assignment]
        try:
            ok = verify_state_delta.battery_ok()
        finally:
            verify_state_delta.run = original_run  # type: ignore[assignment]
        self.assertFalse(ok)

    def test_the_battery_ignores_stderr_when_a_check_succeeds(self):
        # Warnings emitted on stderr (e.g. ResourceWarnings from doctest modules
        # using tempfile) must not be treated as a failure when the exit code
        # is 0.
        original_run = verify_state_delta.run
        reported: list[str] = []

        def fake_run(cmd: list[str], timeout: float = 30.0):
            return subprocess.CompletedProcess(cmd, 0, "", "ResourceWarning: temp")

        import builtins
        original_print = builtins.print

        def fake_print(*args, **kwargs):
            reported.append(" ".join(str(a) for a in args))

        verify_state_delta.run = fake_run  # type: ignore[assignment]
        builtins.print = fake_print  # type: ignore[assignment]
        try:
            ok = verify_state_delta.battery_ok()
        finally:
            verify_state_delta.run = original_run  # type: ignore[assignment]
            builtins.print = original_print  # type: ignore[assignment]
        self.assertTrue(ok)
        self.assertEqual(reported, [])


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


class TestMakefileVerifyTarget(unittest.TestCase):
    """Verify the ``make verify`` target agrees with the battery.

    ``make verify`` is the documented manual entry point for the same
    foundation checks the state-delta guard runs. When it lagged behind the
    battery it silently stopped enforcing a check, so the target is held to the
    suites the battery runs rather than being allowed to drift.
    """

    def test_verify_target_delegates_to_state_delta_guard(self):
        # ``make verify`` must delegate to the state-delta guard so a clean,
        # unchanged tree skips the redundant verification battery instead of
        # re-running every check serially on every invocation.
        text = (ROOT / "Makefile").read_text()
        self.assertIn("tools/verify_state_delta.py", text)

    def test_test_target_runs_the_doctest_suite_on_a_clean_tree(self):
        # The clean-tree fast path of ``make test`` skips the full suite, so it
        # has to keep the doctest suite: it is the only thing that executes the
        # documented examples and it runs in about a second.
        text = (ROOT / "Makefile").read_text()
        self.assertIn("tests.test_public_api tests.test_doctests", text)


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
        # When the working tree has uncommitted changes the helper also
        # reports them, so only assert the negative on a clean tree.
        if verify_state_delta.working_tree_clean():
            self.assertFalse(
                verify_state_delta.source_changed_since(verify_state_delta.head())
            )
        else:
            changed = verify_state_delta.diff_since(verify_state_delta.head())
            self.assertIsInstance(changed, list)

    def test_diff_since_returns_only_source_globs(self):
        # ``diff_since`` lists every changed file between *ref* and the
        # working tree, filtered to SOURCE_GLOBS.
        if verify_state_delta.working_tree_clean():
            self.assertEqual(verify_state_delta.diff_since(verify_state_delta.head()), [])
        else:
            changed = verify_state_delta.diff_since(verify_state_delta.head())
            for path in changed:
                is_source = path.endswith(".py") or any(
                    marker in path
                    for marker in (
                        "Makefile",
                        "pyproject",
                        "scaffold.sh",
                        "README",
                        "AGENTS",
                        "CHANGELOG",
                    )
                )
                self.assertTrue(is_source, f"unexpected path {path!r}")

    def test_source_changed_since_an_unknown_ref_is_true(self):
        # An unknown ref (rebase, force-push, shallow clone) makes ``git diff``
        # fail; the guard must treat that as a change so the battery still runs
        # instead of trusting a checkpoint it cannot compare.
        self.assertTrue(verify_state_delta.source_changed_since("0" * 40))


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
        # The real verification battery costs ~1.2 s per invocation and this
        # class previously ran it twice (once per ``--full`` call). The battery
        # itself is covered end-to-end by ``TestCommandLine``, which invokes
        # the tool as a subprocess. These control-flow tests stub ``battery_ok``
        # so they exercise the marker advancement and skip logic without the
        # redundant in-process cost. ``test_battery_failure_returns_one...``
        # still overrides the stub to False.
        self._original_battery_ok = verify_state_delta.battery_ok
        verify_state_delta.battery_ok = lambda: True  # type: ignore[assignment]

    def tearDown(self):
        verify_state_delta.battery_ok = self._original_battery_ok  # type: ignore[assignment]
        if self._original_marker is None:
            verify_state_delta.MARKER.unlink(missing_ok=True)
        else:
            verify_state_delta.MARKER.write_text(self._original_marker)

    def test_full_flag_runs_the_battery_and_advances_the_checkpoint(self):
        # ``--full`` must force the battery and record the current HEAD in the
        # marker, regardless of what the marker held before. The prior
        # assertion (that the marker *changed*) was brittle: when the marker
        # already equalled HEAD, ``--full`` legitimately re-records the same
        # value and the test failed on a green repository. The battery itself
        # is stubbed here; its real execution is covered by ``TestCommandLine``.
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
        verify_state_delta.battery_ok = lambda: False  # type: ignore[assignment]
        try:
            rc = verify_state_delta.main(["--full"])
        finally:
            verify_state_delta.battery_ok = self._original_battery_ok  # type: ignore[assignment]
        self.assertEqual(rc, 1)
        self.assertEqual(verify_state_delta.read_marker(), original)


class TestCommandLine(unittest.TestCase):
    """Verify the command-line interface of the guard.

    This subprocess invocation is the end-to-end coverage that the real
    verification battery executes successfully from the command line.
    """

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
