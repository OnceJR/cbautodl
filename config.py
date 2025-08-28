"""Global configuration for the bot.

Values are stored in the :class:`BotConfig` dataclass for easy access and can be
customised before running the application. Module level constants are provided
for backward compatibility with existing modules.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Set

@dataclass
class BotConfig:
    TELEGRAM_API_ID: int = 1234567
    TELEGRAM_API_HASH: str = "tu_api_hash"
    BOT_TOKEN: str = "tu_bot_token"
    AUTHORIZED_USERS: Set[int] = field(default_factory=lambda: {123456789})

    OUTPUT_DIR: str = "recordings"
    CLIP_DURATION: int = 30
    MONITOR_POLL_INTERVAL: int = 60
    YTDLP_PATH: str = "yt-dlp"
    FFMPEG_PATH: str = "ffmpeg"

    LOG_LEVEL: str = "INFO"  # DEBUG | INFO | WARNING | ERROR
    NORMAL_UPLOAD_LIMIT_GB: int = 2
    PREMIUM_UPLOAD_LIMIT_GB: int = 4

# Default configuration instance used by the application
config = BotConfig()

# Expose legacy constants for modules that import them directly
TELEGRAM_API_ID = config.TELEGRAM_API_ID
TELEGRAM_API_HASH = config.TELEGRAM_API_HASH
BOT_TOKEN = config.BOT_TOKEN
AUTHORIZED_USERS = config.AUTHORIZED_USERS
OUTPUT_DIR = config.OUTPUT_DIR
CLIP_DURATION = config.CLIP_DURATION
MONITOR_POLL_INTERVAL = config.MONITOR_POLL_INTERVAL
YTDLP_PATH = config.YTDLP_PATH
FFMPEG_PATH = config.FFMPEG_PATH
LOG_LEVEL = config.LOG_LEVEL
