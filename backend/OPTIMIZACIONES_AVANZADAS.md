# Optimizaciones Avanzadas - Reducir Tiempo de Generación

## Análisis del Rendimiento Actual

Tu aplicación tarda ~40 segundos por video. Desglose:
- **LLM (Ollama)**: ~5-10s
- **TTS (Piper)**: ~1-2s
- **Wav2Lip**: **~35-40s** ← CUELLO DE BOTELLA

## Por qué Wav2Lip tarda tanto

1. **Audios largos**: 3-4 MB = 30-40 segundos de habla
2. **FPS alto**: 25 fps para 30s de audio = 750 frames a procesar
3. **Resolución**: PNG de entrada puede ser grande

---

## 🚀 Optimización 1: Reducir FPS (MÁS IMPACTO)

**Cambio**: FPS 25 → 20 (20% más rápido)

Edita `app2v2.py` línea 240:

```python
fps=20  # Antes: 25
```

**Resultado esperado**: ~32 segundos (ahorro de 8s)

---

## 🚀 Optimización 2: Reducir Resolución de Avatar

Si tu `avatar_doctor.png` es muy grande (>1920x1080), redúcelo:

### Usando Python:
```python
from PIL import Image

img = Image.open("avatar_doctor.png")
# Reducir a 720p
img = img.resize((1280, 720), Image.Resampling.LANCZOS)
img.save("avatar_doctor_720p.png")
```

Luego edita `.env`:
```
AVATAR_IMAGE=avatar_doctor_720p.png
```

**Resultado esperado**: ~25-30 segundos (ahorro de 10-15s)

---

## 🚀 Optimización 3: Limitar Longitud de Respuestas

Las respuestas del LLM son muy largas. Acortar = menos audio = menos frames.

Edita `app2v2.py` línea 70-76:

```python
SystemMessage(content=(
    "Eres un asistente médico experto en enfermedades respiratorias.\n"
    "Tu objetivo es ayudar a los usuarios a entender síntomas, causas y tratamientos.\n"
    "- Usa la herramienta 'retrieve' para información médica.\n"
    "- No inventes respuestas.\n"
    "- Cita las fuentes: Fuente: nombre_archivo.txt\n"
    "- Responde en español claro y profesional.\n"
    "- IMPORTANTE: Sé CONCISO. Respuestas de máximo 3-4 frases."  # ← NUEVO
)),
```

**Resultado esperado**: ~15-20 segundos (ahorro de 20-25s)

---

## 🚀 Optimización 4: Aumentar Batch Size (Solo si tienes más VRAM libre)

Si no hay problemas de memoria, prueba `batch_size=64`:

```python
batch_size=64  # Antes: 32
```

⚠️ **PRECAUCIÓN**: Puede causar Out of Memory en tu RTX 3060 Laptop (6GB).

Monitorea con `nvidia-smi` mientras pruebas.

**Resultado esperado**: ~25-30 segundos (ahorro de 10s)

---

## 🚀 Optimización 5: Procesamiento Asíncrono (Avanzado)

Actualmente todo es secuencial:
1. LLM → 2. TTS → 3. Wav2Lip

Podrías iniciar Wav2Lip mientras TTS aún está generando (requiere refactorización).

**NO RECOMENDADO** sin experiencia en async/threading.

---

## 📊 Comparativa de Optimizaciones

| Optimización | Dificultad | Ahorro | Tiempo Final |
|--------------|------------|--------|--------------|
| **Ninguna** | - | - | ~40s |
| FPS 20 | Fácil | ~8s | ~32s |
| Resolución 720p | Fácil | ~10-15s | ~25-30s |
| Respuestas cortas | Fácil | ~20-25s | **~15-20s** ⭐ |
| Batch 64 | Media | ~10s | ~30s |
| **Todas combinadas** | - | **~30s** | **~10s** 🚀 |

---

## 🎯 Recomendación

**Para mejor experiencia de usuario**:

1. ✅ Reducir FPS a 20
2. ✅ Respuestas concisas (máx 3-4 frases)
3. ✅ Reducir avatar a 720p

Con estos 3 cambios → **~15-20 segundos** por video (60% más rápido)

---

## 🔧 Script de Aplicación Rápida

Crea `optimize_avatar.py`:

```python
from PIL import Image

img = Image.open("avatar_doctor.png")
print(f"Tamaño original: {img.size}")

# Reducir a 720p
img_720 = img.resize((1280, 720), Image.Resampling.LANCZOS)
img_720.save("avatar_doctor_720p.png")
print(f"Tamaño optimizado: {img_720.size}")
print("Guardado como: avatar_doctor_720p.png")

# Actualizar .env
with open(".env", "r") as f:
    env_content = f.read()

if "AVATAR_IMAGE" in env_content:
    env_content = env_content.replace(
        'AVATAR_IMAGE=avatar_doctor.png',
        'AVATAR_IMAGE=avatar_doctor_720p.png'
    )
else:
    env_content += "\nAVATAR_IMAGE=avatar_doctor_720p.png\n"

with open(".env", "w") as f:
    f.write(env_content)

print("✓ .env actualizado")
```

Ejecuta:
```bash
pip install Pillow
python optimize_avatar.py
```

---

## ⚠️ Nota sobre el Tiempo

**40 segundos NO es malo** para un sistema completo con:
- RAG + LLM
- TTS realista
- Lip-sync con IA

Sistemas comerciales similares (D-ID, Synthesia) también tardan 20-40s.

Si necesitas respuestas **instantáneas**, considera:
- Usar solo TTS (sin video)
- Pre-generar respuestas comunes
- Usar avatares 2D más simples (FaceAnime, Live2D)
