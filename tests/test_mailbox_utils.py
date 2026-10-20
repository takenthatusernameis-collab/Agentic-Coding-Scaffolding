"""Tests for mailbox_utils."""

import mailbox
import tempfile
import unittest
from pathlib import Path

from mailbox_utils import (
    Error,
    ExternalClashError,
    FormatError,
    NoSuchMailboxError,
    NotEmptyError,
    create_babyl,
    create_babyl_message,
    create_mailbox,
    create_maildir,
    create_maildir_message,
    create_mbox,
    create_mbox_message,
    create_mh,
    create_mh_message,
    create_mmdf,
    create_mmdf_message,
    is_external_clash_error,
    is_format_error,
    is_mailbox_error,
    is_no_such_mailbox_error,
    is_not_empty_error,
)


class TestMailboxBasics(unittest.TestCase):
    def test_exceptions_and_classes(self):
        self.assertIs(Error, mailbox.Error)
        self.assertIs(ExternalClashError, mailbox.ExternalClashError)
        self.assertIs(FormatError, mailbox.FormatError)
        self.assertIs(NoSuchMailboxError, mailbox.NoSuchMailboxError)
        self.assertIs(NotEmptyError, mailbox.NotEmptyError)

    def test_type_checks(self):
        self.assertTrue(is_mailbox_error(FormatError()))
        self.assertFalse(is_mailbox_error(ValueError()))
        self.assertTrue(is_external_clash_error(ExternalClashError()))
        self.assertTrue(is_format_error(FormatError()))
        self.assertTrue(is_no_such_mailbox_error(NoSuchMailboxError()))
        self.assertTrue(is_not_empty_error(NotEmptyError()))


class TestMailboxFactories(unittest.TestCase):
    def test_create_mailbox(self):
        with tempfile.TemporaryDirectory() as td:
            mbox = create_mailbox(Path(td) / "test.mbox")
            self.assertIsInstance(mbox, mailbox.Mailbox)

    def test_create_mbox(self):
        with tempfile.TemporaryDirectory() as td:
            mbox = create_mbox(Path(td) / "test.mbox")
            self.assertIsInstance(mbox, mailbox.mbox)

    def test_create_maildir(self):
        with tempfile.TemporaryDirectory() as td:
            md = create_maildir(Path(td) / "testdir")
            self.assertIsInstance(md, mailbox.Maildir)

    def test_create_mh(self):
        with tempfile.TemporaryDirectory() as td:
            mh = create_mh(Path(td) / "testmh")
            self.assertIsInstance(mh, mailbox.MH)

    def test_create_mmdf(self):
        with tempfile.TemporaryDirectory() as td:
            mmdf = create_mmdf(Path(td) / "test.mmdf")
            self.assertIsInstance(mmdf, mailbox.MMDF)

    def test_create_babyl(self):
        with tempfile.TemporaryDirectory() as td:
            babyl = create_babyl(Path(td) / "test.babyl")
            self.assertIsInstance(babyl, mailbox.Babyl)


class TestMailboxMessages(unittest.TestCase):
    def test_create_messages(self):
        self.assertIsInstance(create_mbox_message("Subject: hi\n\nbody\n"), mailbox.mboxMessage)
        self.assertIsInstance(
            create_maildir_message("Subject: hi\n\nbody\n"), mailbox.MaildirMessage
        )
        self.assertIsInstance(create_mh_message("Subject: hi\n\nbody\n"), mailbox.MHMessage)
        self.assertIsInstance(create_mmdf_message("Subject: hi\n\nbody\n"), mailbox.MMDFMessage)
        self.assertIsInstance(create_babyl_message("Subject: hi\n\nbody\n"), mailbox.BabylMessage)


if __name__ == "__main__":
    unittest.main()
