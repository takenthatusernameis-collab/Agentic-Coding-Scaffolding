"""Tests for smtplib_utils module."""

import smtplib
import socket
import ssl
import unittest
from unittest import mock

import smtplib_utils

GREETING = "220 mail.example.com ESMTP\r\n"
EHLO_REPLY = [
    "250-mail.example.com Hello\r\n",
    "250-SIZE 35882577\r\n",
    "250 HELP\r\n",
]


class FakeSocket:
    """A socket that replays scripted server replies."""

    def __init__(self, replies):
        self._replies = list(replies)
        self._buffer = b""
        self.sent = []
        self.closed = False

    def makefile(self, mode="rb", *args, **kwargs):
        return self

    def readline(self, size=-1):
        if not self._buffer:
            if not self._replies:
                return b""
            self._buffer = self._replies.pop(0).encode("latin-1")
        line, separator, rest = self._buffer.partition(b"\n")
        self._buffer = rest
        if not separator:
            return line
        return line + b"\n"

    def sendall(self, data):
        self.sent.append(data)

    def close(self):
        self.closed = True

    def settimeout(self, timeout):
        return None

    def getpeername(self):
        return ("127.0.0.1", 25)

    def commands(self):
        """Return everything the client sent, without the line endings."""
        return [chunk.decode("latin-1").strip() for chunk in self.sent]


def connected_socket(replies):
    """Return a fake socket and a patcher that hands it to the client."""
    fake = FakeSocket(replies)
    return fake, mock.patch("socket.create_connection", return_value=fake)


class TestExports(unittest.TestCase):
    def test_constants(self):
        self.assertIs(smtplib_utils.CRLF, smtplib.CRLF)
        self.assertEqual(smtplib_utils.SMTP_PORT, smtplib.SMTP_PORT)
        self.assertEqual(smtplib_utils.SMTP_SSL_PORT, smtplib.SMTP_SSL_PORT)
        self.assertEqual(smtplib_utils.LMTP_PORT, smtplib.LMTP_PORT)

    def test_classes_exported(self):
        self.assertIs(smtplib_utils.SMTP, smtplib.SMTP)
        self.assertIs(smtplib_utils.SMTP_SSL, smtplib.SMTP_SSL)
        self.assertIs(smtplib_utils.LMTP, smtplib.LMTP)

    def test_error_classes_exported(self):
        self.assertIs(smtplib_utils.SMTPException, smtplib.SMTPException)
        self.assertIs(
            smtplib_utils.SMTPNotSupportedError, smtplib.SMTPNotSupportedError
        )
        self.assertIs(
            smtplib_utils.SMTPServerDisconnected, smtplib.SMTPServerDisconnected
        )
        self.assertIs(
            smtplib_utils.SMTPResponseException, smtplib.SMTPResponseException
        )
        self.assertIs(smtplib_utils.SMTPSenderRefused, smtplib.SMTPSenderRefused)
        self.assertIs(
            smtplib_utils.SMTPRecipientsRefused, smtplib.SMTPRecipientsRefused
        )
        self.assertIs(smtplib_utils.SMTPDataError, smtplib.SMTPDataError)
        self.assertIs(smtplib_utils.SMTPConnectError, smtplib.SMTPConnectError)
        self.assertIs(smtplib_utils.SMTPHeloError, smtplib.SMTPHeloError)
        self.assertIs(
            smtplib_utils.SMTPAuthenticationError, smtplib.SMTPAuthenticationError
        )


class TestAddressHelpers(unittest.TestCase):
    def test_quoteaddr(self):
        self.assertEqual(smtplib_utils.quoteaddr("user@example.com"), "<user@example.com>")
        self.assertEqual(
            smtplib_utils.quoteaddr("Alice <alice@example.com>"), "<alice@example.com>"
        )

    def test_quoteaddr_bad_type(self):
        with self.assertRaises(TypeError):
            smtplib_utils.quoteaddr(42)  # type: ignore[arg-type]

    def test_quote_string(self):
        self.assertEqual(smtplib_utils.quote_string("plain"), '"plain"')
        self.assertEqual(smtplib_utils.quote_string('say "hi"'), '"say \\"hi\\""')

    def test_quote_string_escapes_backslashes(self):
        self.assertEqual(smtplib_utils.quote_string("a\\b"), '"a\\\\b"')

    def test_quote_string_bad_type(self):
        with self.assertRaises(TypeError):
            smtplib_utils.quote_string(None)  # type: ignore[arg-type]

    def test_quote_data(self):
        self.assertEqual(smtplib_utils.quote_data("one\ntwo"), "one\r\ntwo")
        self.assertEqual(smtplib_utils.quote_data(".hidden"), "..hidden")

    def test_quote_data_bad_type(self):
        with self.assertRaises(TypeError):
            smtplib_utils.quote_data(b"bytes")  # type: ignore[arg-type]

    def test_parse_address(self):
        self.assertEqual(
            smtplib_utils.parse_address("Alice <alice@example.com>"),
            ("Alice", "alice@example.com"),
        )
        self.assertEqual(
            smtplib_utils.parse_address("alice@example.com"), ("", "alice@example.com")
        )

    def test_parse_address_bad_type(self):
        with self.assertRaises(TypeError):
            smtplib_utils.parse_address(1)  # type: ignore[arg-type]

    def test_address_only(self):
        self.assertEqual(
            smtplib_utils.address_only("Alice <alice@example.com>"), "alice@example.com"
        )
        self.assertEqual(smtplib_utils.address_only("alice@example.com"), "alice@example.com")

    def test_address_only_keeps_unparsable_value(self):
        self.assertEqual(smtplib_utils.address_only("not an address"), "not")

    def test_address_only_keeps_a_value_without_an_address(self):
        self.assertEqual(smtplib_utils.address_only("<"), "<")

    def test_address_only_bad_type(self):
        with self.assertRaises(TypeError):
            smtplib_utils.address_only(object())  # type: ignore[arg-type]

    def test_format_address(self):
        self.assertEqual(
            smtplib_utils.format_address("Alice", "alice@example.com"),
            "Alice <alice@example.com>",
        )

    def test_format_address_encodes_non_ascii(self):
        formatted = smtplib_utils.format_address("Älice", "alice@example.com")
        self.assertIn("=?utf-8?", formatted)
        self.assertTrue(formatted.endswith("<alice@example.com>"))

    def test_format_address_bad_type(self):
        with self.assertRaises(TypeError):
            smtplib_utils.format_address(None, "alice@example.com")  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            smtplib_utils.format_address("Alice", 5)  # type: ignore[arg-type]

    def test_getfqdn(self):
        with mock.patch.object(socket, "getfqdn", return_value="host.example.com") as fake:
            self.assertEqual(smtplib_utils.getfqdn("host"), "host.example.com")
        fake.assert_called_once_with("host")

    def test_getfqdn_bad_type(self):
        with self.assertRaises(TypeError):
            smtplib_utils.getfqdn(3)  # type: ignore[arg-type]


class TestParseResponse(unittest.TestCase):
    def test_single_line(self):
        self.assertEqual(smtplib_utils.parse_response("250 OK"), (250, "OK"))

    def test_bytes_input(self):
        self.assertEqual(smtplib_utils.parse_response(b"250 OK"), (250, "OK"))

    def test_multiline(self):
        code, message = smtplib_utils.parse_response("250-First\r\n250 Second")
        self.assertEqual(code, 250)
        self.assertEqual(message, "First\nSecond")

    def test_invalid_code(self):
        self.assertEqual(smtplib_utils.parse_response("oops"), (-1, ""))

    def test_empty_response(self):
        with self.assertRaises(ValueError):
            smtplib_utils.parse_response("")

    def test_bad_type(self):
        with self.assertRaises(TypeError):
            smtplib_utils.parse_response(42)  # type: ignore[arg-type]


class TestParseEhloFeatures(unittest.TestCase):
    def test_message_form(self):
        features = smtplib_utils.parse_ehlo_features(
            "mail.example.com Hello\nSIZE 35882577\n8BITMIME\nHELP"
        )
        self.assertEqual(
            features, {"size": "35882577", "8bitmime": "", "help": ""}
        )

    def test_raw_reply_form(self):
        features = smtplib_utils.parse_ehlo_features(
            "250-mail.example.com Hello\r\n250-SIZE 100\r\n250 HELP\r\n"
        )
        self.assertEqual(features, {"size": "100", "help": ""})

    def test_greeting_can_be_kept(self):
        features = smtplib_utils.parse_ehlo_features("SIZE 100", skip_greeting=False)
        self.assertEqual(features, {"size": "100"})

    def test_auth_mechanisms_are_merged(self):
        features = smtplib_utils.parse_ehlo_features(
            "AUTH LOGIN PLAIN", skip_greeting=False
        )
        self.assertEqual(features, {"auth": "LOGIN PLAIN"})

    def test_empty_response(self):
        self.assertEqual(smtplib_utils.parse_ehlo_features(""), {})

    def test_bad_type(self):
        with self.assertRaises(TypeError):
            smtplib_utils.parse_ehlo_features(7)  # type: ignore[arg-type]


class TestBuildMessage(unittest.TestCase):
    def test_headers(self):
        message = smtplib_utils.build_message(
            "alice@example.com", ["bob@example.com"], "Report", "The body"
        )
        self.assertEqual(message["From"], "alice@example.com")
        self.assertEqual(message["To"], "bob@example.com")
        self.assertEqual(message["Subject"], "Report")
        self.assertEqual(message.get_content_type(), "text/plain")
        self.assertEqual(message.get_content().strip(), "The body")

    def test_multiple_recipients_are_joined(self):
        message = smtplib_utils.build_message(
            "alice@example.com", ["bob@example.com", "carol@example.com"], "Hi", "Body"
        )
        self.assertEqual(message["To"], "bob@example.com, carol@example.com")

    def test_cc_is_added(self):
        message = smtplib_utils.build_message(
            "alice@example.com",
            ["bob@example.com"],
            "Hi",
            "Body",
            cc=["carol@example.com"],
        )
        self.assertEqual(message["Cc"], "carol@example.com")

    def test_bcc_is_not_a_header(self):
        message = smtplib_utils.build_message(
            "alice@example.com",
            ["bob@example.com"],
            "Hi",
            "Body",
            bcc=["hidden@example.com"],
        )
        self.assertIsNone(message["Bcc"])

    def test_reply_to_is_added(self):
        message = smtplib_utils.build_message(
            "alice@example.com",
            ["bob@example.com"],
            "Hi",
            "Body",
            reply_to="replies@example.com",
        )
        self.assertEqual(message["Reply-To"], "replies@example.com")

    def test_html_alternative(self):
        message = smtplib_utils.build_message(
            "alice@example.com",
            ["bob@example.com"],
            "Hi",
            "Body",
            html="<p>Body</p>",
        )
        self.assertEqual(message.get_content_type(), "multipart/alternative")
        self.assertEqual(
            message.get_body(preferencelist=("plain",)).get_content().strip(), "Body"
        )
        self.assertEqual(
            message.get_body(preferencelist=("html",)).get_content().strip(), "<p>Body</p>"
        )

    def test_attachment_media_type_is_guessed(self):
        message = smtplib_utils.build_message(
            "alice@example.com",
            ["bob@example.com"],
            "Hi",
            "Body",
            attachments=[("picture.png", b"\x89PNG")],
        )
        self.assertEqual(message.get_content_type(), "multipart/mixed")
        attachments = list(message.iter_attachments())
        self.assertEqual(len(attachments), 1)
        self.assertEqual(attachments[0].get_content_type(), "image/png")
        self.assertEqual(attachments[0].get_filename(), "picture.png")

    def test_unknown_attachment_type_falls_back(self):
        message = smtplib_utils.build_message(
            "alice@example.com",
            ["bob@example.com"],
            "Hi",
            "Body",
            attachments=[("payload.unknown-extension", b"data")],
        )
        attachment = list(message.iter_attachments())[0]
        self.assertEqual(attachment.get_content_type(), "application/octet-stream")

    def test_bad_sender(self):
        with self.assertRaises(TypeError):
            smtplib_utils.build_message(1, ["bob@example.com"], "Hi", "Body")  # type: ignore[arg-type]

    def test_empty_sender(self):
        with self.assertRaises(ValueError):
            smtplib_utils.build_message("  ", ["bob@example.com"], "Hi", "Body")

    def test_empty_recipients(self):
        with self.assertRaises(ValueError):
            smtplib_utils.build_message("alice@example.com", [], "Hi", "Body")

    def test_bad_recipient(self):
        with self.assertRaises(TypeError):
            smtplib_utils.build_message("alice@example.com", [5], "Hi", "Body")  # type: ignore[list-item]

    def test_empty_recipient(self):
        with self.assertRaises(ValueError):
            smtplib_utils.build_message("alice@example.com", [""], "Hi", "Body")

    def test_bad_body(self):
        with self.assertRaises(TypeError):
            smtplib_utils.build_message("alice@example.com", ["bob@example.com"], "Hi", 5)  # type: ignore[arg-type]

    def test_bad_html(self):
        with self.assertRaises(TypeError):
            smtplib_utils.build_message(
                "alice@example.com", ["bob@example.com"], "Hi", "Body", html=5
            )  # type: ignore[arg-type]

    def test_bad_attachment(self):
        with self.assertRaises(TypeError):
            smtplib_utils.build_message(
                "alice@example.com",
                ["bob@example.com"],
                "Hi",
                "Body",
                attachments=[("picture.png", "not bytes")],  # type: ignore[list-item]
            )

    def test_malformed_attachment(self):
        with self.assertRaises(TypeError):
            smtplib_utils.build_message(
                "alice@example.com",
                ["bob@example.com"],
                "Hi",
                "Body",
                attachments=["picture.png"],  # type: ignore[list-item]
            )


class TestCreateSmtp(unittest.TestCase):
    def test_arguments_are_forwarded(self):
        with mock.patch.object(smtplib, "SMTP") as fake:
            client = smtplib_utils.create_smtp(
                "example.org", 2525, local_hostname="client.example.org", timeout=5
            )
        self.assertIs(client, fake.return_value)
        args, kwargs = fake.call_args
        self.assertEqual(args, ("example.org", 2525))
        self.assertEqual(kwargs["local_hostname"], "client.example.org")
        self.assertEqual(kwargs["timeout"], 5.0)
        self.assertIsNone(kwargs["source_address"])

    def test_source_address_is_forwarded(self):
        with mock.patch.object(smtplib, "SMTP") as fake:
            smtplib_utils.create_smtp("example.org", 25, source_address=("10.0.0.1", 0))
        self.assertEqual(fake.call_args.kwargs["source_address"], ("10.0.0.1", 0))

    def test_bad_host(self):
        with self.assertRaises(TypeError):
            smtplib_utils.create_smtp(123)  # type: ignore[arg-type]

    def test_bad_port(self):
        with self.assertRaises(TypeError):
            smtplib_utils.create_smtp("localhost", "25")  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            smtplib_utils.create_smtp("localhost", True)  # type: ignore[arg-type]

    def test_port_out_of_range(self):
        with self.assertRaises(ValueError):
            smtplib_utils.create_smtp("localhost", 70000)
        with self.assertRaises(ValueError):
            smtplib_utils.create_smtp("localhost", -1)

    def test_bad_timeout(self):
        with self.assertRaises(TypeError):
            smtplib_utils.create_smtp("localhost", 25, timeout="5")  # type: ignore[arg-type]
        with self.assertRaises(ValueError):
            smtplib_utils.create_smtp("localhost", 25, timeout=0)
        with self.assertRaises(ValueError):
            smtplib_utils.create_smtp("localhost", 25, timeout=-1)

    def test_bad_source_address(self):
        with self.assertRaises(TypeError):
            smtplib_utils.create_smtp("localhost", 25, source_address="10.0.0.1")  # type: ignore[arg-type]
        with self.assertRaises(ValueError):
            smtplib_utils.create_smtp("localhost", 25, source_address=("10.0.0.1", 99999))

    def test_bad_local_hostname(self):
        with self.assertRaises(TypeError):
            smtplib_utils.create_smtp("localhost", 25, local_hostname=5)  # type: ignore[arg-type]

    def test_client_connects(self):
        fake, patcher = connected_socket([GREETING])
        with patcher:
            client = smtplib_utils.create_smtp(
                "mail.example.com", 25, local_hostname="client.example.org"
            )
        self.assertIs(client.sock, fake)
        self.assertEqual(client.local_hostname, "client.example.org")


class TestCreateSmtpSsl(unittest.TestCase):
    def test_arguments_are_forwarded(self):
        with mock.patch.object(smtplib, "SMTP_SSL") as fake:
            client = smtplib_utils.create_smtp_ssl(
                "example.org", 465, local_hostname="client.example.org", timeout=3
            )
        self.assertIs(client, fake.return_value)
        args, kwargs = fake.call_args
        self.assertEqual(args, ("example.org", 465))
        self.assertEqual(kwargs["local_hostname"], "client.example.org")
        self.assertEqual(kwargs["timeout"], 3.0)
        self.assertIsNone(kwargs["context"])

    def test_context_is_forwarded(self):
        context = ssl.create_default_context()
        with mock.patch.object(smtplib, "SMTP_SSL") as fake:
            smtplib_utils.create_smtp_ssl("example.org", 465, context=context)
        self.assertIs(fake.call_args.kwargs["context"], context)

    def test_bad_port(self):
        with self.assertRaises(ValueError):
            smtplib_utils.create_smtp_ssl("example.org", 70000)

    def test_client_wraps_the_socket(self):
        fake, patcher = connected_socket([GREETING])
        with patcher, mock.patch.object(
            ssl.SSLContext, "wrap_socket", side_effect=lambda sock, **kwargs: sock
        ):
            client = smtplib_utils.create_smtp_ssl(
                "mail.example.com", 465, local_hostname="client.example.org"
            )
        self.assertIs(client.sock, fake)


class TestCreateLmtp(unittest.TestCase):
    def test_arguments_are_forwarded(self):
        with mock.patch.object(smtplib, "LMTP") as fake:
            client = smtplib_utils.create_lmtp(
                "example.org", 2003, local_hostname="client.example.org", timeout=2
            )
        self.assertIs(client, fake.return_value)
        args, kwargs = fake.call_args
        self.assertEqual(args, ("example.org", 2003))
        self.assertEqual(kwargs["local_hostname"], "client.example.org")
        self.assertEqual(kwargs["timeout"], 2.0)

    def test_default_port(self):
        with mock.patch.object(smtplib, "LMTP") as fake:
            smtplib_utils.create_lmtp()
        self.assertEqual(fake.call_args.args[1], smtplib.LMTP_PORT)

    def test_bad_host(self):
        with self.assertRaises(TypeError):
            smtplib_utils.create_lmtp(5)  # type: ignore[arg-type]

    def test_bad_port(self):
        with self.assertRaises(ValueError):
            smtplib_utils.create_lmtp("example.org", -5)


class TestSend(unittest.TestCase):
    def _client(self, replies):
        fake, patcher = connected_socket(replies)
        return fake, patcher

    def test_send_text_runs_a_full_transaction(self):
        replies = [GREETING] + EHLO_REPLY + [
            "250 OK\r\n",
            "250 OK\r\n",
            "354 Go ahead\r\n",
            "250 OK\r\n",
            "221 Bye\r\n",
        ]
        fake, patcher = self._client(replies)
        with patcher:
            client = smtplib_utils.create_smtp(
                "mail.example.com", 25, local_hostname="client.example.org"
            )
            refused = smtplib_utils.send_text(
                client,
                "alice@example.com",
                ["bob@example.com"],
                "Report",
                "The body",
            )
            client.quit()
        self.assertEqual(refused, {})
        commands = fake.commands()
        self.assertEqual(commands[0], "ehlo client.example.org")
        self.assertTrue(commands[1].startswith("mail FROM:<alice@example.com>"))
        self.assertEqual(commands[2], "rcpt TO:<bob@example.com>")
        self.assertEqual(commands[3], "data")
        self.assertIn("Subject: Report", commands[4])
        self.assertTrue(commands[4].endswith("."))
        self.assertEqual(commands[5], "quit")

    def test_bcc_reaches_the_envelope_only(self):
        replies = [GREETING] + EHLO_REPLY + [
            "250 OK\r\n",
            "250 OK\r\n",
            "250 OK\r\n",
            "354 Go ahead\r\n",
            "250 OK\r\n",
        ]
        fake, patcher = self._client(replies)
        with patcher:
            client = smtplib_utils.create_smtp(
                "mail.example.com", 25, local_hostname="client.example.org"
            )
            smtplib_utils.send_text(
                client,
                "alice@example.com",
                ["bob@example.com"],
                "Report",
                "The body",
                bcc=["hidden@example.com"],
            )
        commands = fake.commands()
        self.assertIn("rcpt TO:<hidden@example.com>", commands)
        self.assertNotIn("Bcc: hidden@example.com", commands[4])

    def test_refused_recipient_is_reported(self):
        replies = [GREETING] + EHLO_REPLY + [
            "250 OK\r\n",
            "550 No such user\r\n",
            "250 OK\r\n",
            "354 Go ahead\r\n",
            "250 OK\r\n",
        ]
        fake, patcher = self._client(replies)
        with patcher:
            client = smtplib_utils.create_smtp(
                "mail.example.com", 25, local_hostname="client.example.org"
            )
            refused = smtplib_utils.send_text(
                client,
                "alice@example.com",
                ["bob@example.com", "carol@example.com"],
                "Report",
                "The body",
            )
        self.assertEqual(list(refused), ["bob@example.com"])
        self.assertEqual(refused["bob@example.com"][0], 550)
        self.assertEqual(refused["bob@example.com"][1], b"No such user")

    def test_all_recipients_refused_raises(self):
        replies = [GREETING] + EHLO_REPLY + [
            "250 OK\r\n",
            "550 No such user\r\n",
            "250 OK\r\n",
        ]
        fake, patcher = self._client(replies)
        with patcher:
            client = smtplib_utils.create_smtp(
                "mail.example.com", 25, local_hostname="client.example.org"
            )
            with self.assertRaises(smtplib.SMTPRecipientsRefused) as caught:
                smtplib_utils.send_text(
                    client,
                    "alice@example.com",
                    ["bob@example.com"],
                    "Report",
                    "The body",
                )
        self.assertIn("bob@example.com", caught.exception.recipients)
        self.assertIn("rset", fake.commands())

    def test_send_message_uses_the_message_headers(self):
        replies = [GREETING] + EHLO_REPLY + [
            "250 OK\r\n",
            "250 OK\r\n",
            "354 Go ahead\r\n",
            "250 OK\r\n",
        ]
        fake, patcher = self._client(replies)
        message = smtplib_utils.build_message(
            "alice@example.com", ["bob@example.com"], "Report", "The body"
        )
        with patcher:
            client = smtplib_utils.create_smtp(
                "mail.example.com", 25, local_hostname="client.example.org"
            )
            refused = smtplib_utils.send_message(client, message)
        self.assertEqual(refused, {})
        commands = fake.commands()
        self.assertTrue(commands[1].startswith("mail FROM:<alice@example.com>"))
        self.assertIn("size=", commands[1])
        self.assertEqual(commands[2], "rcpt TO:<bob@example.com>")

    def test_bad_client(self):
        with self.assertRaises(TypeError):
            smtplib_utils.send_text(object(), "alice@example.com", ["bob@x.com"], "s", "b")  # type: ignore[arg-type]

    def test_bad_message(self):
        client = mock.Mock(spec=smtplib.SMTP)
        with self.assertRaises(TypeError):
            smtplib_utils.send_message(client, "not a message")  # type: ignore[arg-type]

    def test_bad_option(self):
        client = mock.Mock(spec=smtplib.SMTP)
        message = smtplib_utils.build_message(
            "alice@example.com", ["bob@example.com"], "Report", "The body"
        )
        with self.assertRaises(ValueError):
            smtplib_utils.send_message(client, message, mail_options=("SIZE=1\n",))
        with self.assertRaises(TypeError):
            smtplib_utils.send_message(client, message, mail_options=(5,))  # type: ignore[arg-type]

    def test_mail_options_are_forwarded(self):
        replies = [GREETING] + EHLO_REPLY + [
            "250 OK\r\n",
            "250 OK\r\n",
            "354 Go ahead\r\n",
            "250 OK\r\n",
        ]
        fake, patcher = self._client(replies)
        with patcher:
            client = smtplib_utils.create_smtp(
                "mail.example.com", 25, local_hostname="client.example.org"
            )
            smtplib_utils.send_text(
                client,
                "alice@example.com",
                ["bob@example.com"],
                "Report",
                "The body",
                mail_options=["BODY=8BITMIME"],
            )
        self.assertIn("BODY=8BITMIME", fake.commands()[1])


class TestErrorPredicates(unittest.TestCase):
    def test_predicates_match_their_error(self):
        self.assertTrue(smtplib_utils.is_smtp_error(smtplib.SMTPException("x")))
        self.assertTrue(
            smtplib_utils.is_smtp_response_error(smtplib.SMTPResponseException(500, "x"))
        )
        self.assertTrue(
            smtplib_utils.is_smtp_sender_refused(smtplib.SMTPSenderRefused(550, b"x", "a"))
        )
        self.assertTrue(
            smtplib_utils.is_smtp_recipients_refused(
                smtplib.SMTPRecipientsRefused({"a": (550, b"x")})
            )
        )
        self.assertTrue(
            smtplib_utils.is_smtp_data_error(smtplib.SMTPDataError(451, b"x"))
        )
        self.assertTrue(
            smtplib_utils.is_smtp_helo_error(smtplib.SMTPHeloError(550, b"x"))
        )
        self.assertTrue(
            smtplib_utils.is_smtp_not_supported(smtplib.SMTPNotSupportedError("x"))
        )
        self.assertTrue(
            smtplib_utils.is_smtp_server_disconnected(smtplib.SMTPServerDisconnected("x"))
        )
        self.assertTrue(
            smtplib_utils.is_smtp_authentication_error(
                smtplib.SMTPAuthenticationError(535, b"x")
            )
        )

    def test_predicates_reject_other_errors(self):
        self.assertFalse(smtplib_utils.is_smtp_error(ValueError("x")))
        self.assertFalse(smtplib_utils.is_smtp_response_error(ValueError("x")))
        self.assertFalse(smtplib_utils.is_smtp_sender_refused(ValueError("x")))
        self.assertFalse(smtplib_utils.is_smtp_recipients_refused(ValueError("x")))
        self.assertFalse(smtplib_utils.is_smtp_data_error(ValueError("x")))
        self.assertFalse(smtplib_utils.is_smtp_helo_error(ValueError("x")))
        self.assertFalse(smtplib_utils.is_smtp_not_supported(ValueError("x")))
        self.assertFalse(smtplib_utils.is_smtp_server_disconnected(ValueError("x")))
        self.assertFalse(smtplib_utils.is_smtp_authentication_error(ValueError("x")))

    def test_response_error_is_an_smtp_error(self):
        self.assertTrue(
            smtplib_utils.is_smtp_error(smtplib.SMTPResponseException(500, "x"))
        )


if __name__ == "__main__":
    unittest.main()
