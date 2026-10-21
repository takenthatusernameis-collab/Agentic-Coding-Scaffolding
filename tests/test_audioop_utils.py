"""Tests for audioop_utils."""

import unittest

try:
    import audioop as _audioop
except ImportError:  # pragma: no cover - Python 3.13 removed the module
    _audioop = None

import audioop_utils


class TestModuleContract(unittest.TestCase):
    """Verify the contract of the module."""

    def test_all_is_sorted_and_unique(self):
        self.assertEqual(audioop_utils.__all__, sorted(set(audioop_utils.__all__)))

    def test_every_name_exists(self):
        for name in audioop_utils.__all__:
            self.assertTrue(hasattr(audioop_utils, name), name)

    def test_sample_widths(self):
        self.assertEqual(audioop_utils.SAMPLE_WIDTHS, (1, 2, 3, 4))


class TestValidation(unittest.TestCase):
    """Verify argument validation."""

    def test_add_fragments_validates_types(self):
        with self.assertRaises(TypeError):
            audioop_utils.add_fragments("x", b"\x01", 1)
        with self.assertRaises(TypeError):
            audioop_utils.add_fragments(b"\x01", "x", 1)
        with self.assertRaises(TypeError):
            audioop_utils.add_fragments(b"\x01", b"\x01", "1")

    def test_add_fragments_validates_width(self):
        with self.assertRaises(ValueError):
            audioop_utils.add_fragments(b"\x01", b"\x01", 5)
        with self.assertRaises(ValueError):
            audioop_utils.add_fragments(b"\x01", b"\x01", 0)

    def test_add_fragments_validates_frame_alignment(self):
        with self.assertRaises(ValueError):
            audioop_utils.add_fragments(b"\x01\x02", b"\x01", 2)

    def test_bias_validates_arguments(self):
        with self.assertRaises(TypeError):
            audioop_utils.shift_bias("x", 1, 0)
        with self.assertRaises(ValueError):
            audioop_utils.shift_bias(b"\x01", 5, 0)

    def test_average_rejects_empty_fragment(self):
        if _audioop is None:
            self.skipTest("audioop not available")
        with self.assertRaises(ValueError):
            audioop_utils.average(b"", 1)

    def test_describe_fragment_rejects_empty_fragment(self):
        if _audioop is None:
            self.skipTest("audioop not available")
        with self.assertRaises(ValueError):
            audioop_utils.describe_fragment(b"", 1)


class TestAudioOperations(unittest.TestCase):
    """Verify audio operations when available."""

    def setUp(self):
        if _audioop is None:
            self.skipTest("audioop not available")
        self.fragment1 = b"\x00\x01\x02\x03"
        self.fragment2 = b"\x01\x01\x01\x01"

    def test_add_fragments(self):
        result = audioop_utils.add_fragments(self.fragment1, self.fragment2, 1)
        self.assertIsInstance(result, bytes)

    def test_average(self):
        result = audioop_utils.average(self.fragment1, 1)
        self.assertIsInstance(result, (int, float))

    def test_peak_value(self):
        result = audioop_utils.peak_value(self.fragment1, 1)
        self.assertIsInstance(result, int)

    def test_root_mean_square(self):
        result = audioop_utils.root_mean_square(self.fragment1, 1)
        self.assertIsInstance(result, (int, float))

    def test_peak_to_peak(self):
        result = audioop_utils.peak_to_peak(self.fragment1, 1)
        self.assertIsInstance(result, int)

    def test_average_peak_to_peak(self):
        result = audioop_utils.average_peak_to_peak(self.fragment1, 1)
        self.assertIsInstance(result, (int, float))

    def test_describe_fragment(self):
        result = audioop_utils.describe_fragment(self.fragment1, 1)
        self.assertIsInstance(result, dict)
        self.assertIn("width", result)
        self.assertIn("frames", result)
        self.assertIn("peak", result)
        self.assertIn("root_mean_square", result)

    def test_scale(self):
        result = audioop_utils.scale(self.fragment1, 1, 1.0)
        self.assertIsInstance(result, bytes)

    def test_reverse_samples(self):
        result = audioop_utils.reverse_samples(self.fragment1, 1)
        self.assertIsInstance(result, bytes)

    def test_swap_byte_order(self):
        result = audioop_utils.swap_byte_order(self.fragment1, 2)
        self.assertIsInstance(result, bytes)

    def test_mix_to_mono(self):
        stereo = b"\x00\x01\x00\x02"
        result = audioop_utils.mix_to_mono(stereo, 1, 2)
        self.assertIsInstance(result, bytes)

    def test_duplicate_to_stereo(self):
        mono = b"\x00\x01\x02"
        result = audioop_utils.duplicate_to_stereo(mono, 1)
        self.assertIsInstance(result, bytes)

    def test_convert_sample_width(self):
        result = audioop_utils.convert_sample_width(self.fragment1, 1, 2)
        self.assertIsInstance(result, bytes)

    def test_convert_to_u_law(self):
        result = audioop_utils.convert_to_u_law(self.fragment1, 1)
        self.assertIsInstance(result, bytes)

    def test_convert_from_u_law(self):
        ulaw = audioop_utils.convert_to_u_law(self.fragment1, 1)
        result = audioop_utils.convert_from_u_law(ulaw, 1)
        self.assertIsInstance(result, bytes)

    def test_convert_to_a_law(self):
        result = audioop_utils.convert_to_a_law(self.fragment1, 1)
        self.assertIsInstance(result, bytes)

    def test_convert_from_a_law(self):
        alaw = audioop_utils.convert_to_a_law(self.fragment1, 1)
        result = audioop_utils.convert_from_a_law(alaw, 1)
        self.assertIsInstance(result, bytes)

    def test_resample(self):
        result, state = audioop_utils.resample(self.fragment1, 1, 1, 8000, 16000, None)
        self.assertIsInstance(result, bytes)

    def test_find_scale_factor(self):
        result = audioop_utils.find_scale_factor(self.fragment1, self.fragment2)
        self.assertIsInstance(result, (int, float))


class TestResampler(unittest.TestCase):
    """Verify Resampler class."""

    def setUp(self):
        if _audioop is None:
            self.skipTest("audioop not available")

    def test_resampler_initialization(self):
        resampler = audioop_utils.Resampler(1, 8000, 16000)
        self.assertEqual(resampler.channels, 1)
        self.assertEqual(resampler.input_rate, 8000)
        self.assertEqual(resampler.output_rate, 16000)
        self.assertIsNone(resampler.state)

    def test_resampler_reset(self):
        resampler = audioop_utils.Resampler(1, 8000, 16000)
        resampler.reset()
        self.assertIsNone(resampler.state)

    def test_resampler_validates_arguments(self):
        with self.assertRaises(TypeError):
            audioop_utils.Resampler("1", 8000, 16000)
        with self.assertRaises(ValueError):
            audioop_utils.Resampler(0, 8000, 16000)
        with self.assertRaises(ValueError):
            audioop_utils.Resampler(1, 0, 16000)

    def test_resampler_resample(self):
        resampler = audioop_utils.Resampler(1, 8000, 16000)
        fragment = b"\x00\x01\x02\x03"
        result = resampler.resample(fragment, 1)
        self.assertIsInstance(result, bytes)


if __name__ == "__main__":
    unittest.main()
