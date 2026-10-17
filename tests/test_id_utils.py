import unittest

from id_utils import generate_id, is_valid_id, new_id


class TestIdUtils(unittest.TestCase):
    def test_generate_id_default_length(self):
        identifier = generate_id()
        self.assertEqual(len(identifier), 8)
        self.assertTrue(is_valid_id(identifier))

    def test_generate_id_custom_length(self):
        identifier = generate_id(16)
        self.assertEqual(len(identifier), 16)
        self.assertTrue(is_valid_id(identifier, length=16))

    def test_generate_id_alphanumeric(self):
        identifier = generate_id(32)
        self.assertTrue(identifier.isalnum())

    def test_generate_ids_are_unique(self):
        self.assertNotEqual(generate_id(), generate_id())

    def test_new_id(self):
        identifier = new_id()
        self.assertEqual(len(identifier), 8)
        self.assertTrue(is_valid_id(identifier))

    def test_is_valid_id_correct(self):
        self.assertTrue(is_valid_id("abc123XY", length=8))
        self.assertTrue(is_valid_id("a", length=1))

    def test_is_valid_id_wrong_length(self):
        self.assertFalse(is_valid_id("abc123XY", length=4))
        self.assertFalse(is_valid_id("abc", length=8))

    def test_is_valid_id_non_alphanumeric(self):
        self.assertFalse(is_valid_id("abc-123", length=7))

    def test_is_valid_id_not_a_string(self):
        self.assertFalse(is_valid_id(12345678))

    def test_generate_id_type_error(self):
        with self.assertRaises(TypeError):
            generate_id("8")  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            generate_id(8.0)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            generate_id(True)  # type: ignore[arg-type]

    def test_generate_id_value_error(self):
        with self.assertRaises(ValueError):
            generate_id(0)
        with self.assertRaises(ValueError):
            generate_id(-1)


if __name__ == '__main__':
    unittest.main()
