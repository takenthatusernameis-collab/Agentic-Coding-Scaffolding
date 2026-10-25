import unittest

from roman_utils import from_roman, is_valid_roman, to_roman


class TestRomanUtils(unittest.TestCase):
    def test_to_roman_basic(self):
        self.assertEqual(to_roman(1), "I")
        self.assertEqual(to_roman(2), "II")
        self.assertEqual(to_roman(3), "III")
        self.assertEqual(to_roman(4), "IV")
        self.assertEqual(to_roman(5), "V")
        self.assertEqual(to_roman(6), "VI")
        self.assertEqual(to_roman(9), "IX")
        self.assertEqual(to_roman(10), "X")
        self.assertEqual(to_roman(14), "XIV")
        self.assertEqual(to_roman(19), "XIX")
        self.assertEqual(to_roman(40), "XL")
        self.assertEqual(to_roman(49), "XLIX")
        self.assertEqual(to_roman(50), "L")
        self.assertEqual(to_roman(90), "XC")
        self.assertEqual(to_roman(100), "C")
        self.assertEqual(to_roman(400), "CD")
        self.assertEqual(to_roman(500), "D")
        self.assertEqual(to_roman(900), "CM")
        self.assertEqual(to_roman(1000), "M")
        self.assertEqual(to_roman(1984), "MCMLXXXIV")
        self.assertEqual(to_roman(3999), "MMMCMXCIX")

    def test_to_roman_roundtrip(self):
        for number in range(1, 4000):
            self.assertEqual(from_roman(to_roman(number)), number)

    def test_to_roman_rejects_non_int(self):
        with self.assertRaises(TypeError):
            to_roman("1")
        with self.assertRaises(TypeError):
            to_roman(1.5)
        with self.assertRaises(TypeError):
            to_roman(True)

    def test_to_roman_rejects_out_of_range(self):
        with self.assertRaises(ValueError):
            to_roman(0)
        with self.assertRaises(ValueError):
            to_roman(-1)
        with self.assertRaises(ValueError):
            to_roman(4000)

    def test_from_roman(self):
        self.assertEqual(from_roman("I"), 1)
        self.assertEqual(from_roman("IV"), 4)
        self.assertEqual(from_roman("IX"), 9)
        self.assertEqual(from_roman("XL"), 40)
        self.assertEqual(from_roman("XC"), 90)
        self.assertEqual(from_roman("CD"), 400)
        self.assertEqual(from_roman("CM"), 900)
        self.assertEqual(from_roman("MCMLXXXIV"), 1984)
        self.assertEqual(from_roman("MMMCMXCIX"), 3999)

    def test_from_roman_rejects_invalid(self):
        with self.assertRaises(ValueError):
            from_roman("")
        with self.assertRaises(ValueError):
            from_roman("IIII")
        with self.assertRaises(ValueError):
            from_roman("VV")
        with self.assertRaises(ValueError):
            from_roman("XXXX")
        with self.assertRaises(ValueError):
            from_roman("notroman")
        with self.assertRaises(TypeError):
            from_roman(1)

    def test_is_valid_roman(self):
        self.assertTrue(is_valid_roman("I"))
        self.assertTrue(is_valid_roman("IV"))
        self.assertTrue(is_valid_roman("MMMCMXCIX"))
        self.assertFalse(is_valid_roman(""))
        self.assertFalse(is_valid_roman("IIII"))
        self.assertFalse(is_valid_roman("notroman"))
        self.assertFalse(is_valid_roman(1))


if __name__ == "__main__":
    unittest.main()
