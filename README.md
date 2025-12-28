# 🏥 Asistente Médico Virtual con IA

> **Trabajo de Fin de Grado** - Ingeniería Informática
> **Autor:** Diego Martínez López
> **Universidad:** [Nombre de tu Universidad]
> **Curso:** 2024/2025

Asistente médico virtual inteligente especializado en enfermedades respiratorias, que combina **procesamiento de lenguaje natural (LLM)**, **recuperación aumentada por generación (RAG)**, **síntesis de voz (TTS)** y **generación de avatar animado** para proporcionar una experiencia interactiva y educativa.

---

## 📋 Tabla de Contenidos

- [Características](#-características)
- [Arquitectura](#-arquitectura)
- [Tecnologías Utilizadas](#-tecnologías-utilizadas)
- [Estructura del Proyecto](#-estructura-del-proyecto)
- [Requisitos Previos](#-requisitos-previos)
- [Instalación](#-instalación)
- [Uso](#-uso)
- [Configuración](#-configuración)
- [Licencia](#-licencia)

---

## ✨ Características

- 🤖 **LLM con RAG**: Respuestas basadas en conocimiento médico verificado usando Ollama + ChromaDB
- 🎙️ **Síntesis de Voz**: Generación de audio natural en español con Piper TTS
- 🎭 **Avatar Animado**: Sincronización labial realista usando Wav2Lip v2
- 💬 **Interfaz Moderna**: Frontend React con diseño responsive y accesible
- 🔒 **Información Confiable**: Base de datos vectorial con información médica verificada
- ⚡ **Tiempo Real**: Generación de respuestas, audio y video en 2-5 segundos

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
   - Instalar el modelo:
     ```bash
     ollama pull llama3.2
     ollama pull all-minilm:22m
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
EMBEDDING_MODEL=all-minilm:22m

# Rutas
DATABASE_LOCATION=./chunks
PIPER_VOICE_DIR=./voices/piper
PIPER_VOICE_ID=es_MX-claude-high
AVATAR_IMAGE=./avatar_doctor.png

# Directorios de salida
TTS_OUTPUT_DIR=./backend/tts_out
VIDEO_OUTPUT_DIR=./backend/videos_out

# CORS (Frontend)
CORS_ORIGINS=http://localhost:5173,http://localhost:3000
```

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

1. Abre http://localhost:5173 en tu navegador
2. Escribe una pregunta sobre enfermedades respiratorias
3. Marca/desmarca las opciones de audio y video según prefieras
4. Espera 2-5 segundos para la respuesta completa

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
- Generación de texto (LLM): ~1-2 segundos
- Generación de audio (TTS): ~0.5-1 segundo
- Generación de video (Wav2Lip): ~2-4 segundos
- **Total:** ~4-7 segundos por respuesta completa

---

## 🐛 Solución de Problemas

### Error: "Ollama no disponible"
- Asegúrate de que Ollama esté corriendo: `ollama serve`
- Verifica que los modelos estén instalados: `ollama list`

### Error: "CUDA out of memory"
- Reduce el `batch_size` en `avatar_service.py`
- Cierra otras aplicaciones que usen la GPU

### Error: "No se encuentra el avatar"
- Verifica que `avatar_doctor.png` exista en la raíz y en `frontend/public/`

### El video no se genera
- Verifica que Wav2Lip esté correctamente instalado
- Verifica que el checkpoint `wav2lip_gan.pth` exista

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
- Mi tutor/a de TFG por la orientación y apoyo

---

## 📧 Contacto

**Diego Martínez López**
- GitHub: [@dieguitoml](https://github.com/dieguitoml)
- Email: [tu-email@ejemplo.com]

---

<div align="center">
  <p>Desarrollado con ❤️ como parte del TFG de Ingeniería Informática</p>
  <p>© 2025 Diego Martínez López</p>
</div>
