"""
Servicio para añadir parpadeos realistas a videos de avatar
"""
import cv2
import numpy as np
import random
from pathlib import Path
from typing import Optional


class BlinkService:
    """
    Añade parpadeos naturales a videos de avatar usando OpenCV
    """

    def __init__(self):
        # Configuración de parpadeo
        self.blink_duration_frames = 3  # Duración del parpadeo en frames (~0.15s a 20fps)
        self.avg_blink_interval = 4.0  # Promedio de segundos entre parpadeos
        self.blink_variation = 2.0  # Variación aleatoria

    def add_blinks(
        self,
        video_path: str,
        output_path: Optional[str] = None,
        blink_frequency: float = 0.25  # Parpadeos por segundo
    ) -> Optional[str]:
        """
        Añade parpadeos al video

        Args:
            video_path: Ruta del video original
            output_path: Ruta del video de salida (None = sobrescribe original)
            blink_frequency: Frecuencia de parpadeos por segundo (default: 1 cada 4s)

        Returns:
            Ruta del video con parpadeos o None si falla
        """
        try:
            # Cargar video
            cap = cv2.VideoCapture(video_path)
            if not cap.isOpened():
                print("[BLINK] Error: No se pudo abrir el video")
                return None

            # Obtener propiedades del video
            fps = int(cap.get(cv2.CAP_PROP_FPS))
            width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

            print(f"[BLINK] Video: {width}x{height} @ {fps}fps, {total_frames} frames")

            # Preparar salida
            if output_path is None:
                output_path = video_path.replace('.mp4', '_blink.mp4')

            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

            # Generar momentos de parpadeo
            blink_frames = self._generate_blink_frames(total_frames, fps, blink_frequency)
            print(f"[BLINK] Se añadirán {len(blink_frames)} parpadeos")

            # Procesar frames
            frame_idx = 0
            while True:
                ret, frame = cap.read()
                if not ret:
                    break

                # Si es un frame de parpadeo, oscurecer la región de los ojos
                if frame_idx in blink_frames:
                    frame = self._apply_blink(frame, width, height)

                out.write(frame)
                frame_idx += 1

            # Limpiar
            cap.release()
            out.release()

            print(f"[BLINK] ✓ Parpadeos añadidos: {output_path}")
            return output_path

        except Exception as e:
            print(f"[BLINK] ✗ Error: {e}")
            import traceback
            traceback.print_exc()
            return None

    def _generate_blink_frames(
        self,
        total_frames: int,
        fps: int,
        blink_frequency: float
    ) -> set:
        """
        Genera los números de frame donde ocurrirán parpadeos

        Args:
            total_frames: Total de frames del video
            fps: Frames por segundo
            blink_frequency: Parpadeos por segundo

        Returns:
            Set de números de frame donde habrá parpadeo
        """
        blink_frames = set()
        duration_seconds = total_frames / fps
        num_blinks = int(duration_seconds * blink_frequency)

        # Generar momentos aleatorios de parpadeo
        for _ in range(num_blinks):
            # Evitar parpadeos en los primeros y últimos 0.5 segundos
            min_frame = int(0.5 * fps)
            max_frame = total_frames - int(0.5 * fps)

            if max_frame <= min_frame:
                continue

            blink_start = random.randint(min_frame, max_frame)

            # Añadir los frames del parpadeo (inicio, medio cerrado, final)
            for i in range(self.blink_duration_frames):
                frame_num = blink_start + i
                if 0 <= frame_num < total_frames:
                    blink_frames.add(frame_num)

        return blink_frames

    def _apply_blink(self, frame: np.ndarray, width: int, height: int) -> np.ndarray:
        """
        Aplica efecto de parpadeo al frame oscureciendo región de ojos

        Args:
            frame: Frame del video
            width: Ancho del frame
            height: Alto del frame

        Returns:
            Frame con parpadeo aplicado
        """
        # Estimación aproximada de la región de los ojos
        # Asumiendo que el rostro está centrado
        eye_region_y_start = int(height * 0.35)  # ~35% desde arriba
        eye_region_y_end = int(height * 0.48)    # ~48% desde arriba
        eye_region_x_start = int(width * 0.25)   # ~25% desde la izquierda
        eye_region_x_end = int(width * 0.75)     # ~75% desde la izquierda

        # Crear máscara para el parpadeo
        mask = np.ones_like(frame, dtype=np.float32)

        # Oscurecer la región de los ojos
        darkness_factor = 0.3  # Cuanto más bajo, más oscuro (0 = negro total)
        mask[eye_region_y_start:eye_region_y_end,
             eye_region_x_start:eye_region_x_end] = darkness_factor

        # Aplicar suavizado gaussiano a la máscara para transición suave
        mask = cv2.GaussianBlur(mask, (21, 21), 0)

        # Aplicar la máscara al frame
        blurred_frame = (frame * mask).astype(np.uint8)

        return blurred_frame


def add_blinks_to_video(
    video_path: str,
    output_path: Optional[str] = None,
    blink_frequency: float = 0.25
) -> Optional[str]:
    """
    Función auxiliar para añadir parpadeos a un video

    Args:
        video_path: Ruta del video
        output_path: Ruta de salida (None = reemplaza original)
        blink_frequency: Parpadeos por segundo

    Returns:
        Ruta del video procesado
    """
    service = BlinkService()
    return service.add_blinks(video_path, output_path, blink_frequency)
