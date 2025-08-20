import asyncio
from pathlib import Path

import pytest

import recorder


class FakeProcess:
    """Simple fake subprocess process for testing."""
    def __init__(self, returncode: int, out_file: Path | None = None):
        self.returncode = returncode
        self.pid = 123
        self._out_file = out_file

    async def communicate(self):
        if self.returncode == 0 and self._out_file:
            self._out_file.touch()
        return b"", b""

    def send_signal(self, sig):
        pass

    def terminate(self):
        pass

    def kill(self):
        pass


@pytest.mark.asyncio
async def test_record_stream_failure(monkeypatch, tmp_path):
    """Si yt-dlp falla, record_stream debe devolver None o lanzar."""
    monkeypatch.setattr(recorder, "OUTPUT_DIR", tmp_path)
    manager = recorder.RecorderManager()

    async def fake_exec(*cmd, **kwargs):
        out_file = None
        if "-o" in cmd:
            out_file = Path(cmd[cmd.index("-o") + 1])
        return FakeProcess(1, out_file)

    monkeypatch.setattr(asyncio, "create_subprocess_exec", fake_exec)

    result = None
    error = None
    try:
        result = await manager.record_stream("http://example.com", "model")
    except Exception as exc:  # pragma: no cover - comportamiento alternativo
        error = exc

    assert error is not None or result is None
    assert not list(tmp_path.iterdir())


@pytest.mark.asyncio
async def test_record_stream_success(monkeypatch, tmp_path):
    """record_stream debe devolver la ruta del archivo creado."""
    monkeypatch.setattr(recorder, "OUTPUT_DIR", tmp_path)
    manager = recorder.RecorderManager()

    async def fake_exec(*cmd, **kwargs):
        out_file = None
        if "-o" in cmd:
            out_file = Path(cmd[cmd.index("-o") + 1])
        return FakeProcess(0, out_file)

    monkeypatch.setattr(asyncio, "create_subprocess_exec", fake_exec)

    result = await manager.record_stream("http://example.com", "model")
    assert isinstance(result, Path)
    assert result.exists()
    assert result.parent == tmp_path
