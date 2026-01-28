# 🏥 Asistente Médico Virtual con IA

> **Trabajo de Fin de Grado** - Ingeniería Informática
> **Autor:** Diego Martínez López
> **Universidad:** Universidad Complutense de Madrid
> **Curso:** 2024/2025

Asistente médico virtual inteligente especializado en enfermedades respiratorias, que combina **procesamiento de lenguaje natural (LLM)**, **recuperación aumentada por generación (RAG)**, **síntesis de voz (TTS)** y **generación de avatar animado** para proporcionar una experiencia interactiva y educativa.

Demo: https://youtu.be/OeTmN7iEAes

---

## 📋 Tabla de Contenidos

- [Características](#-características)
- [Arquitectura](#-arquitectura)
- [Tecnologías Utilizadas](#-tecnologías-utilizadas)
- [Estructura del Proyecto](#-estructura-del-proyecto)
- [Requisitos Previos](#-requisitos-previos)
- [Instalación](#-instalación)
- [Configuración](#-configuración)
- [Dataset de Enfermedades Respiratorias](#-dataset-de-enfermedades-respiratorias)
- [Sistema de Parpadeos Naturales](#-sistema-de-parpadeos-naturales)
- [Optimizaciones de Wav2Lip](#-optimizaciones-de-wav2lip)
- [Sistema de Reconocimiento de Voz (STT)](#-sistema-de-reconocimiento-de-voz-stt)
- [Uso](#-uso)
- [Endpoints de la API](#-endpoints-de-la-api)
- [Rendimiento](#-rendimiento)
- [Scripts y Pruebas](#-scripts-y-pruebas)
- [Solución de Problemas](#-solución-de-problemas)
- [Licencia](#-licencia)

---

## ✨ Características

- 🤖 **LLM con RAG**: Respuestas basadas en conocimiento médico verificado usando Ollama + ChromaDB
- 🧠 **Embeddings de Alta Calidad**: nomic-embed-text (8192 tokens, 768 dims) para mejor retrieval
- 📚 **Dataset Completo**: 20 enfermedades respiratorias (1500-2400 caracteres cada una)
- 🎤 **Reconocimiento de Voz (STT)**: Entrada por voz usando Web Speech API
- 🎙️ **Síntesis de Voz (TTS)**: Generación de audio natural en español con Piper TTS
- 🎭 **Avatar Animado**: Sincronización labial realista con Wav2Lip v2 + sistema de parpadeos naturales
- 💬 **Interfaz Moderna**: Frontend React con diseño responsive y accesible
- 🔒 **Información Confiable**: Base de datos vectorial con información médica verificada
- ⚡ **Tiempo Real**: Generación de respuestas, audio y video en 8-12 segundos

---

## 🏗️ Arquitectura

```
┌─────────────────────────────────────────────────────────────┐
│                     Frontend (React + TS)                    │
│  - Interfaz de usuario                                       │
│  - Gestión de estado con hooks                               │
│  - Comunicación con API REST                                 │
└─────────────────┬───────────────────────────────────────────┘
                  │ HTTP/REST
┌─────────────────▼───────────────────────────────────────────┐
│                  Backend (FastAPI + Python)                  │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │ Chat Service │  │  TTS Service │  │Avatar Service│      │
│  │  (Ollama +   │  │    (Piper)   │  │  (Wav2Lip)   │      │
│  │   ChromaDB)  │  └──────────────┘  └──────────────┘      │
│  └──────────────┘                                            │
└──────────────────────────────────────────────────────────────┘
```

---

## 🛠️ Tecnologías Utilizadas

### Backend
- **Python 3.10+**
- **FastAPI** - Framework web moderno y rápido
- **Ollama** - Servidor LLM local (Llama 3.2)
- **LangChain** - Framework para aplicaciones con LLM
- **ChromaDB** - Base de datos vectorial para RAG
- **Piper TTS** - Síntesis de voz en español
- **Wav2Lip v2** - Generación de lip-sync

### Frontend
- **React 19** con TypeScript
- **Vite** - Build tool y dev server
- **Tailwind CSS** - Framework CSS utility-first
- **Lucide React** - Iconos
- **Axios** - Cliente HTTP
- **Web Speech API** - Reconocimiento de voz (STT)

### Infraestructura
- **CUDA** - Aceleración GPU (NVIDIA)
- **PyTorch** - Framework de deep learning

---

## 📁 Estructura del Proyecto

```
TFG_INFO/
│
├── backend/                           # Servidor FastAPI
│   ├── app/
│   │   ├── main.py                   # Punto de entrada de la API
│   │   ├── config.py                 # Configuración centralizada
│   │   ├── models.py                 # Modelos Pydantic
│   │   └── services/
│   │       ├── chat_service.py       # LLM + RAG con Ollama
│   │       ├── tts_service.py        # Generación de audio con Piper
│   │       └── avatar_service.py     # Generación de video con Wav2Lip
│   │
│   ├── dataset_respiratorio_es/      # Dataset médico en español
│   ├── gfpgan/weights/               # Pesos para mejora facial
│   ├── requirements.txt              # Dependencias Python
│   └── venv/                         # Entorno virtual Python
│
├── frontend/                          # Aplicación React
│   ├── src/
│   │   ├── components/               # Componentes React
│   │   │   ├── Avatar.tsx           # Visualización del avatar
│   │   │   ├── ChatInput.tsx        # Input con opciones TTS/Avatar
│   │   │   ├── ChatMessage.tsx      # Burbuja de mensaje
│   │   │   └── LoadingIndicator.tsx # Indicador de carga
│   │   ├── hooks/
│   │   │   └── useChat.ts           # Hook para gestión del chat
│   │   ├── api/
│   │   │   └── client.ts            # Cliente HTTP (Axios)
│   │   ├── types/
│   │   │   └── chat.ts              # Tipos TypeScript
│   │   └── App.tsx                  # Componente principal
│   │
│   ├── public/
│   │   └── avatar_doctor.png        # Imagen del avatar médico
│   ├── package.json                 # Dependencias Node.js
│   └── vite.config.ts               # Configuración de Vite
│
├── Wav2Lipv2/                        # Módulo Wav2Lip (submódulo git)
├── chunks/                           # Base de datos vectorial ChromaDB
├── voices/                           # Modelos de voz Piper
├── avatar_doctor.png                # Avatar médico estático
├── .gitignore                       # Archivos ignorados por Git
└── README.md                        # Este archivo
```

---

## 🔧 Requisitos Previos

### Software Necesario

1. **Python 3.10 o superior**
   ```bash
   python --version
   ```

2. **Node.js 18 o superior + npm**
   ```bash
   node --version
   npm --version
   ```

3. **Ollama** (Servidor LLM local)
   - Descargar desde: https://ollama.com
   - Instalar los modelos:
     ```bash
     ollama pull llama3.2
     ollama pull nomic-embed-text
     ```

4. **CUDA Toolkit** (Opcional, para aceleración GPU)
   - Solo si tienes GPU NVIDIA
   - Descargar desde: https://developer.nvidia.com/cuda-downloads

5. **Piper TTS**
   - Se instala automáticamente con `pip install piper-tts`
   - Modelos de voz se descargan automáticamente al primer uso

6. **Wav2Lip v2**
   - Clonar el repositorio:
     ```bash
     git clone https://github.com/Rudrabha/Wav2Lip.git Wav2Lipv2
     ```
   - Descargar checkpoint `wav2lip_gan.pth`:
     - Desde: https://github.com/Rudrabha/Wav2Lip
     - Colocar en: `Wav2Lipv2/checkpoints/wav2lip_gan.pth`

7. **GFPGAN Weights** (Opcional, para mejora facial)
   - Ver instrucciones en: `backend/gfpgan/weights/README.md`

### Hardware Recomendado

- **CPU:** Intel Core i5/AMD Ryzen 5 o superior
- **RAM:** 16 GB mínimo (32 GB recomendado)
- **GPU:** NVIDIA RTX 3060 o superior (6GB VRAM mínimo)
- **Almacenamiento:** 20 GB de espacio libre

---

## 📥 Instalación

### 1. Clonar el repositorio

```bash
git clone https://github.com/dieguitoml/MedicalAssistant.git
cd MedicalAssistant
```

### 2. Configurar el Backend

```bash
cd backend

# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
# En Windows:
venv\Scripts\activate
# En Linux/Mac:
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt

# Descargar modelo de spaCy para análisis de parpadeos
python -m spacy download es_core_news_sm

# Generar base de datos ChromaDB
python ChromaDB.py

# Verificar que el retrieval funciona correctamente
python test_retrieval.py

# Volver a la raíz del proyecto
cd ..
```

### 3. Configurar el Frontend

```bash
cd frontend

# Instalar dependencias
npm install

# Volver a la raíz del proyecto
cd ..
```

### 4. Configurar Variables de Entorno (Opcional)

Crear un archivo `.env` en la raíz del proyecto:

```env
# Modelos
CHAT_MODEL=llama3.2
EMBEDDING_MODEL=nomic-embed-text

# Rutas
DATABASE_LOCATION=./chunks
PIPER_VOICE_DIR=./voices/piper
PIPER_VOICE_ID=es_MX-claude-high
AVATAR_IMAGE=./avatar_doctor.png
WAV2LIP_DIR=./Wav2Lipv2

# Directorios de salida
TTS_OUTPUT_DIR=./backend/tts_out
VIDEO_OUTPUT_DIR=./backend/videos_out

# CORS (Frontend)
CORS_ORIGINS=http://localhost:5173,http://localhost:3000
```

---

## 📚 Dataset de Enfermedades Respiratorias

El sistema incluye 20 archivos en español con información médica verificada sobre enfermedades respiratorias (ubicados en `backend/dataset_respiratorio_es/`). Cada archivo contiene entre 1500-2400 caracteres en formato Markdown.

### Infecciones Respiratorias Agudas
- **covid19.txt** - COVID-19 y sus variantes
- **gripe.txt** - Influenza (con información sobre vacunación)
- **neumonia.txt** - Neumonía bacteriana y viral
- **tos_ferina.txt** - Tos ferina (pertussis)
- **difteria.txt** - Difteria

### Vías Respiratorias Superiores
- **faringitis.txt** - Faringitis aguda y crónica
- **laringitis.txt** - Laringitis aguda y crónica
- **epiglotitis.txt** - Epiglotitis (emergencia médica)
- **sinusitis.txt** - Sinusitis aguda y crónica

### Enfermedades Obstructivas Crónicas
- **asma.txt** - Asma bronquial
- **enfermedad_pulmonar_obstructiva_cronica.txt** - EPOC
- **bronquitis_cronica.txt** - Bronquitis crónica

### Enfermedades Estructurales
- **fibrosis_pulmonar.txt** - Fibrosis pulmonar idiopática
- **fibrosis_quistica.txt** - Fibrosis quística
- **bronquiectasia.txt** - Bronquiectasias

### Enfermedades Ocupacionales e Inflamatorias
- **neumoconiosis.txt** - Neumoconiosis (silicosis, asbestosis)
- **sarcoidosis.txt** - Sarcoidosis (incluye síndrome de Löfgren)
- **tuberculosis.txt** - Tuberculosis

### Cáncer
- **cancer_de_torax.txt** - Cáncer de pulmón
- **cancer_de_faringe_laringe.txt** - Cáncer de faringe y laringe

### Configuración de ChromaDB

**Archivo:** `backend/ChromaDB.py`

```python
# Modelo de embeddings
EMBEDDING_MODEL = "nomic-embed-text"  # 8192 tokens, 768 dimensiones

# Configuración de chunks
splitter = MarkdownTextSplitter(
    chunk_size=1000,      # Caracteres por chunk
    chunk_overlap=200     # Solapamiento entre chunks
)
```

**Ventajas de nomic-embed-text:**
- Límite de 8192 tokens (vs 512 de all-minilm:22m)
- Alta calidad de embeddings (768 dimensiones)
- Permite chunks grandes para mejor contexto
- Sin errores de "chunk demasiado largo"

---

## 🎬 Sistema de Parpadeos Naturales

El avatar incluye un sistema avanzado de parpadeos que simula comportamiento humano natural:

### Características
- **Frecuencia natural**: 15-20 parpadeos por minuto
- **Detección facial**: MediaPipe Face Mesh para ubicación precisa de ojos
- **Análisis de texto**: spaCy para detectar pausas naturales
- **Sincronización inteligente**: Parpadeos en puntos de puntuación y pausas
- **Variación realista**: Distribución gamma para tiempos entre parpadeos

### Implementación

**Archivo:** `backend/app/services/avatar_service.py`

```python
def generate_blinks(video, text):
    # Detecta rostros con MediaPipe
    # Analiza texto con spaCy para encontrar pausas
    # Genera parpadeos en momentos naturales
    # Fusiona frames de parpadeo con el video original
```

**Dependencias:**
```bash
pip install mediapipe spacy
python -m spacy download es_core_news_sm
```

---

## ⚙️ Optimizaciones de Wav2Lip

### Parámetros Optimizados

**Archivo:** `Wav2Lipv2/inference.py`

```python
# Sin padding innecesario
parser.add_argument('--pads', nargs='+', type=int, default=[0, 0, 0, 0])

# FPS óptimo para fluidez
parser.add_argument('--fps', type=float, default=25.)

# Sin redimensionamiento agresivo
parser.add_argument('--resize_factor', default=1, type=int)

# Sin suavizado para mayor nitidez
parser.add_argument('--nosmooth', action='store_true')
```

**Beneficios:**
- Mayor nitidez en el video final
- Mejor sincronización labial
- Procesamiento más rápido
- Sin artefactos de suavizado

---

## 🎤 Sistema de Reconocimiento de Voz (STT)

El frontend incluye reconocimiento de voz para entrada manos libres usando la Web Speech API del navegador.

### Características
- **Reconocimiento en tiempo real**: Transcripción continua mientras hablas
- **Idioma español**: Configurado para `es-ES`
- **Resultados intermedios**: Muestra la transcripción mientras hablas
- **Detección automática**: Detecta cuándo empiezas y terminas de hablar
- **Interfaz visual**: Botón de micrófono con animación cuando está grabando

### Implementación

**Archivo:** `frontend/src/components/ChatInput.tsx`

```typescript
// Inicialización Web Speech API
const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition
const recognition = new SpeechRecognition()
recognition.lang = 'es-ES'
recognition.continuous = true
recognition.interimResults = true

// Manejo de resultados
recognition.onresult = (event) => {
  const transcript = event.results[lastResultIndex][0].transcript
  setInput(transcript)  // Actualiza el campo de texto
}
```

### Compatibilidad de Navegadores

| Navegador | Soporte |
|-----------|---------|
| Chrome | ✅ Completo |
| Edge | ✅ Completo |
| Safari | ✅ Completo (iOS 14.3+) |
| Firefox | ❌ No soportado |
| Opera | ✅ Completo |

**Nota:** Si el navegador no soporta Web Speech API, el botón de micrófono no aparecerá.

### Uso

1. Haz clic en el botón del micrófono (🎤)
2. Comienza a hablar tu consulta médica
3. El texto aparecerá en tiempo real en el campo de entrada
4. Haz clic de nuevo en el micrófono (ahora con ícono 🔇) para detener
5. Opcionalmente, edita el texto transcrito
6. Envía tu consulta normalmente

---

## 🚀 Uso

### 1. Iniciar Ollama

```bash
# Asegúrate de que Ollama esté corriendo
ollama serve
```

### 2. Iniciar el Backend

```bash
cd backend
venv\Scripts\activate  # En Windows
python -m app.main
```

El backend estará disponible en:
- API: http://localhost:8000
- Documentación: http://localhost:8000/docs

### 3. Iniciar el Frontend

En otra terminal:

```bash
cd frontend
npm run dev
```

El frontend estará disponible en: http://localhost:5173

### 4. Usar la Aplicación

1. Abre http://localhost:5173 en tu navegador (recomendado: Chrome o Edge para STT)
2. **Escribe** una pregunta sobre enfermedades respiratorias **o usa el botón del micrófono** para hablar
3. Marca/desmarca las opciones de audio y video según prefieras:
   - ✅ **Respuesta con audio**: El asistente responderá con voz
   - ✅ **Respuesta con video**: El asistente responderá con avatar animado
4. Envía tu consulta y espera la respuesta (1-12 segundos según opciones)

---

## ⚙️ Configuración

### Ajustar el Batch Size de Wav2Lip

Si tienes problemas de memoria GPU, ajusta el `batch_size` en:

**Archivo:** `backend/app/services/avatar_service.py`

```python
batch_size=48,  # RTX 3060 (6GB)
# batch_size=32,  # RTX 3050 (4GB)
# batch_size=16,  # GTX 1660 (6GB)
```

### Cambiar el Modelo LLM

En el archivo `.env` o `backend/app/config.py`:

```python
CHAT_MODEL = "llama3.2"  # Opciones: llama3.2, mistral, phi3, etc.
```

### Cambiar la Voz TTS

```python
PIPER_VOICE_ID = "es_MX-claude-high"  # Español México
# PIPER_VOICE_ID = "es_ES-davefx-medium"  # Español España
```

---

## 🎯 Endpoints de la API

### GET `/api/health`
Verificar estado de los servicios

### POST `/api/chat`
Enviar mensaje al asistente

**Request:**
```json
{
  "message": "¿Qué es el asma?",
  "use_tts": true,
  "use_avatar": true
}
```

**Response:**
```json
{
  "text": "El asma es una enfermedad...",
  "audio_url": "http://localhost:8000/static/audio/tts_12345.wav",
  "video_url": "http://localhost:8000/static/video/avatar_12345.mp4",
  "processing_time": 3.45
}
```

### GET `/api/chat/clear`
Limpiar historial de conversación

### GET `/api/chat/examples`
Obtener preguntas de ejemplo

---

## 📊 Rendimiento

Con una **RTX 3060 Laptop (6GB VRAM)**:
- **Solo texto:** ~1-2 segundos
  - RAG retrieval: ~0.3-0.5s
  - Generación LLM: ~0.7-1.5s
- **Texto + TTS:** ~3-5 segundos
  - + Síntesis de voz: ~2-3s
- **Texto + TTS + Avatar:** ~8-12 segundos
  - + Wav2Lip inference: ~4-6s
  - + Sistema de parpadeos: ~1-2s

**Nota:** Los tiempos varían según la longitud de la respuesta y la carga del sistema.

---

## 🧪 Scripts y Pruebas

### ChromaDB.py
**Ubicación:** `backend/ChromaDB.py`

Genera la base de datos vectorial a partir del dataset de enfermedades respiratorias.

```bash
cd backend
python ChromaDB.py
```

**Salida esperada:**
```
Procesando asma.txt...
   ✅ 4 chunks procesados
Procesando neumonia.txt...
   ✅ 3 chunks procesados
...
✅ Base de datos creada exitosamente en ./chunks
```

### test_retrieval.py
**Ubicación:** `backend/test_retrieval.py`

Verifica que el sistema RAG esté funcionando correctamente.

```bash
cd backend
python test_retrieval.py
```

**Salida esperada:**
```
🔍 Query: ¿Cuáles son los síntomas del asma?
📄 Resultado 1 (score: 0.85): asma.txt
   ## Síntomas del Asma
   - Dificultad para respirar
   - Sibilancias (silbidos al respirar)
   ...

🔍 Query: ¿Cómo se trata la neumonía?
📄 Resultado 1 (score: 0.82): neumonia.txt
   ...
```

### Estructura de Archivos de Salida

```
backend/
├── tts_out/              # Archivos de audio generados
│   └── audio_*.wav
├── videos_out/           # Videos de avatar generados
│   └── video_*.mp4
└── chunks/               # Base de datos ChromaDB
    └── chroma.sqlite3
```

---

## 🐛 Solución de Problemas

### Error: "Chunk X/Y demasiado largo, omitido"

**Causa:** El modelo de embeddings tiene un límite de tokens muy pequeño (512 tokens en all-minilm:22m).

**Solución:**
```bash
# 1. Descargar modelo con mayor límite de tokens
ollama pull nomic-embed-text

# 2. Actualizar backend/app/config.py
EMBEDDING_MODEL = "nomic-embed-text"

# 3. Regenerar la base de datos ChromaDB
cd backend
python ChromaDB.py

# 4. Verificar que funciona
python test_retrieval.py
```

### Error: "Ollama no disponible"
- Asegúrate de que Ollama esté corriendo: `ollama serve`
- Verifica que los modelos estén instalados: `ollama list`

### Error: "CUDA out of memory"
- Reduce el `batch_size` en `avatar_service.py`
- Cierra otras aplicaciones que usen la GPU
- Considera usar CPU para Wav2Lip (más lento pero funcional)

### Error: "No se encuentra el avatar"
- Verifica que `avatar_doctor.png` exista en la raíz del proyecto
- Verifica la ruta en `config.py`: `AVATAR_IMAGE`

### El video no se genera
- Verifica que Wav2Lip esté correctamente instalado
- Verifica que el checkpoint `wav2lip_gan.pth` exista en `Wav2Lipv2/checkpoints/`
- Revisa los logs del backend para errores específicos

### Parpadeos no aparecen en el video
- Verifica instalación de MediaPipe: `pip install mediapipe`
- Verifica instalación de spaCy: `pip install spacy`
- Descarga el modelo de spaCy: `python -m spacy download es_core_news_sm`
- Revisa que el servicio de avatar esté usando `generate_blinks()`

### El retrieval no encuentra información relevante
- Regenera ChromaDB: `python ChromaDB.py`
- Verifica que el modelo de embeddings sea el mismo en `ChromaDB.py` y `config.py`
- Prueba con `test_retrieval.py` para diagnosticar

### No aparece el botón del micrófono (STT)
- Verifica que estás usando Chrome, Edge, Safari u Opera (Firefox no soporta Web Speech API)
- Asegúrate de que el sitio se sirva por HTTPS o localhost (requerido por la API)
- Verifica permisos del micrófono en el navegador
- Comprueba la consola del navegador para ver errores de Web Speech API

### El reconocimiento de voz no funciona bien
- Habla claro y a un volumen normal
- Reduce ruido de fondo
- Asegúrate de que el micrófono esté configurado correctamente en el sistema
- En Chrome/Edge: Ve a Configuración → Privacidad y Seguridad → Configuración del sitio → Micrófono
- El idioma está configurado para español (es-ES)

---

## 📝 Licencia

Este proyecto es parte de un Trabajo de Fin de Grado y está disponible con fines educativos.

---

## ⚠️ Descargo de Responsabilidad

Este asistente médico virtual proporciona **información educativa únicamente** y **NO reemplaza la consulta con un profesional de la salud**. Siempre consulta con un médico cualificado para diagnósticos y tratamientos.

---

## 🙏 Agradecimientos

- **Ollama** - Por el servidor LLM local
- **LangChain** - Por el framework RAG
- **Piper TTS** - Por la síntesis de voz
- **Wav2Lip** - Por la tecnología de sincronización labial
- Mi tutor de TFG Rubén por la orientación y apoyo

---

## 📧 Contacto

**Diego Martínez López**
- GitHub: [@dieguitoml](https://github.com/dieguitoml)
- Email: diegma16@ucm.es

---

<div align="center">
  <p>Desarrollado con ❤️ como parte del TFG de Ingeniería Informática</p>
  <p>© 2025 Diego Martínez López</p>
</div>
