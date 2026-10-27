"""OSS audio device utilities wrapping the standard library ossaudiodev module.

Provides aliases and re-exports for ossaudiodev functionality.
"""

try:
    import ossaudiodev
except Exception:  # pragma: no cover
    ossaudiodev = None  # type: ignore

__all__ = [
    "open",
    "openmixer",
    "OSSAudioError",
    "error",
    "AFMT_S16_LE",
    "SOUND_MIXER_PCM",
    "is_available",
]


def is_available() -> bool:
    """Return True if ossaudiodev is available."""
    return ossaudiodev is not None


if ossaudiodev is not None:
    open = ossaudiodev.open
    openmixer = ossaudiodev.openmixer
    OSSAudioError = ossaudiodev.OSSAudioError
    error = ossaudiodev.error
    AFMT_S16_LE = getattr(ossaudiodev, "AFMT_S16_LE")
    SOUND_MIXER_PCM = getattr(ossaudiodev, "SOUND_MIXER_PCM")
else:  # pragma: no cover
    def open(*args, **kwargs):  # type: ignore
        raise RuntimeError("ossaudiodev is not available")

    def openmixer(*args, **kwargs):  # type: ignore
        raise RuntimeError("ossaudiodev is not available")

    class OSSAudioError(Exception):  # type: ignore
        pass

    error = OSSAudioError
    AFMT_S16_LE = 0x00000010  # common value as fallback
    SOUND_MIXER_PCM = 0
