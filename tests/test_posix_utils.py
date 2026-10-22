"""Tests for posix_utils."""

import os
import signal
import stat
import tempfile
import unittest
from pathlib import Path
from unittest import mock

import posix_utils
from posix_utils import (
    DeviceNumber,
    FileInfo,
    ProcessTimes,
    SchedulerParameters,
    SystemName,
    affinity_mask,
    change_mode,
    change_owner,
    close_fd,
    cpu_count,
    create_directory,
    create_hard_link,
    create_pipe,
    create_symbolic_link,
    delete_file,
    describe_wait_status,
    device_number,
    duplicate_fd,
    duplicate_fd_to,
    error_message,
    exit_code_of,
    file_info,
    file_mode,
    file_size,
    is_available,
    is_blocking,
    is_executable,
    is_inheritable,
    is_readable,
    is_terminal,
    is_writable,
    list_xattrs,
    load_average,
    login_name,
    make_device,
    open_fd,
    path_accessible,
    process_times,
    read_at,
    read_exactly,
    read_fd,
    read_symbolic_link,
    read_xattr,
    remove_directory,
    remove_path,
    remove_xattr,
    rename_path,
    scheduler_parameters,
    scheduler_policy,
    scheduler_policy_name,
    scheduler_priorities,
    seek_fd,
    set_blocking,
    set_inheritable,
    set_umask,
    sync_data,
    sync_fd,
    system_configuration,
    system_limit,
    system_limits,
    terminal_device,
    terminal_size,
    truncate_fd,
    uname,
    write_all,
    write_at,
    write_fd,
    write_xattr,
    yield_cpu,
)

HAVE_POSIX = is_available()

#: The status of a process that exited with the code 0.
STATUS_EXITED = 0

#: The status of a process that exited with the code 3.
STATUS_EXITED_THREE = 3 << 8

#: The status of a process that was terminated by ``SIGTERM``.
STATUS_SIGNALED = int(signal.SIGTERM)

#: The status of a process that was stopped by ``SIGSTOP``.
STATUS_STOPPED = (int(signal.SIGSTOP) << 8) | 0x7F

#: The status of a process that continued.
STATUS_CONTINUED = 0xFFFF


class TestAvailability(unittest.TestCase):
    """The wrapper reports whether the interpreter ships the module."""

    def test_is_available_matches_the_import(self):
        self.assertEqual(is_available(), HAVE_POSIX)

    def test_helpers_raise_when_the_module_is_missing(self):
        with mock.patch.object(posix_utils, "_posix", None):
            self.assertFalse(is_available())
            with self.assertRaises(RuntimeError):
                uname()
            with self.assertRaises(RuntimeError):
                create_pipe()
            with self.assertRaises(RuntimeError):
                file_size("/tmp")


class TestSystemInformation(unittest.TestCase):
    """The wrapper reports the information of the running system."""

    @unittest.skipUnless(HAVE_POSIX, "the posix module is not available")
    def test_uname_reports_the_five_fields(self):
        result = uname()
        self.assertIsInstance(result, SystemName)
        self.assertTrue(result.system)
        self.assertTrue(result.node)
        self.assertTrue(result.release)
        self.assertTrue(result.machine)

    @unittest.skipUnless(HAVE_POSIX, "the posix module is not available")
    def test_cpu_count_is_positive(self):
        count = cpu_count()
        self.assertTrue(count is None or count > 0)

    @unittest.skipUnless(HAVE_POSIX, "the posix module is not available")
    def test_load_average_has_three_values(self):
        average = load_average()
        self.assertEqual(len(average), 3)
        for value in average:
            self.assertGreaterEqual(value, 0.0)

    @unittest.skipUnless(HAVE_POSIX, "the posix module is not available")
    def test_process_times_reports_the_five_fields(self):
        times = process_times()
        self.assertIsInstance(times, ProcessTimes)
        self.assertGreaterEqual(times.elapsed, 0.0)
        self.assertGreaterEqual(times.user, 0.0)

    @unittest.skipUnless(HAVE_POSIX, "the posix module is not available")
    def test_system_limit_reports_a_known_limit(self):
        self.assertGreater(system_limit("SC_PAGE_SIZE"), 0)

    @unittest.skipUnless(HAVE_POSIX, "the posix module is not available")
    def test_system_limit_rejects_an_unknown_limit(self):
        with self.assertRaises(ValueError):
            system_limit("SC_NOT_A_LIMIT")

    @unittest.skipUnless(HAVE_POSIX, "the posix module is not available")
    def test_system_limits_reports_the_default_limits(self):
        limits = system_limits()
        self.assertIn("SC_PAGE_SIZE", limits)
        self.assertGreater(limits["SC_PAGE_SIZE"], 0)

    @unittest.skipUnless(HAVE_POSIX, "the posix module is not available")
    def test_system_limits_rejects_an_unknown_limit(self):
        with self.assertRaises(ValueError):
            system_limits(["SC_NOT_A_LIMIT"])

    @unittest.skipUnless(HAVE_POSIX, "the posix module is not available")
    def test_system_limits_rejects_a_string(self):
        with self.assertRaises(TypeError):
            system_limits("SC_PAGE_SIZE")

    @unittest.skipUnless(HAVE_POSIX, "the posix module is not available")
    def test_system_configuration_reports_a_known_configuration(self):
        value = system_configuration("CS_PATH")
        self.assertIsInstance(value, str)

    @unittest.skipUnless(HAVE_POSIX, "the posix module is not available")
    def test_system_configuration_rejects_an_unknown_configuration(self):
        with self.assertRaises(ValueError):
            system_configuration("CS_NOT_A_CONFIGURATION")

    @unittest.skipUnless(HAVE_POSIX, "the posix module is not available")
    def test_login_name_is_a_string_or_none(self):
        name = login_name()
        self.assertTrue(name is None or isinstance(name, str))

    @unittest.skipUnless(HAVE_POSIX, "the posix module is not available")
    def test_terminal_device_is_a_path(self):
        self.assertIsInstance(terminal_device(), str)


class TestDescriptors(unittest.TestCase):
    """The wrapper reads and writes through the file descriptors."""

    def setUp(self):
        self.descriptors = []

    def tearDown(self):
        for descriptor in self.descriptors:
            try:
                close_fd(descriptor)
            except OSError:  # pragma: no cover - the descriptor is already closed
                pass

    def track(self, descriptor):
        """Remember a descriptor so that the test closes it."""
        self.descriptors.append(descriptor)
        return descriptor

    @unittest.skipUnless(HAVE_POSIX, "the posix module is not available")
    def test_open_fd_creates_and_reads_a_file(self):
        with tempfile.TemporaryDirectory() as directory:
            path = os.path.join(directory, "file.txt")
            descriptor = self.track(
                open_fd(path, os.O_CREAT | os.O_RDWR | os.O_TRUNC, 0o600)
            )
            write_all(descriptor, b"hello")
            self.assertEqual(file_size(path), 5)
            self.assertEqual(read_at(descriptor, 5, 0), b"hello")

    @unittest.skipUnless(HAVE_POSIX, "the posix module is not available")
    def test_read_fd_returns_what_is_available(self):
        read_descriptor, write_descriptor = create_pipe()
        self.track(read_descriptor)
        self.track(write_descriptor)
        write_all(write_descriptor, b"abc")
        self.assertEqual(read_fd(read_descriptor, 10), b"abc")

    @unittest.skipUnless(HAVE_POSIX, "the posix module is not available")
    def test_read_fd_rejects_a_negative_size(self):
        with self.assertRaises(ValueError):
            read_fd(0, -1)

    @unittest.skipUnless(HAVE_POSIX, "the posix module is not available")
    def test_read_exactly_collects_every_byte(self):
        read_descriptor, write_descriptor = create_pipe()
        self.track(read_descriptor)
        self.track(write_descriptor)
        write_all(write_descriptor, b"0123456789")
        self.assertEqual(read_exactly(read_descriptor, 10), b"0123456789")

    @unittest.skipUnless(HAVE_POSIX, "the posix module is not available")
    def test_read_exactly_raises_at_the_end_of_the_file(self):
        with tempfile.TemporaryDirectory() as directory:
            path = os.path.join(directory, "file.txt")
            with open(path, "wb") as handle:
                handle.write(b"abc")
            descriptor = self.track(open_fd(path, os.O_RDONLY))
            with self.assertRaises(EOFError):
                read_exactly(descriptor, 5)

    @unittest.skipUnless(HAVE_POSIX, "the posix module is not available")
    def test_read_exactly_of_no_byte_is_empty(self):
        read_descriptor, _ = create_pipe()
        self.track(read_descriptor)
        self.assertEqual(read_exactly(read_descriptor, 0), b"")

    @unittest.skipUnless(HAVE_POSIX, "the posix module is not available")
    def test_write_fd_reports_the_number_of_bytes(self):
        read_descriptor, write_descriptor = create_pipe()
        self.track(read_descriptor)
        self.track(write_descriptor)
        self.assertEqual(write_fd(write_descriptor, b"abcd"), 4)

    @unittest.skipUnless(HAVE_POSIX, "the posix module is not available")
    def test_write_fd_rejects_a_string(self):
        read_descriptor, write_descriptor = create_pipe()
        self.track(read_descriptor)
        self.track(write_descriptor)
        with self.assertRaises(TypeError):
            write_fd(write_descriptor, "abcd")

    @unittest.skipUnless(HAVE_POSIX, "the posix module is not available")
    def test_write_all_writes_every_byte(self):
        read_descriptor, write_descriptor = create_pipe()
        self.track(read_descriptor)
        self.track(write_descriptor)
        payload = b"payload"
        self.assertEqual(write_all(write_descriptor, payload), len(payload))
        self.assertEqual(read_exactly(read_descriptor, len(payload)), payload)

    @unittest.skipUnless(HAVE_POSIX, "the posix module is not available")
    def test_seek_fd_moves_the_position(self):
        with tempfile.TemporaryDirectory() as directory:
            path = os.path.join(directory, "file.txt")
            with open(path, "wb") as handle:
                handle.write(b"abcdef")
            descriptor = self.track(open_fd(path, os.O_RDONLY))
            self.assertEqual(seek_fd(descriptor, 2, os.SEEK_SET), 2)
            self.assertEqual(read_fd(descriptor, 2), b"cd")
            self.assertEqual(seek_fd(descriptor, 0, os.SEEK_END), 6)

    @unittest.skipUnless(HAVE_POSIX, "the posix module is not available")
    def test_seek_fd_rejects_an_unknown_origin(self):
        with self.assertRaises(ValueError):
            seek_fd(0, 0, 99)

    @unittest.skipUnless(HAVE_POSIX, "the posix module is not available")
    def test_write_at_does_not_move_the_position(self):
        with tempfile.TemporaryDirectory() as directory:
            path = os.path.join(directory, "file.txt")
            descriptor = self.track(
                open_fd(path, os.O_CREAT | os.O_RDWR | os.O_TRUNC, 0o600)
            )
            write_at(descriptor, b"world", 6)
            write_at(descriptor, b"hello ", 0)
            self.assertEqual(read_at(descriptor, 11, 0), b"hello world")

    @unittest.skipUnless(HAVE_POSIX, "the posix module is not available")
    def test_duplicate_fd_shares_the_position(self):
        with tempfile.TemporaryDirectory() as directory:
            path = os.path.join(directory, "file.txt")
            with open(path, "wb") as handle:
                handle.write(b"abcdef")
            descriptor = self.track(open_fd(path, os.O_RDONLY))
            copy = self.track(duplicate_fd(descriptor))
            seek_fd(descriptor, 3, os.SEEK_SET)
            self.assertEqual(seek_fd(copy, 0, os.SEEK_CUR), 3)

    @unittest.skipUnless(HAVE_POSIX, "the posix module is not available")
    def test_duplicate_fd_to_replaces_the_target(self):
        read_descriptor, write_descriptor = create_pipe()
        self.track(read_descriptor)
        self.track(write_descriptor)
        with tempfile.TemporaryDirectory() as directory:
            path = os.path.join(directory, "file.txt")
            with open(path, "wb") as handle:
                handle.write(b"hello")
            descriptor = self.track(open_fd(path, os.O_RDONLY))
            target = duplicate_fd_to(descriptor, read_descriptor)
            self.assertEqual(target, read_descriptor)
            self.assertEqual(read_fd(read_descriptor, 5), b"hello")

    @unittest.skipUnless(HAVE_POSIX, "the posix module is not available")
    def test_create_pipe_returns_two_descriptors(self):
        read_descriptor, write_descriptor = create_pipe()
        self.track(read_descriptor)
        self.track(write_descriptor)
        self.assertNotEqual(read_descriptor, write_descriptor)

    @unittest.skipUnless(HAVE_POSIX, "the posix module is not available")
    def test_create_pipe_rejects_a_non_bool(self):
        with self.assertRaises(TypeError):
            create_pipe("yes")

    @unittest.skipUnless(HAVE_POSIX, "the posix module is not available")
    def test_a_pipe_is_not_a_terminal(self):
        read_descriptor, write_descriptor = create_pipe()
        self.track(read_descriptor)
        self.track(write_descriptor)
        self.assertFalse(is_terminal(read_descriptor))

    @unittest.skipUnless(HAVE_POSIX, "the posix module is not available")
    def test_set_blocking_changes_the_mode(self):
        read_descriptor, write_descriptor = create_pipe()
        self.track(read_descriptor)
        self.track(write_descriptor)
        set_blocking(read_descriptor, False)
        self.assertFalse(is_blocking(read_descriptor))
        set_blocking(read_descriptor, True)
        self.assertTrue(is_blocking(read_descriptor))

    @unittest.skipUnless(HAVE_POSIX, "the posix module is not available")
    def test_set_inheritable_changes_the_flag(self):
        read_descriptor, write_descriptor = create_pipe()
        self.track(read_descriptor)
        self.track(write_descriptor)
        set_inheritable(read_descriptor, False)
        self.assertFalse(is_inheritable(read_descriptor))
        set_inheritable(read_descriptor, True)
        self.assertTrue(is_inheritable(read_descriptor))

    @unittest.skipUnless(HAVE_POSIX, "the posix module is not available")
    def test_sync_fd_and_sync_data_write_the_file(self):
        with tempfile.TemporaryDirectory() as directory:
            path = os.path.join(directory, "file.txt")
            descriptor = self.track(
                open_fd(path, os.O_CREAT | os.O_RDWR | os.O_TRUNC, 0o600)
            )
            write_all(descriptor, b"data")
            sync_fd(descriptor)
            sync_data(descriptor)

    @unittest.skipUnless(HAVE_POSIX, "the posix module is not available")
    def test_truncate_fd_sets_the_length(self):
        with tempfile.TemporaryDirectory() as directory:
            path = os.path.join(directory, "file.txt")
            with open(path, "wb") as handle:
                handle.write(b"abcdef")
            descriptor = self.track(open_fd(path, os.O_RDWR))
            truncate_fd(descriptor, 3)
            self.assertEqual(file_size(path), 3)

    @unittest.skipUnless(HAVE_POSIX, "the posix module is not available")
    def test_terminal_size_reports_the_size_of_a_terminal(self):
        try:
            import fcntl
            import struct
            import termios
        except ImportError:  # pragma: no cover - the platform is not Unix like
            self.skipTest("the platform does not provide the terminal helpers")
        try:
            master, slave = os.openpty()
        except OSError:  # pragma: no cover - the platform has no pseudo terminals
            self.skipTest("the platform does not provide pseudo terminals")
        try:
            fcntl.ioctl(slave, termios.TIOCSWINSZ, struct.pack("HHHH", 24, 80, 0, 0))
            columns, lines = terminal_size(slave)
            self.assertEqual(columns, 80)
            self.assertEqual(lines, 24)
        finally:
            os.close(slave)
            os.close(master)

    @unittest.skipUnless(HAVE_POSIX, "the posix module is not available")
    def test_terminal_size_rejects_a_descriptor_that_is_not_a_terminal(self):
        read_descriptor, write_descriptor = create_pipe()
        self.track(read_descriptor)
        self.track(write_descriptor)
        with self.assertRaises(OSError):
            terminal_size(read_descriptor)

    @unittest.skipUnless(HAVE_POSIX, "the posix module is not available")
    def test_the_helpers_reject_a_descriptor_that_is_not_an_int(self):
        with self.assertRaises(TypeError):
            close_fd("0")
        with self.assertRaises(TypeError):
            read_fd(True, 1)
        with self.assertRaises(ValueError):
            read_fd(-1, 1)


class TestFiles(unittest.TestCase):
    """The wrapper inspects and changes the files of the filesystem."""

    @unittest.skipUnless(HAVE_POSIX, "the posix module is not available")
    def test_file_info_reports_the_metadata(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "file.txt"
            path.write_bytes(b"hello")
            info = file_info(path)
            self.assertIsInstance(info, FileInfo)
            self.assertEqual(info.size, 5)
            self.assertTrue(info.is_regular_file)
            self.assertFalse(info.is_directory)
            self.assertFalse(info.is_symbolic_link)
            self.assertEqual(info.permissions, stat.S_IMODE(os.stat(path).st_mode))

    @unittest.skipUnless(HAVE_POSIX, "the posix module is not available")
    def test_file_info_of_a_directory(self):
        with tempfile.TemporaryDirectory() as directory:
            info = file_info(directory)
            self.assertTrue(info.is_directory)
            self.assertFalse(info.is_regular_file)

    @unittest.skipUnless(HAVE_POSIX, "the posix module is not available")
    def test_file_info_describes_a_symbolic_link(self):
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / "file.txt"
            target.write_bytes(b"hello")
            link = Path(directory) / "link.txt"
            link.symlink_to(target)
            self.assertTrue(file_info(link, follow_symlinks=False).is_symbolic_link)
            self.assertTrue(file_info(link).is_regular_file)

    @unittest.skipUnless(HAVE_POSIX, "the posix module is not available")
    def test_file_info_rejects_a_non_bool(self):
        with self.assertRaises(TypeError):
            file_info("/tmp", follow_symlinks="yes")

    @unittest.skipUnless(HAVE_POSIX, "the posix module is not available")
    def test_file_mode_and_file_size(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "file.txt"
            path.write_bytes(b"hello")
            self.assertEqual(file_mode(path), stat.S_IMODE(os.stat(path).st_mode))
            self.assertEqual(file_size(path), 5)

    @unittest.skipUnless(HAVE_POSIX, "the posix module is not available")
    def test_device_number_reports_the_major_and_minor_number(self):
        with tempfile.TemporaryDirectory() as directory:
            number = device_number(directory)
            self.assertIsInstance(number, DeviceNumber)
            self.assertGreaterEqual(number.major, 0)
            self.assertGreaterEqual(number.minor, 0)

    @unittest.skipUnless(HAVE_POSIX, "the posix module is not available")
    def test_make_device_reverses_the_major_and_minor_number(self):
        number = make_device(8, 1)
        self.assertIsInstance(number, int)

    @unittest.skipUnless(HAVE_POSIX, "the posix module is not available")
    def test_make_device_rejects_a_negative_number(self):
        with self.assertRaises(ValueError):
            make_device(-1, 0)

    @unittest.skipUnless(HAVE_POSIX, "the posix module is not available")
    def test_path_accessible_reports_the_modes(self):
        with tempfile.TemporaryDirectory() as directory:
            path = os.path.join(directory, "file.txt")
            with open(path, "wb"):
                pass
            self.assertTrue(path_accessible(path, os.F_OK))
            self.assertTrue(is_readable(path))
            self.assertTrue(is_writable(path))
            self.assertFalse(is_executable(path))

    @unittest.skipUnless(HAVE_POSIX, "the posix module is not available")
    def test_path_accessible_rejects_an_unknown_mode(self):
        with self.assertRaises(ValueError):
            path_accessible("/tmp", 42)

    @unittest.skipUnless(HAVE_POSIX, "the posix module is not available")
    def test_create_directory_creates_one_directory(self):
        with tempfile.TemporaryDirectory() as directory:
            path = os.path.join(directory, "child")
            create_directory(path)
            self.assertTrue(os.path.isdir(path))

    @unittest.skipUnless(HAVE_POSIX, "the posix module is not available")
    def test_create_directory_creates_the_parents(self):
        with tempfile.TemporaryDirectory() as directory:
            path = os.path.join(directory, "one", "two", "three")
            create_directory(path, parents=True)
            self.assertTrue(os.path.isdir(path))

    @unittest.skipUnless(HAVE_POSIX, "the posix module is not available")
    def test_create_directory_accepts_an_existing_directory(self):
        with tempfile.TemporaryDirectory() as directory:
            path = os.path.join(directory, "child")
            create_directory(path)
            create_directory(path, exist_ok=True)
            with self.assertRaises(FileExistsError):
                create_directory(path)

    @unittest.skipUnless(HAVE_POSIX, "the posix module is not available")
    def test_create_directory_rejects_a_mode_with_foreign_bits(self):
        with self.assertRaises(ValueError):
            create_directory("/tmp/example", mode=0o10000)

    @unittest.skipUnless(HAVE_POSIX, "the posix module is not available")
    def test_remove_directory_removes_an_empty_directory(self):
        with tempfile.TemporaryDirectory() as directory:
            path = os.path.join(directory, "child")
            create_directory(path)
            remove_directory(path)
            self.assertFalse(os.path.exists(path))

    @unittest.skipUnless(HAVE_POSIX, "the posix module is not available")
    def test_delete_file_removes_a_file(self):
        with tempfile.TemporaryDirectory() as directory:
            path = os.path.join(directory, "file.txt")
            with open(path, "wb"):
                pass
            delete_file(path)
            self.assertFalse(os.path.exists(path))

    @unittest.skipUnless(HAVE_POSIX, "the posix module is not available")
    def test_remove_path_removes_a_file_a_link_and_a_directory(self):
        with tempfile.TemporaryDirectory() as directory:
            target = os.path.join(directory, "file.txt")
            with open(target, "wb"):
                pass
            link = os.path.join(directory, "link.txt")
            create_symbolic_link(target, link)
            remove_path(link)
            self.assertTrue(os.path.exists(target))
            remove_path(target)
            self.assertFalse(os.path.exists(target))
            child = os.path.join(directory, "child")
            create_directory(child)
            remove_path(child)
            self.assertFalse(os.path.exists(child))

    @unittest.skipUnless(HAVE_POSIX, "the posix module is not available")
    def test_rename_path_moves_a_file(self):
        with tempfile.TemporaryDirectory() as directory:
            source = os.path.join(directory, "old.txt")
            target = os.path.join(directory, "new.txt")
            with open(source, "wb") as handle:
                handle.write(b"data")
            rename_path(source, target)
            self.assertFalse(os.path.exists(source))
            self.assertTrue(os.path.exists(target))

    @unittest.skipUnless(HAVE_POSIX, "the posix module is not available")
    def test_create_hard_link_points_at_the_same_file(self):
        with tempfile.TemporaryDirectory() as directory:
            source = os.path.join(directory, "file.txt")
            link = os.path.join(directory, "link.txt")
            with open(source, "wb") as handle:
                handle.write(b"data")
            create_hard_link(source, link)
            self.assertEqual(os.stat(source).st_ino, os.stat(link).st_ino)

    @unittest.skipUnless(HAVE_POSIX, "the posix module is not available")
    def test_create_symbolic_link_and_read_it(self):
        with tempfile.TemporaryDirectory() as directory:
            target = os.path.join(directory, "file.txt")
            link = os.path.join(directory, "link.txt")
            with open(target, "wb"):
                pass
            create_symbolic_link(target, link)
            self.assertEqual(read_symbolic_link(link), target)

    @unittest.skipUnless(HAVE_POSIX, "the posix module is not available")
    def test_change_mode_sets_the_permissions(self):
        with tempfile.TemporaryDirectory() as directory:
            path = os.path.join(directory, "file.txt")
            with open(path, "wb"):
                pass
            change_mode(path, 0o600)
            self.assertEqual(file_mode(path), 0o600)

    @unittest.skipUnless(HAVE_POSIX, "the posix module is not available")
    def test_change_owner_keeps_the_owner(self):
        with tempfile.TemporaryDirectory() as directory:
            path = os.path.join(directory, "file.txt")
            with open(path, "wb"):
                pass
            change_owner(path, -1, -1)
            self.assertEqual(os.stat(path).st_uid, os.getuid())

    @unittest.skipUnless(HAVE_POSIX, "the posix module is not available")
    def test_change_owner_rejects_an_identifier_below_minus_one(self):
        with self.assertRaises(ValueError):
            change_owner("/tmp", -2, -1)

    @unittest.skipUnless(HAVE_POSIX, "the posix module is not available")
    def test_set_umask_reports_the_previous_mask(self):
        previous = set_umask(0o022)
        try:
            self.assertIsInstance(previous, int)
            self.assertEqual(set_umask(0o022), 0o022)
        finally:
            set_umask(previous)

    @unittest.skipUnless(HAVE_POSIX, "the posix module is not available")
    def test_the_helpers_reject_a_path_that_is_not_a_path(self):
        with self.assertRaises(TypeError):
            file_info(42)
        with self.assertRaises(TypeError):
            file_size(None)


class TestExtendedAttributes(unittest.TestCase):
    """The wrapper reads and writes the extended attributes of a file."""

    def setUp(self):
        if not HAVE_POSIX:
            self.skipTest("the posix module is not available")
        self.directory = tempfile.TemporaryDirectory()
        self.path = os.path.join(self.directory.name, "file.txt")
        with open(self.path, "wb"):
            pass
        try:
            write_xattr(self.path, "user.posix_utils", b"value")
        except OSError as error:  # pragma: no cover - the filesystem has no support
            self.directory.cleanup()
            self.skipTest(f"the filesystem has no extended attributes: {error}")

    def tearDown(self):
        self.directory.cleanup()

    def test_read_xattr_reports_the_value(self):
        self.assertEqual(read_xattr(self.path, "user.posix_utils"), b"value")

    def test_write_xattr_replaces_the_value(self):
        write_xattr(self.path, "user.posix_utils", b"other")
        self.assertEqual(read_xattr(self.path, "user.posix_utils"), b"other")

    def test_list_xattrs_reports_the_names(self):
        self.assertIn("user.posix_utils", list_xattrs(self.path))

    def test_remove_xattr_removes_the_attribute(self):
        remove_xattr(self.path, "user.posix_utils")
        self.assertNotIn("user.posix_utils", list_xattrs(self.path))

    def test_the_helpers_reject_a_name_that_is_not_a_string(self):
        with self.assertRaises(TypeError):
            read_xattr(self.path, 42)
        with self.assertRaises(TypeError):
            write_xattr(self.path, "user.posix_utils", "value")
        with self.assertRaises(TypeError):
            remove_xattr(self.path, 42)


class TestScheduling(unittest.TestCase):
    """The wrapper reports the scheduling of a process."""

    @unittest.skipUnless(HAVE_POSIX, "the posix module is not available")
    def test_scheduler_policy_reports_a_known_policy(self):
        policy = scheduler_policy()
        self.assertIn(policy, posix_utils.SCHED_POLICIES.values())

    @unittest.skipUnless(HAVE_POSIX, "the posix module is not available")
    def test_scheduler_policy_name_names_the_policy(self):
        name = scheduler_policy_name()
        self.assertIn(name, posix_utils.SCHED_POLICIES)

    @unittest.skipUnless(HAVE_POSIX, "the posix module is not available")
    def test_scheduler_priorities_reports_the_range(self):
        lowest, highest = scheduler_priorities(posix_utils.SCHED_POLICIES["SCHED_OTHER"])
        self.assertLessEqual(lowest, highest)

    @unittest.skipUnless(HAVE_POSIX, "the posix module is not available")
    def test_scheduler_priorities_rejects_a_negative_policy(self):
        with self.assertRaises(ValueError):
            scheduler_priorities(-1)

    @unittest.skipUnless(HAVE_POSIX, "the posix module is not available")
    def test_scheduler_parameters_reports_the_policy_and_the_priority(self):
        parameters = scheduler_parameters()
        self.assertIsInstance(parameters, SchedulerParameters)
        self.assertIn(parameters.policy, posix_utils.SCHED_POLICIES)
        self.assertLessEqual(parameters.minimum_priority, parameters.maximum_priority)

    @unittest.skipUnless(HAVE_POSIX, "the posix module is not available")
    def test_affinity_mask_reports_the_processors(self):
        mask = affinity_mask()
        self.assertIsInstance(mask, set)
        for processor in mask:
            self.assertGreaterEqual(processor, 0)

    @unittest.skipUnless(HAVE_POSIX, "the posix module is not available")
    def test_yield_cpu_gives_up_the_time_slice(self):
        yield_cpu()

    @unittest.skipUnless(HAVE_POSIX, "the posix module is not available")
    def test_the_helpers_reject_a_process_that_is_not_an_int(self):
        with self.assertRaises(TypeError):
            scheduler_policy("0")
        with self.assertRaises(ValueError):
            affinity_mask(-1)


class TestWaitStatus(unittest.TestCase):
    """The wrapper turns a wait status into an exit code and a sentence."""

    @unittest.skipUnless(HAVE_POSIX, "the posix module is not available")
    def test_exit_code_of_a_process_that_exited(self):
        self.assertEqual(exit_code_of(STATUS_EXITED), 0)
        self.assertEqual(exit_code_of(STATUS_EXITED_THREE), 3)

    @unittest.skipUnless(HAVE_POSIX, "the posix module is not available")
    def test_exit_code_of_a_process_that_was_signalled(self):
        self.assertEqual(exit_code_of(STATUS_SIGNALED), -int(signal.SIGTERM))

    @unittest.skipUnless(HAVE_POSIX, "the posix module is not available")
    def test_exit_code_rejects_a_negative_status(self):
        with self.assertRaises(ValueError):
            exit_code_of(-1)

    @unittest.skipUnless(HAVE_POSIX, "the posix module is not available")
    def test_describe_wait_status_of_a_process_that_exited(self):
        self.assertEqual(describe_wait_status(STATUS_EXITED), "exited with code 0")
        self.assertEqual(describe_wait_status(STATUS_EXITED_THREE), "exited with code 3")

    @unittest.skipUnless(HAVE_POSIX, "the posix module is not available")
    def test_describe_wait_status_of_a_process_that_was_signalled(self):
        description = describe_wait_status(STATUS_SIGNALED)
        self.assertIn("SIGTERM", description)
        self.assertIn("terminated by signal", description)

    @unittest.skipUnless(HAVE_POSIX, "the posix module is not available")
    def test_describe_wait_status_of_a_process_that_was_stopped(self):
        description = describe_wait_status(STATUS_STOPPED)
        self.assertIn("SIGSTOP", description)
        self.assertIn("stopped by signal", description)

    @unittest.skipUnless(HAVE_POSIX, "the posix module is not available")
    def test_describe_wait_status_of_a_process_that_continued(self):
        self.assertEqual(describe_wait_status(STATUS_CONTINUED), "continued")

    @unittest.skipUnless(HAVE_POSIX, "the posix module is not available")
    def test_describe_wait_status_rejects_a_non_int(self):
        with self.assertRaises(TypeError):
            describe_wait_status("0")


class TestErrorMessage(unittest.TestCase):
    """The wrapper reports the message of an error number."""

    @unittest.skipUnless(HAVE_POSIX, "the posix module is not available")
    def test_error_message_of_a_known_error(self):
        self.assertIn("No such file", error_message(2))

    @unittest.skipUnless(HAVE_POSIX, "the posix module is not available")
    def test_error_message_rejects_a_non_int(self):
        with self.assertRaises(TypeError):
            error_message("2")


class TestPublicApi(unittest.TestCase):
    """The module exposes a stable and complete public API."""

    def test_all_is_sorted_and_unique(self):
        self.assertEqual(len(posix_utils.__all__), len(set(posix_utils.__all__)))
        self.assertEqual(posix_utils.__all__, sorted(posix_utils.__all__))

    def test_every_name_of_all_exists(self):
        for name in posix_utils.__all__:
            with self.subTest(name=name):
                self.assertTrue(hasattr(posix_utils, name))


if __name__ == "__main__":
    unittest.main()
