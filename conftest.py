"""Test configuration ensuring repository root on ``sys.path``.

Pytest does not always include the project root in ``sys.path`` when executed in
certain environments. This file guarantees that modules like ``recorder`` can be
imported during tests.
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
