# Guía de Optimización Wav2Lip - RTX 3060 Laptop 6GB

## Configuración Actual (Recomendada)
```python
batch_size=32      # Óptimo para 6GB VRAM
fps=25             # Calidad estándar
enhance=False      # Velocidad sobre calidad
```

**Tiempo estimado**: 2-4 segundos por video

---

## Opciones de Optimización

### 1. MODO RÁPIDO (1-2 segundos)
```python
batch_size=32
fps=20             # Reducir FPS
enhance=False
```

### 2. MODO BALANCEADO (2-4 segundos) ⭐ ACTUAL
```python
batch_size=32
fps=25
enhance=False
```

### 3. MODO CALIDAD (5-8 segundos)
```python
batch_size=16      # Reducir batch para más estabilidad
fps=30             # Más frames
enhance=True       # Activar mejora de calidad (GAN)
```

### 4. MODO CONSERVADOR (si hay problemas de memoria)
```python
batch_size=8
fps=25
enhance=False
```

---

## Cómo Cambiar la Configuración

Edita `app2v2.py` en la línea 237:

```python
result_path = wav2lip.run(
    video_path=AVATAR_IMAGE,
    audio_path=audio_path,
    batch_size=32,     # ← Cambia aquí (8, 16, 32)
    enhance=False,     # ← Cambia a True para mejor calidad
    outfile=output_path,
    fps=25             # ← Cambia aquí (20, 25, 30)
)
```

---

## Troubleshooting

### Error: Out of Memory (OOM)
**Síntomas**: "CUDA out of memory"

**Solución**:
1. Reducir `batch_size` a 16 o 8
2. Cerrar otras aplicaciones que usen GPU
3. Reiniciar el sistema

### Generación Muy Lenta
**Posibles causas**:
1. GPU no detectada (verificar con `python test_gpu.py`)
2. Batch size muy bajo
3. Otros procesos usando GPU

**Solución**:
1. Verificar: `python test_gpu.py`
2. Aumentar `batch_size` gradualmente (8 → 16 → 32)
3. Cerrar juegos/software de edición

### Sincronización Labial Mala
**Solución**:
1. Aumentar calidad de audio (TTS)
2. Activar `enhance=True`
3. Reducir `batch_size` a 16

---

## Monitoreo de GPU

Mientras ejecutas la app, puedes monitorear la GPU:

### PowerShell:
```powershell
nvidia-smi -l 1
```

Esto muestra:
- Uso de VRAM
- Temperatura
- % Utilización

**Valores normales durante inferencia**:
- VRAM: 3-5 GB / 6 GB
- GPU Load: 80-100%
- Temperatura: 60-80°C

---

## Recomendaciones Finales

### Para tu RTX 3060 Laptop (6GB):
✅ **Recomendado**: `batch_size=32, fps=25, enhance=False`
- Buen balance velocidad/calidad
- Tiempo: 2-4 segundos
- VRAM: ~5 GB

🎯 **Para demos**: `batch_size=32, fps=20, enhance=False`
- Prioriza velocidad
- Tiempo: 1-2 segundos

🎨 **Para calidad**: `batch_size=16, fps=30, enhance=True`
- Mejor calidad visual
- Tiempo: 5-8 segundos
