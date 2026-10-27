import ossaudiodev
import unittest

from ossaudiodev_utils import AFMT_S16_LE, SOUND_MIXER_PCM, OSSAudioError, error, openmixer
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


if __name__ == "__main__":
    unittest.main()
