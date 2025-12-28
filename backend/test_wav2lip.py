"""
Script de prueba para verificar que Wav2Lip funciona correctamente
"""
import os
import sys
import time

# Fix encoding para Windows
if sys.platform == "win32":
    import codecs
    sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())

print("=" * 70)
print("TEST DE WAV2LIP")
print("=" * 70)

# Agregar Wav2Lipv2 al path
wav2lip_path = os.path.join(os.getcwd(), "Wav2Lipv2")
if wav2lip_path not in sys.path:
    sys.path.insert(0, wav2lip_path)

# Verificar archivos necesarios
print("\n1. Verificando archivos...")

files_to_check = [
    ("Avatar", "avatar_doctor.png"),
    ("Checkpoint", "Wav2Lipv2/checkpoints/wav2lip_gan.pth"),
    ("Face detector", "Wav2Lipv2/face_detection/detection/sfd/s3fd.pth"),
]

all_ok = True
for name, path in files_to_check:
    exists = os.path.exists(path)
    status = "✓" if exists else "✗"
    print(f"   {status} {name}: {path}")
    if not exists:
        all_ok = False

if not all_ok:
    print("\n[ERROR] Faltan archivos necesarios")
    sys.exit(1)

# Verificar GPU
print("\n2. Verificando GPU...")
try:
    import torch
    cuda_available = torch.cuda.is_available()
    print(f"   CUDA disponible: {cuda_available}")
    if cuda_available:
        print(f"   GPU: {torch.cuda.get_device_name(0)}")
except ImportError:
    print("   [ERROR] PyTorch no instalado")
    sys.exit(1)

# Probar importar el wrapper
print("\n3. Importando wrapper de Wav2Lip...")
try:
    from inference_wrapper import Wav2Lipv2
    print("   ✓ Wrapper importado correctamente")
except Exception as e:
    print(f"   ✗ Error al importar: {e}")
    sys.exit(1)

# Inicializar Wav2Lip
print("\n4. Inicializando Wav2Lip...")
try:
    checkpoint_path = os.path.join(wav2lip_path, 'checkpoints/wav2lip_gan.pth')
    wav2lip = Wav2Lipv2(
        checkpoint_path=checkpoint_path,
        pretrained_model_dir=None,
        pads=[0, 10, 0, 0],
        audio_smooth=True,
        rotate=False
    )
    print("   ✓ Wav2Lip inicializado")
except Exception as e:
    print(f"   ✗ Error al inicializar: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Generar audio de prueba
print("\n5. Generando audio de prueba...")
try:
    from piper import PiperVoice
    import wave

    # Buscar modelo de voz
    piper_dir = os.path.join("voices", "piper")
    voice_id = "es_MX-claude-high"

    search_paths = [
        (os.path.join(piper_dir, f"{voice_id}.onnx"),
         os.path.join(piper_dir, f"{voice_id}.onnx.json")),
    ]

    onnx_path = json_path = None
    for onnx, json_file in search_paths:
        if os.path.exists(onnx) and os.path.exists(json_file):
            onnx_path, json_path = onnx, json_file
            break

    if not onnx_path:
        print("   [SKIP] Modelo de voz no encontrado, usando audio dummy")
        # Crear audio dummy silencioso
        import wave
        import array
        test_audio = "test_audio.wav"
        with wave.open(test_audio, 'w') as wav_file:
            wav_file.setnchannels(1)
            wav_file.setsampwidth(2)
            wav_file.setframerate(22050)
            # 2 segundos de silencio
            wav_file.writeframes(array.array('h', [0] * 44100).tobytes())
        print(f"   ✓ Audio dummy creado: {test_audio}")
    else:
        voice = PiperVoice.load(onnx_path, config_path=json_path)
        test_audio = "test_audio.wav"
        with wave.open(test_audio, "wb") as wav_file:
            voice.synthesize_wav("Hola, esta es una prueba del avatar médico.", wav_file)
        print(f"   ✓ Audio de prueba generado: {test_audio}")

except Exception as e:
    print(f"   [SKIP] Error generando audio: {e}")
    # Crear audio dummy
    import wave
    import array
    test_audio = "test_audio.wav"
    with wave.open(test_audio, 'w') as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(22050)
        wav_file.writeframes(array.array('h', [0] * 44100).tobytes())
    print(f"   ✓ Audio dummy creado: {test_audio}")

# Probar generación de video
print("\n6. Generando video de prueba...")
print("   (Esto puede tomar 2-5 segundos con GPU)")
try:
    start = time.time()
    result = wav2lip.run(
        video_path="avatar_doctor.png",
        audio_path=test_audio,
        batch_size=32,
        enhance=False,
        outfile="test_output.mp4",
        fps=25
    )
    elapsed = time.time() - start

    if result and os.path.exists(result):
        size_mb = os.path.getsize(result) / (1024 * 1024)
        print(f"   ✓ Video generado en {elapsed:.2f}s")
        print(f"   ✓ Archivo: {result}")
        print(f"   ✓ Tamaño: {size_mb:.2f} MB")
        print("\n" + "=" * 70)
        print("¡TODO FUNCIONA CORRECTAMENTE!")
        print("=" * 70)
        print("\nPuedes ejecutar tu aplicación: python app2v2.py")
    else:
        print(f"   ✗ Error: Video no generado")
        sys.exit(1)

except Exception as e:
    print(f"   ✗ Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
finally:
    # Limpiar archivos temporales
    for temp_file in [test_audio, "test_output.mp4"]:
        if os.path.exists(temp_file):
            try:
                os.remove(temp_file)
                print(f"\n[CLEANUP] Archivo temporal eliminado: {temp_file}")
            except:
                pass

print("\n" + "=" * 70)
