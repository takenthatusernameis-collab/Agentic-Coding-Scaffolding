"""Tests for color_utils module."""

import unittest

from color_utils import (
    adjust_brightness,
    blend_colors,
    get_contrast_ratio,
    get_luminance,
    hex_to_rgb,
    hsl_to_rgb,
    is_accessible,
    rgb_to_hex,
    rgb_to_hsl,
    validate_hex,
)


class TestValidateHex(unittest.TestCase):
    def test_valid_hash_hex(self) -> None:
        self.assertTrue(validate_hex("#ff5733"))
        self.assertTrue(validate_hex("#000000"))
        self.assertTrue(validate_hex("#FFFFFF"))
        self.assertTrue(validate_hex("#abcdef"))

    def test_valid_plain_hex(self) -> None:
        self.assertTrue(validate_hex("ff5733"))
        self.assertTrue(validate_hex("000000"))

    def test_invalid_hex(self) -> None:
        self.assertFalse(validate_hex("#gg5733"))
        self.assertFalse(validate_hex("#ff57"))
        self.assertFalse(validate_hex("#ff5733aa"))
        self.assertFalse(validate_hex(""))
        self.assertFalse(validate_hex("#"))
        self.assertFalse(validate_hex("not-a-color"))

    def test_non_string_raises(self) -> None:
        with self.assertRaises(TypeError):
            validate_hex(123)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            validate_hex(None)  # type: ignore[arg-type]


class TestHexToRgb(unittest.TestCase):
    def test_basic_conversion(self) -> None:
        self.assertEqual(hex_to_rgb("#ff5733"), (255, 87, 51))
        self.assertEqual(hex_to_rgb("ff5733"), (255, 87, 51))
        self.assertEqual(hex_to_rgb("#000000"), (0, 0, 0))
        self.assertEqual(hex_to_rgb("#FFFFFF"), (255, 255, 255))
        self.assertEqual(hex_to_rgb("#00ff00"), (0, 255, 0))
        self.assertEqual(hex_to_rgb("#0000ff"), (0, 0, 255))

    def test_invalid_raises(self) -> None:
        with self.assertRaises(ValueError):
            hex_to_rgb("#gg5733")
        with self.assertRaises(ValueError):
            hex_to_rgb("#ff57")
        with self.assertRaises(TypeError):
            hex_to_rgb(123)  # type: ignore[arg-type]


class TestRgbToHex(unittest.TestCase):
    def test_basic_conversion(self) -> None:
        self.assertEqual(rgb_to_hex(255, 87, 51), "#ff5733")
        self.assertEqual(rgb_to_hex(0, 0, 0), "#000000")
        self.assertEqual(rgb_to_hex(255, 255, 255), "#ffffff")
        self.assertEqual(rgb_to_hex(0, 255, 0), "#00ff00")

    def test_invalid_channels(self) -> None:
        with self.assertRaises(ValueError):
            rgb_to_hex(256, 0, 0)
        with self.assertRaises(ValueError):
            rgb_to_hex(0, -1, 0)
        with self.assertRaises(TypeError):
            rgb_to_hex(1.5, 0, 0)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            rgb_to_hex(0, 0, None)  # type: ignore[arg-type]


class TestRgbToHsl(unittest.TestCase):
    def test_red(self) -> None:
        h, s, lightness = rgb_to_hsl(255, 0, 0)
        self.assertAlmostEqual(h, 0.0)
        self.assertAlmostEqual(s, 1.0)
        self.assertAlmostEqual(lightness, 0.5)

    def test_gray(self) -> None:
        h, s, lightness = rgb_to_hsl(128, 128, 128)
        self.assertAlmostEqual(h, 0.0)
        self.assertAlmostEqual(s, 0.0)
        self.assertAlmostEqual(lightness, 128 / 255.0, places=6)

    def test_white(self) -> None:
        h, s, lightness = rgb_to_hsl(255, 255, 255)
        self.assertAlmostEqual(h, 0.0)
        self.assertAlmostEqual(s, 0.0)
        self.assertAlmostEqual(lightness, 1.0)

    def test_invalid_channels(self) -> None:
        with self.assertRaises(ValueError):
            rgb_to_hsl(256, 0, 0)
        with self.assertRaises(TypeError):
            rgb_to_hsl("a", 0, 0)  # type: ignore[arg-type]


class TestHslToRgb(unittest.TestCase):
    def test_red(self) -> None:
        self.assertEqual(hsl_to_rgb(0, 1.0, 0.5), (255, 0, 0))

    def test_black_white(self) -> None:
        self.assertEqual(hsl_to_rgb(0, 0.0, 0.0), (0, 0, 0))
        self.assertEqual(hsl_to_rgb(0, 0.0, 1.0), (255, 255, 255))

    def test_green_blue(self) -> None:
        self.assertEqual(hsl_to_rgb(120, 1.0, 0.5), (0, 255, 0))
        self.assertEqual(hsl_to_rgb(240, 1.0, 0.5), (0, 0, 255))

    def test_invalid_s_l(self) -> None:
        with self.assertRaises(ValueError):
            hsl_to_rgb(0, 1.5, 0.5)
        with self.assertRaises(ValueError):
            hsl_to_rgb(0, 0.5, -0.1)
        with self.assertRaises(TypeError):
            hsl_to_rgb("x", 0.5, 0.5)  # type: ignore[arg-type]


class TestGetLuminance(unittest.TestCase):
    def test_bounds(self) -> None:
        self.assertEqual(get_luminance("#000000"), 0.0)
        self.assertEqual(get_luminance("#ffffff"), 1.0)
        self.assertEqual(get_luminance((0, 0, 0)), 0.0)
        self.assertEqual(get_luminance((255, 255, 255)), 1.0)

    def test_gray_midpoint(self) -> None:
        # Mid gray 128 has a known relative luminance.
        self.assertAlmostEqual(get_luminance("#808080"), 0.2159, places=4)

    def test_invalid_color(self) -> None:
        with self.assertRaises(ValueError):
            get_luminance("#gg5733")
        with self.assertRaises(TypeError):
            get_luminance(123)  # type: ignore[arg-type]


class TestGetContrastRatio(unittest.TestCase):
    def test_black_white(self) -> None:
        self.assertAlmostEqual(get_contrast_ratio("#000000", "#ffffff"), 21.0)
        self.assertAlmostEqual(get_contrast_ratio("#ffffff", "#000000"), 21.0)

    def test_identical(self) -> None:
        self.assertAlmostEqual(get_contrast_ratio("#ff5733", "#ff5733"), 1.0)

    def test_range(self) -> None:
        ratio = get_contrast_ratio("#000000", "#ffffff")
        self.assertGreaterEqual(ratio, 1.0)
        self.assertLessEqual(ratio, 21.0)

    def test_tuples_accepted(self) -> None:
        self.assertAlmostEqual(get_contrast_ratio((0, 0, 0), (255, 255, 255)), 21.0)

    def test_invalid_color(self) -> None:
        with self.assertRaises(ValueError):
            get_contrast_ratio("#gg5733", "#000000")
        with self.assertRaises(TypeError):
            get_contrast_ratio(123, "#000000")  # type: ignore[arg-type]


class TestIsAccessible(unittest.TestCase):
    def test_aa_normal_black_white(self) -> None:
        self.assertTrue(is_accessible("#000000", "#ffffff"))
        self.assertTrue(is_accessible("#000000", "#ffffff", level="AA", size="normal"))

    def test_aa_normal_identical_fails(self) -> None:
        self.assertFalse(is_accessible("#ffffff", "#ffffff"))
        self.assertFalse(is_accessible("#ffffff", "#ffffff", level="AA", size="large"))

    def test_aaa_threshold(self) -> None:
        self.assertTrue(is_accessible("#000000", "#ffffff", level="AAA", size="normal"))
        self.assertFalse(is_accessible("#777777", "#ffffff", level="AAA", size="normal"))

    def test_large_text_threshold(self) -> None:
        self.assertTrue(is_accessible("#777777", "#ffffff", level="AA", size="large"))

    def test_invalid_level_size(self) -> None:
        with self.assertRaises(ValueError):
            is_accessible("#000000", "#ffffff", level="ZZZ")
        with self.assertRaises(ValueError):
            is_accessible("#000000", "#ffffff", size="tiny")
        with self.assertRaises(TypeError):
            is_accessible("#000000", "#ffffff", level=1)  # type: ignore[arg-type]


class TestAdjustBrightness(unittest.TestCase):
    def test_half_brightness(self) -> None:
        # Python's round() rounds half to even: 127.5 -> 128, 43.5 -> 44, 25.5 -> 26.
        self.assertEqual(adjust_brightness("#ff5733", 0.5), "#802c1a")

    def test_unchanged_and_black(self) -> None:
        self.assertEqual(adjust_brightness("#ff5733", 1.0), "#ff5733")
        self.assertEqual(adjust_brightness("#000000", 2.0), "#000000")

    def test_clamp(self) -> None:
        self.assertEqual(adjust_brightness("#ffffff", 2.0), "#ffffff")

    def test_invalid(self) -> None:
        with self.assertRaises(ValueError):
            adjust_brightness("#gg5733", 0.5)
        with self.assertRaises(ValueError):
            adjust_brightness("#ff5733", -0.1)
        with self.assertRaises(TypeError):
            adjust_brightness("#ff5733", "high")  # type: ignore[arg-type]


class TestBlendColors(unittest.TestCase):
    def test_midpoint(self) -> None:
        self.assertEqual(blend_colors("#000000", "#ffffff", 0.5), "#808080")

    def test_edges(self) -> None:
        self.assertEqual(blend_colors("#ff0000", "#0000ff", 0.0), "#ff0000")
        self.assertEqual(blend_colors("#ff0000", "#0000ff", 1.0), "#0000ff")

    def test_tuples(self) -> None:
        self.assertEqual(blend_colors((255, 0, 0), (0, 0, 255), 0.5), "#800080")

    def test_invalid_weight(self) -> None:
        with self.assertRaises(ValueError):
            blend_colors("#000000", "#ffffff", 1.5)
        with self.assertRaises(ValueError):
            blend_colors("#000000", "#ffffff", -0.1)
        with self.assertRaises(TypeError):
            blend_colors("#000000", "#ffffff", "half")  # type: ignore[arg-type]

    def test_invalid_color(self) -> None:
        with self.assertRaises(ValueError):
            blend_colors("#gg5733", "#000000")


if __name__ == "__main__":
    unittest.main()
