# 📡 CB Auto Recorder Bot (Local + Monitoreo Automático)

Bot de Telegram para grabar transmisiones y clips de Chaturbate **sin Selenium**, usando solo `yt-dlp` y `ffmpeg`.  
Incluye **monitoreo automático** para comenzar a grabar cuando una modelo se ponga en línea.

---

## 🚀 Características
- **🎥 Grabación completa** de transmisiones en vivo.
- **🎬 Grabación de clips cortos** (duración configurable).
- **📡 Monitoreo automático** de modelos: el bot comprueba cada minuto si están en línea y empieza a grabar.
- **🔐 Control de acceso**: solo usuarios autorizados pueden usarlo.
- **📂 Gestión de archivos**: todo se guarda en la carpeta `recordings/`.

---

## 🛠 Requisitos
- **Sistema operativo**: Linux recomendado (probado en Ubuntu/Debian).  
- **Python**: 3.10 o superior.
- **Dependencias**:  
  - `yt-dlp`
  - `ffmpeg`
  - `telethon`

---

## 📦 Instalación
1. Clona este repositorio:
   ```bash
   git clone https://github.com/usuario/cbautorec.git
   cd cbautorec
