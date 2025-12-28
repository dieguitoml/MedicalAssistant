"""
Servicio de generación de avatar con Wav2Lip
"""
import os
import sys
import time
from pathlib import Path
from typing import Optional

from ..config import AVATAR_IMAGE, WAV2LIP_DIR, VIDEO_OUTPUT_DIR
from .blink_service import BlinkService

class AvatarService:
    """
    Servicio para generar video del avatar con Wav2Lip
    """
    
    def __init__(self, enable_blinks: bool = True):
        self._wav2lip = None
        self._blink_service = BlinkService() if enable_blinks else None
        self._load_model()
    
    def _load_model(self):
        """Cargar modelo Wav2Lip"""
        try:
            wav2lip_path = Path(WAV2LIP_DIR)
            
            if not wav2lip_path.exists():
                print(f"[AVATAR] ✗ No se encuentra {WAV2LIP_DIR}")
                return
            
            # Añadir al path
            if str(wav2lip_path) not in sys.path:
                sys.path.insert(0, str(wav2lip_path))
            
            print("[AVATAR] Cargando Wav2Lip v2...")

            from inference_wrapper import Wav2Lipv2

            checkpoint_path = wav2lip_path / "checkpoints" / "wav2lip_gan.pth"
            weights_dir = wav2lip_path / "checkpoints" / "weights"
            
            if not checkpoint_path.exists():
                print(f"[AVATAR] ✗ Checkpoint no encontrado: {checkpoint_path}")
                return
            
            self._wav2lip = Wav2Lipv2(
                checkpoint_path=str(checkpoint_path),
                pretrained_model_dir=str(weights_dir),
                pads=[0, 10, 0, 0],
                audio_smooth=True,
                rotate=False
            )
            
            print("[AVATAR] ✓ Wav2Lip v2 cargado exitosamente")
            
        except Exception as e:
            print(f"[AVATAR] ✗ Error cargando Wav2Lip: {e}")
            import traceback
            traceback.print_exc()
            self._wav2lip = None
    
    def is_available(self) -> bool:
        """Verificar si el servicio está disponible"""
        return self._wav2lip is not None and Path(AVATAR_IMAGE).exists()
    
    def generate_video(self, audio_path: str) -> Optional[str]:
        """
        Generar video del avatar hablando
        
        Args:
            audio_path: Path del archivo de audio
            
        Returns:
            Path del video generado o None si falla
        """
        if not self.is_available():
            print("[AVATAR] Servicio no disponible")
            return None
        
        if not os.path.exists(audio_path):
            print(f"[AVATAR] ✗ Audio no encontrado: {audio_path}")
            return None
        
        try:
            timestamp = int(time.time() * 1000)
            output_path = VIDEO_OUTPUT_DIR / f"avatar_{timestamp}.mp4"
            
            print(f"[AVATAR] Generando video con parámetros optimizados...")
            start_time = time.time()

            # Generar video con Wav2Lip - Configuración optimizada para velocidad
            result_path = self._wav2lip.run(
                video_path=AVATAR_IMAGE,
                audio_path=audio_path,
                batch_size=96,  # RTX 3060: 96 es un buen equilibrio velocidad/memoria
                enhance=False,  # False = más rápido (sin mejora facial)
                outfile=str(output_path),
                fps=20  # Reducido de 25 a 20 para ~20% más velocidad
            )
            
            elapsed = time.time() - start_time

            if result_path and os.path.exists(result_path) and os.path.getsize(result_path) > 1000:
                size = os.path.getsize(result_path) / (1024 * 1024)  # MB
                print(f"[AVATAR] ✓ Video generado en {elapsed:.2f}s: {size:.1f}MB")

                # Añadir parpadeos si está habilitado
                if self._blink_service:
                    print(f"[AVATAR] Añadiendo parpadeos naturales...")
                    blink_start = time.time()

                    # Generar video con parpadeos
                    output_with_blinks = VIDEO_OUTPUT_DIR / f"avatar_{timestamp}_final.mp4"
                    result_with_blinks = self._blink_service.add_blinks(
                        result_path,
                        str(output_with_blinks),
                        blink_frequency=0.25  # 1 parpadeo cada 4 segundos
                    )

                    if result_with_blinks:
                        blink_elapsed = time.time() - blink_start
                        # Eliminar video temporal sin parpadeos
                        try:
                            os.remove(result_path)
                        except:
                            pass
                        print(f"[AVATAR] ✓ Parpadeos añadidos en {blink_elapsed:.2f}s")
                        return result_with_blinks
                    else:
                        print(f"[AVATAR] ⚠ No se pudieron añadir parpadeos, usando video original")
                        return result_path

                return result_path
            else:
                print("[AVATAR] ✗ Video no generado correctamente")
                return None
                
        except Exception as e:
            print(f"[AVATAR] ✗ Error: {e}")
            import traceback
            traceback.print_exc()
            return None