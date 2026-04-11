"""
Decode API audio bytes and export as WAV, MP3, or M4A using ffmpeg-python.

Requires ffmpeg to be installed and on PATH.
"""

from __future__ import annotations

from pathlib import Path
from typing import Literal

import ffmpeg

OutputFormat = Literal["wav", "mp3", "m4a"]

# response_format values treated as raw signed-16-bit PCM (no container header)
_RAW_PCM_FORMATS = {"pcm16", "wav", "wave"}

# response_format → ffmpeg input format string for containerized formats
_CONTAINER_INPUT_FORMAT: dict[str, str] = {
    "mp3": "mp3",
    "m4a": "m4a",
}


def save_audio_bytes(
    audio: bytes,
    path: str | Path,
    *,
    output_format: OutputFormat,
    response_format: str,
    sample_rate: int = 24000,
    channels: int = 1,
) -> None:
    """
    Decode synthesized audio bytes and write to ``path``.

    Args:
        audio: Raw bytes from the TTS API (format matches ``response_format``).
        path: Output file path.
        output_format: Container to write (``wav``, ``mp3``, or ``m4a``).
        response_format: API response format (``pcm16``, ``wav``, ``mp3``, or ``m4a``).
        sample_rate: Sample rate for raw PCM formats (default 24000).
        channels: Channel count for raw PCM formats (default 1).
    """
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)

    rf = response_format.lower().strip()

    try:
        if rf in _RAW_PCM_FORMATS:
            stream = ffmpeg.input(
                "pipe:",
                format="s16le",
                ar=sample_rate,
                ac=channels,
            )
        else:
            fmt = _CONTAINER_INPUT_FORMAT.get(rf)
            if fmt is None:
                raise ValueError(
                    f"Unsupported response_format: {response_format!r}. "
                    "Expected one of: pcm16, wav, mp3, m4a."
                )
            stream = ffmpeg.input("pipe:", format=fmt)

        stream.output(str(path)).run(
            input=audio,
            capture_stdout=True,
            capture_stderr=True,
            overwrite_output=True,
        )
    except ffmpeg.Error as e:
        stderr = e.stderr.decode(errors="replace") if e.stderr else ""
        raise RuntimeError(f"Failed to export audio to {path}: {stderr}") from e
    except ValueError:
        raise
    except Exception as e:
        raise RuntimeError(f"Failed to export audio to {path}: {e}") from e
