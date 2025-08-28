"""Priority based task queue used by workers.

This is a lightweight wrapper around :mod:`heapq` to manage asynchronous tasks
with priorities. Each task is represented by the :class:`Task` dataclass.
"""
from __future__ import annotations

from dataclasses import dataclass, field
import heapq
from typing import Any, List, Optional

__all__ = ["Task", "TaskQueue"]

@dataclass(order=True)
class Task:
    """Representation of a unit of work."""
    priority: int
    task_id: str = field(compare=False)
    data: Any = field(default_factory=dict, compare=False)

class TaskQueue:
    """Simple priority queue for tasks."""

    def __init__(self) -> None:
        self._queue: List[Task] = []

    def add_task(self, task: Task) -> None:
        """Push a new task onto the queue."""
        heapq.heappush(self._queue, task)

    def get_task(self) -> Optional[Task]:
        """Pop the highest priority task or return ``None`` if empty."""
        if not self._queue:
            return None
        return heapq.heappop(self._queue)

    def __len__(self) -> int:
        return len(self._queue)
