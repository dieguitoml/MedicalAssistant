import os
import time
import gradio as gr
from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings, ChatOllama
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_core.tools import tool
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder

# =========================
# 1. CONFIG
# =========================
espeak_path = r"C:\Program Files (x86)\eSpeak"
if os.path.isdir(espeak_path) and espeak_path not in os.environ["PATH"]:
    print(f"Añadiendo eSpeak al PATH: {espeak_path}")
    os.environ["PATH"] = espeak_path + os.pathsep + os.environ["PATH"]

load_dotenv()

CHROMA_DIR = os.getenv("DATABASE_LOCATION", "./chunks")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "all-minilm:22m")
OLLAMA_MODEL = os.getenv("CHAT_MODEL", "llama3.2")
PIPER_DIR = os.getenv("PIPER_VOICE_DIR", os.path.join("voices", "piper"))
PIPER_VOICE_ID = os.getenv("PIPER_VOICE_ID", "es_MX-claude-high")
AVATAR_IMAGE = os.getenv("AVATAR_IMAGE", "avatar_doctor.png")
VIDEOS_DIR = os.getenv("VIDEOS_DIR", "videos_out")
WAV2LIP_DIR = "Wav2Lipv2"  # Directorio de Wav2Lip v2

os.makedirs(VIDEOS_DIR, exist_ok=True)

# =========================
# 2. CARGA EMBEDDINGS Y CHROMADB
# =========================
print("Cargando embeddings y vectorstore...")
embeddings = OllamaEmbeddings(model=EMBEDDING_MODEL)
vectorstore = Chroma(
    collection_name="respiratory_docs",
    embedding_function=embeddings,
    persist_directory=CHROMA_DIR,
)

# =========================
# 3. MODELO DE CHAT OLLAMA
# =========================
print("Cargando modelo de Ollama...")
llm = ChatOllama(model=OLLAMA_MODEL)

# =========================
# 4. TOOL DE RETRIEVAL
# =========================
@tool
def retrieve(query: str) -> str:
    """Recupera información médica relevante desde la base vectorial."""
    docs = vectorstore.similarity_search(query, k=3)
    if not docs:
        return "No se encontró información relevante en la base de datos médica."
    output = "\n=== Resultados de búsqueda ===\n"
    for doc in docs:
        source = doc.metadata.get("source", "desconocida")
        output += f"\nFuente: {source}\n{doc.page_content}\n"
    output += "\n=== Fin de resultados ===\n"
    return output

# =========================
# 5. PROMPT Y AGENTE
# =========================
prompt = ChatPromptTemplate.from_messages([
    SystemMessage(content=(
        "Eres un asistente médico experto en enfermedades respiratorias.\n"
        "Tu objetivo es ayudar a los usuarios a entender síntomas, causas y tratamientos de enfermedades respiratorias.\n"
        "-Si el usuario pregunta algo general como 'Hola' responde brevemente y luego indícale que puede hacer preguntas médicas relacionadas con enfermedades respiratorias.\n"
        "- Usa la herramienta 'retrieve' solo si la pregunta requiere información médica o factual.\n"
        "- Si la pregunta no es médica, no está en la base de datos o no es de caracter general como una conversación normal, responde 'No lo sé'.\n"
        "- No inventes respuestas.\n"
        "- Cuando uses información recuperada, resume y cita las fuentes en el formato:\n  Fuente: nombre_del_archivo.txt\n"
        "- Responde en español claro y profesional."
        "-Dados unos sintomas,responde unicamente con la informacion que tienes en tu base de datos, solo responde si es una enfermedad de tipo respiratoria."
    )),
    MessagesPlaceholder(variable_name="chat_history"),
    ("human", "{input}"),
    MessagesPlaceholder(variable_name="agent_scratchpad"),
])

tools = [retrieve]
agent = create_tool_calling_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

# =========================
# 6. TTS: PIPER
# =========================
_piper_voice = None

def _ensure_piper_voice():
    global _piper_voice
    if _piper_voice is not None:
        return _piper_voice
    
    try:
        from piper import PiperVoice
    except ImportError as e:
        raise RuntimeError("Instala piper-tts: pip install piper-tts") from e
    
    os.makedirs(PIPER_DIR, exist_ok=True)
    
    search_paths = [
        (os.path.join(PIPER_DIR, f"{PIPER_VOICE_ID}.onnx"), 
         os.path.join(PIPER_DIR, f"{PIPER_VOICE_ID}.onnx.json")),
        (os.path.join(PIPER_DIR, "es", f"{PIPER_VOICE_ID}.onnx"),
         os.path.join(PIPER_DIR, "es", f"{PIPER_VOICE_ID}.onnx.json")),
    ]
    
    onnx_path = json_path = None
    for onnx, json_file in search_paths:
        if os.path.exists(onnx) and os.path.exists(json_file):
            onnx_path, json_path = onnx, json_file
            break
    
    if not onnx_path:
        print(f"[TTS] Descargando modelo {PIPER_VOICE_ID}...")
        from huggingface_hub import hf_hub_download
        voice_paths = {
            "es_MX-claude-high": ("es/es_MX/claude/high", "es_MX-claude-high"),
            "es_ES-davefx-medium": ("es/es_ES/davefx/medium", "es_ES-davefx-medium"),
        }
        if PIPER_VOICE_ID not in voice_paths:
            raise ValueError(f"Voz no soportada: {PIPER_VOICE_ID}")
        
        voice_path, voice_name = voice_paths[PIPER_VOICE_ID]
        onnx_path = hf_hub_download("rhasspy/piper-voices", f"{voice_path}/{voice_name}.onnx", local_dir=PIPER_DIR)
        json_path = hf_hub_download("rhasspy/piper-voices", f"{voice_path}/{voice_name}.onnx.json", local_dir=PIPER_DIR)
    
    _piper_voice = PiperVoice.load(onnx_path, config_path=json_path)
    print(f"[TTS] Piper cargado: {_piper_voice.config.sample_rate} Hz")
    return _piper_voice

def tts_es(text: str):
    import wave
    out_dir = os.path.join(os.getcwd(), "tts_out")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, f"tts_{int(time.time()*1000)}.wav")
    
    try:
        voice = _ensure_piper_voice()
        text = text.replace('*', '').replace('_', '').replace('#', '')
        text = text.replace('\n\n', '. ').replace('\n', ', ')
        
        with wave.open(out_path, "wb") as wav_file:
            voice.synthesize_wav(text, wav_file)
        
        if os.path.exists(out_path) and os.path.getsize(out_path) > 44:
            print(f"[TTS] Audio: {out_path} ({os.path.getsize(out_path)} bytes)")
            return out_path
        return None
    except Exception as e:
        print(f"[TTS] Error: {e}")
        return None

# =========================
# 7. WAV2LIP V2 INTEGRATION
# =========================
_wav2lip_model = None

def _ensure_wav2lip():
    """Inicializa Wav2Lip v2."""
    global _wav2lip_model
    if _wav2lip_model is not None:
        return _wav2lip_model
    
    try:
        import sys
        wav2lip_path = os.path.join(os.getcwd(), WAV2LIP_DIR)
        
        if not os.path.exists(wav2lip_path):
            print(f"[AVATAR] ERROR: No se encuentra {WAV2LIP_DIR}/")
            print("[AVATAR] Clona: git clone https://github.com/your-repo/Wav2Lipv2.git")
            return None
        
        if wav2lip_path not in sys.path:
            sys.path.insert(0, wav2lip_path)
        
        print("[AVATAR] Cargando Wav2Lip v2...")

        # Importar el módulo Wav2Lipv2 (wrapper personalizado)
        from inference_wrapper import Wav2Lipv2
        
        checkpoint_path = os.path.join(wav2lip_path, 'checkpoints/wav2lip_gan.pth')
        weights_dir = os.path.join(wav2lip_path, 'checkpoints/weights')
        
        if not os.path.exists(checkpoint_path):
            print(f"[AVATAR] ERROR: No se encuentra {checkpoint_path}")
            print("[AVATAR] Descarga el checkpoint desde el repositorio")
            return None
        
        _wav2lip_model = Wav2Lipv2(
            checkpoint_path=checkpoint_path,
            pretrained_model_dir=weights_dir,
            pads=[0, 10, 0, 0],  # Padding para mejor encuadre
            audio_smooth=True,   # Suavizado de audio para mejor sincronización
            rotate=False         # No rotar la imagen del avatar
        )
        
        print("[AVATAR] ✓ Wav2Lip v2 cargado exitosamente")
        return _wav2lip_model
        
    except Exception as e:
        print(f"[AVATAR] Error cargando Wav2Lip v2: {e}")
        import traceback
        traceback.print_exc()
        return None

def generate_avatar_video(audio_path: str, text: str):
    """Genera video del avatar con lip-sync usando Wav2Lip v2 (RÁPIDO)."""
    
    if not os.path.exists(AVATAR_IMAGE):
        print(f"[AVATAR] Imagen no encontrada: {AVATAR_IMAGE}")
        return None
    
    if not os.path.exists(audio_path):
        print(f"[AVATAR] Audio no encontrado: {audio_path}")
        return None
    
    try:
        wav2lip = _ensure_wav2lip()
        if wav2lip is None:
            print("[AVATAR] Wav2Lip v2 no disponible, usando solo audio")
            return None
        
        print(f"[AVATAR] Generando video con lip-sync (2-5 segundos)...")
        start_time = time.time()
        
        # Generar nombre de salida
        output_path = os.path.join(VIDEOS_DIR, f"avatar_{int(time.time()*1000)}.mp4")
        
        # Ejecutar Wav2Lip v2 (Optimizado para RTX 3060 Laptop 6GB)
        result_path = wav2lip.run(
            video_path=AVATAR_IMAGE,  # Imagen estática del avatar
            audio_path=audio_path,
            batch_size=48,  # RTX 3060 Laptop (6GB): 32 es óptimo para evitar OOM
            enhance=False,  # False = más velocidad, True = mejor calidad (más lento)
            outfile=output_path,
            fps=25  # Puedes bajar a 20 para más velocidad
        )
        
        elapsed = time.time() - start_time

        if result_path and os.path.exists(result_path) and os.path.getsize(result_path) > 1000:
            print(f"[AVATAR] ✓ Video generado en {elapsed:.2f}s: {result_path}")
            return result_path
        else:
            print("[AVATAR] Error: Video no generado correctamente")
            return None
            
    except Exception as e:
        print(f"[AVATAR] Error generando video: {e}")
        print("[AVATAR] El sistema continuará funcionando solo con audio")
        import traceback
        traceback.print_exc()
        return None

# =========================
# 8. LÓGICA DE CHAT
# =========================
messages = []

def chat_fn(message, history, use_tts):
    global messages
    
    # Reconstruir historial
    temp_messages = []
    for msg in history:
        if isinstance(msg, dict):
            if msg.get("role") == "user":
                temp_messages.append(HumanMessage(content=msg["content"]))
            elif msg.get("role") == "assistant":
                temp_messages.append(AIMessage(content=msg["content"]))
    
    messages = temp_messages
    messages.append(HumanMessage(content=message))
    
    try:
        respuesta = agent_executor.invoke({"input": message, "chat_history": messages})
        ai_reply = respuesta["output"]
    except Exception as e:
        ai_reply = f"Error: {str(e)}"
        print(f"[ERROR] {e}")
    
    messages.append(AIMessage(content=ai_reply))
    
    # Generar audio y video
    video_path = None
    audio_path = None
    
    if use_tts and ai_reply.strip():
        audio_path = tts_es(ai_reply)
        if audio_path:
            # Generar video del avatar (2-5 segundos)
            video_path = generate_avatar_video(audio_path, ai_reply)
    
    return ai_reply, video_path, audio_path

# =========================
# 9. INTERFAZ GRADIO
# =========================
custom_css = """
.gradio-container {
    font-family: 'Segoe UI', sans-serif !important;
    background: linear-gradient(135deg, #f5f7fa 0%, #e8f5e9 100%) !important;
}

.main-header {
    background: linear-gradient(135deg, #2196F3 0%, #1976D2 100%);
    padding: 2rem;
    border-radius: 15px;
    margin-bottom: 1.5rem;
    box-shadow: 0 4px 15px rgba(33, 150, 243, 0.3);
}

.avatar-container {
    background: white;
    border-radius: 20px;
    padding: 1.5rem;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
    margin-bottom: 1rem;
    text-align: center;
    display: flex;

}

.response-text {
    background: white;
    padding: 1.5rem;
    border-radius: 12px;
    border-left: 4px solid #4CAF50;
    margin: 1rem 0;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
    font-size: 1.1rem;
    line-height: 1.6;
}

.info-box {
    background: white;
    border-left: 4px solid #2196F3;
    padding: 1rem;
    border-radius: 8px;
    margin: 1rem 0;
}

button {
    border-radius: 10px !important;
    font-weight: 500 !important;
    transition: all 0.3s ease !important;
}

.primary {
    background: linear-gradient(135deg, #4CAF50 0%, #45a049 100%) !important;
    color: white !important;
}
"""

with gr.Blocks(title="🏥 Asistente Médico Virtual", css=custom_css, theme=gr.themes.Soft()) as demo:
    
    gr.HTML("""
        <div class="main-header">
            <h1>🏥 Asistente Médico Virtual con Avatar</h1>
            <p>💬 Consulta con avatar médico realista - Respuestas con lip-sync en 2-5 segundos</p>
        </div>
    """)
    
    gr.HTML("""
        <div class="info-box">
            <p style="margin: 0; color: #555;">
                <strong>ℹ️ Información:</strong> Este asistente proporciona información educativa. 
                No reemplaza una consulta médica profesional.
            </p>
        </div>
    """)
    
    # Avatar y respuesta
    with gr.Column(elem_classes="avatar-container"):
        gr.Markdown("### 👨‍⚕️ Tu Asistente Médico Virtual")
        
        # Imagen inicial del avatar
        avatar_img = gr.Image(
            value=AVATAR_IMAGE if os.path.exists(AVATAR_IMAGE) else None,
            height=2000,
            width=1600,
            interactive=False,
            visible=True,
            show_label=False
        )
        
        # Video del avatar (se muestra cuando hay respuesta)
        video_output = gr.Video(
            autoplay=True,
            height=2000,
            width=1600,
            show_download_button=False,
            show_share_button=False,
            visible=False
        )
        
        # Texto de respuesta
        response_text = gr.Markdown(
            value="¡Hola! 👋 Soy tu asistente médico virtual. Pregúntame sobre enfermedades respiratorias.",
            elem_classes="response-text"
        )
        
        # Audio (oculto, autoplay)
        audio_output = gr.Audio(visible=False, autoplay=True)
    
    # Input
    with gr.Row():
        with gr.Column(scale=5):
            msg = gr.Textbox(
                placeholder="💭 Escribe tu consulta médica aquí...",
                label="📝 Tu mensaje",
                lines=2
            )
        with gr.Column(scale=1):
            use_tts = gr.Checkbox(label="🔊 Activar voz y avatar", value=True)
            send_btn = gr.Button("📤 Enviar", elem_classes="primary", size="lg")
    
    gr.Examples(
        examples=[
            "¿Qué es el COVID-19?",
            "¿Cuáles son los síntomas de la faringitis?",
            "¿Cómo se trata el asma?",
        ],
        inputs=msg,
        label="💡 Preguntas de ejemplo"
    )
    
    gr.HTML("""
        <div style="background: #FFF3E0; border-left: 4px solid #FF9800; padding: 1rem; border-radius: 8px; margin-top: 1rem;">
            <p style="margin: 0; color: #555;">
                <strong>⚠️ Aviso:</strong> Información con fines educativos. Consulta con un profesional de salud.
            </p>
        </div>
    """)
    
    # Eventos
    def process_and_update(message, history, use_tts):
        text_response, video, audio = chat_fn(message, history, use_tts)
        
        # Si hay video, ocultamos imagen y mostramos video
        if video:
            img_visible = False
            vid_visible = True
            vid_value = video
        else:
            img_visible = True
            vid_visible = False
            vid_value = None
        
        return "", text_response, gr.update(visible=img_visible), gr.update(value=vid_value, visible=vid_visible), audio
    
    msg.submit(
        process_and_update,
        inputs=[msg, gr.State([]), use_tts],
        outputs=[msg, response_text, avatar_img, video_output, audio_output]
    )
    
    send_btn.click(
        process_and_update,
        inputs=[msg, gr.State([]), use_tts],
        outputs=[msg, response_text, avatar_img, video_output, audio_output]
    )

# =========================
# 10. EJECUCIÓN
# =========================
if __name__ == "__main__":
    try:
        print("=" * 50)
        print("Preparando TTS (Piper)...")
        _ensure_piper_voice()
        print("Preparando Avatar (Wav2Lip v2)...")
        _ensure_wav2lip()
        print("=" * 50)
        print("✓ Sistema listo - Videos en 2-5 segundos")
        print("=" * 50)
    except Exception as e:
        print(f"Error: {e}")
    
    demo.launch(server_name="0.0.0.0", server_port=7860)