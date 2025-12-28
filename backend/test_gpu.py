"""
Script para verificar que PyTorch detecta tu GPU RTX 3060
"""
import sys

print("=" * 70)
print("VERIFICACION DE GPU PARA WAV2LIP")
print("=" * 70)

# Verificar PyTorch
try:
    import torch
    print(f"\n[OK] PyTorch version: {torch.__version__}")
except ImportError:
    print("\n[ERROR] PyTorch no esta instalado")
    print("Instala con: pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118")
    sys.exit(1)

# Verificar CUDA
print(f"\nCUDA disponible: {torch.cuda.is_available()}")

if torch.cuda.is_available():
    print(f"CUDA version: {torch.version.cuda}")
    print(f"Numero de GPUs: {torch.cuda.device_count()}")

    for i in range(torch.cuda.device_count()):
        print(f"\nGPU {i}: {torch.cuda.get_device_name(i)}")
        print(f"  Memoria total: {torch.cuda.get_device_properties(i).total_memory / 1024**3:.2f} GB")
        print(f"  Memoria libre: {torch.cuda.memory_reserved(i) / 1024**3:.2f} GB")

    # Test simple
    print("\nTest de GPU...")
    try:
        x = torch.randn(1000, 1000).cuda()
        y = torch.randn(1000, 1000).cuda()
        z = x @ y
        print("[OK] GPU funciona correctamente!")

        # Limpiar
        del x, y, z
        torch.cuda.empty_cache()

    except Exception as e:
        print(f"[ERROR] GPU no funciona: {e}")
else:
    print("\n[ADVERTENCIA] CUDA no esta disponible")
    print("Wav2Lip funcionara en CPU (mucho mas lento)")
    print("\nPara habilitar GPU:")
    print("1. Instala CUDA Toolkit 11.8 o superior")
    print("2. Reinstala PyTorch con soporte CUDA:")
    print("   pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118")

print("\n" + "=" * 70)

# Recomendaciones de batch size
if torch.cuda.is_available():
    vram_gb = torch.cuda.get_device_properties(0).total_memory / 1024**3

    print("RECOMENDACIONES DE BATCH SIZE PARA TU GPU:")
    print("=" * 70)

    if vram_gb >= 12:
        print(f"\nTu GPU tiene {vram_gb:.1f} GB VRAM (RTX 3060)")
        print("Batch sizes recomendados:")
        print("  - Rapido (recomendado):   batch_size=128")
        print("  - Balanceado:             batch_size=64")
        print("  - Conservador:            batch_size=32")
        print("\nTiempo estimado de generacion: 1-3 segundos")
    elif vram_gb >= 8:
        print(f"\nTu GPU tiene {vram_gb:.1f} GB VRAM")
        print("Batch sizes recomendados:")
        print("  - Rapido:                 batch_size=64")
        print("  - Balanceado:             batch_size=32")
        print("  - Conservador:            batch_size=16")
    else:
        print(f"\nTu GPU tiene {vram_gb:.1f} GB VRAM")
        print("Batch sizes recomendados:")
        print("  - Rapido:                 batch_size=32")
        print("  - Balanceado:             batch_size=16")
        print("  - Conservador:            batch_size=8")

print("\n" + "=" * 70)
