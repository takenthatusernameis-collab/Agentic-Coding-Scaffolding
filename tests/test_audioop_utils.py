"""Tests for audioop_utils.

The tests work on byte strings that the test itself builds, so the suite needs
no audio device, no file, and no network.  The tests of the standard library
module are skipped on an interpreter that removed the module, and the tests of
the degradation are skipped on an interpreter that still ships it.
"""

import unittest
import warnings
from typing import Any

with warnings.catch_warnings():
    warnings.simplefilter("ignore", DeprecationWarning)
    try:
        import audioop as _audioop
    except ImportError:  # pragma: no cover - Python 3.13 removed the module
        _audioop = None  # type: ignore[assignment]

import audioop_utils

#: The convention of the ADPCM helpers of the running interpreter.
_STATEFUL = False
if _audioop is not None:
    try:
        _audioop.lin2adpcm(b"", 2, None)
    except TypeError:
        _STATEFUL = False
    else:
        _STATEFUL = True


def _standard_encode(fragment: bytes, width: int, bits: int = 4) -> Any:
    """Return the ADPCM coded form of a fragment, the way the standard library does."""
    module: Any = _audioop
    if _STATEFUL:
        coded, state = module.lin2adpcm(fragment, width, None)
        return coded, state
    return module.lin2adpcm(fragment, width, bits), None


def _standard_decode(fragment: bytes, width: int, bits: int = 4) -> Any:
    """Return the linear form of a coded fragment, the way the standard library does."""
    module: Any = _audioop
    if _STATEFUL:
        decoded, state = module.adpcm2lin(fragment, width, None)
        return decoded, state
    return module.adpcm2lin(fragment, width, bits), None


class TestModuleContract(unittest.TestCase):
    """Verify the contract of the module."""

    def test_all_is_sorted_and_unique(self):
        self.assertEqual(audioop_utils.__all__, sorted(set(audioop_utils.__all__)))

    def test_every_name_exists(self):
        for name in audioop_utils.__all__:
            self.assertTrue(hasattr(audioop_utils, name), name)

    def test_the_sample_widths_are_the_widths_of_the_standard_library(self):
        self.assertEqual(audioop_utils.SAMPLE_WIDTHS, (1, 2, 3, 4))

    def test_is_available_reports_a_bool(self):
        self.assertIsInstance(audioop_utils.is_available(), bool)

    def test_is_available_matches_the_standard_library(self):
        self.assertEqual(audioop_utils.is_available(), _audioop is not None)

    @unittest.skipUnless(_audioop is not None, "audioop module not available")
    def test_the_error_of_the_standard_library_is_reexported(self):
        self.assertIs(audioop_utils.AudioOpError, _audioop.error)


class TestValidation(unittest.TestCase):
    """Verify the validation of the arguments.

    The arguments are validated before the standard library is reached, so the
    same error is raised on an interpreter that removed the module.
    """

    def test_a_fragment_must_be_bytes_like(self):
        with self.assertRaises(TypeError):
            audioop_utils.add_fragments("x", b"\x01", 1)
        with self.assertRaises(TypeError):
            audioop_utils.add_fragments(b"\x01", "x", 1)
        with self.assertRaises(TypeError):
            audioop_utils.shift_bias("x", 1, 0)
        with self.assertRaises(TypeError):
            audioop_utils.scale(b"\x01", 1, "2")
        with self.assertRaises(TypeError):
            audioop_utils.sample_at(b"\x01", 1, "0")

    def test_a_width_must_be_an_integer(self):
        with self.assertRaises(TypeError):
            audioop_utils.add_fragments(b"\x01", b"\x01", "1")
        with self.assertRaises(TypeError):
            audioop_utils.frame_count(b"\x01", "1")

    def test_a_boolean_is_not_an_integer(self):
        with self.assertRaises(TypeError):
            audioop_utils.shift_bias(b"\x01", 1, True)
        with self.assertRaises(TypeError):
            audioop_utils.sample_at(b"\x01", 1, True)
        with self.assertRaises(TypeError):
            audioop_utils.scale(b"\x01", 1, True)

    def test_a_width_must_be_a_width_of_the_standard_library(self):
        for width in (0, 5, -1):
            with self.assertRaises(ValueError):
                audioop_utils.frame_count(b"\x01", width)
        with self.assertRaises(ValueError):
            audioop_utils.convert_sample_width(b"\x01", 1, 5)

    def test_a_fragment_must_hold_whole_frames(self):
        with self.assertRaises(ValueError):
            audioop_utils.add_fragments(b"\x01\x02", b"\x01", 2)
        with self.assertRaises(ValueError):
            audioop_utils.frame_count(b"\x01\x02\x03", 2)

    def test_the_measurements_reject_an_empty_fragment(self):
        with self.assertRaises(ValueError):
            audioop_utils.average(b"", 1)
        with self.assertRaises(ValueError):
            audioop_utils.root_mean_square(b"", 1)
        with self.assertRaises(ValueError):
            audioop_utils.describe_fragment(b"", 1)

    def test_two_fragments_must_hold_the_same_number_of_bytes(self):
        with self.assertRaises(ValueError):
            audioop_utils.add_fragments(b"\x01", b"\x01\x02", 1)
        with self.assertRaises(ValueError):
            audioop_utils.find_scale_factor(b"\x01", b"\x01\x02")

    def test_a_rate_must_be_greater_than_zero(self):
        with self.assertRaises(ValueError):
            audioop_utils.resample(b"\x01", 1, 1, 0, 16000, None)
        with self.assertRaises(ValueError):
            audioop_utils.resample(b"\x01", 1, 1, 8000, 0, None)

    def test_the_number_of_channels_must_be_greater_than_zero(self):
        with self.assertRaises(ValueError):
            audioop_utils.resample(b"\x01", 1, 0, 8000, 16000, None)

    def test_a_stereo_fragment_must_hold_an_even_number_of_frames(self):
        with self.assertRaises(ValueError):
            audioop_utils.mix_to_mono(b"\x01\x02\x03", 1)

    def test_the_resampler_validates_its_arguments(self):
        with self.assertRaises(TypeError):
            audioop_utils.Resampler("1", 8000, 16000)
        with self.assertRaises(ValueError):
            audioop_utils.Resampler(0, 8000, 16000)
        with self.assertRaises(ValueError):
            audioop_utils.Resampler(1, 0, 16000)
        with self.assertRaises(ValueError):
            audioop_utils.Resampler(1, 8000, 0)

    def test_a_sample_index_must_be_inside_the_fragment(self):
        with self.assertRaises(IndexError):
            audioop_utils.sample_at(b"\x01\x02", 1, 2)
        with self.assertRaises(IndexError):
            audioop_utils.sample_at(b"\x01\x02", 1, -3)


class TestFrameCount(unittest.TestCase):
    """Verify the helper that counts the frames of a fragment."""

    def test_the_frames_are_counted(self):
        self.assertEqual(audioop_utils.frame_count(b"\x01\x02\x03\x04", 2), 2)
        self.assertEqual(audioop_utils.frame_count(b"\x01\x02\x03\x04", 1), 4)

    def test_an_empty_fragment_holds_no_frame(self):
        self.assertEqual(audioop_utils.frame_count(b"", 2), 0)


class TestMeasurements(unittest.TestCase):
    """Verify the helpers that measure a fragment."""

    def setUp(self):
        if _audioop is None:
            self.skipTest("audioop module not available")
        self.fragment = b"\x00\x01\x02\x03"

    def test_the_average_is_the_exact_mean_of_the_samples(self):
        self.assertEqual(audioop_utils.average(self.fragment, 1), 1.5)
        self.assertEqual(audioop_utils.average(b"\x02\x04", 1), 3.0)

    def test_the_root_mean_square_is_the_exact_value(self):
        self.assertAlmostEqual(
            audioop_utils.root_mean_square(self.fragment, 1), (3.5) ** 0.5
        )

    def test_the_peak_is_the_largest_absolute_sample(self):
        self.assertEqual(audioop_utils.peak_value(self.fragment, 1), 3)
        self.assertEqual(audioop_utils.peak_value(b"\xff\x01", 1), 1)

    def test_the_peak_range_holds_the_smallest_and_the_largest_sample(self):
        self.assertEqual(audioop_utils.peak_range(self.fragment, 1), (0, 3))
        self.assertEqual(audioop_utils.peak_range(b"\xff\x01", 1), (-1, 1))

    def test_the_peak_to_peak_value_is_the_distance_of_two_samples(self):
        self.assertEqual(
            audioop_utils.peak_to_peak(self.fragment, 1),
            _audioop.maxpp(self.fragment, 1),
        )

    def test_the_average_peak_to_peak_value_matches_the_standard_library(self):
        self.assertEqual(
            audioop_utils.average_peak_to_peak(self.fragment, 1),
            float(_audioop.avgpp(self.fragment, 1)),
        )

    def test_the_zero_crossings_are_counted(self):
        self.assertEqual(audioop_utils.count_zero_crossings(b"\xff\x00\xff\x00", 1), 3)
        self.assertEqual(audioop_utils.count_zero_crossings(self.fragment, 1), 0)

    def test_the_description_holds_the_measurements(self):
        description = audioop_utils.describe_fragment(self.fragment, 1)
        self.assertEqual(description["width"], 1)
        self.assertEqual(description["frames"], 4)
        self.assertEqual(description["minimum"], 0)
        self.assertEqual(description["maximum"], 3)
        self.assertEqual(description["peak"], 3)
        self.assertEqual(description["peak_to_peak"], _audioop.maxpp(self.fragment, 1))
        self.assertEqual(description["average"], 1.5)
        self.assertAlmostEqual(description["root_mean_square"], (3.5) ** 0.5)
        self.assertEqual(description["zero_crossings"], 0)
        self.assertEqual(
            description["average_peak_to_peak"], float(_audioop.avgpp(self.fragment, 1))
        )


class TestConversions(unittest.TestCase):
    """Verify the helpers that convert a fragment."""

    def setUp(self):
        if _audioop is None:
            self.skipTest("audioop module not available")
        self.fragment = b"\x00\x01\x02\x03"

    def test_the_width_of_a_sample_is_converted(self):
        self.assertEqual(
            audioop_utils.convert_sample_width(b"\x01\x02", 1, 2), b"\x00\x01\x00\x02"
        )

    def test_the_u_law_form_holds_one_byte_per_sample(self):
        self.assertEqual(len(audioop_utils.convert_to_u_law(self.fragment, 1)), 4)

    def test_the_a_law_form_holds_one_byte_per_sample(self):
        self.assertEqual(len(audioop_utils.convert_to_a_law(self.fragment, 1)), 4)

    def test_the_u_law_form_is_read_back_within_the_step_of_the_coding(self):
        coded = audioop_utils.convert_to_u_law(self.fragment, 1)
        decoded = audioop_utils.convert_from_u_law(coded, 1)
        self.assertEqual(len(decoded), len(self.fragment))
        for original, restored in zip(self.fragment, decoded):
            self.assertLessEqual(abs(original - restored), 2)

    def test_the_a_law_form_is_read_back_within_the_step_of_the_coding(self):
        coded = audioop_utils.convert_to_a_law(self.fragment, 1)
        decoded = audioop_utils.convert_from_a_law(coded, 1)
        self.assertEqual(len(decoded), len(self.fragment))
        for original, restored in zip(self.fragment, decoded):
            self.assertLessEqual(abs(original - restored), 2)

    def test_the_small_samples_survive_the_u_law_coding(self):
        self.assertEqual(
            audioop_utils.convert_from_u_law(
                audioop_utils.convert_to_u_law(self.fragment, 1), 1
            ),
            self.fragment,
        )

    def test_the_small_samples_survive_the_a_law_coding(self):
        self.assertEqual(
            audioop_utils.convert_from_a_law(
                audioop_utils.convert_to_a_law(self.fragment, 1), 1
            ),
            self.fragment,
        )


class TestArithmetic(unittest.TestCase):
    """Verify the helpers that compute on a fragment."""

    def setUp(self):
        if _audioop is None:
            self.skipTest("audioop module not available")
        self.fragment = b"\x00\x01\x02\x03"

    def test_two_fragments_are_added(self):
        self.assertEqual(
            audioop_utils.add_fragments(self.fragment, b"\x01\x01\x01\x01", 1),
            b"\x01\x02\x03\x04",
        )

    def test_a_bias_is_added_to_every_sample(self):
        self.assertEqual(
            audioop_utils.shift_bias(self.fragment, 1, 10), b"\x0a\x0b\x0c\x0d"
        )

    def test_every_sample_is_multiplied_by_a_factor(self):
        self.assertEqual(audioop_utils.scale(self.fragment, 1, 2.0), b"\x00\x02\x04\x06")

    def test_the_byte_order_of_every_sample_is_reversed(self):
        self.assertEqual(audioop_utils.swap_byte_order(b"\x01\x02", 2), b"\x02\x01")

    def test_the_samples_are_reversed(self):
        self.assertEqual(audioop_utils.reverse_samples(b"\x01\x02\x03", 1), b"\x03\x02\x01")

    def test_a_bytearray_is_accepted(self):
        self.assertEqual(
            audioop_utils.reverse_samples(bytearray(b"\x01\x02\x03"), 1), b"\x03\x02\x01"
        )

    def test_a_memory_view_is_accepted(self):
        self.assertEqual(
            audioop_utils.reverse_samples(memoryview(b"\x01\x02\x03"), 1), b"\x03\x02\x01"
        )


class TestChannels(unittest.TestCase):
    """Verify the helpers that change the number of channels."""

    def setUp(self):
        if _audioop is None:
            self.skipTest("audioop module not available")

    def test_a_stereo_fragment_is_mixed_down(self):
        self.assertEqual(
            audioop_utils.mix_to_mono(b"\x01\x02\x03\x04", 1),
            _audioop.tomono(b"\x01\x02\x03\x04", 1, 1.0, 1.0),
        )

    def test_a_mono_fragment_is_duplicated(self):
        self.assertEqual(
            audioop_utils.duplicate_to_stereo(b"\x01\x02", 1),
            _audioop.tostereo(b"\x01\x02", 1, 1.0, 1.0),
        )

    def test_the_factors_of_the_channels_are_used(self):
        self.assertEqual(
            audioop_utils.mix_to_mono(b"\x01\x02\x03\x04", 1, 1.0, 0.0),
            _audioop.tomono(b"\x01\x02\x03\x04", 1, 1.0, 0.0),
        )

    def test_the_duplicated_fragment_holds_both_channels(self):
        self.assertEqual(len(audioop_utils.duplicate_to_stereo(b"\x01\x02", 1)), 4)


class TestSamples(unittest.TestCase):
    """Verify the helpers that read a single sample of a fragment."""

    def setUp(self):
        if _audioop is None:
            self.skipTest("audioop module not available")
        self.fragment = b"\x01\x02\x03\x04"

    def test_a_sample_is_read_by_its_position(self):
        self.assertEqual(audioop_utils.sample_at(self.fragment, 1, 0), 1)
        self.assertEqual(audioop_utils.sample_at(self.fragment, 1, 2), 3)

    def test_a_negative_position_counts_from_the_end(self):
        self.assertEqual(audioop_utils.sample_at(self.fragment, 1, -1), 4)
        self.assertEqual(audioop_utils.sample_at(self.fragment, 1, -4), 1)

    def test_the_scale_factor_of_a_fragment_is_one_for_equal_fragments(self):
        self.assertAlmostEqual(
            audioop_utils.find_scale_factor(self.fragment, self.fragment), 1.0
        )

    def test_the_scale_factor_needs_whole_sixteen_bit_samples(self):
        with self.assertRaises(ValueError):
            audioop_utils.find_scale_factor(b"\x01\x02\x03", b"\x01\x02\x03")
        with self.assertRaises(ValueError):
            audioop_utils.find_scale_factor(b"\x01\x02", b"\x01\x02\x03\x04")


class TestResampling(unittest.TestCase):
    """Verify the helpers that resample a fragment."""

    def setUp(self):
        if _audioop is None:
            self.skipTest("audioop module not available")
        self.fragment = b"\x00\x01\x02\x03"

    def test_the_resampled_fragment_and_the_state_are_returned(self):
        data, state = audioop_utils.resample(self.fragment, 1, 1, 8000, 16000, None)
        self.assertIsInstance(data, bytes)
        self.assertIsNotNone(state)

    def test_the_state_is_handed_back_to_the_standard_library(self):
        data, state = audioop_utils.resample(self.fragment, 1, 1, 8000, 16000, None)
        self.assertEqual(
            data, _audioop.ratecv(self.fragment, 1, 1, 8000, 16000, None)[0]
        )
        self.assertIsNotNone(state)

    def test_a_fragment_must_hold_whole_frames_of_every_channel(self):
        with self.assertRaises(ValueError):
            audioop_utils.resample(b"\x01\x02\x03", 1, 2, 8000, 16000, None)

    def test_the_resampler_keeps_the_state_of_the_conversion(self):
        resampler = audioop_utils.Resampler(1, 8000, 16000)
        first = resampler.resample(self.fragment, 1)
        self.assertIsInstance(first, bytes)
        self.assertIsNotNone(resampler.state)
        second = resampler.resample(self.fragment, 1)
        self.assertIsInstance(second, bytes)

    def test_the_resampler_reports_its_settings(self):
        resampler = audioop_utils.Resampler(2, 8000, 16000)
        self.assertEqual(resampler.channels, 2)
        self.assertEqual(resampler.input_rate, 8000)
        self.assertEqual(resampler.output_rate, 16000)
        self.assertIsNone(resampler.state)

    def test_the_resampler_forgets_the_state_on_a_reset(self):
        resampler = audioop_utils.Resampler(1, 8000, 16000)
        resampler.resample(self.fragment, 1)
        resampler.reset()
        self.assertIsNone(resampler.state)

    def test_the_resampler_continues_where_the_standard_library_stops(self):
        resampler = audioop_utils.Resampler(1, 8000, 16000)
        first = resampler.resample(self.fragment, 1)
        second = resampler.resample(self.fragment, 1)
        manual, state = _audioop.ratecv(self.fragment, 1, 1, 8000, 16000, None)
        expected, _ = _audioop.ratecv(self.fragment, 1, 1, 8000, 16000, state)
        self.assertEqual(first, manual)
        self.assertEqual(second, expected)


class TestAdpcm(unittest.TestCase):
    """Verify the helpers that code a fragment with ADPCM."""

    def setUp(self):
        if _audioop is None:
            self.skipTest("audioop module not available")
        self.fragment = b"\x00\x10\x20\x30\x40"

    def test_the_coded_fragment_and_the_state_are_returned(self):
        coded, state = audioop_utils.encode_adpcm(self.fragment, 1)
        self.assertIsInstance(coded, bytes)
        self.assertIsNotNone(state)

    def test_the_coded_fragment_holds_four_bits_per_sample(self):
        coded, _ = audioop_utils.encode_adpcm(self.fragment, 1)
        self.assertLessEqual(len(coded), len(self.fragment) // 2)

    def test_the_coded_fragment_matches_the_standard_library(self):
        coded, _ = audioop_utils.encode_adpcm(self.fragment, 1)
        self.assertEqual(coded, _standard_encode(self.fragment, 1)[0])

    def test_the_decoded_fragment_matches_the_standard_library(self):
        coded, _ = _standard_encode(self.fragment, 1)
        decoded, _ = audioop_utils.decode_adpcm(coded, 1)
        self.assertEqual(decoded, _standard_decode(coded, 1)[0])

    def test_the_decoded_fragment_is_read_as_bytes(self):
        coded, _ = audioop_utils.encode_adpcm(self.fragment, 1)
        decoded, _ = audioop_utils.decode_adpcm(coded, 1)
        self.assertIsInstance(decoded, bytes)

    def test_the_number_of_bits_must_be_one_the_standard_library_understands(self):
        with self.assertRaises(ValueError):
            audioop_utils.encode_adpcm(self.fragment, 1, None, 9)
        with self.assertRaises(ValueError):
            audioop_utils.decode_adpcm(b"\x00", 1, None, 9)

    def test_the_number_of_bits_must_be_an_integer(self):
        with self.assertRaises(TypeError):
            audioop_utils.encode_adpcm(self.fragment, 1, None, "4")


class TestDegradation(unittest.TestCase):
    """Verify the behaviour on an interpreter that removed the module."""

    @unittest.skipIf(_audioop is not None, "audioop module available")
    def test_the_helpers_report_the_missing_module(self):
        with self.assertRaises(RuntimeError):
            audioop_utils.convert_sample_width(b"\x01", 1, 2)
        with self.assertRaises(RuntimeError):
            audioop_utils.describe_fragment(b"\x01", 1)
        with self.assertRaises(RuntimeError):
            audioop_utils.resample(b"\x01", 1, 1, 8000, 16000, None)

    @unittest.skipIf(_audioop is not None, "audioop module available")
    def test_the_pure_helpers_keep_working(self):
        self.assertEqual(audioop_utils.frame_count(b"\x01\x02", 1), 2)
        self.assertEqual(audioop_utils.average(b"\x02\x04", 1), 3.0)


class TestStateOfTheModule(unittest.TestCase):
    """Verify the state the module keeps between two calls."""

    def test_the_adpcm_convention_is_detected_once(self):
        if _audioop is None:
            self.skipTest("audioop module not available")
        audioop_utils.encode_adpcm(b"\x00\x10", 1)
        self.assertIn(audioop_utils._ADPCM_CONVENTION, ("stateful", "legacy"))

    def test_the_convention_matches_the_running_interpreter(self):
        if _audioop is None:
            self.skipTest("audioop module not available")
        audioop_utils.encode_adpcm(b"\x00\x10", 1)
        self.assertEqual(audioop_utils._ADPCM_CONVENTION == "stateful", _STATEFUL)


if __name__ == "__main__":
    unittest.main()
