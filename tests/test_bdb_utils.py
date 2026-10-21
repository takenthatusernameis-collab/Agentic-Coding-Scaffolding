"""Tests for bdb_utils."""

import bdb
import os
import sys
import types
import unittest

import bdb_utils
from bdb_utils import (
    Bdb,
    BdbQuit,
    Breakpoint,
    breakpoint_hits,
    canonical_filename,
    checkfuncname,
    clear_all_breakpoints,
    clear_breakpoint,
    clear_breakpoints,
    create_bdb,
    disable_breakpoint,
    effective_breakpoint,
    enable_breakpoint,
    get_breakpoint,
    get_breakpoints,
    get_file_breakpoints,
    is_bdb_instance,
    is_breakpoint,
    is_breakpoint_enabled,
    set_breakpoint,
)


def _frame_and_line() -> tuple[types.FrameType, int]:
    """Return a frame of this file together with the line it stopped at."""
    frame = sys._getframe()
    return frame, frame.f_lineno


class TestModuleContract(unittest.TestCase):
    """Verify the contract of the module."""

    def test_all_is_sorted_and_unique(self):
        self.assertEqual(bdb_utils.__all__, sorted(set(bdb_utils.__all__)))

    def test_every_name_exists(self):
        for name in bdb_utils.__all__:
            self.assertTrue(hasattr(bdb_utils, name), name)

    def test_the_standard_library_classes_are_re_exported(self):
        self.assertIs(Bdb, bdb.Bdb)
        self.assertIs(Breakpoint, bdb.Breakpoint)
        self.assertIs(BdbQuit, bdb.BdbQuit)


class TestDebuggerCreation(unittest.TestCase):
    """Verify the helpers that create a debugger."""

    def test_create_bdb_returns_a_debugger(self):
        debugger = create_bdb()
        self.assertIsInstance(debugger, Bdb)
        self.assertTrue(is_bdb_instance(debugger))

    def test_create_bdb_accepts_skip_patterns(self):
        debugger = create_bdb(skip=["unittest", "doctest"])
        self.assertIn("unittest", debugger.skip)

    def test_create_bdb_rejects_a_single_string(self):
        with self.assertRaises(TypeError):
            create_bdb(skip="unittest")

    def test_create_bdb_rejects_a_bad_container(self):
        with self.assertRaises(TypeError):
            create_bdb(skip=42)

    def test_create_bdb_rejects_a_bad_entry(self):
        with self.assertRaises(TypeError):
            create_bdb(skip=[42])

    def test_is_bdb_instance_rejects_other_objects(self):
        self.assertFalse(is_bdb_instance("not a debugger"))


class TestCanonicalFilename(unittest.TestCase):
    """Verify the helper that canonicalizes a file name."""

    def test_canonical_filename_is_absolute(self):
        self.assertTrue(os.path.isabs(canonical_filename("example.py")))

    def test_canonical_filename_rejects_a_bad_type(self):
        with self.assertRaises(TypeError):
            canonical_filename(42)

    def test_canonical_filename_rejects_an_empty_name(self):
        with self.assertRaises(ValueError):
            canonical_filename("")


class TestBreakpoints(unittest.TestCase):
    """Verify the helpers that manage the breakpoints of a session."""

    def setUp(self):
        clear_all_breakpoints()

    def tearDown(self):
        clear_all_breakpoints()

    def test_set_breakpoint_registers_the_breakpoint(self):
        bp = set_breakpoint(__file__, 12)
        self.assertIsInstance(bp, Breakpoint)
        self.assertTrue(is_breakpoint(bp))
        self.assertEqual(get_breakpoints(), {bp.number: bp})

    def test_set_breakpoint_keeps_the_line(self):
        self.assertEqual(set_breakpoint(__file__, 12).line, 12)

    def test_set_breakpoint_canonicalizes_the_file(self):
        bp = set_breakpoint("example.py", 12)
        self.assertEqual(bp.file, canonical_filename("example.py"))

    def test_set_breakpoint_rejects_a_bad_line(self):
        with self.assertRaises(TypeError):
            set_breakpoint(__file__, "12")
        with self.assertRaises(ValueError):
            set_breakpoint(__file__, 0)

    def test_set_breakpoint_rejects_a_bad_condition(self):
        with self.assertRaises(TypeError):
            set_breakpoint(__file__, 12, cond=42)

    def test_set_breakpoint_rejects_a_bad_function_name(self):
        with self.assertRaises(TypeError):
            set_breakpoint(__file__, 12, funcname=42)

    def test_set_breakpoint_rejects_a_bad_temporary_flag(self):
        with self.assertRaises(TypeError):
            set_breakpoint(__file__, 12, temporary="yes")

    def test_get_breakpoint_returns_the_breakpoint(self):
        bp = set_breakpoint(__file__, 12)
        self.assertIs(get_breakpoint(bp.number), bp)

    def test_get_breakpoint_returns_none_for_an_unknown_number(self):
        self.assertIsNone(get_breakpoint(9999))

    def test_get_breakpoint_rejects_a_bad_number(self):
        with self.assertRaises(TypeError):
            get_breakpoint("1")
        with self.assertRaises(ValueError):
            get_breakpoint(-1)

    def test_get_file_breakpoints_finds_the_breakpoint(self):
        bp = set_breakpoint(__file__, 12)
        self.assertEqual(get_file_breakpoints(__file__), [bp])

    def test_get_file_breakpoints_ignores_other_files(self):
        set_breakpoint(__file__, 12)
        self.assertEqual(get_file_breakpoints("other.py"), [])

    def test_clear_breakpoint_removes_the_breakpoint(self):
        bp = set_breakpoint(__file__, 12)
        self.assertTrue(clear_breakpoint(bp))
        self.assertEqual(get_breakpoints(), {})

    def test_clear_breakpoint_reports_an_unknown_breakpoint(self):
        bp = set_breakpoint(__file__, 12)
        clear_breakpoint(bp)
        self.assertFalse(clear_breakpoint(bp))

    def test_clear_breakpoint_rejects_other_objects(self):
        with self.assertRaises(TypeError):
            clear_breakpoint("not a breakpoint")

    def test_clear_breakpoints_removes_the_breakpoints_of_a_file(self):
        set_breakpoint(__file__, 12)
        set_breakpoint(__file__, 13)
        self.assertEqual(clear_breakpoints(__file__), 2)
        self.assertEqual(get_breakpoints(), {})

    def test_clear_all_breakpoints_empties_the_registry(self):
        set_breakpoint(__file__, 12)
        self.assertEqual(clear_all_breakpoints(), 1)
        self.assertEqual(get_breakpoints(), {})


class TestBreakpointState(unittest.TestCase):
    """Verify the helpers that read and change the state of a breakpoint."""

    def setUp(self):
        clear_all_breakpoints()

    def tearDown(self):
        clear_all_breakpoints()

    def test_a_new_breakpoint_is_enabled(self):
        self.assertTrue(is_breakpoint_enabled(set_breakpoint(__file__, 12)))

    def test_disable_and_enable_change_the_state(self):
        bp = set_breakpoint(__file__, 12)
        disable_breakpoint(bp)
        self.assertFalse(is_breakpoint_enabled(bp))
        enable_breakpoint(bp)
        self.assertTrue(is_breakpoint_enabled(bp))

    def test_the_hits_of_a_new_breakpoint_are_zero(self):
        self.assertEqual(breakpoint_hits(set_breakpoint(__file__, 12)), 0)

    def test_the_helpers_reject_other_objects(self):
        with self.assertRaises(TypeError):
            disable_breakpoint("not a breakpoint")
        with self.assertRaises(TypeError):
            enable_breakpoint("not a breakpoint")
        with self.assertRaises(TypeError):
            is_breakpoint_enabled("not a breakpoint")
        with self.assertRaises(TypeError):
            breakpoint_hits("not a breakpoint")


class TestEffectiveBreakpoint(unittest.TestCase):
    """Verify the helper that finds the breakpoint of a line of code."""

    def setUp(self):
        clear_all_breakpoints()

    def tearDown(self):
        clear_all_breakpoints()

    def test_a_location_without_a_breakpoint_is_not_effective(self):
        frame, line = _frame_and_line()
        self.assertEqual(effective_breakpoint(__file__, line, frame), (None, None))

    def test_the_breakpoint_of_the_line_is_effective(self):
        frame, line = _frame_and_line()
        bp = set_breakpoint(__file__, line)
        breakpoint, temporary = effective_breakpoint(__file__, line, frame)
        self.assertIs(breakpoint, bp)
        self.assertTrue(temporary)

    def test_a_disabled_breakpoint_is_not_effective(self):
        frame, line = _frame_and_line()
        disable_breakpoint(set_breakpoint(__file__, line))
        self.assertEqual(effective_breakpoint(__file__, line, frame), (None, None))

    def test_a_hit_is_counted(self):
        frame, line = _frame_and_line()
        bp = set_breakpoint(__file__, line)
        effective_breakpoint(__file__, line, frame)
        self.assertEqual(breakpoint_hits(bp), 1)

    def test_effective_breakpoint_rejects_a_bad_file(self):
        frame, line = _frame_and_line()
        with self.assertRaises(TypeError):
            effective_breakpoint(42, line, frame)

    def test_effective_breakpoint_rejects_a_bad_line(self):
        frame, line = _frame_and_line()
        with self.assertRaises(TypeError):
            effective_breakpoint(__file__, "12", frame)
        with self.assertRaises(ValueError):
            effective_breakpoint(__file__, 0, frame)

    def test_effective_breakpoint_rejects_a_bad_frame(self):
        frame, line = _frame_and_line()
        with self.assertRaises(TypeError):
            effective_breakpoint(__file__, line, "not a frame")


class TestCheckFuncName(unittest.TestCase):
    """Verify the helper that matches a breakpoint against a frame."""

    def setUp(self):
        clear_all_breakpoints()

    def tearDown(self):
        clear_all_breakpoints()

    def test_the_breakpoint_matches_the_line_of_the_frame(self):
        frame, line = _frame_and_line()
        bp = set_breakpoint(__file__, line)
        self.assertTrue(checkfuncname(bp, frame))

    def test_the_breakpoint_does_not_match_another_line(self):
        frame, line = _frame_and_line()
        bp = set_breakpoint(__file__, line + 100)
        self.assertFalse(checkfuncname(bp, frame))

    def test_checkfuncname_rejects_a_bad_breakpoint(self):
        frame, line = _frame_and_line()
        with self.assertRaises(TypeError):
            checkfuncname("not a breakpoint", frame)

    def test_checkfuncname_rejects_a_bad_frame(self):
        frame, line = _frame_and_line()
        bp = set_breakpoint(__file__, 12)
        with self.assertRaises(TypeError):
            checkfuncname(bp, "not a frame")


if __name__ == "__main__":
    unittest.main()
