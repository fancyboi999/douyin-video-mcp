"""ASR 提供方"""

from .base import ASRProvider
from .factory import get_asr_provider

__all__ = ["ASRProvider", "get_asr_provider"]
