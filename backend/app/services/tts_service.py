"""
Servicio de Text-to-Speech usando Piper
"""
import os
import time
import wave
from pathlib import Path
from typing import Optional

from ..config import PIPER_VOICE_DIR, PIPER_VOICE_ID, TTS_OUTPUT_DIR

class TTSService:
    """
    Servicio para generar audio con Piper TTS
    """
    
    def __init__(self):
        self._piper_voice = None
        self._load_voice()
    
    def _load_voice(self):
        """Cargar el modelo de voz Piper"""
        try:
            from piper import PiperVoice
            
            # Buscar archivos del modelo
            search_paths = [
                (
                    Path(PIPER_VOICE_DIR) / f"{PIPER_VOICE_ID}.onnx",
                    Path(PIPER_VOICE_DIR) / f"{PIPER_VOICE_ID}.onnx.json"
                ),
                (
                    Path(PIPER_VOICE_DIR) / "es" / f"{PIPER_VOICE_ID}.onnx",
                    Path(PIPER_VOICE_DIR) / "es" / f"{PIPER_VOICE_ID}.onnx.json"
                ),
            ]
            
            onnx_path = json_path = None
            for onnx, json_file in search_paths:
                if onnx.exists() and json_file.exists():
                    onnx_path, json_path = str(onnx), str(json_file)
                    break
            
            if not onnx_path:
                # Intentar descargar
                print(f"[TTS] Descargando modelo {PIPER_VOICE_ID}...")
                from huggingface_hub import hf_hub_download
                
                voice_paths = {
                    "es_MX-claude-high": ("es/es_MX/claude/high", "es_MX-claude-high"),
                    "es_ES-davefx-medium": ("es/es_ES/davefx/medium", "es_ES-davefx-medium"),
                }
                
                if PIPER_VOICE_ID in voice_paths:
                    voice_path, voice_name = voice_paths[PIPER_VOICE_ID]
                    onnx_path = hf_hub_download(
                        "rhasspy/piper-voices",
                        f"{voice_path}/{voice_name}.onnx",
                        local_dir=PIPER_VOICE_DIR
                    )
                    json_path = hf_hub_download(
                        "rhasspy/piper-voices",
                        f"{voice_path}/{voice_name}.onnx.json",
                        local_dir=PIPER_VOICE_DIR
                    )
            
            self._piper_voice = PiperVoice.load(onnx_path, config_path=json_path)
            sr = self._piper_voice.config.sample_rate if hasattr(self._piper_voice, 'config') else 22050
            print(f"[TTS] ✓ Piper cargado: {sr} Hz")
            
        except Exception as e:
            print(f"[TTS] ✗ Error cargando Piper: {e}")
            self._piper_voice = None
    
    def is_available(self) -> bool:
        """Verificar si el servicio está disponible"""
        return self._piper_voice is not None
    
    def generate_audio(self, text: str) -> Optional[str]:
        """
        Generar audio a partir de texto
        
        Args:
            text: Texto a sintetizar
            
        Returns:
            Path del archivo de audio generado o None si falla
        """
        if not self.is_available():
            print("[TTS] Servicio no disponible")
            return None
        
        try:
            # Limpiar texto
            clean_text = text.replace('*', '').replace('_', '').replace('#', '')
            clean_text = clean_text.replace('\n\n', '. ').replace('\n', ', ')
            
            # Generar nombre de archivo
            timestamp = int(time.time() * 1000)
            output_path = TTS_OUTPUT_DIR / f"tts_{timestamp}.wav"
            
            print(f"[TTS] Sintetizando: '{clean_text[:50]}...'")
            
            # Generar audio
            with wave.open(str(output_path), "wb") as wav_file:
                self._piper_voice.synthesize_wav(clean_text, wav_file)
            
            # Verificar
            if output_path.exists() and output_path.stat().st_size > 44:
                size = output_path.stat().st_size
                print(f"[TTS] ✓ Audio generado: {output_path.name} ({size} bytes)")
                return str(output_path)
            else:
                print("[TTS] ✗ Archivo vacío o muy pequeño")
                if output_path.exists():
                    output_path.unlink()
                return None
                
        except Exception as e:
            print(f"[TTS] ✗ Error: {e}")
            import traceback
            traceback.print_exc()
            return None
