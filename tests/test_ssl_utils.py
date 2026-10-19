import unittest
import ssl
from datetime import datetime

import ssl_utils


class TestSSLUtils(unittest.TestCase):
    def test_create_default_context(self):
        ctx = ssl_utils.create_default_context()
        self.assertIsInstance(ctx, ssl.SSLContext)

    def test_create_context_defaults(self):
        ctx = ssl_utils.create_context()
        self.assertIsInstance(ctx, ssl.SSLContext)

    def test_create_context_with_protocol(self):
        if ssl_utils.PROTOCOL_TLS_CLIENT is not None:
            ctx = ssl_utils.create_context(protocol=ssl_utils.PROTOCOL_TLS_CLIENT)
            self.assertIsInstance(ctx, ssl.SSLContext)
        if ssl_utils.PROTOCOL_TLS_SERVER is not None:
            ctx = ssl_utils.create_context(protocol=ssl_utils.PROTOCOL_TLS_SERVER)
            self.assertIsInstance(ctx, ssl.SSLContext)

    def test_create_context_invalid_protocol(self):
        with self.assertRaises(ValueError):
            ssl_utils.create_context(protocol=999999)

    def test_create_context_invalid_type(self):
        with self.assertRaises(TypeError):
            ssl_utils.create_context(protocol="tls")

    def test_create_context_invalid_type_bool(self):
        with self.assertRaises(TypeError):
            ssl_utils.create_context(protocol=True)

    def test_create_context_invalid_type_float(self):
        with self.assertRaises(TypeError):
            ssl_utils.create_context(protocol=1.0)

    def test_get_default_verify_paths(self):
        paths = ssl_utils.get_default_verify_paths()
        self.assertTrue(hasattr(paths, "cafile"))
        self.assertTrue(hasattr(paths, "capath"))
        self.assertTrue(hasattr(paths, "openssl_cafile"))
        self.assertTrue(hasattr(paths, "openssl_capath"))

    def test_is_tls_version_supported(self):
        self.assertIsInstance(ssl_utils.is_tls_version_supported(ssl.PROTOCOL_TLS_CLIENT), bool)
        if ssl_utils.PROTOCOL_TLSv1_2 is not None:
            self.assertIsInstance(ssl_utils.is_tls_version_supported(ssl_utils.PROTOCOL_TLSv1_2), bool)

    def test_is_tls_version_supported_invalid_type(self):
        with self.assertRaises(TypeError):
            ssl_utils.is_tls_version_supported("1.2")

    def test_is_tls_version_supported_invalid_type_bool(self):
        with self.assertRaises(TypeError):
            ssl_utils.is_tls_version_supported(True)

    def test_cert_time_to_seconds_valid(self):
        # GeneralizedTime format as in certs
        result = ssl_utils.cert_time_to_seconds("20240101000000Z")
        self.assertIsInstance(result, int)

    def test_cert_time_to_seconds_valid_no_z(self):
        result = ssl_utils.cert_time_to_seconds("20240101000000")
        self.assertIsInstance(result, int)

    def test_cert_time_to_seconds_invalid_type(self):
        with self.assertRaises(TypeError):
            ssl_utils.cert_time_to_seconds(20240101)

    def test_cert_time_to_seconds_invalid_empty(self):
        with self.assertRaises(ValueError):
            ssl_utils.cert_time_to_seconds("")

    def test_cert_time_to_seconds_invalid_format(self):
        with self.assertRaises(ValueError):
            ssl_utils.cert_time_to_seconds("not-a-date")

    def test_get_cert_subject(self):
        cert = {"subject": ((("commonName", "example.com"),),)}
        subject = ssl_utils.get_cert_subject(cert)
        self.assertEqual(subject, ((("commonName", "example.com"),),))

    def test_get_cert_subject_invalid_type(self):
        with self.assertRaises(TypeError):
            ssl_utils.get_cert_subject("cert")

    def test_get_cert_issuer(self):
        cert = {"issuer": ((("commonName", "CA"),),)}
        issuer = ssl_utils.get_cert_issuer(cert)
        self.assertEqual(issuer, ((("commonName", "CA"),),))

    def test_get_cert_issuer_invalid_type(self):
        with self.assertRaises(TypeError):
            ssl_utils.get_cert_issuer(None)

    def test_get_cert_san(self):
        cert = {"subjectAltName": [("DNS", "example.com")]}
        san = ssl_utils.get_cert_san(cert)
        self.assertEqual(san, [("DNS", "example.com")])

    def test_get_cert_san_missing(self):
        cert = {}
        san = ssl_utils.get_cert_san(cert)
        self.assertEqual(san, [])

    def test_get_cert_san_invalid_type(self):
        with self.assertRaises(TypeError):
            ssl_utils.get_cert_san("bad")

    def test_cert_is_valid_at_time(self):
        now = datetime.utcnow().replace(tzinfo=None)
        not_before = (now.replace(year=now.year - 1)).strftime("%Y%m%d%H%M%S") + "Z"
        not_after = (now.replace(year=now.year + 1)).strftime("%Y%m%d%H%M%S") + "Z"
        cert = {"notBefore": not_before, "notAfter": not_after}
        self.assertTrue(ssl_utils.cert_is_valid_at_time(cert))

    def test_cert_is_valid_at_time_with_time_arg(self):
        # Far past
        cert = {"notBefore": "20200101000000Z", "notAfter": "20200102000000Z"}
        self.assertFalse(ssl_utils.cert_is_valid_at_time(cert, time=1690000000))
        # In range
        self.assertTrue(ssl_utils.cert_is_valid_at_time(cert, time=1577865600))  # 2020-01-01 12:00:00Z approx

    def test_cert_is_valid_at_time_invalid_cert_type(self):
        with self.assertRaises(TypeError):
            ssl_utils.cert_is_valid_at_time("cert")

    def test_cert_is_valid_at_time_missing_fields(self):
        with self.assertRaises(KeyError):
            ssl_utils.cert_is_valid_at_time({})

    def test_cert_is_valid_at_time_invalid_time_type(self):
        cert = {"notBefore": "20200101000000Z", "notAfter": "20200102000000Z"}
        with self.assertRaises(TypeError):
            ssl_utils.cert_is_valid_at_time(cert, time="now")

    def test_cert_is_valid_at_time_invalid_time_bool(self):
        cert = {"notBefore": "20200101000000Z", "notAfter": "20200102000000Z"}
        with self.assertRaises(TypeError):
            ssl_utils.cert_is_valid_at_time(cert, time=True)
