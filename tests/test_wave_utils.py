"""Tests for wave_utils module."""

import os
import tempfile
import unittest
from unittest import mock

import wave

import wave_utils


def write_wave_file(path, nchannels=1, sampwidth=2, framerate=8000, frames=None):
    """Write a small WAV fixture at *path* and return its params."""
    if frames is None:
        frames = [b"\x00\x00" * 4]
    with wave.open(path, "wb") as writer:
        writer.setnchannels(nchannels)
        writer.setsampwidth(sampwidth)
        writer.setframerate(framerate)
        writer.setnframes(len(frames))
        writer.setcomptype("NONE", "not compressed")
        for frame in frames:
            writer.writeframes(frame)
    return {
        "nchannels": nchannels,
        "sampwidth": sampwidth,
        "framerate": framerate,
        "nframes": len(frames),
        "comptype": "NONE",
        "compname": "not compressed",
    }


class TestExports(unittest.TestCase):
    def test_constants(self):
        self.assertIs(wave_utils.Error, wave.Error)
        self.assertEqual(wave_utils.WAVE_FORMAT_PCM, wave.WAVE_FORMAT_PCM)
        self.assertEqual(wave_utils.WAVE_FORMAT_EXTENSIBLE, wave.WAVE_FORMAT_EXTENSIBLE)


class TestOpenRead(unittest.TestCase):
    def test_open_read_passes_arguments(self):
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
            path = tmp.name
        try:
            with mock.patch.object(wave, "open") as fake:
                reader = wave_utils.open_read(path, "rb")
            fake.assert_called_once_with(path, "rb")
            self.assertIs(reader, fake.return_value)
        finally:
            os.unlink(path)

    def test_open_read_defaults(self):
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
            path = tmp.name
        try:
            with mock.patch.object(wave, "open") as fake:
                wave_utils.open_read(path)
            fake.assert_called_once_with(path, "rb")
        finally:
            os.unlink(path)

    def test_open_read_bad_types(self):
        with self.assertRaises(TypeError):
            wave_utils.open_read(123)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            wave_utils.open_read("path", 5)  # type: ignore[arg-type]


class TestOpenWrite(unittest.TestCase):
    def test_open_write_passes_arguments(self):
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
            path = tmp.name
        try:
            with mock.patch.object(wave, "open") as fake:
                writer = wave_utils.open_write(path, "wb")
            fake.assert_called_once_with(path, "wb")
            self.assertIs(writer, fake.return_value)
        finally:
            os.unlink(path)

    def test_open_write_bad_types(self):
        with self.assertRaises(TypeError):
            wave_utils.open_write(123)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            wave_utils.open_write("path", 5)  # type: ignore[arg-type]


class TestWaveInfo(unittest.TestCase):
    def test_wave_info(self):
        with tempfile.TemporaryDirectory() as d:
            path = os.path.join(d, "test.wav")
            expected = write_wave_file(path, nchannels=2, sampwidth=2, framerate=16000)
            info = wave_utils.wave_info(path)
            self.assertEqual(info, expected)

    def test_wave_info_bad_type(self):
        with self.assertRaises(TypeError):
            wave_utils.wave_info(123)  # type: ignore[arg-type]


class TestGetters(unittest.TestCase):
    def test_getters(self):
        with tempfile.TemporaryDirectory() as d:
            path = os.path.join(d, "test.wav")
            write_wave_file(path, nchannels=2, sampwidth=2, framerate=16000)
            with wave.open(path, "rb") as reader:
                self.assertEqual(wave_utils.nchannels(reader), 2)
                self.assertEqual(wave_utils.sampwidth(reader), 2)
                self.assertEqual(wave_utils.framerate(reader), 16000)
                self.assertEqual(wave_utils.nframes(reader), 1)
                self.assertEqual(wave_utils.comptype(reader), "NONE")
                self.assertEqual(wave_utils.compname(reader), "not compressed")

    def test_getters_bad_type(self):
        for fn in (
            wave_utils.nchannels,
            wave_utils.sampwidth,
            wave_utils.framerate,
            wave_utils.nframes,
            wave_utils.comptype,
            wave_utils.compname,
        ):
            with self.assertRaises(TypeError):
                fn(123)  # type: ignore[arg-type]


class TestGetSetParams(unittest.TestCase):
    def test_get_params(self):
        with tempfile.TemporaryDirectory() as d:
            path = os.path.join(d, "test.wav")
            write_wave_file(path, nchannels=2, sampwidth=2, framerate=16000)
            with wave.open(path, "rb") as reader:
                params = wave_utils.get_params(reader)
            self.assertEqual(params, (2, 2, 16000, 1, "NONE", "not compressed"))

    def test_get_params_bad_type(self):
        with self.assertRaises(TypeError):
            wave_utils.get_params(123)  # type: ignore[arg-type]

    def test_set_params(self):
        with tempfile.TemporaryDirectory() as d:
            path = os.path.join(d, "test.wav")
            writer = wave_utils.create_writer(path, 1, 2, 8000)
            try:
                wave_utils.set_params(writer, (2, 2, 16000, 0, "NONE", "not compressed"))
                params = wave_utils.get_params(writer)
                self.assertEqual(params.nchannels, 2)
                self.assertEqual(params.framerate, 16000)
            finally:
                wave_utils.close_wave(writer)

    def test_set_params_bad(self):
        with tempfile.TemporaryDirectory() as d:
            path = os.path.join(d, "test.wav")
            writer = wave_utils.create_writer(path, 1, 2, 8000)
            try:
                with self.assertRaises(TypeError):
                    wave_utils.set_params(writer, "not a tuple")  # type: ignore[arg-type]
                with self.assertRaises(TypeError):
                    wave_utils.set_params(writer, (1, 2, 8000))  # wrong length
            finally:
                wave_utils.close_wave(writer)


class TestSetters(unittest.TestCase):
    def test_setters(self):
        with tempfile.TemporaryDirectory() as d:
            path = os.path.join(d, "test.wav")
            writer = wave_utils.create_writer(path, 1, 2, 8000)
            try:
                wave_utils.set_nchannels(writer, 2)
                wave_utils.set_sampwidth(writer, 2)
                wave_utils.set_framerate(writer, 16000)
                wave_utils.set_nframes(writer, 100)
                wave_utils.set_comptype(writer, "NONE", "not compressed")
                params = wave_utils.get_params(writer)
                self.assertEqual(params.nchannels, 2)
                self.assertEqual(params.sampwidth, 2)
                self.assertEqual(params.framerate, 16000)
                self.assertEqual(params.nframes, 100)
                self.assertEqual(params.comptype, "NONE")
                self.assertEqual(params.compname, "not compressed")
            finally:
                wave_utils.close_wave(writer)

    def test_setters_validation(self):
        with tempfile.TemporaryDirectory() as d:
            path = os.path.join(d, "test.wav")
            writer = wave_utils.create_writer(path, 1, 2, 8000)
            try:
                with self.assertRaises(TypeError):
                    wave_utils.set_nchannels("not a writer", 1)  # type: ignore[arg-type]
                with self.assertRaises(TypeError):
                    wave_utils.set_nchannels(writer, "one")  # type: ignore[arg-type]
                with self.assertRaises(ValueError):
                    wave_utils.set_nchannels(writer, 0)
                with self.assertRaises(ValueError):
                    wave_utils.set_sampwidth(writer, -1)
                with self.assertRaises(TypeError):
                    wave_utils.set_comptype(writer, 5, "x")  # type: ignore[arg-type]
            finally:
                wave_utils.close_wave(writer)


class TestCreateWriter(unittest.TestCase):
    def test_create_writer(self):
        with tempfile.TemporaryDirectory() as d:
            path = os.path.join(d, "test.wav")
            writer = wave_utils.create_writer(path, 2, 2, 16000, nframes=50)
            try:
                self.assertIsInstance(writer, wave.Wave_write)
                params = wave_utils.get_params(writer)
                self.assertEqual(params.nchannels, 2)
                self.assertEqual(params.sampwidth, 2)
                self.assertEqual(params.framerate, 16000)
                self.assertEqual(params.nframes, 50)
                self.assertEqual(params.comptype, "NONE")
                self.assertEqual(params.compname, "not compressed")
            finally:
                wave_utils.close_wave(writer)

    def test_create_writer_bad_arguments(self):
        with self.assertRaises(TypeError):
            wave_utils.create_writer(123, 1, 2, 8000)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            wave_utils.create_writer("path", "1", 2, 8000)  # type: ignore[arg-type]
        with self.assertRaises(ValueError):
            wave_utils.create_writer("path", 0, 2, 8000)
        with self.assertRaises(ValueError):
            wave_utils.create_writer("path", 1, 0, 8000)
        with self.assertRaises(ValueError):
            wave_utils.create_writer("path", 1, 2, 0)


class TestReadFrames(unittest.TestCase):
    def test_read_frames_all(self):
        with tempfile.TemporaryDirectory() as d:
            path = os.path.join(d, "test.wav")
            write_wave_file(path, frames=[b"\x01\x02", b"\x03\x04"])
            with wave.open(path, "rb") as reader:
                data = wave_utils.read_frames(reader)
            self.assertEqual(data, b"\x01\x02\x03\x04")

    def test_read_frames_some(self):
        with tempfile.TemporaryDirectory() as d:
            path = os.path.join(d, "test.wav")
            write_wave_file(path, frames=[b"\x01\x02", b"\x03\x04"])
            with wave.open(path, "rb") as reader:
                data = wave_utils.read_frames(reader, 1)
            self.assertEqual(data, b"\x01\x02")

    def test_read_frames_negative_reads_all(self):
        with tempfile.TemporaryDirectory() as d:
            path = os.path.join(d, "test.wav")
            write_wave_file(path, frames=[b"\x01\x02"])
            with wave.open(path, "rb") as reader:
                data = wave_utils.read_frames(reader, -1)
            self.assertEqual(data, b"\x01\x02")

    def test_read_frames_bad_type(self):
        with self.assertRaises(TypeError):
            wave_utils.read_frames(123)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            wave_utils.read_frames(123, "one")  # type: ignore[arg-type]


class TestWriteFrames(unittest.TestCase):
    def test_write_frames(self):
        with tempfile.TemporaryDirectory() as d:
            path = os.path.join(d, "test.wav")
            writer = wave_utils.create_writer(path, 1, 1, 8000)
            try:
                wave_utils.write_frames(writer, b"\x01\x02\x03")
                wave_utils.close_wave(writer)
                info = wave_utils.wave_info(path)
                self.assertEqual(info["sampwidth"], 1)
            except Exception:
                wave_utils.close_wave(writer)
                raise

    def test_write_frames_bad_type(self):
        with tempfile.TemporaryDirectory() as d:
            path = os.path.join(d, "test.wav")
            writer = wave_utils.create_writer(path, 1, 1, 8000)
            try:
                with self.assertRaises(TypeError):
                    wave_utils.write_frames("not a writer", b"\x01")  # type: ignore[arg-type]
                with self.assertRaises(TypeError):
                    wave_utils.write_frames(writer, "not bytes")  # type: ignore[arg-type]
            finally:
                wave_utils.close_wave(writer)


class TestCloseWave(unittest.TestCase):
    def test_close_wave_read(self):
        with tempfile.TemporaryDirectory() as d:
            path = os.path.join(d, "test.wav")
            write_wave_file(path)
            reader = wave_utils.open_read(path)
            wave_utils.close_wave(reader)
            self.assertTrue(reader.closed)

    def test_close_wave_write(self):
        with tempfile.TemporaryDirectory() as d:
            path = os.path.join(d, "test.wav")
            writer = wave_utils.create_writer(path, 1, 1, 8000)
            wave_utils.close_wave(writer)
            self.assertTrue(writer.closed)

    def test_close_wave_bad_type(self):
        with self.assertRaises(TypeError):
            wave_utils.close_wave(123)  # type: ignore[arg-type]


if __name__ == "__main__":
    unittest.main()
