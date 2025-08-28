"""Stream monitoring utilities.

This module provides helpers for periodically checking whether a stream is
online and triggering recording tasks. The actual recording is delegated to the
:mod:`recorder` module or other workers.
"""
from __future__ import annotations

import asyncio
from typing import Awaitable, Callable

from config import MONITOR_POLL_INTERVAL

__all__ = ["monitor_stream"]

Callback = Callable[[str], Awaitable[None]]

async def monitor_stream(url: str, on_online: Callback, poll_interval: int = MONITOR_POLL_INTERVAL) -> None:
    """Periodically check *url* and call ``on_online(url)`` when it becomes available."""
    # TODO: implement monitoring using yt-dlp or other method
    raise NotImplementedError
