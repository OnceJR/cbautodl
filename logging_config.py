"""Logging configuration for the bot.

The project uses structured JSON logging to simplify parsing and aggregation of
logs. Use :func:`configure_logging` at the entry point to enable it.
"""
from __future__ import annotations

import json
import logging
import sys
from typing import Any, Dict

__all__ = ["configure_logging"]

class JsonFormatter(logging.Formatter):
    """Minimal JSON formatter for logging records."""

    def format(self, record: logging.LogRecord) -> str:  # pragma: no cover - formatting logic
        data: Dict[str, Any] = {
            "time": self.formatTime(record, "%Y-%m-%dT%H:%M:%S"),
            "level": record.levelname,
            "name": record.name,
            "message": record.getMessage(),
        }
        if record.exc_info:
            data["exc_info"] = self.formatException(record.exc_info)
        return json.dumps(data, ensure_ascii=False)

def configure_logging(level: int | None = None) -> None:
    """Configure root logger to output JSON lines."""
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(JsonFormatter())
    root = logging.getLogger()
    root.handlers.clear()
    root.addHandler(handler)
    if level is None:
        level = logging.INFO
    root.setLevel(level)
