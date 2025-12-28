"""
Servicios de la APP
"""
from .chat_service import ChatService
from .tts_service import TTSService
from .avatar_service import AvatarService
from .blink_service import BlinkService

__all__ = ["ChatService", "TTSService", "AvatarService", "BlinkService"]