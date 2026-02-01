"""
Schemas de datos (Pydantic Models)
Definen la estructura de requests y responses
"""
from pydantic import BaseModel,Field
from typing import Optional
from datetime import datetime


class ChatRequest(BaseModel):
    """
    Request del frontend para el endpoint del chat
    """
    message: str = Field(
        ...,
        min_length=1,
        max_length=2000,
        description="Mensaje del usuario"
    )
    use_tts: bool = Field(
        default=False,
        description= "Generar respuesta con audio"
    )
    use_avatar: bool = Field(
        default=False,
        description="Incluir avatar en el video de respuesta"
    )
    class Config:
        json_schema_extra = {
            "example": {
                "message": "¿Cuáles son los síntomas de la faringitis?",
                "use_tts": True,
                "use_avatar": True
            }
        }    

class ChatResponse(BaseModel):
    """
    Respuesta del backend al frondtend
    """
    text: str = Field(
        ...,
        description="Respuesta textual del asistente médico"
    )
    audio_url: Optional[str] = Field(
        None,
        description="URL al archivo de audio generado (si use_tts=True)"
    )
    video_url: Optional[str] = Field(
        None,
        description="URL al archivo de video generado (si use_avatar=True)"
    )
    processing_time: float = Field(
        ...,
        description="Tiempo de procesamiento en segundos"
    )
    timestamp: datetime = Field(default_factory=datetime.now)

class HealthResponse(BaseModel):
    """
    Respuesta del health check endpoint
    """
    status: str = Field(
        ...,
        description="Estado del servicio"
    )
    model_loaded: bool = Field(
        ...,
        description="Indica si el modelo de chat está cargado"
    )
    services: dict = Field(
        ...,
        description="Estado de cada servicio"
    )
    timestamp: datetime = Field(default_factory=datetime.now)

class ErrorResponse(BaseModel):
    """
    Respuesta de error
    """
    error: str = Field(
        ...,
        description="Mensaje de error"
    )
    detail: Optional[str] = Field(
        None,
        description="Detalle adicional del error"
    )
    timestamp: datetime = Field(default_factory=datetime.now)


class MediaRequest(BaseModel):
    """
    Request para generar audio/video a partir de texto ya generado
    """
    text: str = Field(
        ...,
        min_length=1,
        description="Texto para convertir a audio/video"
    )
    use_avatar: bool = Field(
        default=False,
        description="Si es True genera video con avatar, si es False solo audio"
    )


class MediaResponse(BaseModel):
    """
    Respuesta con URLs de audio/video generados
    """
    audio_url: Optional[str] = None
    video_url: Optional[str] = None
    processing_time: float = 0.0