import importlib
import ossaudiodev
import sys
import unittest
from unittest import mock

import ossaudiodev_utils
from ossaudiodev_utils import (
    AFMT_S16_LE,
    SOUND_MIXER_PCM,
    OSSAudioError,
    error,
    is_available,
    openmixer,
)
from ossaudiodev_utils import open as _open


class TestOssaudiodevUtils(unittest.TestCase):
    def test_error_alias(self):
        self.assertIs(OSSAudioError, ossaudiodev.OSSAudioError)
        self.assertIs(error, ossaudiodev.error)

    def test_open_callable(self):
        self.assertTrue(callable(_open))

    def test_openmixer_callable(self):
        self.assertTrue(callable(openmixer))

    def test_constants(self):
        self.assertIsInstance(AFMT_S16_LE, int)
        self.assertIsInstance(SOUND_MIXER_PCM, int)
        self.assertEqual(AFMT_S16_LE, ossaudiodev.AFMT_S16_LE)
        self.assertEqual(SOUND_MIXER_PCM, ossaudiodev.SOUND_MIXER_PCM)

    def test_is_available(self):
        result = is_available()
        self.assertIsInstance(result, bool)
        self.assertEqual(result, ossaudiodev is not None)


class TestUnavailableModule(unittest.TestCase):
    """Verify the Python 3.13+ path where :mod:`ossaudiodev` no longer ships."""

    def test_unavailable_branch(self) -> None:
        try:
            with mock.patch.dict(sys.modules, {"ossaudiodev": None}):
                reloaded = importlib.reload(ossaudiodev_utils)
                assert reloaded.is_available() is False
                assert issubclass(reloaded.OSSAudioError, Exception)
                assert reloaded.error is reloaded.OSSAudioError
                with self.assertRaises(RuntimeError):
                    reloaded.open()
                with self.assertRaises(RuntimeError):
                    reloaded.openmixer()
                # Constants have fallback values
                assert reloaded.AFMT_S16_LE == 0x00000010
                assert reloaded.SOUND_MIXER_PCM == 0
        finally:
            importlib.reload(ossaudiodev_utils)
        assert ossaudiodev_utils.is_available() is True


if __name__ == "__main__":
    unittest.main()
