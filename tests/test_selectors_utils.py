import selectors
import socket
import unittest

from selectors_utils import (
    EVENT_READ,
    EVENT_WRITE,
    close_selector,
    create_default_selector,
    get_key,
    get_map,
    register,
    select,
    unregister,
)


class TestCreateDefaultSelector(unittest.TestCase):
    def test_create_default_selector(self):
        selector = create_default_selector()
        self.assertIsInstance(selector, selectors.DefaultSelector)
        selector.close()

    def test_events_constants_match_stdlib(self):
        self.assertEqual(EVENT_READ, selectors.EVENT_READ)
        self.assertEqual(EVENT_WRITE, selectors.EVENT_WRITE)


class TestRegister(unittest.TestCase):
    def test_register_socket(self):
        selector = create_default_selector()
        try:
            reader, _ = socket.socketpair()
            key = register(selector, reader, EVENT_READ, data="reader")
            self.assertIsInstance(key, selectors.SelectorKey)
            self.assertEqual(key.fd, reader.fileno())
            self.assertEqual(key.data, "reader")
            self.assertEqual(key.events, EVENT_READ)
        finally:
            selector.close()

    def test_register_read_and_write(self):
        selector = create_default_selector()
        try:
            reader, _ = socket.socketpair()
            key = register(selector, reader, EVENT_READ | EVENT_WRITE)
            self.assertEqual(key.events, EVENT_READ | EVENT_WRITE)
        finally:
            selector.close()

    def test_register_invalid_selector(self):
        with self.assertRaises(TypeError):
            register("not a selector", object(), EVENT_READ)  # type: ignore[arg-type]

    def test_register_invalid_fileobj(self):
        selector = create_default_selector()
        try:
            with self.assertRaises(TypeError):
                register(selector, object(), EVENT_READ)  # type: ignore[arg-type]
        finally:
            selector.close()

    def test_register_invalid_events_type(self):
        selector = create_default_selector()
        try:
            reader, _ = socket.socketpair()
            with self.assertRaises(TypeError):
                register(selector, reader, "read")  # type: ignore[arg-type]
        finally:
            selector.close()

    def test_register_invalid_events_value(self):
        selector = create_default_selector()
        try:
            reader, _ = socket.socketpair()
            with self.assertRaises(ValueError):
                register(selector, reader, 999)  # type: ignore[arg-type]
        finally:
            selector.close()


class TestUnregister(unittest.TestCase):
    def test_unregister_socket(self):
        selector = create_default_selector()
        try:
            reader, _ = socket.socketpair()
            key = register(selector, reader, EVENT_READ)
            removed = unregister(selector, reader)
            self.assertEqual(removed.fd, key.fd)
        finally:
            selector.close()

    def test_unregister_invalid_selector(self):
        with self.assertRaises(TypeError):
            unregister("not a selector", object())  # type: ignore[arg-type]

    def test_unregister_invalid_fileobj(self):
        selector = create_default_selector()
        try:
            with self.assertRaises(TypeError):
                unregister(selector, object())  # type: ignore[arg-type]
        finally:
            selector.close()

    def test_unregister_not_registered(self):
        selector = create_default_selector()
        try:
            reader, _ = socket.socketpair()
            with self.assertRaises(KeyError):
                unregister(selector, reader)
        finally:
            selector.close()


class TestSelect(unittest.TestCase):
    def test_select_returns_list(self):
        selector = create_default_selector()
        try:
            reader, _ = socket.socketpair()
            register(selector, reader, EVENT_READ)
            ready = select(selector, timeout=0)
            self.assertIsInstance(ready, list)
            for key, events in ready:
                self.assertIsInstance(key, selectors.SelectorKey)
                self.assertIsInstance(events, int)
        finally:
            selector.close()

    def test_select_invalid_selector(self):
        with self.assertRaises(TypeError):
            select("not a selector")  # type: ignore[arg-type]

    def test_select_invalid_timeout_type(self):
        selector = create_default_selector()
        try:
            with self.assertRaises(TypeError):
                select(selector, timeout="1")  # type: ignore[arg-type]
        finally:
            selector.close()

    def test_select_negative_timeout(self):
        selector = create_default_selector()
        try:
            with self.assertRaises(ValueError):
                select(selector, timeout=-1)  # type: ignore[arg-type]
        finally:
            selector.close()


class TestGetKey(unittest.TestCase):
    def test_get_key(self):
        selector = create_default_selector()
        try:
            reader, _ = socket.socketpair()
            key = register(selector, reader, EVENT_READ, data="data")
            looked_up = get_key(selector, reader)
            self.assertEqual(looked_up.fd, key.fd)
            self.assertEqual(looked_up.data, "data")
        finally:
            selector.close()

    def test_get_key_invalid_selector(self):
        with self.assertRaises(TypeError):
            get_key("not a selector", object())  # type: ignore[arg-type]

    def test_get_key_invalid_fileobj(self):
        selector = create_default_selector()
        try:
            with self.assertRaises(TypeError):
                get_key(selector, object())  # type: ignore[arg-type]
        finally:
            selector.close()

    def test_get_key_not_registered(self):
        selector = create_default_selector()
        try:
            reader, _ = socket.socketpair()
            with self.assertRaises(KeyError):
                get_key(selector, reader)
        finally:
            selector.close()


class TestGetMap(unittest.TestCase):
    def test_get_map(self):
        selector = create_default_selector()
        try:
            reader, _ = socket.socketpair()
            register(selector, reader, EVENT_READ)
            mapping = get_map(selector)
            self.assertIsInstance(mapping, dict)
            self.assertIn(reader.fileno(), mapping)
            self.assertEqual(mapping[reader.fileno()].fd, reader.fileno())
        finally:
            selector.close()

    def test_get_map_invalid_selector(self):
        with self.assertRaises(TypeError):
            get_map("not a selector")  # type: ignore[arg-type]


class TestCloseSelector(unittest.TestCase):
    def test_close_selector(self):
        selector = create_default_selector()
        close_selector(selector)

    def test_close_selector_invalid(self):
        with self.assertRaises(TypeError):
            close_selector("not a selector")  # type: ignore[arg-type]


if __name__ == "__main__":
    unittest.main()
