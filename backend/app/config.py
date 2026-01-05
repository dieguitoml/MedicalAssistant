"""
Configuración centralizada de la aplicación
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Directorios base
BASE_DIR = Path(__file__).resolve().parent.parent
PROJECT_ROOT = BASE_DIR.parent

# Configuración de modelos
CHAT_MODEL = os.getenv("CHAT_MODEL", "llama3.2")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "nomic-embed-text")
DATABASE_LOCATION = os.getenv("DATABASE_LOCATION", str(PROJECT_ROOT / "chunks"))

# Configuración TTS
PIPER_VOICE_DIR = os.getenv("PIPER_VOICE_DIR", str(PROJECT_ROOT / "voices" / "piper"))
PIPER_VOICE_ID = os.getenv("PIPER_VOICE_ID", "es_MX-claude-high")

# Configuración Avatar
AVATAR_IMAGE = os.getenv("AVATAR_IMAGE", str(PROJECT_ROOT / "avatar_doctor.png"))
WAV2LIP_DIR = os.getenv("WAV2LIP_DIR", str(PROJECT_ROOT / "Wav2Lipv2"))

# Directorios de salida
TTS_OUTPUT_DIR = Path(os.getenv("TTS_OUTPUT_DIR", str(BASE_DIR / "tts_out")))
VIDEO_OUTPUT_DIR = Path(os.getenv("VIDEO_OUTPUT_DIR", str(BASE_DIR / "videos_out")))

# Crear directorios si no existen
TTS_OUTPUT_DIR.mkdir(exist_ok=True)
VIDEO_OUTPUT_DIR.mkdir(exist_ok=True)

# CORS
CORS_ORIGINS = os.getenv("CORS_ORIGINS", "http://localhost:5173,http://localhost:3000").split(",")

# Configuración de eSpeak (Windows)
ESPEAK_PATH = r"C:\Program Files (x86)\eSpeak"
if os.path.isdir(ESPEAK_PATH) and ESPEAK_PATH not in os.environ["PATH"]:
    os.environ["PATH"] = ESPEAK_PATH + os.pathsep + os.environ["PATH"]

print("=" * 60)
print("🏥 Medical Assistant API - Configuración")
print("=" * 60)
print(f"📁 Database: {DATABASE_LOCATION}")
print(f"🎤 TTS Voice: {PIPER_VOICE_ID}")
print(f"🎭 Avatar: {AVATAR_IMAGE}")
print(f"📁 Output TTS: {TTS_OUTPUT_DIR}")
print(f"📁 Output Video: {VIDEO_OUTPUT_DIR}")
print("=" * 60)