"""Media ingestion helpers using yt-dlp.

The real implementation should download external resources and validate that the
resulting file matches expected codecs/containers before handing it over for
further processing.
"""
from __future__ import annotations

import asyncio
from pathlib import Path
from typing import Optional

from config import YTDLP_PATH

__all__ = ["download"]

async def download(url: str, output: Path, fmt: Optional[str] = None) -> Path:
    """Download *url* into *output* and return the resulting path.

    ``fmt`` can be used to force a specific yt-dlp format selection. The
    function should raise an exception if the download fails or the file does not
    comply with validation rules.
    """
    # TODO: implement download via yt-dlp with validations
    raise NotImplementedError
