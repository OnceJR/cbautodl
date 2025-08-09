# config.py
# -------------------------
# Rellena estos valores antes de ejecutar

TELEGRAM_API_ID = 1234567           # tu API ID en my.telegram.org
TELEGRAM_API_HASH = "tu_api_hash"   # tu API Hash
BOT_TOKEN = "tu_bot_token"          # token del bot (BotFather)
AUTHORIZED_USERS = {123456789}      # IDs permitidos a usar el bot (enteros)

OUTPUT_DIR = "recordings"           # carpeta donde se guardan los videos
CLIP_DURATION = 30                  # segundos para clips
MONITOR_POLL_INTERVAL = 60          # segundos entre comprobaciones del estado (monitor)
YTDLP_PATH = "yt-dlp"               # comando de yt-dlp (ajusta si usas ruta completa)
FFMPEG_PATH = "ffmpeg"              # comando de ffmpeg (ajusta si usas ruta completa)

LOG_LEVEL = "INFO"                  # DEBUG | INFO | WARNING | ERROR
