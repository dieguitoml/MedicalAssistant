"""
API FastAPI - Servidor backend principal
"""
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
import time
from pathlib import Path
import os

from .models import ChatRequest, ChatResponse, HealthResponse, ErrorResponse, MediaRequest, MediaResponse
from .services import ChatService, TTSService, AvatarService
from .config import CORS_ORIGINS, TTS_OUTPUT_DIR, VIDEO_OUTPUT_DIR

app = FastAPI(
    title = "Medical Assistant API",
    description = "API REST para asistente médico con IA, TTS y avatar animado",
    version = "1.0.0",
    docs_url = "/docs",
    redoc_url = "/redoc"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#Servicios
chat_service: ChatService = None
tts_service: TTSService = None
avatar_service: AvatarService = None

@app.on_event("startup")
async def startup_event():
  """Inicializar servicios al inicial la app"""
  global chat_service, tts_service, avatar_service
  print("\n" + "="*60)
  print("🏥 Iniciando Medical Assistant API...")
  print("="*60 + "\n")
  #Inicializar servicios
  print("[1/3] Iniciando ChatService...")
  chat_service = ChatService()

  print("\n[2/3] Iniciando TTSService...")
  tts_service = TTSService()

  print("\n[3/3] Iniciando AvatarService...")
  avatar_service = AvatarService()

  print("\n" + "="*60)
  print("✅ Servicios inicializados")
  print("=" * 60)
  print(f"📚 Documentación: http://localhost:8000/docs")
  print(f"🏥 Health check: http://localhost:8000/api/health")
  print("=" * 60 + "\n")

#Servir archivos estáticos para audio y video
app.mount(
    "/static/audio",
    StaticFiles(directory=str(TTS_OUTPUT_DIR)),
    name = "audio"
)
app.mount(
    "/static/video",
    StaticFiles(directory=str(VIDEO_OUTPUT_DIR)),
    name = "video"
)


# Endpoints

@app.get("/")
async def root():
    """Endpoint raíz"""
    return {
       "name": "Medical Assistant API",
       "version": "1.0.0",
       "status": "online",
       "endpoints" : {
          "docs" : "/docs",
          "health" : "/api/health",
          "chat" : "/api/chat",
          "examples": "/api/chat/examples"
       }
    }

@app.get("/api/health", response_model=HealthResponse)
async def health_check():
   """Endpoint de health check"""
   services_status = {
      "chat" : chat_service.is_available() if chat_service else False,
      "tts" : tts_service.is_available() if tts_service else False,
      "avatar" : avatar_service.is_available() if avatar_service else False
   }
   all_ok = all(services_status.values())
   return HealthResponse(
      status = "healthy" if all_ok else "degraded",
      model_loaded = all_ok,
      services = services_status
   )

@app.post("/api/chat", response_model = ChatResponse)
async def chat(request: ChatRequest):
   """Endopint principal del chat
   El flujo es el siguiente:
   1.Procesar el mensaje con LLM + RAG
   2.Generar audio con TTS si use_tts=True
   3.Generar video con avatar si use_avatar=True
   
   Devuelve:
    -text: Respuesta textual
    -audio_url: URL al audio generado (si use_tts=True)
    -video_url: URL al video generado (si use_avatar=True)
    -processing_time: Tiempo de procesamiento en segundos
   """
   start_time = time.time()
   #Validar servicios
   if not chat_service or not chat_service.is_available():
      raise HTTPException(
         status_code = 503,
         detail = "Servicio de chat no disponible, verifica que Ollama está abierto"
      )
   
   try:
      print(f"\n{'='*60}")
      print(f"📨 Nueva consulta: {request.message[:50]}...")
      print(f"{'='*60}")

      #1. Procesar el mensaje con LLM + RAG
      print("\n[1/3] Procesando con LLM + RAG...")
      text_response = chat_service.process_message(request.message)
      print(f"✓ Respuesta generada: {len(text_response)} caracteres")
      
      audio_url = None
      video_url = None

      #2. Generar audio con TTS si use_tts=True

      if request.use_tts and tts_service and tts_service.is_available():
         print("\n[2/3] Generando audio con TTS...")
         audio_path = tts_service.generate_audio(text_response)
         if audio_path:
            filename = Path(audio_path).name
            audio_url = f"http://localhost:8000/static/audio/{filename}"
            print(f"✓ Audio disponible en: {audio_url}")
         else:
            print("⚠ No se pudo generar audio")  
      else:
         print("\n[2/3] Audio desactivado o no disponible")

      #3. Generar video si está habilitado y hay audio
      if request.use_avatar and avatar_service and avatar_service.is_available() and audio_url:
        print("\n[3/3] Generando video con Wav2Lip...")
        video_path = avatar_service.generate_video(audio_path)

        if video_path:
           filename = Path(video_path).name
           video_url = f"http://localhost:8000/static/video/{filename}"
           print(f"✓ Video disponible en: {video_url}")
        else:
           print("⚠ No se pudo generar video")
      else:
          print("\n[3/3] Video desactivado o no disponible")
    
      processing_time = time.time() - start_time

      print(f"\n{'='*60}")
      print(f"✅ Procesamiento completado en {processing_time:.2f}s")
      print(f"{'='*60}\n")

      return ChatResponse(
         text= text_response,
         audio_url = audio_url,
         video_url = video_url,
         processing_time = processing_time
      )
   except Exception as e:
      print(f"\n❌ Error procesando chat: {e}")
      import traceback
      traceback.print_exc()
        
      raise HTTPException(
        status_code=500,
        detail=f"Error procesando mensaje: {str(e)}"
      )
   
@app.get("/api/chat/clear")
async def clear_chat():
   """Endpoint para limpiar el historial de conversación"""
   if chat_service and chat_service.is_available():
      chat_service.clear_history()
      return {"message": "Historial limpiado correctamente"}
   else:
      raise HTTPException(
        status_code=503,
        detail = "Chat service no disponible"
      )


@app.post("/api/chat/media", response_model=MediaResponse)
async def generate_media(request: MediaRequest):
   """
   Endpoint para generar audio/video a partir de texto.
   Usado para carga asíncrona: el frontend obtiene el texto primero,
   luego llama a este endpoint para generar audio/video en segundo plano.
   """
   start_time = time.time()

   audio_url = None
   video_url = None
   audio_path = None

   try:
      # 1. Generar audio con TTS
      if tts_service and tts_service.is_available():
         print(f"\n[MEDIA] Generando audio para texto de {len(request.text)} caracteres...")
         audio_path = tts_service.generate_audio(request.text)
         if audio_path:
            filename = Path(audio_path).name
            audio_url = f"http://localhost:8000/static/audio/{filename}"
            print(f"[MEDIA] ✓ Audio: {audio_url}")

      # 2. Generar video si se solicita y hay audio
      if request.use_avatar and avatar_service and avatar_service.is_available() and audio_path:
         print("[MEDIA] Generando video con Wav2Lip...")
         video_path = avatar_service.generate_video(audio_path)
         if video_path:
            filename = Path(video_path).name
            video_url = f"http://localhost:8000/static/video/{filename}"
            print(f"[MEDIA] ✓ Video: {video_url}")

      processing_time = time.time() - start_time
      print(f"[MEDIA] Completado en {processing_time:.2f}s")

      return MediaResponse(
         audio_url=audio_url,
         video_url=video_url,
         processing_time=processing_time
      )

   except Exception as e:
      print(f"[MEDIA] ✗ Error: {e}")
      import traceback
      traceback.print_exc()
      raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/chat/examples")
async def chat_examples():
   """Endpoint para obtener ejemplos de preguntas"""
   return {
      "examples" : [
         "¿Qué es el COVID-19?",
         "¿Cuáles son los síntomas de la faringitis?",
         "¿Cómo se trata el asma?",
         "¿Qué hacer si tengo tos persistente?",
         "¿Cuándo debo ir al médico por dolor de garganta?"
      ]
   }

#Manejo de errores global

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
   """Manejo global de excepciones"""
   print(f"❌ Error global: {exc}")
   import traceback
   traceback.print_exc()

   error_response = ErrorResponse(
      error = "Internal Server Error",
      detail = str(exc)
   )

   return JSONResponse(
      status_code = 500,
      content = error_response.model_dump(mode='json')
   )


# Ejecutar directamente
if __name__ == "__main__":
    import uvicorn
    
    print("\n" + "=" * 60)
    print("🏥 Medical Assistant API")
    print("=" * 60)
    print("Starting server...")
    print("=" * 60 + "\n")
    
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,  # Auto-reload en desarrollo
        log_level="info"
    )