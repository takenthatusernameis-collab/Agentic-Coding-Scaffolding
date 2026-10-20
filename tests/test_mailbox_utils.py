"""Tests for mailbox_utils."""

from __future__ import annotations

import email.message
import mailbox
import os
import tempfile
import unittest

import mailbox_utils


class TestMailboxUtils(unittest.TestCase):
    def test_exports(self) -> None:
        self.assertTrue(hasattr(mailbox_utils, "mbox"))
        self.assertTrue(hasattr(mailbox_utils, "Maildir"))
        self.assertTrue(hasattr(mailbox_utils, "MH"))
        self.assertTrue(hasattr(mailbox_utils, "Babyl"))
        self.assertTrue(hasattr(mailbox_utils, "MMDF"))

    def test_create_mbox_and_operations(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            path = os.path.join(tmpdir, "test.mbox")
            mbox = mailbox_utils.create_mbox(path, create=True)
            self.assertIsInstance(mbox, mailbox.mbox)
            msg = email.message.Message()
            msg["From"] = "a@example.com"
            msg["To"] = "b@example.com"
            msg["Subject"] = "Hello"
            msg.set_payload("Body\n")
            key = mailbox_utils.add_message(mbox, msg)
            self.assertTrue(isinstance(key, (str, int, bytes)))
            keys = mailbox_utils.list_message_keys(mbox)
            keys_str = [k if isinstance(k, str) else str(k) for k in keys]
            key_str = key if isinstance(key, str) else str(key)
            self.assertIn(key_str, keys_str)
            got = mailbox_utils.get_message(mbox, key_str)
            self.assertIsInstance(got, email.message.Message)
            self.assertEqual(list(mailbox_utils.iter_messages(mbox))[0]["Subject"], "Hello")
            mailbox_utils.remove_message(mbox, key_str)
            self.assertEqual(len(mailbox_utils.list_message_keys(mbox)), 0)
            mbox.close()

    def test_create_maildir(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            path = os.path.join(tmpdir, "Maildir")
            md = mailbox_utils.create_maildir(path, create=True)
            self.assertIsInstance(md, mailbox.Maildir)
            md.close()

    def test_create_mh(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            path = os.path.join(tmpdir, "MH")
            mh = mailbox_utils.create_mh(path, create=True)
            self.assertIsInstance(mh, mailbox.MH)
            mh.close()

    def test_create_babyl(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            path = os.path.join(tmpdir, "Babyl")
            babyl = mailbox_utils.create_babyl(path, create=True)
            self.assertIsInstance(babyl, mailbox.Babyl)
            babyl.close()

    def test_create_mmdf(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            path = os.path.join(tmpdir, "test.mmdf")
            mmdf = mailbox_utils.create_mmdf(path, create=True)
            self.assertIsInstance(mmdf, mailbox.MMDF)
            mmdf.close()

    def test_open_mailbox(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            path = os.path.join(tmpdir, "test.mbox")
            mb = mailbox_utils.open_mailbox(path, factory=mailbox.mbox, create=True)
            self.assertIsInstance(mb, mailbox.Mailbox)
            mb.close()

    def test_iter_message_keys(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            path = os.path.join(tmpdir, "test.mbox")
            mbox = mailbox_utils.create_mbox(path, create=True)
            msg = email.message.Message()
            msg.set_payload("hi")
            key = mailbox_utils.add_message(mbox, msg)
            keys = list(mailbox_utils.iter_message_keys(mbox))
            keys_str = [k if isinstance(k, str) else str(k) for k in keys]
            self.assertIn(key if isinstance(key, str) else str(key), keys_str)
            mbox.close()

    def test_lock_unlock(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            path = os.path.join(tmpdir, "test.mbox")
            mbox = mailbox_utils.create_mbox(path, create=True)
            mailbox_utils.lock_mailbox(mbox)
            mailbox_utils.unlock_mailbox(mbox)
            mbox.close()

    def test_type_errors(self) -> None:
        with self.assertRaises(TypeError):
            mailbox_utils.create_mbox(123)  # type: ignore
        with self.assertRaises(TypeError):
            mailbox_utils.create_mbox("/tmp/x", create="yes")  # type: ignore
        with tempfile.TemporaryDirectory() as tmpdir:
            path = os.path.join(tmpdir, "test.mbox")
            mbox = mailbox_utils.create_mbox(path, create=True)
            with self.assertRaises(TypeError):
                mailbox_utils.iter_messages("not_a_mailbox")  # type: ignore
            with self.assertRaises(TypeError):
                mailbox_utils.get_message(mbox, 123)  # type: ignore
            mbox.close()


if __name__ == "__main__":
    unittest.main()
