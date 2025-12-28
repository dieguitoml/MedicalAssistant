"""
Script para descargar automáticamente los modelos de Wav2Lip
"""
import os
import urllib.request
import sys
from pathlib import Path

def download_file(url, destination):
    """Descarga un archivo con barra de progreso."""
    print(f"\n📥 Descargando: {os.path.basename(destination)}")
    print(f"   Desde: {url}")
    print(f"   Hacia: {destination}")

    def show_progress(block_num, block_size, total_size):
        downloaded = block_num * block_size
        percent = min(100, (downloaded / total_size) * 100)
        bar_length = 50
        filled = int(bar_length * downloaded / total_size)
        bar = '█' * filled + '-' * (bar_length - filled)
        print(f'\r   [{bar}] {percent:.1f}% ({downloaded / 1024 / 1024:.1f} MB)', end='')

    try:
        urllib.request.urlretrieve(url, destination, show_progress)
        print(f"\n   ✓ Descarga completada")
        return True
    except Exception as e:
        print(f"\n   ✗ Error: {e}")
        return False

def main():
    # Directorios
    wav2lip_dir = Path("Wav2Lipv2")
    checkpoints_dir = wav2lip_dir / "checkpoints"
    face_detection_dir = wav2lip_dir / "face_detection" / "detection" / "sfd"

    # Crear directorios
    checkpoints_dir.mkdir(parents=True, exist_ok=True)
    face_detection_dir.mkdir(parents=True, exist_ok=True)

    print("=" * 70)
    print("🎭 DESCARGADOR DE MODELOS WAV2LIP")
    print("=" * 70)

    # Modelos a descargar
    models = [
        {
            "name": "Wav2Lip GAN (Mejor calidad visual)",
            "url": "https://drive.usercontent.google.com/download?id=1ORBujdpCFJlhWgYgCCVnTEXW2l2vHlRB&export=download&confirm=t",
            "destination": checkpoints_dir / "wav2lip_gan.pth",
            "size": "~350 MB"
        },
        {
            "name": "Detector Facial S3FD",
            "url": "https://www.adrianbulat.com/downloads/python-fan/s3fd-619a316812.pth",
            "destination": face_detection_dir / "s3fd.pth",
            "size": "~90 MB"
        }
    ]

    # Verificar y descargar
    for model in models:
        print(f"\n{'=' * 70}")
        print(f"📦 Modelo: {model['name']}")
        print(f"   Tamaño: {model['size']}")

        if model["destination"].exists():
            print(f"   ✓ Ya existe: {model['destination']}")
            continue

        success = download_file(model["url"], str(model["destination"]))

        if not success:
            print(f"\n⚠️  ADVERTENCIA: No se pudo descargar {model['name']}")
            print(f"   Descarga manualmente desde el navegador:")
            print(f"   URL: {model['url']}")
            print(f"   Guarda en: {model['destination']}")

    print("\n" + "=" * 70)
    print("✓ PROCESO COMPLETADO")
    print("=" * 70)

    # Verificación final
    print("\n📋 Verificación de archivos:")
    all_ok = True
    for model in models:
        exists = model["destination"].exists()
        status = "✓" if exists else "✗"
        print(f"   {status} {model['destination']}")
        if not exists:
            all_ok = False

    if all_ok:
        print("\n🎉 ¡Todos los modelos están listos!")
        print("   Puedes ejecutar tu aplicación: python app2v2.py")
    else:
        print("\n⚠️  Algunos modelos faltan. Descárgalos manualmente:")
        print("   1. Wav2Lip GAN: https://drive.google.com/file/d/1ORBujdpCFJlhWgYgCCVnTEXW2l2vHlRB/view")
        print("   2. S3FD: https://www.adrianbulat.com/downloads/python-fan/s3fd-619a316812.pth")

    return 0 if all_ok else 1

if __name__ == "__main__":
    sys.exit(main())
