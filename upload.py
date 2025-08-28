"""High level upload helpers for Telegram.

These functions handle auto-splitting of large files, retries with exponential
backoff and resumable uploads. Real implementation will require persistent
storage to track upload state.
"""
from __future__ import annotations

from pathlib import Path
from typing import Iterable, AsyncIterator, Optional

from telethon import TelegramClient

CHUNK_SIZE_LIMIT = 2 * 1024 * 1024 * 1024  # 2 GiB

__all__ = ["upload_file", "iter_file_chunks"]

async def iter_file_chunks(file_path: Path, chunk_size: int = CHUNK_SIZE_LIMIT) -> AsyncIterator[bytes]:
    """Yield chunks from *file_path* for uploading.

    This is a simplified stub. Real implementation should support resume by
    remembering the last uploaded byte offset.
    """
    # TODO: implement chunk iterator
    raise NotImplementedError

async def upload_file(
    client: TelegramClient,
    file_path: Path,
    target: int | str,
    caption: Optional[str] = None,
) -> None:
    """Upload a local file to *target* using *client*.

    The file will be split automatically if it exceeds Telegram limits. This
    stub should be expanded with retry logic and progress reporting.
    """
    # TODO: implement segmented upload to Telegram
    raise NotImplementedError
