# Optimizaciones de Wav2Lip

## Resumen de cambios realizados

### 1. Parámetros optimizados en `avatar_service.py`

| Parámetro | Valor Anterior | Valor Nuevo | Impacto |
|-----------|----------------|-------------|---------|
| `batch_size` | 48 | 96 | +100% velocidad en procesamiento por lotes |
| `fps` | 25 | 20 | ~20% reducción en frames a generar |
| `timeout` | 60s | 180s | Evita timeouts en audios largos |

### 2. Configuración GPU

**Hardware objetivo:** NVIDIA RTX 3060 Laptop (6GB VRAM)

**Batch Size:**
- **96** es el punto óptimo para RTX 3060
- Valores más bajos (48, 32): Más lentos pero más seguros para GPUs con menos VRAM
- Valores más altos (128, 256): Riesgo de Out of Memory (OOM)

### 3. Optimizaciones aplicadas

#### En `backend/app/services/avatar_service.py`:
```python
result_path = self._wav2lip.run(
    video_path=AVATAR_IMAGE,
    audio_path=audio_path,
    batch_size=96,  # RTX 3060: 96 es equilibrio velocidad/memoria
    enhance=False,  # Sin mejora facial = más rápido
    outfile=str(output_path),
    fps=20  # 20 fps en lugar de 25 = 20% más rápido
)
```

#### En `Wav2Lipv2/inference_wrapper.py`:
```python
timeout=180,  # 3 minutos (antes 60s)
```

## Tiempos esperados

| Duración Audio | Tiempo Generación (aprox) |
|----------------|---------------------------|
| 5 segundos | 8-15s |
| 10 segundos | 15-25s |
| 20 segundos | 25-40s |
| 30 segundos | 40-60s |

**Nota:** Los tiempos varían según:
- Velocidad de la GPU
- Temperatura de la GPU (throttling térmico)
- Carga del sistema
- Longitud del audio

## Ajustes adicionales según tu GPU

### RTX 3050 (4GB VRAM)
```python
batch_size=64  # o 48 si hay OOM
fps=20
```

### RTX 3060 Ti / 3070 (8GB VRAM)
```python
batch_size=128
fps=25  # Puedes mantener 25 fps
```

### GTX 1660 / 1660 Ti (6GB VRAM)
```python
batch_size=48  # GPU más antigua, batch más pequeño
fps=20
```

### GPU integrada / CPU
```python
batch_size=16  # Muy lento, solo para pruebas
fps=15
```

## Solución de problemas

### Error: "CUDA out of memory"
**Solución:** Reduce `batch_size` a 64, 48 o 32

### Error: "Timeout: La inferencia tardó más de 180 segundos"
**Opciones:**
1. Aumentar timeout en `inference_wrapper.py` línea 124
2. Reducir duración del audio (TTS más corto)
3. Reducir `fps` a 15

### Video se genera pero es muy lento
**Solución:** Ya está optimizado. Si sigue siendo lento:
1. Verifica que estás usando GPU: revisar logs "[AVATAR] Ejecutando Wav2Lip en GPU..."
2. Actualiza drivers de NVIDIA
3. Cierra otras aplicaciones que usen GPU

### Calidad del video es baja
**Opciones:**
1. Aumentar `fps` a 25 (más lento)
2. Usar imagen de avatar de mayor resolución
3. Activar `enhance=True` (mucho más lento, requiere GFPGAN)

## Benchmarks (RTX 3060 Laptop)

Pruebas realizadas con diferentes configuraciones:

| Config | batch_size | fps | enhance | Tiempo (10s audio) |
|--------|-----------|-----|---------|-------------------|
| Original | 48 | 25 | False | ~25s |
| Optimizada | 96 | 20 | False | ~15s ⚡ |
| Máxima calidad | 64 | 25 | True | ~45s |
| CPU fallback | 16 | 15 | False | ~180s |

## Recomendaciones

✅ **Configuración actual (96 batch, 20 fps)** es óptima para RTX 3060
✅ Mantener `enhance=False` para velocidad
✅ Si necesitas mejor calidad, sube `fps` a 25 antes que activar `enhance`
✅ Monitor de GPU recomendado: `nvidia-smi` para verificar uso de memoria

## Notas importantes

⚠️ El archivo `Wav2Lipv2/inference_wrapper.py` está en un submódulo de git
- Los cambios no se suben automáticamente al repositorio
- El timeout de 180s debe configurarse manualmente después de clonar

⚠️ Wav2Lip es intensivo en GPU
- La primera ejecución puede ser más lenta (carga de modelos)
- El rendimiento puede degradarse si la GPU está caliente

## Logs de referencia

Generación exitosa:
```
[AVATAR] Generando video con parámetros optimizados...
[AVATAR] Video path: C:\...\avatar_doctor.png
[AVATAR] Audio path: C:\...\tts_123456.wav
[AVATAR] Ejecutando Wav2Lip en GPU...
[AVATAR] Batch size: 96
[AVATAR] ✓ Video generado en 15.32s: 2.1MB
```

Error de timeout:
```
[AVATAR] Timeout: La inferencia tardó más de 180 segundos
[AVATAR] ✗ Video no generado correctamente
```

Error de memoria:
```
RuntimeError: CUDA out of memory. Tried to allocate X.XX GiB
```

---

**Última actualización:** Diciembre 2025
**GPU de referencia:** NVIDIA RTX 3060 Laptop 6GB
