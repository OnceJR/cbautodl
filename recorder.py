# recorder.py
import asyncio
import logging
import shlex
from pathlib import Path
from datetime import datetime
from typing import Dict, Optional, Set

import signal

from config import OUTPUT_DIR, CLIP_DURATION, MONITOR_POLL_INTERVAL, YTDLP_PATH, FFMPEG_PATH, LOG_LEVEL

LOG_LEVEL_MAP = {
    "DEBUG": logging.DEBUG,
    "INFO": logging.INFO,
    "WARNING": logging.WARNING,
    "ERROR": logging.ERROR,
}
logging.basicConfig(
    level=LOG_LEVEL_MAP.get(LOG_LEVEL, logging.INFO),
    format="[%(asctime)s] %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

Path(OUTPUT_DIR).mkdir(exist_ok=True)


def _timestamp() -> str:
    return datetime.now().strftime("%Y%m%d_%H%M%S")


class Recording:
    """Representa una grabación en curso: proceso yt-dlp, tarea asyncio y metadata."""
    def __init__(self, model: str, url: str, proc: asyncio.subprocess.Process, task: asyncio.Task, out_path: Path):
        self.model = model
        self.url = url
        self.proc = proc
        self.task = task
        self.out_path = out_path


class RecorderManager:
    """Gestiona grabaciones y monitores."""
    def __init__(self):
        self.recordings: Dict[str, Recording] = {}  # key: model_name
        self.monitor_tasks: Dict[str, asyncio.Task] = {}  # key: model_name
        self._running = True

    async def _run_subprocess(self, *cmd) -> asyncio.subprocess.Process:
        """Lanza un subprocess sin esperar, devolviendo el handle."""
        logging.debug("Ejecutando subproceso: %s", " ".join(cmd))
        proc = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        return proc

    async def record_stream(self, url: str, model_name: str) -> Path:
        """
        Inicia grabación con yt-dlp y devuelve Path de salida.
        Esta coroutine finaliza cuando la grabación termina o cuando se cancela.
        """
        ts = _timestamp()
        out_file = Path(OUTPUT_DIR) / f"{model_name}_{ts}.mp4"

        cmd = [
            YTDLP_PATH,
            url,
            "-f", "best",
            "-o", str(out_file),
            "--no-part",
            "--hls-use-mpegts",
            "--retries", "infinite",
            "--fragment-retries", "infinite",
        ]

        proc = await self._run_subprocess(*cmd)
        # Crear tarea que espere al proceso y registre resultado
        async def waiter():
            try:
                logging.info("🟢 Grabando %s -> %s (pid=%s)", model_name, out_file, proc.pid)
                stdout, stderr = await proc.communicate()
                if proc.returncode == 0:
                    logging.info("✅ Grabación finalizada %s", out_file)
                else:
                    logging.warning("⚠ yt-dlp finalizó con código %s para %s", proc.returncode, model_name)
                    logging.debug("stderr: %s", (stderr or b"").decode(errors="ignore"))
            except asyncio.CancelledError:
                logging.info("⛔ Cancelando grabación de %s", model_name)
                # enviar SIGINT y después SIGTERM si sigue vivo
                try:
                    proc.send_signal(signal.SIGINT)
                    await asyncio.sleep(1)
                    if proc.returncode is None:
                        proc.terminate()
                        await asyncio.sleep(0.5)
                        if proc.returncode is None:
                            proc.kill()
                except Exception as ex:
                    logging.debug("error al matar proceso: %s", ex)
                raise

        task = asyncio.create_task(waiter())
        rec = Recording(model_name, url, proc, task, out_file)
        self.recordings[model_name] = rec
        try:
            await task  # se espera a que termine o se cancele externamente
        finally:
            # limpiar registro si ya no existe
            self.recordings.pop(model_name, None)
        return out_file

    async def stop_recording(self, model_name: str) -> bool:
        """Intenta detener una grabación en curso. Devuelve True si existía y fue solicitada a detener."""
        rec = self.recordings.get(model_name)
        if not rec:
            return False
        logging.info("Solicitando detención de grabación de %s (pid=%s)", model_name, rec.proc.pid if rec.proc else "N/A")
        rec.task.cancel()
        # rec.proc es manejado dentro del waiter (muerte segura)
        try:
            await asyncio.wait_for(rec.task, timeout=15)
        except asyncio.TimeoutError:
            logging.warning("El proceso no finalizó a tiempo; forzando kill.")
            try:
                rec.proc.kill()
            except Exception:
                pass
        return True

    async def record_clip(self, url: str, model_name: str, duration: int = CLIP_DURATION) -> Path:
        """Corta un clip de la transmisión usando yt-dlp (downloader ffmpeg con -t)."""
        ts = _timestamp()
        out_file = Path(OUTPUT_DIR) / f"{model_name}_clip_{ts}.mp4"

        cmd = [
            YTDLP_PATH,
            "--hls-use-mpegts",
            "--no-part",
            "--downloader", "ffmpeg",
            "--downloader-args", f"ffmpeg_i:-t {duration}",
            "-f", "best",
            url,
            "-o", str(out_file)
        ]
        proc = await self._run_subprocess(*cmd)
        stdout, stderr = await proc.communicate()
        if proc.returncode == 0:
            logging.info("🎬 Clip creado: %s", out_file)
        else:
            logging.warning("⚠ Error creando clip para %s (code=%s)", model_name, proc.returncode)
            logging.debug("stderr: %s", (stderr or b"").decode(errors="ignore"))
        return out_file

    async def _is_online_via_ytdlp(self, url: str) -> bool:
        """
        Comprueba si la URL tiene stream disponible utilizando 'yt-dlp -g <url>'.
        Devuelve True si devuelve una URL directa.
        """
        cmd = [YTDLP_PATH, "-g", url]
        try:
            proc = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            try:
                stdout, stderr = await asyncio.wait_for(proc.communicate(), timeout=20)
            except asyncio.TimeoutError:
                proc.kill()
                return False
            if proc.returncode == 0 and stdout:
                text = stdout.decode(errors="ignore").strip()
                if text:
                    logging.debug("yt-dlp -g returned: %s", text.splitlines()[0])
                    return True
            logging.debug("yt-dlp -g no devolvió URL (code=%s)", proc.returncode)
            return False
        except FileNotFoundError:
            logging.error("yt-dlp no encontrado: asegúrate de que YTDLP_PATH apunta al ejecutable.")
            return False

    async def start_monitor(self, model_name: str, url: str, poll_interval: int = MONITOR_POLL_INTERVAL):
        """Crea una tarea que vigila la URL y lanza record_stream cuando esté online."""
        if model_name in self.monitor_tasks:
            logging.info("Monitor ya activo para %s", model_name)
            return

        async def monitor_loop():
            logging.info("🔎 Monitor iniciado para %s (interval=%ss)", model_name, poll_interval)
            while True:
                try:
                    # si ya está grabando, esperar un poco y seguir
                    if model_name in self.recordings:
                        logging.debug("%s ya está grabando; check en %ss", model_name, poll_interval)
                        await asyncio.sleep(poll_interval)
                        continue
                    online = await self._is_online_via_ytdlp(url)
                    if online:
                        logging.info("🔔 %s está ONLINE — iniciando grabación automática", model_name)
                        # arrancar la grabación en background y no bloquear el loop de monitor
                        asyncio.create_task(self.record_stream(url, model_name))
                        # esperar un tiempo mayor tras detectar online para evitar reintentos excesivos
                        await asyncio.sleep(max(poll_interval, 30))
                    else:
                        logging.debug("%s offline", model_name)
                        await asyncio.sleep(poll_interval)
                except asyncio.CancelledError:
                    logging.info("🛑 Monitor cancelled para %s", model_name)
                    break
                except Exception as ex:
                    logging.exception("Error en monitor de %s: %s", model_name, ex)
                    await asyncio.sleep(poll_interval)

        task = asyncio.create_task(monitor_loop())
        self.monitor_tasks[model_name] = task

    async def stop_monitor(self, model_name: str) -> bool:
        """Detiene el monitor para un modelo (si existe)."""
        t = self.monitor_tasks.get(model_name)
        if not t:
            return False
        t.cancel()
        try:
            await t
        except asyncio.CancelledError:
            pass
        self.monitor_tasks.pop(model_name, None)
        logging.info("🟡 Monitor detenido para %s", model_name)
        return True

    def list_monitors(self) -> Dict[str, str]:
        """Devuelve un dict con monitores activos (model_name -> task state)."""
        out = {}
        for m, t in self.monitor_tasks.items():
            out[m] = "running" if not t.done() else "done"
        return out

    def list_recordings(self) -> Dict[str, str]:
        """Lista grabaciones en curso (model -> out path)."""
        return {m: str(r.out_path) for m, r in self.recordings.items()}


# Crear una instancia compartida
manager = RecorderManager()
