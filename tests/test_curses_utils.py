"""Tests for curses_utils."""

import curses
import unittest
from unittest import mock

import curses_utils


class TestModuleContract(unittest.TestCase):
    """Test the contract of the module."""

    def test_all_is_sorted_and_unique(self):
        self.assertEqual(
            curses_utils.__all__, sorted(set(curses_utils.__all__))
        )

    def test_every_name_exists(self):
        for name in curses_utils.__all__:
            self.assertTrue(hasattr(curses_utils, name), name)


class TestAvailability(unittest.TestCase):
    """Test the availability of the standard library module."""

    def test_is_available_returns_a_bool(self):
        self.assertIsInstance(curses_utils.is_available(), bool)

    def test_is_available_matches_the_standard_library(self):
        try:
            import curses as standard_curses  # noqa: F401
        except ImportError:
            self.assertFalse(curses_utils.is_available())
        else:
            self.assertTrue(curses_utils.is_available())


@unittest.skipUnless(curses_utils.is_available(), "curses module not available")
class TestConstantsMatchTheStandardLibrary(unittest.TestCase):
    """Test that the constants match the standard library."""

    def test_attribute_constants_match(self):
        self.assertEqual(curses_utils.A_BOLD, curses.A_BOLD)
        self.assertEqual(curses_utils.A_REVERSE, curses.A_REVERSE)

    def test_color_constants_match(self):
        self.assertEqual(curses_utils.COLOR_BLACK, curses.COLOR_BLACK)
        self.assertEqual(curses_utils.COLOR_RED, curses.COLOR_RED)

    def test_key_constants_match(self):
        self.assertEqual(curses_utils.KEY_UP, curses.KEY_UP)
        self.assertEqual(curses_utils.KEY_DOWN, curses.KEY_DOWN)

    def test_result_constants_match(self):
        self.assertEqual(curses_utils.OK, curses.OK)
        self.assertEqual(curses_utils.ERR, curses.ERR)

    def test_window_is_the_standard_library_window(self):
        self.assertIs(curses_utils.Window, curses.window)


@unittest.skipUnless(curses_utils.is_available(), "curses module not available")
class TestDelegation(unittest.TestCase):
    """Test that the helpers delegate to the standard library."""

    def test_initscr_delegates(self):
        with mock.patch.object(curses_utils._curses, "initscr") as initscr:
            initscr.return_value = mock.Mock()
            curses_utils.initscr()
            initscr.assert_called_once_with()

    def test_endwin_delegates(self):
        with mock.patch.object(curses_utils._curses, "endwin") as endwin:
            curses_utils.endwin()
            endwin.assert_called_once_with()

    def test_isendwin_delegates(self):
        with mock.patch.object(curses_utils._curses, "isendwin") as isendwin:
            isendwin.return_value = True
            self.assertTrue(curses_utils.isendwin())
            isendwin.assert_called_once_with()

    def test_curs_set_delegates(self):
        with mock.patch.object(curses_utils._curses, "curs_set") as curs_set:
            curs_set.return_value = 1
            self.assertEqual(curses_utils.curs_set(1), 1)
            curs_set.assert_called_once_with(1)

    def test_baudrate_delegates(self):
        with mock.patch.object(curses_utils._curses, "baudrate") as baudrate:
            baudrate.return_value = 9600
            self.assertEqual(curses_utils.baudrate(), 9600)
            baudrate.assert_called_once_with()

    def test_has_colors_delegates(self):
        with mock.patch.object(curses_utils._curses, "has_colors") as has_colors:
            has_colors.return_value = True
            self.assertTrue(curses_utils.has_colors())
            has_colors.assert_called_once_with()

    def test_keyname_delegates(self):
        with mock.patch.object(curses_utils._curses, "keyname") as keyname:
            keyname.return_value = "KEY_UP"
            self.assertEqual(curses_utils.keyname(curses.KEY_UP), "KEY_UP")
            keyname.assert_called_once_with(curses.KEY_UP)

    def test_longname_delegates(self):
        with mock.patch.object(curses_utils._curses, "longname") as longname:
            longname.return_value = "xterm"
            self.assertEqual(curses_utils.longname(), "xterm")
            longname.assert_called_once_with()

    def test_termattrs_delegates(self):
        with mock.patch.object(
            curses_utils._curses, "termattrs"
        ) as termattrs:
            termattrs.return_value = curses_utils.A_BOLD | curses_utils.A_REVERSE
            self.assertEqual(
                curses_utils.termattrs(), curses_utils.A_BOLD | curses_utils.A_REVERSE
            )
            termattrs.assert_called_once_with()

    def test_use_default_colors_delegates(self):
        with mock.patch.object(
            curses_utils._curses, "use_default_colors"
        ) as use_default_colors:
            use_default_colors.return_value = curses_utils.OK
            self.assertEqual(curses_utils.use_default_colors(), curses_utils.OK)
            use_default_colors.assert_called_once_with()

    def test_start_color_delegates(self):
        with mock.patch.object(curses_utils._curses, "start_color") as start_color:
            curses_utils.start_color()
            start_color.assert_called_once_with()

    def test_init_pair_delegates(self):
        with mock.patch.object(curses_utils._curses, "init_pair") as init_pair:
            curses_utils.init_pair(1, curses_utils.COLOR_RED, curses_utils.COLOR_BLACK)
            init_pair.assert_called_once_with(
                1, curses_utils.COLOR_RED, curses_utils.COLOR_BLACK
            )

    def test_color_pair_delegates(self):
        with mock.patch.object(curses_utils._curses, "color_pair") as color_pair:
            color_pair.return_value = curses_utils.A_COLOR | 1
            self.assertEqual(
                curses_utils.color_pair(1), curses_utils.A_COLOR | 1
            )
            color_pair.assert_called_once_with(1)

    def test_napms_delegates(self):
        with mock.patch.object(curses_utils._curses, "napms") as napms:
            curses_utils.napms(100)
            napms.assert_called_once_with(100)

    def test_flash_delegates(self):
        with mock.patch.object(curses_utils._curses, "flash") as flash:
            curses_utils.flash()
            flash.assert_called_once_with()

    def test_beep_delegates(self):
        with mock.patch.object(curses_utils._curses, "beep") as beep:
            curses_utils.beep()
            beep.assert_called_once_with()

    def test_getsyx_returns_none_before_a_screen(self):
        with mock.patch.object(curses_utils._curses, "getsyx") as getsyx:
            getsyx.return_value = None
            self.assertIsNone(curses_utils.getsyx())
            getsyx.assert_called_once_with()

    def test_setsyx_delegates(self):
        with mock.patch.object(curses_utils._curses, "setsyx") as setsyx:
            curses_utils.setsyx(2, 4)
            setsyx.assert_called_once_with(2, 4)

    def test_erasechar_delegates(self):
        with mock.patch.object(curses_utils._curses, "erasechar") as erasechar:
            erasechar.return_value = "\x7f"
            self.assertEqual(curses_utils.erasechar(), "\x7f")
            erasechar.assert_called_once_with()

    def test_killchar_delegates(self):
        with mock.patch.object(curses_utils._curses, "killchar") as killchar:
            killchar.return_value = "\x15"
            self.assertEqual(curses_utils.killchar(), "\x15")
            killchar.assert_called_once_with()

    def test_has_ic_delegates(self):
        with mock.patch.object(curses_utils._curses, "has_ic") as has_ic:
            has_ic.return_value = True
            self.assertTrue(curses_utils.has_ic())
            has_ic.assert_called_once_with()

    def test_has_il_delegates(self):
        with mock.patch.object(curses_utils._curses, "has_il") as has_il:
            has_il.return_value = True
            self.assertTrue(curses_utils.has_il())
            has_il.assert_called_once_with()

    def test_filter_delegates(self):
        with mock.patch.object(curses_utils._curses, "filter") as filter:
            curses_utils.filter()
            filter.assert_called_once_with()

    def test_typeahead_delegates(self):
        with mock.patch.object(curses_utils._curses, "typeahead") as typeahead:
            curses_utils.typeahead(1)
            typeahead.assert_called_once_with(1)

    def test_mouseinterval_delegates(self):
        with mock.patch.object(
            curses_utils._curses, "mouseinterval"
        ) as mouseinterval:
            mouseinterval.return_value = 0
            self.assertEqual(curses_utils.mouseinterval(0), 0)
            mouseinterval.assert_called_once_with(0)

    def test_mousemask_delegates(self):
        with mock.patch.object(curses_utils._curses, "mousemask") as mousemask:
            mousemask.return_value = 0
            self.assertEqual(curses_utils.mousemask(0), 0)
            mousemask.assert_called_once_with(0)

    def test_putp_delegates(self):
        with mock.patch.object(curses_utils._curses, "putp") as putp:
            curses_utils.putp("\n")
            putp.assert_called_once_with("\n")

    def test_use_env_delegates(self):
        with mock.patch.object(curses_utils._curses, "use_env") as use_env:
            curses_utils.use_env(True)
            use_env.assert_called_once_with(True)

    def test_savetty_and_resetty_delegate(self):
        with mock.patch.object(curses_utils._curses, "savetty") as savetty:
            curses_utils.savetty()
            savetty.assert_called_once_with()
        with mock.patch.object(curses_utils._curses, "resetty") as resetty:
            curses_utils.resetty()
            resetty.assert_called_once_with()

    def test_def_and_reset_prog_mode_delegate(self):
        with mock.patch.object(
            curses_utils._curses, "def_prog_mode"
        ) as def_prog_mode:
            curses_utils.def_prog_mode()
            def_prog_mode.assert_called_once_with()
        with mock.patch.object(
            curses_utils._curses, "reset_prog_mode"
        ) as reset_prog_mode:
            curses_utils.reset_prog_mode()
            reset_prog_mode.assert_called_once_with()

    def test_def_and_reset_shell_mode_delegate(self):
        with mock.patch.object(
            curses_utils._curses, "def_shell_mode"
        ) as def_shell_mode:
            curses_utils.def_shell_mode()
            def_shell_mode.assert_called_once_with()
        with mock.patch.object(
            curses_utils._curses, "reset_shell_mode"
        ) as reset_shell_mode:
            curses_utils.reset_shell_mode()
            reset_shell_mode.assert_called_once_with()

    def test_cbreak_and_nocbreak_delegate(self):
        with mock.patch.object(curses_utils._curses, "cbreak") as cbreak:
            curses_utils.cbreak()
            cbreak.assert_called_once_with()
        with mock.patch.object(curses_utils._curses, "nocbreak") as nocbreak:
            curses_utils.nocbreak()
            nocbreak.assert_called_once_with()

    def test_echo_and_noecho_delegate(self):
        with mock.patch.object(curses_utils._curses, "echo") as echo:
            curses_utils.echo()
            echo.assert_called_once_with()
        with mock.patch.object(curses_utils._curses, "noecho") as noecho:
            curses_utils.noecho()
            noecho.assert_called_once_with()

    def test_raw_and_noraw_delegate(self):
        with mock.patch.object(curses_utils._curses, "raw") as raw:
            curses_utils.raw()
            raw.assert_called_once_with()
        with mock.patch.object(curses_utils._curses, "noraw") as noraw:
            curses_utils.noraw()
            noraw.assert_called_once_with()

    def test_nl_and_nonl_delegate(self):
        with mock.patch.object(curses_utils._curses, "nl") as nl:
            curses_utils.nl()
            nl.assert_called_once_with()
        with mock.patch.object(curses_utils._curses, "nonl") as nonl:
            curses_utils.nonl()
            nonl.assert_called_once_with()

    def test_qiflush_and_noqiflush_delegate(self):
        with mock.patch.object(curses_utils._curses, "qiflush") as qiflush:
            curses_utils.qiflush()
            qiflush.assert_called_once_with()
        with mock.patch.object(curses_utils._curses, "noqiflush") as noqiflush:
            curses_utils.noqiflush()
            noqiflush.assert_called_once_with()

    def test_intrflush_delegates(self):
        with mock.patch.object(curses_utils._curses, "intrflush") as intrflush:
            curses_utils.intrflush(True)
            intrflush.assert_called_once_with(True)

    def test_meta_delegates(self):
        with mock.patch.object(curses_utils._curses, "meta") as meta:
            curses_utils.meta(True)
            meta.assert_called_once_with(True)

    def test_halfdelay_delegates(self):
        with mock.patch.object(curses_utils._curses, "halfdelay") as halfdelay:
            curses_utils.halfdelay(10)
            halfdelay.assert_called_once_with(10)

    def test_delay_output_delegates(self):
        with mock.patch.object(
            curses_utils._curses, "delay_output"
        ) as delay_output:
            curses_utils.delay_output(50)
            delay_output.assert_called_once_with(50)

    def test_flushinp_delegates(self):
        with mock.patch.object(curses_utils._curses, "flushinp") as flushinp:
            curses_utils.flushinp()
            flushinp.assert_called_once_with()

    def test_ungetch_delegates(self):
        with mock.patch.object(curses_utils._curses, "ungetch") as ungetch:
            curses_utils.ungetch(curses.KEY_UP)
            ungetch.assert_called_once_with(curses.KEY_UP)

    def test_unget_wch_delegates(self):
        with mock.patch.object(curses_utils._curses, "unget_wch") as unget_wch:
            curses_utils.unget_wch("A")
            unget_wch.assert_called_once_with("A")

    def test_doupdate_delegates(self):
        with mock.patch.object(curses_utils._curses, "doupdate") as doupdate:
            curses_utils.doupdate()
            doupdate.assert_called_once_with()

    def test_newwin_delegates(self):
        with mock.patch.object(curses_utils._curses, "newwin") as newwin:
            newwin.return_value = mock.Mock()
            curses_utils.newwin(5, 10, 0, 0)
            newwin.assert_called_once_with(5, 10, 0, 0)

    def test_resize_term_and_resizeterm_delegate(self):
        with mock.patch.object(curses_utils._curses, "resize_term") as resize_term:
            curses_utils.resize_term(20, 40)
            resize_term.assert_called_once_with(20, 40)
        with mock.patch.object(curses_utils._curses, "resizeterm") as resizeterm:
            curses_utils.resizeterm(20, 40)
            resizeterm.assert_called_once_with(20, 40)

    def test_is_term_resized_delegates(self):
        with mock.patch.object(
            curses_utils._curses, "is_term_resized"
        ) as is_term_resized:
            is_term_resized.return_value = False
            self.assertFalse(curses_utils.is_term_resized(20, 40))
            is_term_resized.assert_called_once_with(20, 40)

    def test_update_lines_cols_delegates(self):
        with mock.patch.object(
            curses_utils._curses, "update_lines_cols"
        ) as update_lines_cols:
            curses_utils.update_lines_cols()
            update_lines_cols.assert_called_once_with()

    def test_setupterm_delegates(self):
        with mock.patch.object(curses_utils._curses, "setupterm") as setupterm:
            curses_utils.setupterm("xterm")
            setupterm.assert_called_once_with("xterm")

    def test_get_escdelay_and_set_escdelay_delegate(self):
        with mock.patch.object(
            curses_utils._curses, "get_escdelay"
        ) as get_escdelay:
            get_escdelay.return_value = 250
            self.assertEqual(curses_utils.get_escdelay(), 250)
            get_escdelay.assert_called_once_with()
        with mock.patch.object(
            curses_utils._curses, "set_escdelay"
        ) as set_escdelay:
            curses_utils.set_escdelay(100)
            set_escdelay.assert_called_once_with(100)

    def test_get_tabsize_and_set_tabsize_delegate(self):
        with mock.patch.object(
            curses_utils._curses, "get_tabsize"
        ) as get_tabsize:
            get_tabsize.return_value = 8
            self.assertEqual(curses_utils.get_tabsize(), 8)
            get_tabsize.assert_called_once_with()
        with mock.patch.object(
            curses_utils._curses, "set_tabsize"
        ) as set_tabsize:
            curses_utils.set_tabsize(4)
            set_tabsize.assert_called_once_with(4)

    def test_can_change_color_delegates(self):
        with mock.patch.object(
            curses_utils._curses, "can_change_color"
        ) as can_change_color:
            can_change_color.return_value = True
            self.assertTrue(curses_utils.can_change_color())
            can_change_color.assert_called_once_with()

    def test_init_color_delegates(self):
        with mock.patch.object(curses_utils._curses, "init_color") as init_color:
            curses_utils.init_color(1, 100, 200, 50)
            init_color.assert_called_once_with(1, 100, 200, 50)

    def test_color_content_delegates(self):
        with mock.patch.object(curses_utils._curses, "color_content") as color_content:
            color_content.return_value = (100, 200, 50)
            self.assertEqual(curses_utils.color_content(1), (100, 200, 50))
            color_content.assert_called_once_with(1)

    def test_pair_content_delegates(self):
        with mock.patch.object(curses_utils._curses, "pair_content") as pair_content:
            pair_content.return_value = (
                curses_utils.COLOR_RED,
                curses_utils.COLOR_BLACK,
            )
            self.assertEqual(
                curses_utils.pair_content(1),
                (curses_utils.COLOR_RED, curses_utils.COLOR_BLACK),
            )
            pair_content.assert_called_once_with(1)

    def test_pair_number_delegates(self):
        with mock.patch.object(curses_utils._curses, "pair_number") as pair_number:
            pair_number.return_value = 1
            self.assertEqual(curses_utils.pair_number(curses_utils.A_COLOR | 1), 1)
            pair_number.assert_called_once_with(curses_utils.A_COLOR | 1)


@unittest.skipUnless(curses_utils.is_available(), "curses module not available")
class TestTypeValidation(unittest.TestCase):
    """Test that invalid argument types are rejected."""

    def test_curs_set_rejects_a_non_int(self):
        with self.assertRaises(TypeError):
            curses_utils.curs_set("high")  # type: ignore[arg-type]

    def test_setsyx_rejects_non_ints(self):
        with self.assertRaises(TypeError):
            curses_utils.setsyx("a", 1)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            curses_utils.setsyx(1, "b")  # type: ignore[arg-type]

    def test_init_pair_rejects_non_ints(self):
        with self.assertRaises(TypeError):
            curses_utils.init_pair(
                "1", curses_utils.COLOR_RED, curses_utils.COLOR_BLACK
            )  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            curses_utils.init_pair(1, "red", curses_utils.COLOR_BLACK)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            curses_utils.init_pair(
                1, curses_utils.COLOR_RED, "black"
            )  # type: ignore[arg-type]

    def test_color_pair_rejects_a_non_int(self):
        with self.assertRaises(TypeError):
            curses_utils.color_pair("1")  # type: ignore[arg-type]

    def test_pair_content_rejects_a_non_int(self):
        with self.assertRaises(TypeError):
            curses_utils.pair_content("1")  # type: ignore[arg-type]

    def test_pair_number_rejects_a_non_int(self):
        with self.assertRaises(TypeError):
            curses_utils.pair_number("1")  # type: ignore[arg-type]

    def test_napms_rejects_a_non_int(self):
        with self.assertRaises(TypeError):
            curses_utils.napms("100")  # type: ignore[arg-type]

    def test_delay_output_rejects_a_non_int(self):
        with self.assertRaises(TypeError):
            curses_utils.delay_output("50")  # type: ignore[arg-type]

    def test_ungetch_rejects_a_non_int(self):
        with self.assertRaises(TypeError):
            curses_utils.ungetch("A")  # type: ignore[arg-type]

    def test_unget_wch_rejects_a_non_str(self):
        with self.assertRaises(TypeError):
            curses_utils.unget_wch(65)  # type: ignore[arg-type]

    def test_newwin_rejects_non_ints(self):
        with self.assertRaises(TypeError):
            curses_utils.newwin("5", 10, 0, 0)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            curses_utils.newwin(5, "10", 0, 0)  # type: ignore[arg-type]

    def test_resize_term_rejects_non_ints(self):
        with self.assertRaises(TypeError):
            curses_utils.resize_term("20", 40)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            curses_utils.resize_term(20, "40")  # type: ignore[arg-type]

    def test_is_term_resized_rejects_non_ints(self):
        with self.assertRaises(TypeError):
            curses_utils.is_term_resized("20", 40)  # type: ignore[arg-type]

    def test_keyname_rejects_an_invalid_type(self):
        with self.assertRaises(TypeError):
            curses_utils.keyname(12.5)  # type: ignore[arg-type]

    def test_mouseinterval_rejects_a_non_int(self):
        with self.assertRaises(TypeError):
            curses_utils.mouseinterval("0")  # type: ignore[arg-type]

    def test_mousemask_rejects_a_non_int(self):
        with self.assertRaises(TypeError):
            curses_utils.mousemask("0")  # type: ignore[arg-type]

    def test_putp_rejects_a_non_str(self):
        with self.assertRaises(TypeError):
            curses_utils.putp(123)  # type: ignore[arg-type]

    def test_intrflush_rejects_a_non_bool(self):
        with self.assertRaises(TypeError):
            curses_utils.intrflush(1)  # type: ignore[arg-type]

    def test_meta_rejects_a_non_bool(self):
        with self.assertRaises(TypeError):
            curses_utils.meta(1)  # type: ignore[arg-type]

    def test_halfdelay_rejects_a_non_int(self):
        with self.assertRaises(TypeError):
            curses_utils.halfdelay("10")  # type: ignore[arg-type]

    def test_use_env_rejects_a_non_bool(self):
        with self.assertRaises(TypeError):
            curses_utils.use_env(1)  # type: ignore[arg-type]

    def test_init_color_rejects_non_ints(self):
        with self.assertRaises(TypeError):
            curses_utils.init_color("1", 100, 200, 50)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            curses_utils.init_color(1, "100", 200, 50)  # type: ignore[arg-type]

    def test_typeahead_rejects_a_non_int(self):
        with self.assertRaises(TypeError):
            curses_utils.typeahead("1")  # type: ignore[arg-type]

    def test_has_key_rejects_a_non_int(self):
        with self.assertRaises(TypeError):
            curses_utils.has_key("KEY_UP")  # type: ignore[arg-type]


class TestMissingModule(unittest.TestCase):
    """Test the behaviour when the standard library module is absent."""

    def test_helpers_raise_when_the_module_is_missing(self):
        with mock.patch.object(curses_utils, "_curses", None):
            with self.assertRaises(RuntimeError):
                curses_utils.isendwin()
            with self.assertRaises(RuntimeError):
                curses_utils.baudrate()
            with self.assertRaises(RuntimeError):
                curses_utils.start_color()
            with self.assertRaises(RuntimeError):
                curses_utils.beep()


if __name__ == "__main__":
    unittest.main()
