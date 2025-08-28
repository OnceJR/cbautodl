"""Utilities for filesystem operations.

This module centralizes all file-related helpers like path sanitization and
directory creation. It aims to keep all file system interactions safe and
portable across platforms.
"""
from __future__ import annotations

from pathlib import Path
import re

__all__ = ["sanitize_filename", "ensure_directory"]

# Regex that matches any character not allowed in safe filenames.
_SANITIZE_RE = re.compile(r"[^-_.() a-zA-Z0-9]")

def sanitize_filename(name: str) -> str:
    """Return a filesystem-safe version of *name*.

    This function removes characters that may be unsafe or unsupported on
    various filesystems. It does not attempt to handle reserved names.
    """
    return _SANITIZE_RE.sub("_", name)

def ensure_directory(path: Path) -> None:
    """Create *path* if it doesn't exist."""
    path.mkdir(parents=True, exist_ok=True)
