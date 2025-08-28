"""Command handlers for the Telegram bot.

Each command validates user authorization and enqueues tasks for workers. The
actual business logic is expected to live in other modules (``upload``,
``ingest``, ``processing``...).
"""
from __future__ import annotations

from typing import Iterable

from telethon import events, TelegramClient

from config import AUTHORIZED_USERS
from task_queue import TaskQueue, Task

__all__ = ["register_handlers"]

async def _is_authorized(event: events.NewMessage.Event) -> bool:
    """Check whether the sender of *event* is authorized."""
    sender = await event.get_sender()
    return bool(sender and getattr(sender, "id", None) in AUTHORIZED_USERS)

def register_handlers(client: TelegramClient, queue: TaskQueue) -> None:
    """Register all command handlers on the given *client*."""

    @client.on(events.NewMessage(pattern="/upload"))
    async def cmd_upload(event: events.NewMessage.Event) -> None:
        """Upload local files with auto splitting."""
        if not await _is_authorized(event):
            await event.reply("❌ No autorizado")
            return
        await event.reply("📝 Subida en cola (función aún no implementada)")

    @client.on(events.NewMessage(pattern=r"/ingest\s+(.+)"))
    async def cmd_ingest(event: events.NewMessage.Event) -> None:
        """Download media from a URL using yt-dlp."""
        if not await _is_authorized(event):
            await event.reply("❌ No autorizado")
            return
        await event.reply("📥 Descarga en cola (función aún no implementada)")

    @client.on(events.NewMessage(pattern=r"/clip\s+([0-9:]+-[0-9:]+)"))
    async def cmd_clip(event: events.NewMessage.Event) -> None:
        """Generate a clip from a file or URL."""
        if not await _is_authorized(event):
            await event.reply("❌ No autorizado")
            return
        await event.reply("✂️ Clip solicitado (función aún no implementada)")

    @client.on(events.NewMessage(pattern=r"/record\s+(.+)"))
    async def cmd_record(event: events.NewMessage.Event) -> None:
        """Record a live stream."""
        if not await _is_authorized(event):
            await event.reply("❌ No autorizado")
            return
        await event.reply("⏺️ Grabación en cola (función aún no implementada)")

    @client.on(events.NewMessage(pattern=r"/monitor\s+(.+)"))
    async def cmd_monitor(event: events.NewMessage.Event) -> None:
        """Monitor a stream and record automatically when online."""
        if not await _is_authorized(event):
            await event.reply("❌ No autorizado")
            return
        await event.reply("👀 Monitor en cola (función aún no implementada)")

    @client.on(events.NewMessage(pattern="/queue"))
    async def cmd_queue(event: events.NewMessage.Event) -> None:
        """List queued tasks."""
        if not await _is_authorized(event):
            await event.reply("❌ No autorizado")
            return
        tasks = "\n".join(t.task_id for t in queue._queue) or "(vacío)"
        await event.reply(f"📋 Tareas en cola:\n{tasks}")

    @client.on(events.NewMessage(pattern="/settings"))
    async def cmd_settings(event: events.NewMessage.Event) -> None:
        """Change runtime settings like quality or proxy."""
        if not await _is_authorized(event):
            await event.reply("❌ No autorizado")
            return
        await event.reply("⚙️ Configuración no implementada")

    @client.on(events.NewMessage(pattern="/help"))
    async def cmd_help(event: events.NewMessage.Event) -> None:
        """Provide contextual help."""
        if not await _is_authorized(event):
            await event.reply("❌ No autorizado")
            return
        await event.reply(
            """Comandos disponibles:
/upload - Subir archivos
/ingest <URL> - Descargar media
/clip HH:MM:SS-HH:MM:SS - Crear clip
/record <URL|canal> - Grabar stream
/monitor <URL|canal> - Vigilar y grabar
/queue - Ver tareas pendientes
/settings - Ajustes
/help - Esta ayuda
"""
        )
