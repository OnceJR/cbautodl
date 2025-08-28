"""Entrypoint for the Telegram bot.

It bootstraps the Telethon client, initializes the task queue and launches
worker tasks responsible for ingesting, processing and uploading media.
"""
from __future__ import annotations

import asyncio
import contextlib
import logging

from telethon import TelegramClient

from config import TELEGRAM_API_ID, TELEGRAM_API_HASH, BOT_TOKEN, LOG_LEVEL
from logging_config import configure_logging
from commands import register_handlers
from task_queue import TaskQueue

async def _run_workers(queue: TaskQueue) -> None:
    """Background worker loop that processes tasks from *queue*.

    The real implementation should spawn dedicated workers for download,
    processing and uploading, possibly in separate processes. This stub simply
    waits for tasks and logs them.
    """
    while True:
        task = queue.get_task()
        if task is None:
            await asyncio.sleep(1)
            continue
        # TODO: dispatch task to the appropriate handler
        print(f"processing task: {task.task_id}")

async def main() -> None:
    """Async entry point for running the bot."""
    level = getattr(logging, LOG_LEVEL.upper(), logging.INFO)
    configure_logging(level)
    queue = TaskQueue()
    client = TelegramClient("bot", TELEGRAM_API_ID, TELEGRAM_API_HASH)
    await client.start(bot_token=BOT_TOKEN)
    register_handlers(client, queue)
    worker = asyncio.create_task(_run_workers(queue))
    try:
        await client.run_until_disconnected()
    finally:
        worker.cancel()
        with contextlib.suppress(Exception):
            await worker

if __name__ == "__main__":
    asyncio.run(main())
