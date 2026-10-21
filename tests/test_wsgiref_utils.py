"""Tests for wsgiref_utils."""

import io
import unittest
import wsgiref.headers
import wsgiref.simple_server
import wsgiref.util
import wsgiref.validate
from unittest import mock

import wsgiref_utils
from wsgiref_utils import (
    HOP_BY_HOP_HEADERS,
    FileWrapper,
    Headers,
    WSGIRequestHandler,
    WSGIServer,
    WSGIWarning,
    application_uri,
    build_headers,
    check_environ,
    demo_app,
    encode_headers,
    environ_errors,
    file_wrapper,
    guess_scheme,
    header_values,
    is_hop_by_hop,
    make_server,
    request_uri,
    setup_testing_defaults,
    shift_path_info,
    validator,
)


def make_environ(**overrides):
    """Return the environment of a request that follows the specification."""
    environ = setup_testing_defaults({})
    environ["QUERY_STRING"] = ""
    environ.update(overrides)
    return environ


class TestModuleContract(unittest.TestCase):
    """Verify the contract of the module."""

    def test_all_is_sorted_and_unique(self):
        self.assertEqual(wsgiref_utils.__all__, sorted(set(wsgiref_utils.__all__)))

    def test_every_name_exists(self):
        for name in wsgiref_utils.__all__:
            self.assertTrue(hasattr(wsgiref_utils, name), name)

    def test_the_classes_are_the_classes_of_the_standard_library(self):
        self.assertIs(Headers, wsgiref.headers.Headers)
        self.assertIs(FileWrapper, wsgiref.util.FileWrapper)
        self.assertIs(WSGIServer, wsgiref.simple_server.WSGIServer)
        self.assertIs(WSGIRequestHandler, wsgiref.simple_server.WSGIRequestHandler)

    def test_the_warning_is_the_warning_of_the_standard_library(self):
        self.assertIs(WSGIWarning, wsgiref.validate.WSGIWarning)

    def test_the_hop_by_hop_headers_are_the_ones_of_the_standard_library(self):
        self.assertEqual(
            set(HOP_BY_HOP_HEADERS),
            {
                "connection",
                "keep-alive",
                "proxy-authenticate",
                "proxy-authorization",
                "te",
                "trailers",
                "transfer-encoding",
                "upgrade",
            },
        )


class TestTestingDefaults(unittest.TestCase):
    """Verify the helper that fills the environment of a request."""

    def test_the_defaults_are_added(self):
        environ = setup_testing_defaults({})
        self.assertEqual(environ["REQUEST_METHOD"], "GET")
        self.assertEqual(environ["SERVER_NAME"], "127.0.0.1")
        self.assertEqual(environ["SERVER_PORT"], "80")
        self.assertEqual(environ["PATH_INFO"], "/")
        self.assertEqual(environ["SCRIPT_NAME"], "")
        self.assertEqual(environ["wsgi.version"], (1, 0))
        self.assertEqual(environ["wsgi.url_scheme"], "http")

    def test_the_environment_is_returned(self):
        environ = {}
        self.assertIs(setup_testing_defaults(environ), environ)

    def test_the_existing_settings_are_kept(self):
        environ = setup_testing_defaults({"REQUEST_METHOD": "POST"})
        self.assertEqual(environ["REQUEST_METHOD"], "POST")

    def test_an_environment_that_is_not_a_dict_is_rejected(self):
        with self.assertRaises(TypeError):
            setup_testing_defaults([("REQUEST_METHOD", "GET")])  # type: ignore[arg-type]


class TestRequestUri(unittest.TestCase):
    """Verify the helpers that build the URI of a request."""

    def test_guess_scheme_reports_http(self):
        self.assertEqual(guess_scheme(make_environ()), "http")

    def test_guess_scheme_reports_https(self):
        self.assertEqual(guess_scheme(make_environ(HTTPS="on")), "https")

    def test_guess_scheme_rejects_an_environment_that_is_not_a_dict(self):
        with self.assertRaises(TypeError):
            guess_scheme("environ")  # type: ignore[arg-type]

    def test_the_application_uri_holds_the_host(self):
        environ = make_environ(HTTP_HOST="example.com")
        self.assertEqual(application_uri(environ), "http://example.com/")

    def test_the_application_uri_holds_the_port(self):
        environ = make_environ(SERVER_NAME="example.com", SERVER_PORT="8080")
        del environ["HTTP_HOST"]
        self.assertEqual(application_uri(environ), "http://example.com:8080/")

    def test_the_application_uri_omits_the_default_port(self):
        environ = make_environ(SERVER_NAME="example.com", SERVER_PORT="80")
        del environ["HTTP_HOST"]
        self.assertEqual(application_uri(environ), "http://example.com/")

    def test_the_application_uri_reports_a_missing_key(self):
        environ = make_environ()
        del environ["wsgi.url_scheme"]
        with self.assertRaises(ValueError) as caught:
            application_uri(environ)
        self.assertIn("wsgi.url_scheme", str(caught.exception))

    def test_the_request_uri_holds_the_path(self):
        environ = make_environ(HTTP_HOST="example.com", PATH_INFO="/a/b")
        self.assertEqual(request_uri(environ), "http://example.com/a/b")

    def test_the_request_uri_escapes_the_path(self):
        environ = make_environ(HTTP_HOST="example.com", PATH_INFO="/a b")
        self.assertEqual(request_uri(environ), "http://example.com/a%20b")

    def test_the_request_uri_holds_the_query_string(self):
        environ = make_environ(HTTP_HOST="example.com", QUERY_STRING="x=1")
        self.assertEqual(request_uri(environ), "http://example.com/?x=1")

    def test_the_query_string_can_be_left_out(self):
        environ = make_environ(HTTP_HOST="example.com", QUERY_STRING="x=1")
        self.assertEqual(request_uri(environ, include_query=False), "http://example.com/")

    def test_the_request_uri_rejects_a_flag_that_is_not_a_bool(self):
        with self.assertRaises(TypeError):
            request_uri(make_environ(), include_query="yes")  # type: ignore[arg-type]

    def test_the_request_uri_rejects_an_environment_that_is_not_a_dict(self):
        with self.assertRaises(TypeError):
            request_uri(None)  # type: ignore[arg-type]


class TestShiftPathInfo(unittest.TestCase):
    """Verify the helper that moves a segment of the path of a request."""

    def test_the_first_segment_is_moved(self):
        environ = make_environ(PATH_INFO="/foo/bar")
        self.assertEqual(shift_path_info(environ), "foo")
        self.assertEqual(environ["SCRIPT_NAME"], "/foo")
        self.assertEqual(environ["PATH_INFO"], "/bar")

    def test_the_path_of_a_request_without_a_segment_is_empty(self):
        environ = make_environ(PATH_INFO="")
        self.assertIsNone(shift_path_info(environ))

    def test_the_environment_is_changed_in_place(self):
        environ = make_environ(PATH_INFO="/foo")
        shift_path_info(environ)
        self.assertEqual(environ["SCRIPT_NAME"], "/foo")
        self.assertEqual(environ["PATH_INFO"], "")

    def test_an_environment_that_is_not_a_dict_is_rejected(self):
        with self.assertRaises(TypeError):
            shift_path_info([])  # type: ignore[arg-type]


class TestHopByHopHeaders(unittest.TestCase):
    """Verify the helper that recognizes a hop-by-hop header."""

    def test_a_hop_by_hop_header_is_recognized(self):
        for name in ("Connection", "keep-alive", "TE", "Transfer-Encoding"):
            self.assertTrue(is_hop_by_hop(name), name)

    def test_an_ordinary_header_is_not_a_hop_by_hop_header(self):
        for name in ("Content-Type", "Host", "Accept"):
            self.assertFalse(is_hop_by_hop(name), name)

    def test_a_name_that_is_not_a_string_is_rejected(self):
        with self.assertRaises(TypeError):
            is_hop_by_hop(42)  # type: ignore[arg-type]


class TestHeaders(unittest.TestCase):
    """Verify the helpers of the headers of a response."""

    def test_the_headers_are_built(self):
        headers = build_headers([("Content-Type", "text/plain")])
        self.assertIsInstance(headers, Headers)
        self.assertEqual(headers.get("Content-Type"), "text/plain")

    def test_the_headers_keep_their_order(self):
        headers = build_headers([("X-Test", "one"), ("X-Test", "two")])
        self.assertEqual(header_values(headers, "X-Test"), ["one", "two"])

    def test_the_headers_reject_a_single_string(self):
        with self.assertRaises(TypeError):
            build_headers("Content-Type")  # type: ignore[arg-type]

    def test_the_headers_reject_a_bad_container(self):
        with self.assertRaises(TypeError):
            build_headers(42)  # type: ignore[arg-type]

    def test_the_headers_reject_a_bad_pair(self):
        with self.assertRaises(TypeError):
            build_headers([("Content-Type",)])  # type: ignore[list-item]

    def test_the_headers_reject_a_name_that_is_not_a_string(self):
        with self.assertRaises(TypeError):
            build_headers([(1, "text/plain")])  # type: ignore[list-item]

    def test_the_headers_reject_a_control_character(self):
        with self.assertRaises(ValueError):
            build_headers([("Content-Type", "text/plain\n")])

    def test_the_values_of_a_missing_header_are_empty(self):
        headers = build_headers([("Content-Type", "text/plain")])
        self.assertEqual(header_values(headers, "X-Missing"), [])

    def test_the_values_reject_a_collection_that_is_not_a_headers(self):
        with self.assertRaises(TypeError):
            header_values([("Content-Type", "text/plain")], "Content-Type")  # type: ignore[arg-type]

    def test_the_values_reject_a_name_that_is_not_a_string(self):
        headers = build_headers([("Content-Type", "text/plain")])
        with self.assertRaises(TypeError):
            header_values(headers, 42)  # type: ignore[arg-type]

    def test_the_headers_are_encoded_for_the_wire(self):
        headers = build_headers([("Content-Type", "text/plain")])
        self.assertEqual(encode_headers(headers), b"Content-Type: text/plain\r\n\r\n")

    def test_the_encoding_rejects_a_collection_that_is_not_a_headers(self):
        with self.assertRaises(TypeError):
            encode_headers([])  # type: ignore[arg-type]


class TestFileWrapper(unittest.TestCase):
    """Verify the helper that reads a stream in blocks."""

    def test_the_stream_is_read_in_blocks(self):
        stream = io.BytesIO(b"abcdef")
        self.assertEqual(list(file_wrapper(stream, 2)), [b"ab", b"cd", b"ef"])

    def test_the_whole_stream_is_read_by_default(self):
        stream = io.BytesIO(b"abcdef")
        self.assertEqual(list(file_wrapper(stream)), [b"abcdef"])

    def test_a_stream_without_a_read_method_is_rejected(self):
        with self.assertRaises(TypeError):
            file_wrapper(object())  # type: ignore[arg-type]

    def test_a_block_size_that_is_not_an_integer_is_rejected(self):
        with self.assertRaises(TypeError):
            file_wrapper(io.BytesIO(b""), "2")  # type: ignore[arg-type]

    def test_a_block_size_that_is_not_positive_is_rejected(self):
        with self.assertRaises(ValueError):
            file_wrapper(io.BytesIO(b""), 0)


class TestValidation(unittest.TestCase):
    """Verify the helpers that check an application against the specification."""

    def test_a_valid_environment_is_accepted(self):
        check_environ(make_environ())

    def test_a_broken_environment_is_refused(self):
        environ = make_environ()
        del environ["REQUEST_METHOD"]
        with self.assertRaises(AssertionError):
            check_environ(environ)

    def test_an_environment_that_is_not_a_dict_is_rejected(self):
        with self.assertRaises(TypeError):
            check_environ("environ")  # type: ignore[arg-type]

    def test_a_valid_environment_has_no_errors(self):
        self.assertEqual(environ_errors(make_environ()), [])

    def test_the_errors_of_the_environment_are_reported(self):
        environ = make_environ()
        del environ["REQUEST_METHOD"]
        errors = environ_errors(environ)
        self.assertEqual(len(errors), 1)
        self.assertIn("REQUEST_METHOD", errors[0])

    def test_the_warnings_of_the_environment_are_reported(self):
        environ = make_environ()
        del environ["QUERY_STRING"]
        errors = environ_errors(environ)
        self.assertTrue(any("QUERY_STRING" in message for message in errors), errors)

    def test_a_conforming_application_passes_the_middleware(self):
        def application(environ, start_response):
            start_response("200 OK", [("Content-Type", "text/plain")])
            return [b"hello"]

        checked = validator(application)
        result = checked(make_environ(), lambda status, headers: None)
        self.assertEqual(list(result), [b"hello"])
        result.close()

    def test_an_application_that_breaks_the_specification_is_refused(self):
        def application(environ, start_response):
            start_response("200 OK", [("Content-Type", "text/plain")])
            return "hello"

        checked = validator(application)
        with self.assertRaises(AssertionError):
            checked(make_environ(), lambda status, headers: None)

    def test_the_middleware_rejects_an_application_that_is_not_callable(self):
        with self.assertRaises(TypeError):
            validator(42)  # type: ignore[arg-type]


class TestDemoApp(unittest.TestCase):
    """Verify the helper that runs the demonstration application."""

    def test_the_application_answers_with_the_environment(self):
        recorded = {}

        def start_response(status, headers, exc_info=None):
            recorded["status"] = status
            recorded["headers"] = headers
            return lambda data: None

        body = demo_app(make_environ(HTTP_HOST="example.com"), start_response)
        self.assertEqual(recorded["status"], "200 OK")
        self.assertEqual(len(body), 1)
        self.assertIn(b"Hello world!", body[0])
        self.assertIn(b"example.com", body[0])

    def test_the_application_rejects_an_environment_that_is_not_a_dict(self):
        with self.assertRaises(TypeError):
            demo_app("environ", lambda status, headers: None)  # type: ignore[arg-type]

    def test_the_application_rejects_a_responder_that_is_not_callable(self):
        with self.assertRaises(TypeError):
            demo_app(make_environ(), None)  # type: ignore[arg-type]


class TestMakeServer(unittest.TestCase):
    """Verify the helper that creates a server.

    The tests never bind a socket, so the standard library is patched and the
    server is never opened.
    """

    def test_the_server_is_created_by_the_standard_library(self):
        def application(environ, start_response):
            return []

        with mock.patch.object(wsgiref_utils._simple_server, "make_server") as mocked:
            mocked.return_value = "server"
            server = make_server("127.0.0.1", 0, application)
        self.assertEqual(server, "server")
        mocked.assert_called_once_with("127.0.0.1", 0, application, WSGIServer, WSGIRequestHandler)

    def test_a_host_that_is_not_a_string_is_rejected(self):
        with self.assertRaises(TypeError):
            make_server(None, 0, lambda environ, start_response: [])  # type: ignore[arg-type]

    def test_a_port_that_is_not_an_integer_is_rejected(self):
        with self.assertRaises(TypeError):
            make_server("127.0.0.1", "0", lambda environ, start_response: [])  # type: ignore[arg-type]

    def test_a_port_that_is_out_of_range_is_rejected(self):
        with self.assertRaises(ValueError):
            make_server("127.0.0.1", 70000, lambda environ, start_response: [])

    def test_an_application_that_is_not_callable_is_rejected(self):
        with self.assertRaises(TypeError):
            make_server("127.0.0.1", 0, None)  # type: ignore[arg-type]

    def test_a_server_class_that_is_not_a_class_is_rejected(self):
        with self.assertRaises(TypeError):
            make_server(
                "127.0.0.1",
                0,
                lambda environ, start_response: [],
                server_class="WSGIServer",  # type: ignore[arg-type]
            )

    def test_a_handler_class_that_is_not_a_class_is_rejected(self):
        with self.assertRaises(TypeError):
            make_server(
                "127.0.0.1",
                0,
                lambda environ, start_response: [],
                handler_class=42,  # type: ignore[arg-type]
            )


if __name__ == "__main__":
    unittest.main()
