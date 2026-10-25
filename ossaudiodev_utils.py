"""Utilities for OSS audio device access (wrapping :mod:`ossaudiodev`)."""

import ossaudiodev as _ossaudiodev


def open(*args, **kwargs):
    return _ossaudiodev.open(*args, **kwargs)


def openmixer(*args, **kwargs):
    return _ossaudiodev.openmixer(*args, **kwargs)


OSSAudioError = _ossaudiodev.OSSAudioError
error = _ossaudiodev.error
AFMT_S16_LE = _ossaudiodev.AFMT_S16_LE
SOUND_MIXER_PCM = _ossaudiodev.SOUND_MIXER_PCM
