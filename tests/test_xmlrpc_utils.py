import unittest
from unittest.mock import patch

import xmlrpc_utils
from xmlrpc_utils import (
    Binary,
    DateTime,
    Fault,
    Marshaller,
    ServerProxy,
    SimpleXMLRPCDispatcher,
    SimpleXMLRPCRequestHandler,
    Transport,
    build_request,
    create_dispatcher,
    create_marshaller,
    create_multi_path_server,
    create_proxy,
    create_server,
    create_transport,
    dumps_value,
    list_public_methods,
    loads_value,
    marshal_params,
    parse_method_call,
    parse_method_response,
    register_function,
    register_instance,
    register_introspection_functions,
    register_multicall_functions,
    resolve_dotted_attribute,
    unmarshal_params,
)


class Service:
    """A small object used to exercise the instance registration."""

    def ping(self):
        return "pong"

    def _private(self):
        return "hidden"


class TestXmlrpcUtils(unittest.TestCase):
    def test_dumps_value(self):
        document = dumps_value((1, 2), methodname="add")
        self.assertIn("<methodName>add</methodName>", document)
        params, methodname = loads_value(document)
        self.assertEqual(params, (1, 2))
        self.assertEqual(methodname, "add")

    def test_dumps_value_rejects_bad_arguments(self):
        with self.assertRaises(TypeError):
            dumps_value("not-a-list")
        with self.assertRaises(TypeError):
            dumps_value((1,), methodname=5)  # type: ignore[arg-type]
        with self.assertRaises(ValueError):
            dumps_value((), methodname="")
        with self.assertRaises(TypeError):
            dumps_value((1,), methodresponse="yes")  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            dumps_value((1,), encoding=5)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            dumps_value((1,), allow_none="yes")  # type: ignore[arg-type]

    def test_dumps_value_response_requires_one_value(self):
        with self.assertRaises(ValueError):
            dumps_value((1, 2), methodresponse=True)
        document = dumps_value((3,), methodresponse=True)
        self.assertIn("<methodResponse>", document)

    def test_loads_value_rejects_bad_arguments(self):
        with self.assertRaises(TypeError):
            loads_value(42)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            loads_value(document=b"<methodCall/>", use_datetime="yes")  # type: ignore[arg-type]

    def test_build_request(self):
        document = build_request("add", (2, 3))
        self.assertIn("<methodCall>", document)
        methodname, params = parse_method_call(document)
        self.assertEqual(methodname, "add")
        self.assertEqual(params, (2, 3))

    def test_build_request_rejects_bad_arguments(self):
        with self.assertRaises(TypeError):
            build_request(5)  # type: ignore[arg-type]
        with self.assertRaises(ValueError):
            build_request("")
        with self.assertRaises(TypeError):
            build_request("add", "nope")  # type: ignore[arg-type]

    def test_parse_method_call(self):
        methodname, params = parse_method_call(build_request("ping"))
        self.assertEqual(methodname, "ping")
        self.assertEqual(params, ())

    def test_parse_method_call_rejects_a_response(self):
        with self.assertRaises(ValueError):
            parse_method_call(dumps_value((1,), methodresponse=True))

    def test_parse_method_response(self):
        document = dumps_value(("done",), methodresponse=True)
        self.assertEqual(parse_method_response(document), ("done",))

    def test_parse_method_response_rejects_a_call(self):
        with self.assertRaises(ValueError):
            parse_method_response(build_request("ping"))

    def test_parse_method_response_raises_fault(self):
        document = (
            "<?xml version='1.0'?>\n"
            "<methodResponse><fault><value><struct>"
            "<member><name>faultCode</name><value><int>7</int></value></member>"
            "<member><name>faultString</name><value><string>boom</string></value></member>"
            "</struct></value></fault></methodResponse>"
        )
        with self.assertRaises(Fault) as caught:
            parse_method_response(document)
        self.assertEqual(caught.exception.faultCode, 7)
        self.assertEqual(caught.exception.faultString, "boom")

    def test_marshal_and_unmarshal_params(self):
        document = marshal_params((1, "two", True))
        self.assertIn("<params>", document)
        self.assertEqual(unmarshal_params(document), (1, "two", True))

    def test_marshal_params_rejects_bad_arguments(self):
        with self.assertRaises(TypeError):
            marshal_params("nope")  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            unmarshal_params(42)  # type: ignore[arg-type]

    def test_create_marshaller(self):
        marshaller = create_marshaller()
        self.assertIsInstance(marshaller, Marshaller)
        with self.assertRaises(TypeError):
            create_marshaller(encoding=5)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            create_marshaller(allow_none="yes")  # type: ignore[arg-type]

    def test_create_transport(self):
        transport = create_transport()
        self.assertIsInstance(transport, Transport)
        with self.assertRaises(TypeError):
            create_transport(use_datetime="yes")  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            create_transport(headers="x")  # type: ignore[arg-type]

    def test_create_proxy_does_not_connect(self):
        proxy = create_proxy("http://localhost:1/RPC2")
        self.assertIsInstance(proxy, ServerProxy)

    def test_create_proxy_rejects_bad_arguments(self):
        with self.assertRaises(TypeError):
            create_proxy(5)  # type: ignore[arg-type]
        with self.assertRaises(ValueError):
            create_proxy("")
        with self.assertRaises(TypeError):
            create_proxy("http://localhost:1/RPC2", transport=object())  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            create_proxy("http://localhost:1/RPC2", verbose="yes")  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            create_proxy("http://localhost:1/RPC2", headers="x")  # type: ignore[arg-type]

    def test_create_dispatcher(self):
        dispatcher = create_dispatcher()
        self.assertIsInstance(dispatcher, SimpleXMLRPCDispatcher)
        with self.assertRaises(TypeError):
            create_dispatcher(allow_none="yes")  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            create_dispatcher(encoding=5)  # type: ignore[arg-type]

    def test_register_function(self):
        dispatcher = create_dispatcher()
        register_function(dispatcher, lambda value: value * 2, "double")
        self.assertIn("double", dispatcher.system_listMethods())

    def test_register_function_rejects_bad_arguments(self):
        dispatcher = create_dispatcher()
        with self.assertRaises(TypeError):
            register_function(object(), lambda: None)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            register_function(dispatcher, "not-callable")  # type: ignore[arg-type]
        with self.assertRaises(ValueError):
            register_function(dispatcher, lambda: None, "")
        with self.assertRaises(TypeError):
            register_function(dispatcher, lambda: None, 5)  # type: ignore[arg-type]

    def test_register_instance(self):
        dispatcher = create_dispatcher()
        register_instance(dispatcher, Service())
        self.assertEqual(dispatcher.system_listMethods(), ["ping"])

    def test_register_instance_rejects_bad_arguments(self):
        dispatcher = create_dispatcher()
        with self.assertRaises(TypeError):
            register_instance(object(), Service())  # type: ignore[arg-type]
        with self.assertRaises(ValueError):
            register_instance(dispatcher, None)
        with self.assertRaises(TypeError):
            register_instance(dispatcher, Service(), allow_dotted_names="yes")  # type: ignore[arg-type]

    def test_register_introspection_functions(self):
        dispatcher = create_dispatcher()
        register_introspection_functions(dispatcher)
        methods = dispatcher.system_listMethods()
        self.assertIn("system.listMethods", methods)
        self.assertIn("system.methodHelp", methods)
        self.assertIn("system.methodSignature", methods)

    def test_register_multicall_functions(self):
        dispatcher = create_dispatcher()
        register_multicall_functions(dispatcher)
        self.assertIn("system.multicall", dispatcher.system_listMethods())

    def test_registration_helpers_reject_bad_dispatchers(self):
        with self.assertRaises(TypeError):
            register_introspection_functions(object())  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            register_multicall_functions(object())  # type: ignore[arg-type]

    def test_resolve_dotted_attribute(self):
        self.assertEqual(resolve_dotted_attribute(Service(), "ping").__name__, "ping")
        with self.assertRaises(ValueError):
            resolve_dotted_attribute(None, "ping")
        with self.assertRaises(ValueError):
            resolve_dotted_attribute(Service(), "")
        with self.assertRaises(TypeError):
            resolve_dotted_attribute(Service(), 5)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            resolve_dotted_attribute(Service(), "ping", allow_dotted_names="yes")  # type: ignore[arg-type]

    def test_list_public_methods(self):
        self.assertEqual(list_public_methods(Service()), ["ping"])
        with self.assertRaises(ValueError):
            list_public_methods(None)

    @patch("xmlrpc_utils._server.SimpleXMLRPCServer")
    def test_create_server(self, mock_server):
        server = create_server(("127.0.0.1", 0))
        mock_server.assert_called_once()
        self.assertIs(server, mock_server.return_value)
        _, kwargs = mock_server.call_args
        self.assertEqual(kwargs["logRequests"], True)
        self.assertEqual(kwargs["bind_and_activate"], True)

    def test_create_server_rejects_bad_arguments(self):
        with self.assertRaises(TypeError):
            create_server("127.0.0.1:0")  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            create_server((1, 0))  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            create_server(("127.0.0.1", "0"))  # type: ignore[arg-type]
        with self.assertRaises(ValueError):
            create_server(("127.0.0.1", 70000))
        with self.assertRaises(TypeError):
            create_server(("127.0.0.1", 0), request_handler=object)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            create_server(("127.0.0.1", 0), log_requests="yes")  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            create_server(("127.0.0.1", 0), encoding=5)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            create_server(("127.0.0.1", 0), bind_and_activate="yes")  # type: ignore[arg-type]

    @patch("xmlrpc_utils._server.MultiPathXMLRPCServer")
    def test_create_multi_path_server(self, mock_server):
        paths = {"/": create_dispatcher()}
        server = create_multi_path_server(("127.0.0.1", 0), paths)
        mock_server.assert_called_once()
        self.assertIs(server, mock_server.return_value)

    def test_create_multi_path_server_rejects_bad_arguments(self):
        with self.assertRaises(TypeError):
            create_multi_path_server("127.0.0.1:0", {})  # type: ignore[arg-type]
        with self.assertRaises(ValueError):
            create_multi_path_server(("127.0.0.1", 0), None)
        with self.assertRaises(TypeError):
            create_multi_path_server(("127.0.0.1", 0), {}, request_handler=object)  # type: ignore[arg-type]

    def test_reexported_types(self):
        self.assertTrue(issubclass(Fault, Exception))
        self.assertEqual(Binary(b"x").data, b"x")
        self.assertEqual(DateTime("20240101T00:00:00").value, "20240101T00:00:00")
        self.assertTrue(issubclass(SimpleXMLRPCRequestHandler, object))
        self.assertIsNotNone(xmlrpc_utils.__all__)

    def test_all_is_sorted_and_unique(self):
        self.assertEqual(len(xmlrpc_utils.__all__), len(set(xmlrpc_utils.__all__)))
        for name in xmlrpc_utils.__all__:
            self.assertTrue(hasattr(xmlrpc_utils, name), name)


if __name__ == "__main__":
    unittest.main()
