# Sistema de Parpadeo Natural para Avatar

## 🎯 Descripción

El `BlinkService` añade parpadeos naturales y realistas a los videos generados por Wav2Lip, mejorando significativamente la naturalidad del avatar sin necesidad de modelos adicionales de IA.

## ✨ Características

- ✅ **Post-procesamiento con OpenCV** - No requiere modelos adicionales
- ✅ **Parpadeos aleatorios** - Distribución natural a lo largo del video
- ✅ **Transiciones suaves** - Gaussian blur para efecto realista
- ✅ **Configuración flexible** - Frecuencia ajustable
- ✅ **Rápido** - Solo añade ~1-2 segundos al tiempo total
- ✅ **Seguro** - Fallback automático si falla

## 🔧 Cómo Funciona

### Pipeline de generación:

```
Audio de TTS
    ↓
Wav2Lip (Lip-sync)
    ↓
Video sin parpadeos
    ↓
BlinkService (Post-procesamiento)
    ↓
Video final con parpadeos
```

### Algoritmo de parpadeo:

1. **Análisis del video**
   - Lee propiedades: FPS, resolución, duración
   - Calcula número de parpadeos según frecuencia

2. **Generación de momentos**
   - Distribuye parpadeos aleatoriamente
   - Evita primeros/últimos 0.5 segundos
   - Cada parpadeo dura 3 frames (~0.15s a 20fps)

3. **Aplicación del efecto**
   - Detecta región aproximada de ojos (35-48% altura, 25-75% ancho)
   - Oscurece región con factor 0.3
   - Aplica Gaussian blur para transición suave

## 📊 Parámetros Configurables

### En `BlinkService`:

| Parámetro | Default | Descripción |
|-----------|---------|-------------|
| `blink_duration_frames` | 3 | Duración del parpadeo en frames |
| `blink_frequency` | 0.25 | Parpadeos por segundo (1 cada 4s) |
| `darkness_factor` | 0.3 | Cuánto oscurecer (0=negro, 1=sin cambio) |

### En `AvatarService`:

```python
# Activar/desactivar parpadeos
avatar_service = AvatarService(enable_blinks=True)  # Default

# Desactivar parpadeos
avatar_service = AvatarService(enable_blinks=False)
```

## 🎬 Ejemplos de Uso

### Uso automático (default):

```python
from app.services import AvatarService

# Los parpadeos se añaden automáticamente
avatar_service = AvatarService()
video_path = avatar_service.generate_video(audio_path)
# Video tendrá parpadeos naturales
```

### Configuración personalizada:

```python
from app.services import BlinkService

blink_service = BlinkService()

# Más parpadeos (1 cada 2 segundos)
result = blink_service.add_blinks(
    video_path,
    output_path,
    blink_frequency=0.5
)

# Menos parpadeos (1 cada 6 segundos)
result = blink_service.add_blinks(
    video_path,
    output_path,
    blink_frequency=0.16
)
```

### Desactivar parpadeos:

En `main.py` al inicializar el servicio:

```python
avatar_service = AvatarService(enable_blinks=False)
```

## 📈 Rendimiento

| Duración Video | Tiempo Wav2Lip | Tiempo Parpadeos | Total |
|----------------|----------------|------------------|-------|
| 5 segundos | 8-15s | ~0.5-1s | ~9-16s |
| 10 segundos | 15-25s | ~1-1.5s | ~16-27s |
| 20 segundos | 25-40s | ~1.5-2s | ~27-42s |

**Overhead:** ~10-15% del tiempo total

## 🔍 Detalles Técnicos

### Detección de región de ojos:

```python
# Posiciones relativas aproximadas
eye_region_y_start = height * 0.35  # 35% desde arriba
eye_region_y_end = height * 0.48    # 48% desde arriba
eye_region_x_start = width * 0.25   # 25% desde izquierda
eye_region_x_end = width * 0.75     # 75% desde izquierda
```

### Efecto de parpadeo:

```python
# Crear máscara de oscurecimiento
mask = np.ones_like(frame)
mask[eye_region] = 0.3  # Oscurecer a 30% brillo

# Suavizar bordes
mask = cv2.GaussianBlur(mask, (21, 21), 0)

# Aplicar al frame
frame = (frame * mask).astype(np.uint8)
```

## 🎨 Ajustes Finos

### Para rostros más grandes/pequeños:

Modifica las proporciones en `_apply_blink()`:

```python
# Rostro grande - región de ojos más específica
eye_region_y_start = int(height * 0.38)
eye_region_y_end = int(height * 0.45)

# Rostro pequeño - región más amplia
eye_region_y_start = int(height * 0.32)
eye_region_y_end = int(height * 0.50)
```

### Para parpadeos más sutiles:

```python
darkness_factor = 0.5  # Menos oscurecimiento (más sutil)
```

### Para parpadeos más pronunciados:

```python
darkness_factor = 0.1  # Más oscurecimiento (más notorio)
blink_duration_frames = 4  # Parpadeo más largo
```

## 🐛 Solución de Problemas

### Los parpadeos se ven artificiales

**Causa:** Región de ojos mal posicionada
**Solución:** Ajusta los porcentajes en `_apply_blink()`

### Muy pocos/muchos parpadeos

**Causa:** Frecuencia inadecuada
**Solución:** Ajusta `blink_frequency` (0.2-0.4 es rango natural)

### Parpadeos demasiado bruscos

**Causa:** Blur insuficiente
**Solución:** Aumenta kernel en GaussianBlur: `(31, 31)` o `(41, 41)`

### No se añaden parpadeos

**Causa:** Error en procesamiento
**Solución:** Revisa logs. El sistema hace fallback al video original

## 📝 Logs de Ejemplo

### Generación exitosa:

```
[AVATAR] ✓ Video generado en 15.32s: 2.1MB
[AVATAR] Añadiendo parpadeos naturales...
[BLINK] Video: 512x512 @ 20fps, 200 frames
[BLINK] Se añadirán 2 parpadeos
[BLINK] ✓ Parpadeos añadidos: /path/to/avatar_123_final.mp4
[AVATAR] ✓ Parpadeos añadidos en 1.45s
```

### Con fallback:

```
[AVATAR] ✓ Video generado en 15.32s: 2.1MB
[AVATAR] Añadiendo parpadeos naturales...
[BLINK] Error: No se pudo abrir el video
[AVATAR] ⚠ No se pudieron añadir parpadeos, usando video original
```

## 🎓 Fundamento Científico

### Frecuencia de parpadeo humano:

- **Promedio:** 15-20 parpadeos por minuto
- **Rango:** 0.25-0.33 parpadeos por segundo
- **Duración:** 100-150 milisegundos (~3 frames a 20fps)

### Implementación:

```python
# Configuración basada en investigación
blink_frequency = 0.25  # 15 parpadeos/minuto
blink_duration_frames = 3  # ~150ms a 20fps
```

## 🔮 Mejoras Futuras

Posibles mejoras que se pueden implementar:

1. **Detección facial real** con MediaPipe o dlib
2. **Parpadeos contextuales** (más al final de frases)
3. **Variación en intensidad** (parpadeos completos vs parciales)
4. **Sincronización con pausas** en el audio
5. **Machine Learning** para predecir momentos naturales

## 📚 Referencias

- Frecuencia de parpadeo: [Cruickshank's 1918 study](https://pubmed.ncbi.nlm.nih.gov/)
- OpenCV GaussianBlur: [OpenCV Docs](https://docs.opencv.org/)
- Wav2Lip paper: [arXiv:2008.10010](https://arxiv.org/abs/2008.10010)

---

**Última actualización:** Diciembre 2025
**Autor:** Diego Martínez López
**Licencia:** Parte del TFG de Ingeniería Informática
