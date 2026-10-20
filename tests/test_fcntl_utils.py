"""Tests for fcntl_utils."""

import os
import tempfile
import unittest
from unittest.mock import Mock, patch

import fcntl_utils
from fcntl_utils import (
    F_DUPFD,
    F_DUPFD_CLOEXEC,
    F_GETFD,
    F_GETFL,
    F_LOCK,
    F_SETFD,
    F_SETFL,
    F_TLOCK,
    F_ULOCK,
    FD_CLOEXEC,
    LOCK_EX,
    LOCK_NB,
    LOCK_SH,
    LOCK_UN,
    control,
    duplicate_fd,
    file_lock,
    flock,
    get_descriptor_flags,
    get_file_status_flags,
    ioctl,
    is_available,
    is_cloexec,
    lock_kind,
    lock_modes,
    lockf,
    set_descriptor_flags,
    set_file_status_flags,
    unlock,
)


class TestFcntlUtils(unittest.TestCase):
    """Verify the file control helpers.

    The tests lock files in a temporary directory that the test itself
    creates, so no test ever locks a file of the system and no test ever
    waits for a lock that another program holds.
    """

    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.path = os.path.join(self.directory.name, "lockfile")
        self.fd = os.open(self.path, os.O_RDWR | os.O_CREAT, 0o600)

    def tearDown(self):
        try:
            os.close(self.fd)
        except OSError:  # pragma: no cover - the descriptor is already closed
            pass
        self.directory.cleanup()

    def test_is_available(self):
        self.assertIsInstance(is_available(), bool)

    def test_constants_match_the_standard_library(self):
        if not is_available():
            self.skipTest("fcntl module not available")
        import fcntl

        self.assertEqual(fcntl_utils.LOCK_SH, fcntl.LOCK_SH)
        self.assertEqual(fcntl_utils.LOCK_EX, fcntl.LOCK_EX)
        self.assertEqual(fcntl_utils.LOCK_NB, fcntl.LOCK_NB)
        self.assertEqual(fcntl_utils.LOCK_UN, fcntl.LOCK_UN)
        self.assertEqual(fcntl_utils.F_GETFD, fcntl.F_GETFD)
        self.assertEqual(fcntl_utils.F_SETFD, fcntl.F_SETFD)
        self.assertEqual(fcntl_utils.F_GETFL, fcntl.F_GETFL)
        self.assertEqual(fcntl_utils.F_SETFL, fcntl.F_SETFL)
        self.assertEqual(fcntl_utils.F_DUPFD, fcntl.F_DUPFD)
        self.assertEqual(fcntl_utils.F_DUPFD_CLOEXEC, fcntl.F_DUPFD_CLOEXEC)
        self.assertEqual(fcntl_utils.FD_CLOEXEC, fcntl.FD_CLOEXEC)
    def test_flock_locks_the_file(self):
        other = os.open(self.path, os.O_RDWR | os.O_CREAT, 0o600)
        try:
            flock(self.fd, LOCK_EX)
            with self.assertRaises(BlockingIOError):
                flock(other, LOCK_EX | LOCK_NB)
        finally:
            os.close(other)

    def test_flock_releases_the_lock(self):
        other = os.open(self.path, os.O_RDWR | os.O_CREAT, 0o600)
        try:
            flock(self.fd, LOCK_EX)
            unlock(self.fd)
            flock(other, LOCK_EX | LOCK_NB)
        finally:
            os.close(other)

    def test_flock_accepts_a_shared_lock(self):
        other = os.open(self.path, os.O_RDWR | os.O_CREAT, 0o600)
        try:
            flock(self.fd, LOCK_SH)
            flock(other, LOCK_SH | LOCK_NB)
        finally:
            os.close(other)

    def test_flock_validates_its_arguments(self):
        with self.assertRaises(TypeError):
            flock("0", LOCK_EX)  # type: ignore[arg-type]
        with self.assertRaises(ValueError):
            flock(-1, LOCK_EX)
        with self.assertRaises(TypeError):
            flock(self.fd, "exclusive")  # type: ignore[arg-type]
        with self.assertRaises(ValueError):
            flock(self.fd, 1 << 20)
        with self.assertRaises(ValueError):
            flock(self.fd, LOCK_SH | LOCK_EX)
        with self.assertRaises(ValueError):
            flock(self.fd, 0)

    def test_unlock_validates_its_arguments(self):
        with self.assertRaises(TypeError):
            unlock("0")  # type: ignore[arg-type]
        with self.assertRaises(ValueError):
            unlock(-1)

    def test_lockf_locks_and_releases_the_region(self):
        lockf(self.fd, F_LOCK, 4, 0, os.SEEK_SET)
        lockf(self.fd, F_ULOCK, 4, 0, os.SEEK_SET)

    def test_lockf_validates_its_arguments(self):
        with self.assertRaises(TypeError):
            lockf("0", F_LOCK)  # type: ignore[arg-type]
        with self.assertRaises(ValueError):
            lockf(-1, F_LOCK)
        with self.assertRaises(TypeError):
            lockf(self.fd, "lock")  # type: ignore[arg-type]
        with self.assertRaises(ValueError):
            lockf(self.fd, 99)
        with self.assertRaises(TypeError):
            lockf(self.fd, F_LOCK, "4")  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            lockf(self.fd, F_LOCK, 4, "0")  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            lockf(self.fd, F_LOCK, 4, 0, "set")  # type: ignore[arg-type]
        with self.assertRaises(ValueError):
            lockf(self.fd, F_LOCK, 4, 0, 99)

    def test_lockf_translates_the_commands_of_the_interpreter(self):
        older = Mock(spec=["lockf", "F_LOCK"])
        with patch("fcntl_utils._fcntl", older):
            lockf(self.fd, F_LOCK)
        older.lockf.assert_called_once_with(self.fd, F_LOCK, 0, 0, os.SEEK_SET)

        newer = Mock(spec=["lockf"])
        with patch("fcntl_utils._fcntl", newer):
            lockf(self.fd, F_LOCK)
            lockf(self.fd, F_TLOCK)
            lockf(self.fd, F_ULOCK)
        self.assertEqual(newer.lockf.call_count, 3)
        self.assertEqual(newer.lockf.call_args_list[0].args[1], LOCK_EX)
        self.assertEqual(newer.lockf.call_args_list[1].args[1], LOCK_EX | LOCK_NB)
        self.assertEqual(newer.lockf.call_args_list[2].args[1], LOCK_UN)

    def test_control_reads_the_flags_of_the_descriptor(self):
        flags = control(self.fd, F_GETFD)
        self.assertIsInstance(flags, int)
        status = control(self.fd, F_GETFL)
        self.assertIsInstance(status, int)

    def test_control_writes_the_flags(self):
        original = control(self.fd, F_GETFD)
        try:
            control(self.fd, F_SETFD, 0)
            self.assertFalse(is_cloexec(self.fd))
            control(self.fd, F_SETFD, FD_CLOEXEC)
            self.assertTrue(is_cloexec(self.fd))
        finally:
            control(self.fd, F_SETFD, original)
        status = control(self.fd, F_GETFL)
        try:
            control(self.fd, F_SETFL, status | os.O_APPEND)
            self.assertTrue(control(self.fd, F_GETFL) & os.O_APPEND)
        finally:
            control(self.fd, F_SETFL, status)

    def test_control_validates_its_arguments(self):
        with self.assertRaises(TypeError):
            control("0", F_GETFD)  # type: ignore[arg-type]
        with self.assertRaises(ValueError):
            control(-1, F_GETFD)
        with self.assertRaises(TypeError):
            control(self.fd, "get")  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            control(self.fd, F_GETFD, 1.5)  # type: ignore[arg-type]

    def test_ioctl_reports_an_unsupported_request(self):
        with self.assertRaises(OSError):
            ioctl(self.fd, 0x1234)

    def test_ioctl_validates_its_arguments(self):
        with self.assertRaises(TypeError):
            ioctl("0", 1)  # type: ignore[arg-type]
        with self.assertRaises(ValueError):
            ioctl(-1, 1)
        with self.assertRaises(TypeError):
            ioctl(self.fd, "request")  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            ioctl(self.fd, 1, "arg")  # type: ignore[arg-type]

    def test_descriptor_flags_round_trip(self):
        original = get_descriptor_flags(self.fd)
        try:
            set_descriptor_flags(self.fd, 0)
            self.assertFalse(is_cloexec(self.fd))
            set_descriptor_flags(self.fd, FD_CLOEXEC)
            self.assertTrue(is_cloexec(self.fd))
        finally:
            set_descriptor_flags(self.fd, original)

    def test_descriptor_flags_validate_their_arguments(self):
        with self.assertRaises(TypeError):
            get_descriptor_flags("0")  # type: ignore[arg-type]
        with self.assertRaises(ValueError):
            get_descriptor_flags(-1)
        with self.assertRaises(TypeError):
            set_descriptor_flags(self.fd, "flags")  # type: ignore[arg-type]
        with self.assertRaises(ValueError):
            set_descriptor_flags(self.fd, -1)

    def test_file_status_flags_round_trip(self):
        original = get_file_status_flags(self.fd)
        try:
            set_file_status_flags(self.fd, original | os.O_APPEND)
            self.assertTrue(get_file_status_flags(self.fd) & os.O_APPEND)
        finally:
            set_file_status_flags(self.fd, original)

    def test_file_status_flags_validate_their_arguments(self):
        with self.assertRaises(TypeError):
            get_file_status_flags("0")  # type: ignore[arg-type]
        with self.assertRaises(ValueError):
            get_file_status_flags(-1)
        with self.assertRaises(TypeError):
            set_file_status_flags(self.fd, 1.5)  # type: ignore[arg-type]
        with self.assertRaises(ValueError):
            set_file_status_flags(self.fd, -1)

    def test_duplicate_fd_copies_the_descriptor(self):
        copy = duplicate_fd(self.fd)
        try:
            self.assertNotEqual(copy, self.fd)
            self.assertTrue(is_cloexec(copy))
        finally:
            os.close(copy)

    def test_duplicate_fd_uses_the_expected_command(self):
        real = fcntl_utils._fcntl
        module = Mock(spec=["fcntl"])
        module.fcntl.side_effect = real.fcntl
        with patch("fcntl_utils._fcntl", module):
            copy = duplicate_fd(self.fd)
            os.close(copy)
            inheritable = duplicate_fd(self.fd, inheritable=True)
            os.close(inheritable)
        self.assertEqual(module.fcntl.call_args_list[0].args[1], F_DUPFD_CLOEXEC)
        self.assertEqual(module.fcntl.call_args_list[1].args[1], F_DUPFD)

    def test_duplicate_fd_can_keep_the_copy_inheritable(self):
        copy = duplicate_fd(self.fd, inheritable=True)
        try:
            self.assertFalse(is_cloexec(copy))
        finally:
            os.close(copy)

    def test_duplicate_fd_validates_its_arguments(self):
        with self.assertRaises(TypeError):
            duplicate_fd("0")  # type: ignore[arg-type]
        with self.assertRaises(ValueError):
            duplicate_fd(-1)
        with self.assertRaises(TypeError):
            duplicate_fd(self.fd, "0")  # type: ignore[arg-type]
        with self.assertRaises(ValueError):
            duplicate_fd(self.fd, -1)
        with self.assertRaises(TypeError):
            duplicate_fd(self.fd, 0, "yes")  # type: ignore[arg-type]

    def test_lock_modes_and_lock_kind(self):
        modes = lock_modes()
        self.assertEqual(modes["shared"], LOCK_SH)
        self.assertEqual(modes["exclusive"], LOCK_EX)
        self.assertEqual(modes["unlock"], LOCK_UN)
        self.assertEqual(lock_kind("shared"), LOCK_SH)
        self.assertEqual(lock_kind("EXCLUSIVE"), LOCK_EX)
        self.assertEqual(lock_kind("unlock", blocking=False), LOCK_UN | LOCK_NB)

    def test_lock_kind_validates_its_arguments(self):
        with self.assertRaises(TypeError):
            lock_kind(1)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            lock_kind("shared", "yes")  # type: ignore[arg-type]
        with self.assertRaises(ValueError):
            lock_kind("unknown")

    def test_file_lock_holds_the_lock_for_the_block(self):
        other = os.open(self.path, os.O_RDWR | os.O_CREAT, 0o600)
        try:
            with file_lock(self.path) as fd:
                self.assertIsInstance(fd, int)
                with self.assertRaises(BlockingIOError):
                    flock(other, LOCK_EX | LOCK_NB)
            flock(other, LOCK_EX | LOCK_NB)
        finally:
            os.close(other)

    def test_file_lock_can_refuse_to_create_the_file(self):
        missing = os.path.join(self.directory.name, "missing")
        with self.assertRaises(FileNotFoundError):
            with file_lock(missing, create=False):
                pass

    def test_file_lock_validates_its_arguments(self):
        with self.assertRaises(TypeError):
            with file_lock(1):  # type: ignore[arg-type]
                pass
        with self.assertRaises(TypeError):
            with file_lock(self.path, "exclusive", "yes"):  # type: ignore[arg-type]
                pass
        with self.assertRaises(TypeError):
            with file_lock(self.path, "exclusive", True, "yes"):  # type: ignore[arg-type]
                pass
        with self.assertRaises(ValueError):
            with file_lock(self.path, "unknown"):
                pass

    def test_helpers_report_a_missing_standard_library_module(self):
        with patch("fcntl_utils._fcntl", None):
            self.assertFalse(is_available())
            with self.assertRaises(RuntimeError):
                flock(self.fd, LOCK_EX)
            with self.assertRaises(RuntimeError):
                unlock(self.fd)
            with self.assertRaises(RuntimeError):
                lockf(self.fd, F_LOCK)
            with self.assertRaises(RuntimeError):
                control(self.fd, F_GETFD)
            with self.assertRaises(RuntimeError):
                ioctl(self.fd, 1)
            with self.assertRaises(RuntimeError):
                get_descriptor_flags(self.fd)
            with self.assertRaises(RuntimeError):
                set_descriptor_flags(self.fd, 0)
            with self.assertRaises(RuntimeError):
                get_file_status_flags(self.fd)
            with self.assertRaises(RuntimeError):
                set_file_status_flags(self.fd, 0)
            with self.assertRaises(RuntimeError):
                duplicate_fd(self.fd)
            with self.assertRaises(RuntimeError):
                file_lock(self.path).__enter__()

    def test_all_names_are_exported(self):
        self.assertIsNotNone(fcntl_utils.__all__)
        self.assertEqual(len(fcntl_utils.__all__), len(set(fcntl_utils.__all__)))
        for name in fcntl_utils.__all__:
            self.assertTrue(hasattr(fcntl_utils, name), name)


if __name__ == "__main__":
    unittest.main()
