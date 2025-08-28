"""Media processing helpers using ffmpeg.

This module contains coroutine helpers that spawn ``ffmpeg`` subprocesses to
perform operations like cutting, concatenation or transcoding. Each function is
currently a stub and should be implemented with proper error handling and
retries.
"""
from __future__ import annotations

import asyncio
from pathlib import Path
from typing import Iterable

from config import FFMPEG_PATH

__all__ = [
    "cut_clip",
    "concat_videos",
    "transcode_video",
    "normalize_audio",
    "snapshot",
]

async def _run_ffmpeg(args: Iterable[str]) -> asyncio.subprocess.Process:
    """Run ffmpeg with *args* and return the process handle."""
    return await asyncio.create_subprocess_exec(
        FFMPEG_PATH, *args, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
    )

async def cut_clip(src: Path, dst: Path, start: str, end: str) -> Path:
    """Cut a segment from *src* into *dst* using timestamps ``start`` and ``end``.
    """
    # TODO: implement ffmpeg slicing
    raise NotImplementedError

async def concat_videos(files: Iterable[Path], dst: Path) -> Path:
    """Concatenate multiple video files into one."""
    # TODO: implement ffmpeg concatenation
    raise NotImplementedError

async def transcode_video(src: Path, dst: Path, video_codec: str = "libx264", audio_codec: str = "aac") -> Path:
    """Transcode *src* into *dst* with provided codecs."""
    # TODO: implement ffmpeg transcoding
    raise NotImplementedError

async def normalize_audio(src: Path, dst: Path) -> Path:
    """Normalize audio track loudness."""
    # TODO: implement ffmpeg loudnorm
    raise NotImplementedError

async def snapshot(src: Path, dst: Path, at: str = "00:00:01") -> Path:
    """Save a thumbnail image at timestamp ``at``."""
    # TODO: implement snapshot generation
    raise NotImplementedError
